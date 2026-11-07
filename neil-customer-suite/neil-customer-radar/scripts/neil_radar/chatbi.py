"""传输层：ChatBI 开放 API 唯一出口（createSession/createChat/queryUpdateChat），
会话本地缓存与过期重建、轮询至 finalize、结果双通道解析（sqlDatas 结构化优先、
finalAnswer markdown 表格兜底）。重试预算只改 RETRY_TRANSPORT 常量，禁裸数字。

出处：neil-weekly-service-report/scripts/neil_weekly/chatbi.py（2026-11-07 逐行移植，
实测契约：限流 201000 长退避、instantQueryMode=False、queryUpdateChat 瞬态 201000 续轮询）。
改动须同步回写出处或在本文件头注记差异。"""
import json
import os
import re
import time
import urllib.parse
import urllib.request

RETRY_TRANSPORT = 3
RETRY_RATE_LIMIT = 4
RATE_LIMIT_CODE = 201000
RATE_LIMIT_SLEEP = 25
HTTP_TIMEOUT = 60

SESSION_FILE_NAME = ".chatbi_session.json"


class ChatBIError(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code


def _post(cfg, path, form):
    """x-www-form-urlencoded POST；超时/网络抖动指数退避 RETRY_TRANSPORT 次；
    限流 201000 单独长退避 RETRY_RATE_LIMIT 次（实测并发/高频 createChat 必触发）。"""
    url = cfg["server_domain"] + path
    body = urllib.parse.urlencode(form).encode("utf-8")
    last_err = None
    for attempt in range(RETRY_TRANSPORT + RETRY_RATE_LIMIT):
        try:
            req = urllib.request.Request(
                url, data=body,
                headers={"Content-Type": "application/x-www-form-urlencoded"})
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            if result.get("returnCode") == RATE_LIMIT_CODE:
                last_err = ChatBIError(f"{path} 限流 201000", code=RATE_LIMIT_CODE)
                time.sleep(RATE_LIMIT_SLEEP)
                continue
            if result.get("returnCode") != 0:
                raise ChatBIError(f"{path} returnCode={result.get('returnCode')}: "
                                  f"{result.get('returnMessage')}",
                                  code=result.get("returnCode"))
            return result.get("returnValue")
        except ChatBIError:
            raise
        except Exception as exc:  # noqa: BLE001 网络/解析抖动一律退避重试
            last_err = exc
            time.sleep(2 ** attempt)
    raise last_err


def _session_path(out_dir):
    return os.path.join(out_dir, SESSION_FILE_NAME)


def get_session(cfg, out_dir):
    """会话缓存（1h TTL，与 fbi-ask-data 同口径）；过期/缺失即重建并落盘。"""
    path = _session_path(out_dir)
    cached = {}
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as fh:
                cached = json.load(fh)
        except Exception:  # noqa: BLE001 坏缓存当缺失处理
            cached = {}
    created = cached.get("created_at", "")
    fresh = False
    if cached.get("session_id") and created:
        try:
            age = time.time() - time.mktime(time.strptime(created, "%Y-%m-%d %H:%M:%S"))
            fresh = age < cfg.get("session_expire_hours", 1) * 3600
        except ValueError:
            fresh = False
    if fresh:
        return cached["session_id"]
    param = {
        "assistantId": cfg["assistant_id"],
        "name": cfg.get("session_name", "neil-customer-radar"),
        "empId": cfg["token"].split("_")[0],
        "needCheckPermission": "false",
    }
    session_id = _post(cfg, "/ai/FbiOpenChatBiAction/createSession",
                       {"createSessionParam": json.dumps(param), "token": cfg["token"]})
    if not session_id:
        raise ChatBIError("createSession 未返回会话 ID")
    os.makedirs(out_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"session_id": session_id,
                   "created_at": time.strftime("%Y-%m-%d %H:%M:%S")}, fh)
    return session_id


def _agent_id(cfg):
    agents = _post(cfg, "/ai/FbiOpenChatBiAction/queryAssistantAgent",
                   {"assistantId": cfg["assistant_id"], "token": cfg["token"]}) or []
    for item in agents:
        if str(item.get("agentId", "")).startswith("askData"):
            return item["agentId"]
    raise ChatBIError("queryAssistantAgent 未找到 askData agentId")


