"""渲染层：日报 Markdown 模板渲染与转义纯函数（{{token}} 逐 token str.replace，
禁 str.format，AGENTS.md 规则 G）。改日报列须两处同批：templates/daily-report.md
表头 + 本文件行格式（规则 L）；一切入 Markdown 文本必经 esc_cell/esc_prose；
回读校验标记在 verification_markers（与 render 同层，publish 消费）。零新工单的
「昨日结转」节在 carryover_section（数据由 publish 备好后经 render 的 carryover 参
数注入，替换默认零工单说明；改零工单口径＝render/publish 结转逻辑，见规则 L）。"""
from datetime import datetime

from .config import TEMPLATE_PATH, tz_of, window_of
from .gate import default_effective


def esc_cell(val):
    return (val or "—").replace("|", "\\|").replace("\n", " ")


def esc_prose(val):
    return (val or "").replace("\n", " ").replace("|", "\\|")


def _effective(t, s, readable, sig):
    eff = s.get("effective_status") or default_effective(t, sig, readable)
    if s.get("effective_status_invalid_evidence"):
        eff += "(引证校验失败回退规则)"
    return eff


def _evidence_text(s, slice_, tid, start_str, end_str):
    """引证渲染 +「（窗口外）」标注。subgroup_msg_times 由 cmd_collect 写在
    tickets[tid] 内部（ticket 级），必须从同级读取；旧代码读 slice 级恒 None，
    标注永不触发（三方评审裁定真 bug，此处为修复点）。"""
    ev = s.get("effective_evidence") or {}
    text = f"{ev.get('quote', '')} / {ev.get('message_id', '')}" if ev.get("message_id") else "—"
    times = slice_["tickets"].get(tid, {}).get("subgroup_msg_times") or {}
    ev_time = times.get(ev.get("message_id", ""))
    if ev_time and not (start_str <= ev_time < end_str):
        text += "（窗口外）"
    return text


def _overview_row(tid, t, eff, readable, probe_err):
    if readable:
        read = "已入群"
    elif readable is False:
        read = {"已解散": "子群已解散(降级)",
                "未入群": "未入群(降级)"}.get(probe_err, "不可读(降级)")
    else:
        read = "无子群"
    return "| {tid} | {title} | {status} | {eff} | {creator} | {xiaoer} | {read} |".format(
        tid=tid, title=esc_cell(t["title"]), status=esc_cell(t["status"]),
        eff=esc_cell(eff), creator=esc_cell(t["creator"]), xiaoer=esc_cell(t["xiaoer"]),
        read=read)


def _ticket_section(tid, t, s, eff, ev_text, readable):
    bullets = s.get("process_bullets") or (
        [] if readable else ["子群未入群，无过程细节"])
    timeline = f"{t['created_at'] or '—'} 建单"
    timeline += f" → {t['completed_at']} 完结" if t["completed_at"] else " → 未完结"
    return "\n".join([
        f"### {tid} {esc_prose(t['title']) or '—'}",
        f"- 时间线：{timeline}",
        f"- 建单人 / 当前小二：{esc_cell(t['creator'])} / {esc_cell(t['xiaoer'])}",
        f"- 实质状态：{esc_prose(eff)}（引证：{esc_prose(ev_text)}）",
        f"- 问题描述：{esc_prose(s.get('problem') or t['desc_card']) or '—'}",
        "- 处理过程：" + ("" if bullets else "—"),
    ] + [f"  - {esc_prose(b)}" for b in bullets] + [
        f"- 解决方案：{esc_prose(s.get('solution') or t['sol_card']) or '截至生成时无完结总结'}",
        f"- 溯源：建单卡 {t['create_msg_id'] or '—'} / 完结卡 {t['done_msg_id'] or '—'} / 子群 {t['subgroup_cid'] or '—'}",
    ])


