"""解析层：主群机器人卡片正则与卡片→工单结构化、实质状态确定性信号抽取（纯函数，无 I/O）。
新增卡片事件类型（如催单）在此加正则常量与 parse_cards 分支，并同批落地
templates/daily-report.md、tests/fixtures 与回归断言、reference.md 报文解剖节
（AGENTS.md 规则 L）；解析哨兵（缺工单ID卡/陌生服务台发送者）也归本层。
关注等级（AGENTS.md 规则 R）：compute_urgency_signals 抽取确定性紧急度信号，
compute_attention 合成三档关注等级（🔴重点/🟡留意/⚪常规）。"""
import re
from datetime import date, datetime
from urllib.parse import unquote


def double_unquote(val):
    return unquote(unquote(val))


RE_CREATE = re.compile(r"已为您创建新企业工单")
RE_DONE = re.compile(r"企业工单已完结")
RE_CREATOR = re.compile(r"@(\S+?)\s+已为您创建新企业工单")
RE_TITLE_FONT = re.compile(r"企业工单标题：<font color=#096DD9>(.*?)</font>", re.S)
RE_TITLE_PLAIN = re.compile(r"企业工单标题：([^\n]+)")
RE_TID = re.compile(r"企业工单ID：(E[0-9A-Za-z]+)")
RE_STATUS = re.compile(r"企业工单状态：(\S+)")
RE_XIAOER = re.compile(r"当前小二：(\S+)")
RE_CONV_ID = re.compile(r"openconversitionid(?:%3D|=)([A-Za-z0-9%=_\-+/.]+)")
RE_DESC = re.compile(r"【问题描述】(.*?)(?=【[^】]{1,12}】|$)", re.S)
RE_SOL = re.compile(r"【解决方案】(.*?)(?=【[^】]{1,12}】|聊天记录：|$)", re.S)
RE_CONFIRM = re.compile(r"(没有了|谢谢|感谢|解决了|已解决|好的\s*收到|没问题|可以关单|恢复了|正常了)")

# 催单事件（区别于建单卡 Tips 里的「催单」按钮链接——按钮每张卡都有，不是信号）。
# 实测样式：`催单信息：<font >业务阻塞</font>`，是子群里阿里云服务台发的独立机器人消息，
# 2026-10-16 于 outputs/transcripts-2026-10-13-haidilao.json 工单 E2610134H5HZYU 核对。
# 冒号兼容全角「：」与半角「:」；催单原因取 <font> 内文本（无 font 标签则取到行尾/空白）。
RE_URGE = re.compile(r"催单信息[：:]\s*(?:<font[^>]*>)?\s*([^<\n]+?)\s*(?:</font>)?(?:\s|$|<br)")

# 关注等级硬信号风险词表（AGENTS.md 规则 R）：命中即升级。放代码常量而非客户配置，
# 便于统一审计；改词表须同批回写 reference.md「关注等级硬信号词表」（规则 L/M）。
SAFETY_KEYWORDS = ("漏洞", "注入", "绕过", "泄露", "越权", "攻击", "安全风险", "waf")
PRODUCTION_KEYWORDS = ("生产", "不可用", "宕机", "故障", "挂了", "影响业务", "业务阻塞",
                       "无法访问", "报错", "异常", "中断", "超时")


def _ticket_open_date(tid, created_at):
    """建单日（date 对象）：优先 tid 前缀 E26MMDD 解码（比 created_at 可靠——完结日
    collect 的 created_at 为空），解码失败回退 created_at 的日期部分。都拿不到返回 None。"""
    m = re.match(r"E(\d{2})(\d{2})(\d{2})", tid or "")
    if m:
        yy, mm, dd = (int(x) for x in m.groups())
        try:
            return date(2000 + yy, mm, dd)
        except ValueError:
            pass
    if created_at:
        try:
            return datetime.strptime(created_at[:10], "%Y-%m-%d").date()
        except ValueError:
            pass
    return None


def _days_span(tid, created_at, completed_at, today):
    """存活天数：完结日（有）或 today（无）− 建单日。建单日无法解析返回 0。"""
    open_d = _ticket_open_date(tid, created_at)
    if open_d is None:
        return 0
    if completed_at:
        try:
            end_d = datetime.strptime(completed_at[:10], "%Y-%m-%d").date()
        except ValueError:
            end_d = today
    else:
        end_d = today
    return max(0, (end_d - open_d).days)


def _last_active(sub_messages, completed_at):
    """最近活动时间字符串：子群消息 createTime 最大值；无子群消息回退 completed_at；都无返回 ""。"""
    times = [m.get("createTime", "") for m in (sub_messages or []) if m.get("createTime")]
    if times:
        return max(times)
    return completed_at or ""


