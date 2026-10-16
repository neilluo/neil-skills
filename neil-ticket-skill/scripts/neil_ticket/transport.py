"""传输层：dws 子进程唯一出口 run_dws、重试预算常量表、130003 结构化判定、
desc/older 通用翻页 _paginate。扩展时改这里：重试次数只改 RETRY_* 常量表
（AGENTS.md 规则 B）；require 谓词只做信封形状校验（规则 A）；130003 只按
结构化字段/stderr 数字边界判定（规则 C）；翻页与告警策略只改 _paginate（规则 D）。"""
import json
import os
import re
import subprocess
import time

DWS = os.environ.get("NEIL_TICKET_DWS", "/Users/neil/.qoder/bin/dws")

# ── 重试预算表（各调用点一律引用常量，禁裸数字）────────────────────────
# RETRY_TRANSPORT=3   run_dws 传输层：超时/非零 rc/非 JSON/空回 envelope 指数退避（trap#6）
# RETRY_EMPTY_PAGE=2  fetch_page 业务层：messages 空列表重试（trap#14）。原为 3，
#                     因传输层已 3 次，叠加后单层最坏 3×3=9 次子进程过多，降为 2（最坏 6 次）
# RETRY_AUTH=2        cross-org data-auth：幂等授权，2 次足够
# RETRY_CREATE=1      doc create 单轮内 run_dws 不重试；建/查重决策交给
#                     create_doc_idempotent 外层（RETRY_TRANSPORT 轮），防同名重复文档
RETRY_TRANSPORT = 3
RETRY_EMPTY_PAGE = 2
RETRY_AUTH = 2
RETRY_CREATE = 1


class AccessDenied(Exception):
    """130003 不在群内：降级信号，不重试。label 区分未入群/已解散/不可读。
    构造入参为命中源文本（stderr + 结构化错误字段值，见 _denied_source），
    label 只基于该源文本分类，绝不扫 stdout 全量（规则 C 延伸至 label）。"""

    def __init__(self, blob):
        super().__init__(blob[:300])
        low = blob.lower()
        if "not in conversation" in low:
            self.label = "未入群"
        elif "解散" in blob or "disband" in low or "not exist" in low:
            self.label = "已解散"
        else:
            self.label = "不可读"


_RE_130003 = re.compile(r"(?<!\d)130003(?!\d)")


def _scan_envelope(node):
    """结构化错误字段精确判定（数字边界防 1300030 误伤），递归一层嵌套信封。"""
    if isinstance(node, dict):
        for field in ("errorCode", "errorMsg", "error", "errMsg"):
            val = node.get(field)
            if isinstance(val, str) and _RE_130003.search(val):
                return True
            if isinstance(val, int) and val == 130003:
                return True
        for sub in ("data", "result"):
            if _scan_envelope(node.get(sub)):
                return True
    return False


def _access_denied(proc, parsed):
    """trap#15：只看结构化错误字段（含一层嵌套）与 stderr，绝不扫消息正文/文档正文。"""
    if _scan_envelope(parsed):
        return True
    return bool(_RE_130003.search(proc.stderr or ""))


def _error_field_values(node, out):
    """收集结构化错误字段值（与 _scan_envelope 同字段面、同一层嵌套信封），供 label 分类。"""
    if isinstance(node, dict):
        for field in ("errorCode", "errorMsg", "error", "errMsg"):
            val = node.get(field)
            if isinstance(val, str):
                out.append(val)
            elif isinstance(val, int):
                out.append(str(val))
        for sub in ("data", "result"):
            _error_field_values(node.get(sub), out)
    return out


def _denied_source(proc, parsed):
    """_access_denied 命中时的命中源文本：仅 stderr 文本 + 结构化错误字段值，
    不含 stdout 全量——防消息正文/文档正文里的「解散」「not in conversation」
    等字样混入 AccessDenied.label 造成误分类。"""
    parts = [proc.stderr or ""] + _error_field_values(parsed, [])
    return "\n".join(p for p in parts if p)


def run_dws(args, require=None, retries=RETRY_TRANSPORT, timeout=180):
    """require: 谓词 data->bool；不满足视为 trap#6 空回，重试。重试耗尽 raise。"""
    last_err = None
    for attempt in range(retries):
        try:
            proc = subprocess.run([DWS] + args, capture_output=True, text=True,
                                  timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            last_err = exc
            time.sleep(2 ** attempt)
            continue
        parsed = None
        try:
            parsed = json.loads(proc.stdout.strip())
        except Exception:  # noqa: BLE001
            parsed = None
        if _access_denied(proc, parsed):
            raise AccessDenied(_denied_source(proc, parsed))
        if proc.returncode != 0:
            last_err = RuntimeError(f"dws {' '.join(args[:4])}... rc={proc.returncode}: {proc.stderr[:300]}")
            time.sleep(2 ** attempt)
            continue
        if parsed is None:
            last_err = RuntimeError(f"dws {' '.join(args[:4])}... 非 JSON 输出")
            time.sleep(2 ** attempt)
            continue
        if require is not None and not require(parsed):
            last_err = RuntimeError(f"dws {' '.join(args[:4])}... 空回 envelope")
            time.sleep(2 ** attempt)
            continue
        return parsed
    raise last_err


def fetch_page(cid, boundary, limit):
    """单页读取；空 messages 列表视为 trap#14 抖动，重试至 RETRY_EMPTY_PAGE=2 次后接受为空
    （传输层 run_dws 已有 RETRY_TRANSPORT=3 次，两层叠加最坏 6 次子进程；原 3×3=9 过多）。
    返回 (page, flaky_exhausted)。"""
    page = []
    for attempt in range(RETRY_EMPTY_PAGE):
        data = run_dws(
            ["chat", "+chat-messages", "--group", cid, "--time", boundary,
             "--direction", "older", "--limit", str(limit)],
            require=lambda d: "messages" in d,
        )
        page = data.get("messages") or []
        if page:
            return page, False
        if attempt < RETRY_EMPTY_PAGE - 1:
            time.sleep(2 ** attempt)
    return page, True


def _paginate(cid, boundary_init, lower_bound, limit, max_pages, label, warnings,
              stop_on_short_page=False, seen_cap=None):
    """desc/older 通用翻页生成器（read_messages / probe_subgroup 共用）：
    空页重试由 fetch_page 承担；此处做 messageId 去重、boundary 推进、防死循环，
    异常追加 warnings（带 label 前缀），逐条 yield 新消息。
    stop_on_short_page: 不满 limit 即视为到底（子群探读用）；seen_cap: 去重消息数上限。"""
    seen = set()
    boundary = boundary_init
    got_any = False
    for _ in range(max_pages):
        page, flaky = fetch_page(cid, boundary, limit)
        got_any = got_any or bool(page)
        for m in page:
            if m["messageId"] not in seen:
                seen.add(m["messageId"])
                yield m
        if not page or (stop_on_short_page and len(page) < limit):
            if flaky and got_any:  # 首页即空=群内无消息，不告警；有内容后空页=可能漏读
                warnings.append(f"{label}翻页在 boundary={boundary} 处连续空页，可能漏读")
            return
        min_ct = min(m["createTime"] for m in page)
        if lower_bound and min_ct < lower_bound:
            return
        if min_ct == boundary:
            warnings.append(f"{label}翻页 boundary={boundary} 不前进（边界含等值或同时间戳满页），提前停止防死循环")
            return
        boundary = min_ct
        if seen_cap is not None and len(seen) >= seen_cap:
            return
    warnings.append(f"{label}翻页达 max_pages={max_pages} 上限仍未到边界，可能漏读")
