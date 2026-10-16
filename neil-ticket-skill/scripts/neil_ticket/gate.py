"""门禁层：effective_status「LLM 提议、脚本门禁」三重校验（AGENTS.md 规则 E），纯函数。
改门禁/枚举只改本文件：取值枚举唯一事实源是 EFFECTIVE_ENUM（reference.md 只引用
常量名不复制值）；引证校验（messageId 存在性 + quote 原文子串 + 按工单隔离）在
sanitize_summary；回退默认值在 default_effective。校验失败必须留痕不可静默。"""
import re

EFFECTIVE_ENUM = {"已完结", "已解决待关单", "处理中", "无法判定(无子群)"}

# 情绪等级枚举（AGENTS.md 规则 Q）：关注等级合成的输入。唯一事实源在此，
# reference.md 只引用常量名不复制值（规则 L）。「轻微/明显」必须有本工单有效引证，
# 校验失败回退「无法判定」并留痕——与 effective_status 三重门禁同构。
SENTIMENT_ENUM = {"无", "轻微", "明显", "无法判定"}
# 需要引证才能成立的情绪等级（「无」是默认安全值不需引证；「无法判定」是回退值）
SENTIMENT_NEEDS_EVIDENCE = {"轻微", "明显"}

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


def _allowed_ids(ticket):
    """本工单可引证的 messageId 集合（建单/完结卡 id + 子群消息 id），按工单隔离，
    禁跨工单引用（规则 E/Q 共用）。sanitize_summary 与 sanitize_sentiment 共享。"""
    allowed = {ticket.get("create_msg_id"), ticket.get("done_msg_id")}
    allowed.update(ticket.get("subgroup_msg_ids") or [])
    allowed.discard("")
    return allowed


def _evidence_bad(ev, allowed, tid_texts, needs_evidence):
    """引证三重校验的共用核心（规则 E/Q，sanitize_summary 与 sanitize_sentiment 共享）：
    ① ev 非 dict → 结构异常（needs_evidence 时判失败，否则宽容放行）；② 跨工单引用
    （mid 不在 allowed）优先判；③ needs_evidence 时缺 message_id → <缺引证>、空 quote →
    <空quote>（规则 E 明令「禁止空 quote 绕过」）；④ quote 非所指消息原文归一化子串 →
    判 mid。返回 bad 标记字符串（空＝合规）。纯函数、不崩溃于畸形 evidence。"""
    if not isinstance(ev, dict):
        return "<evidence结构异常>" if needs_evidence else ""
    mid = ev.get("message_id") or ""
    quote = ev.get("quote") or ""
    if mid and mid not in allowed:  # 按工单隔离，禁跨工单引用（优先于缺引证判定）
        return mid
    if needs_evidence and not mid:
        return "<缺引证>"
    if needs_evidence and not quote:
        return "<空quote>"
    if mid and mid in (tid_texts or {}) and quote:
        if _norm(quote) not in _norm(tid_texts[mid]):
            return mid
    return ""


def sanitize_sentiment(summary, slice_, texts=None):
    """情绪等级「LLM 提议、脚本门禁」（AGENTS.md 规则 Q，与规则 E 同构）：
    校验 ① sentiment.level ∈ SENTIMENT_ENUM；② 「轻微/明显」必须有 evidence.message_id
    存在于本工单 allowed 集合（按工单隔离）+ 非空 quote + quote 是原文子串（经 _evidence_bad）。
    任一失败 → level 回退「无法判定」并写 sentiment_invalid_evidence 留痕（不可静默）。
    缺 sentiment 字段（LLM 未产出）→ 「无法判定」+ sentiment_missing 标记，
    由 render 决定水印，绝不臆断为「无」（避免把没评估装成没情绪）。"""
    texts = texts or {}
    out = {}
    for tid, s in (summary or {}).items():
        s = dict(s)
        allowed = _allowed_ids(slice_["tickets"].get(tid, {}))
        sent = s.get("sentiment")
        if not isinstance(sent, dict):
            s["sentiment"] = {"level": "无法判定", "evidence": {}, "reason": ""}
            s["sentiment_missing"] = True
            out[tid] = s
            continue
        sent = dict(sent)
        level = sent.get("level")
        ev = sent.get("evidence")
        mid = ev.get("message_id", "") if isinstance(ev, dict) else ""
        if level not in SENTIMENT_ENUM:
            bad = mid or f"<level:{level}>"
        else:
            bad = _evidence_bad(ev, allowed, texts.get(tid),
                                level in SENTIMENT_NEEDS_EVIDENCE)
        if bad:
            sent["level"] = "无法判定"
            s["sentiment_invalid_evidence"] = bad
        s["sentiment"] = sent
        out[tid] = s
    return out


def sanitize_summary(summary, slice_, texts=None):
    """LLM 提议、脚本门禁：effective_status 枚举校验 + effective_evidence 的
    messageId 存在性 + 非空 quote + quote 对所指消息原文做子串校验（经 _evidence_bad）；
    任一失败回退规则默认并留痕。"""
    texts = texts or {}
    out = {}
    for tid, s in (summary or {}).items():
        s = dict(s)
        sig = slice_.get("signals", {}).get(tid, {})
        readable = slice_.get("subgroup_readable", {}).get(tid)
        t = slice_["tickets"].get(tid, {})
        fallback = default_effective(t, sig, readable)
        allowed = _allowed_ids(t)
        ev = s.get("effective_evidence")
        mid = ev.get("message_id", "") if isinstance(ev, dict) else ""
        status = s.get("effective_status")
        if status not in EFFECTIVE_ENUM:
            bad = mid or "<status>"
        else:
            bad = _evidence_bad(ev, allowed, texts.get(tid),
                                status != "无法判定(无子群)")
        if bad:
            s["effective_status_invalid_evidence"] = bad
            s["effective_status"] = fallback
        if not s.get("effective_status"):
            s["effective_status"] = fallback
        out[tid] = s
    return out
