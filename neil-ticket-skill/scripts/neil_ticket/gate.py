"""门禁层：effective_status「LLM 提议、脚本门禁」三重校验（AGENTS.md 规则 E），纯函数。
改门禁/枚举只改本文件：取值枚举唯一事实源是 EFFECTIVE_ENUM（reference.md 只引用
常量名不复制值）；引证校验（messageId 存在性 + quote 原文子串 + 按工单隔离）在
sanitize_summary；回退默认值在 default_effective。校验失败必须留痕不可静默。"""
import re

EFFECTIVE_ENUM = {"已完结", "已解决待关单", "处理中", "无法判定(无子群)"}

# process_bullets 精简合成观察哨常量（AGENTS.md 规则 N）：超此条数视为疑似流水账
MAX_BULLETS = 8
# 逐条时间戳流水账签名：bullet 以「HH:MM」或「YYYY-MM-DD HH:MM」开头
_RE_TS_PREFIX = re.compile(r"^\s*(?:20\d{2}[-/]\d{1,2}[-/]\d{1,2}[\s,]*)?\d{1,2}:\d{2}")


def lint_process_bullets(bullets):
    """process_bullets 精简合成观察哨（只报不改，AGENTS.md 规则 N；用户 2026-10-16
    指令「几乎没有总结、原封不动把群聊摘录下来这种是不对的」）。检测逐条时间戳流水
    账签名：bullet 数超 MAX_BULLETS，或以时间戳开头的 bullet 占比过高。返回告警字符
    串列表（空＝合规）。绝不修改/截断 bullets（用户拒截断式 normalize，长度约束只
    报观察）；本函数不判合成质量好坏，只机械识别「疑似原样摘录」信号供发布行提示。"""
    if not isinstance(bullets, list) or not bullets:
        return []
    warns = []
    if len(bullets) > MAX_BULLETS:
        warns.append(f"{len(bullets)}条超上限{MAX_BULLETS}(疑似流水账)")
    ts = sum(1 for b in bullets if isinstance(b, str) and _RE_TS_PREFIX.match(b))
    if len(bullets) >= 3 and ts >= 2 and ts / len(bullets) >= 0.5:
        warns.append(f"{ts}/{len(bullets)}条以时间戳开头(疑似逐条摘录)")
    return warns


def default_effective(ticket, sig, readable):
    """规则默认实质状态：子代理引证校验失败时的回退值。"""
    if ticket.get("completed_at"):
        return "已完结"
    if sig.get("engineer_summary_msgs") or sig.get("customer_confirm_msgs"):
        return "已解决待关单"
    if readable:
        return "处理中"
    return "无法判定(无子群)"


def _norm(text):
    return re.sub(r"\s+", "", text or "")


def sanitize_summary(summary, slice_, texts=None):
    """LLM 提议、脚本门禁：effective_status 枚举校验 + effective_evidence 的
    messageId 存在性 + quote 对所指消息原文做子串校验；任一失败回退规则默认并留痕。"""
    texts = texts or {}
    out = {}
    for tid, s in (summary or {}).items():
        s = dict(s)
        sig = slice_.get("signals", {}).get(tid, {})
        readable = slice_.get("subgroup_readable", {}).get(tid)
        t = slice_["tickets"].get(tid, {})
        fallback = default_effective(t, sig, readable)
        allowed = {t.get("create_msg_id"), t.get("done_msg_id")}
        allowed.update(t.get("subgroup_msg_ids") or [])
        allowed.discard("")
        ev = s.get("effective_evidence") or {}
        mid = ev.get("message_id") or ""
        status = s.get("effective_status")
        bad = ""
        if status not in EFFECTIVE_ENUM:
            bad = mid or "<status>"
        elif status != "无法判定(无子群)" and not mid:
            bad = "<缺引证>"
        elif mid and mid not in allowed:  # 按工单隔离，禁跨工单引用
            bad = mid
        elif mid and mid in (texts.get(tid) or {}) and ev.get("quote"):
            if _norm(ev["quote"]) not in _norm(texts[tid][mid]):
                bad = mid
        if bad:
            s["effective_status_invalid_evidence"] = bad
            s["effective_status"] = fallback
        if not s.get("effective_status"):
            s["effective_status"] = fallback
        out[tid] = s
    return out