def _detect_urge(sub_messages, create_card_text, done_card_text):
    """催单信号探测（AGENTS.md 规则 R）。🔴关键：真实催单事件是子群里「阿里云服务台」
    发出的独立机器人消息，正文含「催单信息：<font >业务阻塞</font>」（2026-10-13 实测
    E2610134H5HZYU），**不在** create_card_text/done_card_text 里——建单卡 Tips 的「催单」
    只是每张卡都有的按钮链接（RE_URGE 只匹配「催单信息：」前缀，天然排除按钮）。
    故按序扫：子群消息文本 → 建单卡 → 完结卡，命中即返回催单原因，全不中返回 ""。"""
    sources = [m.get("text") or "" for m in (sub_messages or [])]
    sources += [create_card_text or "", done_card_text or ""]
    for text in sources:
        m = RE_URGE.search(text)
        if m:
            return m.group(1).strip()
    return ""


def compute_urgency_signals(ticket, sub_messages, today, create_card_text="", done_card_text=""):
    """关注等级的确定性紧急度信号（纯函数，无 I/O；AGENTS.md 规则 R）。
    抽取：存活天数、是否完结、最近活跃时间、催单命中、安全/生产标题词命中、
    子群是否可读（决定能否做僵单判定）。只抽事实，不做等级判定（判定在 compute_attention）。
    today＝跑批当日 date 对象（由调用方传入，保持纯函数）。催单探测走 _detect_urge
    （扫子群消息文本 + 建单/完结卡，因真实催单事件是子群独立机器人消息）。"""
    tid = ticket.get("tid", "")
    created_at = ticket.get("created_at", "")
    completed_at = ticket.get("completed_at", "")
    title = ticket.get("title", "") or ""
    span = _days_span(tid, created_at, completed_at, today)
    last_active = _last_active(sub_messages, completed_at)
    readable = bool(sub_messages) or ticket.get("subgroup_readable") is True
    return {
        "days_span": span,
        "completed": bool(completed_at),
        "last_active": last_active,
        "urge_reason": _detect_urge(sub_messages, create_card_text, done_card_text),
        "safety_hit": next((k for k in SAFETY_KEYWORDS if k in title), ""),
        "production_hit": next((k for k in PRODUCTION_KEYWORDS if k in title), ""),
        "readable": readable,
        "stalled": _is_stalled(span, completed_at, last_active, readable, today),
    }