def _carryover_ticket_section(d0_date, tid, t, s, eff, ev_text, readable):
    """结转工单块：与正常详情同形（复用 _ticket_section），仅在标题下加一行结转来源标注。"""
    lines = _ticket_section(tid, t, s, eff, ev_text, readable).split("\n")
    carry = f"- 结转自：{d0_date} 日报，当日无新工单"
    return "\n".join([lines[0], carry] + lines[1:])


def carryover_section(d0_date, carry_tids, d0_slice, d0_summary, tz_label="+08:00"):
    """零新工单时「三、零工单说明与昨日结转」节纯函数：D0 官方未完结工单逐张结转。
    D0 slice/summary 由 publish 读盘并经 sanitize_summary（以 D0 slice 校验）后传入；
    时间窗按 D0 计算（引证「窗口外」标注以 D0 为准）。概览表不重复列结转工单。"""
    start_str, end_str = window_of(d0_date, tz_of(tz_label))
    blocks = []
    for tid in carry_tids:
        t = d0_slice["tickets"][tid]
        s = (d0_summary or {}).get(tid, {})
        readable = d0_slice.get("subgroup_readable", {}).get(tid)
        eff = _effective(t, s, readable, d0_slice.get("signals", {}).get(tid, {}))
        ev_text = _evidence_text(s, d0_slice, tid, start_str, end_str)
        blocks.append(_carryover_ticket_section(d0_date, tid, t, s, eff, ev_text, readable))
    head = (f"## 三、零工单说明与昨日结转\n\n窗口内无新工单；"
            f"以下工单结转自 {d0_date}，官方状态仍未完结")
    return head + ("\n\n" + "\n\n".join(blocks) if blocks else "")


def render(customer, date_str, slice_, summary, followup="", watermark="",
           tz_label="+08:00", carryover=""):
    """模板渲染纯函数：timezone 由调用方从 cfg 取后传入，本函数不读 config。
    carryover＝零新工单时的结转节（publish 经 carryover_section 备好后传入），
    非空则替换默认零工单说明节；概览表仍保持零行占位（结转工单不入表）。"""
    with open(TEMPLATE_PATH, encoding="utf-8") as fh:
        tpl = fh.read()
    tz = tz_of(tz_label)
    start_str, end_str = window_of(date_str, tz)
    rows, sections = [], []
    for tid in slice_["ticket_order"]:
        t = slice_["tickets"][tid]
        s = (summary or {}).get(tid, {})
        readable = slice_["subgroup_readable"].get(tid)
        eff = _effective(t, s, readable, slice_.get("signals", {}).get(tid, {}))
        ev_text = _evidence_text(s, slice_, tid, start_str, end_str)
        rows.append(_overview_row(tid, t, eff, readable,
                                  slice_.get("probe_errors", {}).get(tid, "")))
        sections.append(_ticket_section(tid, t, s, eff, ev_text, readable))
    zero = ""
    if not slice_["ticket_order"]:
        zero = carryover or (
            "## 三、零工单说明\n\n窗口内无工单事件（无建单/完结卡片；催单事件尚未建模，见 reference 开放项）。")
    values = {
        "ticket_date_compact": date_str.replace("-", ""), "customer_name": customer["name"],
        "window_start": start_str, "window_end": end_str,
        "timezone": tz_label,
        "generated_at": datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S"),
        "source_group": customer["service_group_name"],
        "overview_rows": "\n".join(rows) if rows else "| — | — | — | — | — | — | — |",
        "watermark": watermark,
        "ticket_sections": "\n\n".join(sections), "zero_section": zero,
        "followup_section": followup,
    }
    out = tpl
    for key, val in values.items():
        out = out.replace("{{" + key + "}}", val)
    return out


def verification_markers(customer, slice_):
    """回读校验必现文本标记，与 render 同层（原 publish_one 内硬编码字符串抽出）。
    返回 [(文档中必须出现的文本, 缺失时汇报的标签)]。"""
    markers = [(f"工单日报（{customer['name']}）", "<标题行>")]
    if not slice_["ticket_order"]:
        markers.append(("零工单", "<零工单说明>"))
    return markers