def create_chat(cfg, out_dir, question, resource_id, resource_type="report"):
    """仅创建问数（不轮询），返回 answerMessageId。错开创建+并发轮询的调度基础。"""
    param = {
        "sessionId": get_session(cfg, out_dir),
        "customAgentId": _agent_id(cfg),
        "question": question,
        "empId": cfg["token"].split("_")[0],
        "parentMessageId": "",
        "model": "",
        "deepThinkMode": "false",
        "notUseWebSearchTool": "true",
        "notUseClarifyTool": "true",
        # 实测 instantQueryMode=True（极速模式）对本报表返回空行；think 模式才有数
        "instantQueryMode": False,
        "attachments": [{"type": "inner_resource", "subType": resource_type,
                         "resourceId": str(resource_id)}],
    }
    created = _post(cfg, "/ai/FbiOpenChatBiAction/createChat",
                    {"createChatParam": json.dumps(param), "token": cfg["token"]})
    answer_id = (created or {}).get("answerMessageId")
    if not answer_id:
        raise ChatBIError("createChat 未返回 answerMessageId")
    return answer_id


def poll_chat(cfg, answer_id):
    """轮询单个 answerMessageId 至 finalize；返回 returnValue。
    201000 query update chat error:null = 服务端尚未就绪的瞬态错，继续轮询。"""
    interval = cfg.get("poll_interval_seconds", 5)
    deadline = time.time() + cfg.get("poll_timeout_seconds", 900)
    while time.time() < deadline:
        qparam = {"updateMessageId": answer_id, "empId": cfg["token"].split("_")[0]}
        try:
            value = _post(cfg, "/ai/FbiOpenChatBiAction/queryUpdateChat",
                          {"queryUpdateChatParam": json.dumps(qparam, ensure_ascii=False),
                           "token": cfg["token"]})
        except ChatBIError as exc:
            if exc.code == 201000:
                time.sleep(interval)
                continue
            raise
        if isinstance(value, dict) and value.get("finalize"):
            value["answerMessageId"] = answer_id
            return value
        time.sleep(interval)
    raise ChatBIError(f"轮询超时（answerMessageId={answer_id}）")


def ask(cfg, out_dir, question, resource_id, resource_type="report"):
    """创建+轮询一体（串行场景）；并发场景用 create_chat/poll_chat 自行调度。"""
    answer_id = create_chat(cfg, out_dir, question, resource_id, resource_type)
    return poll_chat(cfg, answer_id)


def rows_from_sql_datas(result):
    """结构化优先：originalData.general.sqlDatas[].columns/rows → 行字典列表。"""
    out = []
    general = ((result or {}).get("originalData") or {}).get("general") or {}
    for sql_data in general.get("sqlDatas") or []:
        names = [c.get("dataIndex", "") for c in sql_data.get("columns") or []]
        for row in sql_data.get("rows") or []:
            out.append({names[i]: (row[i] if i < len(row) else None)
                        for i in range(len(names))})
    return out


_MD_CELL_RE = re.compile(r"\|")


def rows_from_markdown(result):
    """兜底：解析 finalAnswer 里的 markdown 表格（首行为表头）。"""
    text = (result or {}).get("finalAnswer") or ""
    table_lines = [ln.strip() for ln in text.splitlines()
                   if ln.strip().startswith("|") and ln.strip().endswith("|")]
    if len(table_lines) < 3:
        return []

    def cells(line):
        return [c.strip() for c in _MD_CELL_RE.split(line)[1:-1]]
    header = cells(table_lines[0])
    out = []
    for line in table_lines[2:]:
        vals = cells(line)
        if all(re.fullmatch(r":?-{2,}:?", v or "-") for v in vals):
            continue
        out.append({header[i]: (vals[i] if i < len(vals) else None)
                    for i in range(len(header))})
    return out


def parse_number(raw):
    """'11,666.00' / '**11,666**' / '643.78' → float；'-'/空/非数 → None。"""
    if raw is None:
        return None
    text = str(raw).replace("*", "").replace(",", "").strip()
    if not text or text in {"-", "--", "null", "None"}:
        return None
    try:
        return float(text)
    except ValueError:
        return None