def _is_stalled(span, completed_at, last_active, readable, today):
    """疑似僵单：仅当子群可读（合思那种未自动入群的降级单不做僵单判定，用户 2026-10-16）
    且未完结且最近活动距今 >24h（或存活≥2天但无任何子群消息活动）。"""
    if completed_at or not readable:
        return False
    if not last_active:
        return span >= 2
    try:
        la = datetime.strptime(last_active[:19], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return span >= 2
    now = datetime.combine(today, datetime.min.time())
    return (now - la).total_seconds() > 24 * 3600


def compute_attention(ticket, urgency, sentiment_level):
    """合成三档关注等级（AGENTS.md 规则 R，纯函数）。返回 (emoji, level_name, [触发原因])。
    ticket 形参当前未读取（保留契约位：未来按客户/建单人分级时可用，签名与调用方已对齐）。
    🔴重点：催单事件(业务阻塞)｜安全类标题｜未完结且明显负面｜明显负面情绪。
    🟡留意：跨天未完结(存活≥2)｜跨天已完结(耗时≥2天，关注时效)｜轻微负面｜生产故障标题｜疑似僵单(仅子群可读)。
    ⚪常规：其余（当天完结普通问答／建单无应答但子群不可读）。
    sentiment_level ∈ SENTIMENT_ENUM（gate 层枚举，经 sanitize_sentiment 门禁后传入）。"""
    reasons = []
    span = urgency.get("days_span", 0)
    completed = urgency.get("completed", False)
    sentiment_level = sentiment_level or "无法判定"
    if urgency.get("urge_reason"):
        reasons.append(f"催单事件：{urgency['urge_reason']}")
    if urgency.get("safety_hit"):
        reasons.append(f"安全类标题命中「{urgency['safety_hit']}」")
    if sentiment_level == "明显":
        reasons.append("未完结且客户明显负面情绪" if not completed else "客户明显负面情绪")
    if reasons:
        return "🔴", "重点", reasons
    if not completed and span >= 2:
        reasons.append(f"跨天未完结（存活 {span} 天）")
    if completed and span >= 2:
        reasons.append(f"跨天已完结（耗时 {span} 天，关注服务时效）")
    if sentiment_level == "轻微":
        reasons.append("客户轻微负面（催促/质疑）")
    if urgency.get("production_hit"):
        reasons.append(f"生产故障标题命中「{urgency['production_hit']}」")
    if urgency.get("stalled"):
        reasons.append("疑似僵单（子群可读但超 24h 无新活动）")
    if reasons:
        return "🟡", "留意", reasons
    return "⚪", "常规", ["当天完结普通问答" if completed and span == 0 else "常规问答"]


def _blank_ticket(tid):
    return {"tid": tid, "title": "", "status": "", "creator": "", "xiaoer": "",
            "created_at": "", "completed_at": "", "subgroup_cid": "",
            "create_msg_id": "", "done_msg_id": "", "desc_card": "", "sol_card": "",
            "chatrecord_url": "", "create_card_text": "", "done_card_text": ""}


def _apply_create(ticket, msg, text):
    """建单卡分支：重发卡取最早建单时间（比较式而非顺序式）；小二/状态取最新卡。"""
    if not ticket["created_at"] or msg["createTime"] < ticket["created_at"]:
        ticket["created_at"] = msg["createTime"]
        ticket["create_msg_id"] = msg["messageId"]
        ticket["create_card_text"] = text
        c = RE_CREATOR.search(text)
        ticket["creator"] = c.group(1).strip() if c else ticket["creator"]
        t = RE_TITLE_FONT.search(text) or RE_TITLE_PLAIN.search(text)
        ticket["title"] = t.group(1).strip() if t else ticket["title"]
    x = RE_XIAOER.search(text)
    ticket["xiaoer"] = x.group(1).strip() if x else ticket["xiaoer"]
    s = RE_STATUS.search(text)
    ticket["status"] = s.group(1).strip() if s else ticket["status"]


def _apply_done(ticket, msg, text):
    """完结卡分支：状态/标题兜底/问题描述/解决方案/聊天记录链接以完结卡为准。"""
    ticket["completed_at"] = msg["createTime"]
    ticket["done_msg_id"] = msg["messageId"]
    ticket["done_card_text"] = text
    ticket["status"] = "已完结"
    t = RE_TITLE_PLAIN.search(text)
    ticket["title"] = ticket["title"] or (t.group(1).strip() if t else "")
    d = RE_DESC.search(text)
    ticket["desc_card"] = d.group(1).strip() if d else ""
    s = RE_SOL.search(text)
    ticket["sol_card"] = s.group(1).strip() if s else ""
    url_m = re.search(r"聊天记录：\[查看\]\((dingtalk://[^)]+)\)", text)
    ticket["chatrecord_url"] = url_m.group(1) if url_m else ""


def _note_subgroup(ticket, cids, tid, order):
    """建单/完结两分支共用尾部：首个非主群会话 id 定为子群，order 去重登记。"""
    if cids and not ticket["subgroup_cid"]:
        ticket["subgroup_cid"] = sorted(cids)[0]
    if tid not in order:
        order.append(tid)


def parse_cards(messages, main_cid, bot="阿里云服务台"):
    """主群机器人卡片解析 → (tickets, order, warnings)。
    解析哨兵归本层（评审分层归位）：卡片文案命中但缺工单ID = 改版/漏配信号；
    未配置的服务台类发送者 = 机器人更名/多机器人信号。"""
    tickets, order, warnings = {}, [], []
    odd_senders = set()
    for msg in messages:
        text = msg.get("text") or ""
        sender = msg.get("sender")
        if sender != bot:
            if "服务台" in (sender or ""):
                odd_senders.add(sender)
            continue
        tid_m = RE_TID.search(text)
        if not tid_m:
            if RE_CREATE.search(text) or RE_DONE.search(text):
                warnings.append(f"机器人卡片缺工单ID，解析可能漏单：{msg.get('messageId')}")
            continue
        tid = tid_m.group(1)
        ticket = tickets.setdefault(tid, _blank_ticket(tid))
        cids = {double_unquote(c) for c in RE_CONV_ID.findall(text)}
        cids.discard(main_cid)
        cids.discard("")
        if RE_CREATE.search(text):
            _apply_create(ticket, msg, text)
            _note_subgroup(ticket, cids, tid, order)
        if RE_DONE.search(text):
            _apply_done(ticket, msg, text)
            _note_subgroup(ticket, cids, tid, order)
        if not ticket["status"]:
            s = RE_STATUS.search(text)
            ticket["status"] = s.group(1).strip() if s else ""
    if odd_senders:
        warnings.append(f"出现未配置的服务台类发送者：{sorted(odd_senders)}")
    return tickets, order, warnings


def compute_signals(ticket, sub_messages):
    """实质状态的确定性信号：工程师总结块 / 客户确认语。只抽事实，不做判定。
    确认语排除小二本人发言（评审 P2：小二说「没问题」不是客户确认）。"""
    sig = {"engineer_summary_msgs": [], "customer_confirm_msgs": []}
    xiaoer = (ticket.get("xiaoer") or "").strip()
    msgs = list(sub_messages or [])
    engineer_senders = {(m.get("sender") or "").strip() for m in msgs
                        if "【解决方案】" in (m.get("text") or "") and len(m.get("text") or "") > 80}
    for m in msgs:
        text = m.get("text") or ""
        sender = (m.get("sender") or "").strip()
        item = {"messageId": m.get("messageId", ""), "sender": sender,
                "quote": text[:60].replace("\n", " ")}
        if "【解决方案】" in text and len(text) > 80:
            sig["engineer_summary_msgs"].append(item)
        elif (RE_CONFIRM.search(text) and len(text) < 120
              and sender != xiaoer and not sender.startswith("TAM")
              and sender not in engineer_senders):
            sig["customer_confirm_msgs"].append(item)
    return sig
