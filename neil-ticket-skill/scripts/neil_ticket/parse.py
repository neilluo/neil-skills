"""解析层：主群机器人卡片正则与卡片→工单结构化、实质状态确定性信号抽取（纯函数，无 I/O）。
新增卡片事件类型（如催单）在此加正则常量与 parse_cards 分支，并同批落地
templates/daily-report.md、tests/fixtures 与回归断言、reference.md 报文解剖节
（AGENTS.md 规则 L）；解析哨兵（缺工单ID卡/陌生服务台发送者）也归本层。"""
import re
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
