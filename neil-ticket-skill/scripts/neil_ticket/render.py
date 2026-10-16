"""渲染层：日报 Markdown 模板渲染与转义纯函数（{{token}} 逐 token str.replace，
禁 str.format，AGENTS.md 规则 G）。改日报列须两处同批：templates/daily-report.md
表头 + 本文件行格式（规则 L）；一切入 Markdown 文本必经 esc_cell/esc_prose；
回读校验标记在 verification_markers（与 render 同层，publish 消费）。零新工单的
「昨日结转」节在 carryover_section（数据由 publish 备好后经 render 的 carryover 参
数注入，替换默认零工单说明；改零工单口径＝render/publish 结转逻辑，见规则 L）。"""
from datetime import datetime

from .config import TEMPLATE_PATH, tz_of, window_of
from .gate import default_effective
from .parse import compute_attention


def esc_cell(val):
    return (val or "—").replace("|", "\\|").replace("\n", " ")


def esc_prose(val):
    return (val or "").replace("\n", " ").replace("|", "\\|")


def _urgency(slice_, tid):
    """本工单确定性紧急度信号（collect 写入 slice.signals[tid].urgency）；缺失回退空 dict。"""
    return slice_.get("signals", {}).get(tid, {}).get("urgency", {}) or {}


def _sentiment_level(summary, tid):
    """本工单情绪等级（经 sanitize_sentiment 门禁后），供 _attention_map 合成关注等级。
    summary 缺该工单或缺 sentiment 字段 → 「无法判定」（由 publish 层水印兜底）。"""
    sent = (summary or {}).get(tid, {}).get("sentiment") or {}
    return sent.get("level", "无法判定")


def _attention_map(slice_, summary):
    """逐工单合成关注等级 → {tid: (emoji, level_name, [原因])}（AGENTS.md 规则 R）。
    输入＝slice.signals[tid].urgency（确定性，collect 算好）+ summary[tid].sentiment.level
    （LLM 提议、已过 sanitize_sentiment 门禁）。纯函数，render 顶层调用一次。"""
    out = {}
    for tid in slice_["ticket_order"]:
        t = slice_["tickets"][tid]
        level = _sentiment_level(summary, tid)
        out[tid] = compute_attention(t, _urgency(slice_, tid), level)
    return out


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


def _overview_row(tid, t, eff, readable, probe_err, span, emoji):
    if readable:
        read = "已入群"
    elif readable is False:
        read = {"已解散": "子群已解散(降级)",
                "未入群": "未入群(降级)"}.get(probe_err, "不可读(降级)")
    else:
        read = "无子群"
    return "| {tid} | {title} | {status} | {eff} | {span} | {emoji} | {creator} | {xiaoer} | {read} |".format(
        tid=tid, title=esc_cell(t["title"]), status=esc_cell(t["status"]),
        eff=esc_cell(eff), span=f"{span}天", emoji=emoji,
        creator=esc_cell(t["creator"]), xiaoer=esc_cell(t["xiaoer"]),
        read=read)


def _sentiment_line(s):
    """负面情绪引证行（AGENTS.md 规则 Q/R）：level ∈ {轻微,明显} 且有 reason 时渲染，
    含情绪引证原文（evidence.quote）；LLM 显式判「无法判定」（子群不可读等）渲染标注
    行不留白。合规返回 ""。sentiment 字段整体缺失（sentiment_missing，属流水线缺口/
    旧总结）→ 不在每单渲染（避免逐单噪声），改由 publish 层水印统一提示。
    引证校验失败时 sanitize_sentiment 已把 level 回退「无法判定」并写
    sentiment_invalid_evidence，故回退标注在「无法判定」分支体现（与 effective_status
    的「引证校验失败回退规则」可观测性对齐；不在「轻微/明显」分支——该分支的 level
    必为校验通过值，回退不可能停在此）。"""
    if s.get("sentiment_missing"):
        return ""
    sent = s.get("sentiment") or {}
    level = sent.get("level", "无法判定")
    ev = sent.get("evidence") if isinstance(sent.get("evidence"), dict) else {}
    reason = sent.get("reason", "")
    invalid = s.get("sentiment_invalid_evidence")
    if level in ("轻微", "明显"):
        quote = ev.get("quote", "")
        tail = f"（原文「{esc_prose(quote)}」）" if quote else ""
        return f"- ⚠️ 情绪信号（{level}）：{esc_prose(reason)}{tail}"
    if level == "无法判定":
        why = f"引证校验失败回退（{invalid}）" if invalid else "子群不可读或无充分证据"
        return f"- ⚠️ 情绪信号：无法判定（{why}，无法评估）"
    return ""


def _ticket_section(tid, t, s, eff, ev_text, readable, emoji="", span=None):
    bullets = s.get("process_bullets") or (
        [] if readable else ["子群未入群，无过程细节"])
    timeline = f"{t['created_at'] or '—'} 建单"
    timeline += f" → {t['completed_at']} 完结" if t["completed_at"] else " → 未完结"
    span_txt = f"（存活 {span} 天）" if span is not None else ""
    lines = [
        f"### {emoji} {tid} {esc_prose(t['title']) or '—'}".replace("  ", " "),
        f"- 时间线：{timeline}{span_txt}",
        f"- 建单人 / 当前小二：{esc_cell(t['creator'])} / {esc_cell(t['xiaoer'])}",
        f"- 实质状态：{esc_prose(eff)}（引证：{esc_prose(ev_text)}）",
        f"- 问题描述：{esc_prose(s.get('problem') or t['desc_card']) or '—'}",
        "- 处理过程：" + ("" if bullets else "—"),
    ]
    lines += [f"  - {esc_prose(b)}" for b in bullets]
    sent_line = _sentiment_line(s)
    if sent_line:
        lines.append(sent_line)
    lines += [
        f"- 解决方案：{esc_prose(s.get('solution') or t['sol_card']) or '截至生成时无完结总结'}",
        f"- 溯源：建单卡 {t['create_msg_id'] or '—'} / 完结卡 {t['done_msg_id'] or '—'} / 子群 {t['subgroup_cid'] or '—'}",
    ]
    return "\n".join(lines)


def _carryover_ticket_section(d0_date, tid, t, s, eff, ev_text, readable, emoji="", span=None):
    """结转工单块：与正常详情同形（复用 _ticket_section），仅在标题下加一行结转来源标注。"""
    lines = _ticket_section(tid, t, s, eff, ev_text, readable, emoji, span).split("\n")
    carry = f"- 结转自：{d0_date} 日报，当日无新工单"
    return "\n".join([lines[0], carry] + lines[1:])


def _attention_rows(slice_, attention, tids=None):
    """从 slice + attention map 构造重点关注行 [(emoji,tid,title,level,reasons)]，
    只收 🔴/🟡（⚪不入表）。tids 缺省＝slice.ticket_order（当日工单）；结转场景传入
    carry_tids 只取结转单。解耦 slice 查找，便于当日行与结转行合并后统一排序渲染。"""
    rows = []
    for tid in (slice_["ticket_order"] if tids is None else tids):
        emoji, level, reasons = attention.get(tid, ("⚪", "常规", []))
        if emoji in ("🔴", "🟡"):
            rows.append((emoji, tid, slice_["tickets"][tid].get("title", ""), level, reasons))
    return rows


def _attention_section(rows):
    """「零、重点关注」节（AGENTS.md 规则 R）：rows=[(emoji,tid,title,level,reasons)]，
    🔴在前🟡在后（同档保持传入顺序，sorted 稳定）。全空 → 「今日无重点关注工单」。
    rows 由当日 _attention_rows + 结转 _attention_rows 合并而来（结转的跨多日未完结单
    同样是「重点关注」对象，不能只在结转详情块显示而顶部漏列）。reasons 过 esc_prose
    （规则 G：urge_reason 源自子群机器人正文，可能含 | 等 Markdown 敏感字符）。"""
    order = {"🔴": 0, "🟡": 1}
    rows = sorted(rows, key=lambda r: order.get(r[0], 9))
    head = "## 零、重点关注\n"
    if not rows:
        return head + "\n今日无重点关注工单（全部为常规问答）。"
    lines = [f"- {e} **{tid}** {esc_cell(title)}（{level}）：{esc_prose('；'.join(reasons))}"
             for e, tid, title, level, reasons in rows]
    return head + "\n" + "\n".join(lines)


def carryover_section(d0_date, carry_tids, d0_slice, d0_summary, tz_label="+08:00"):
    """零新工单时「三、零工单说明与昨日结转」节纯函数：D0 官方未完结工单逐张结转。
    D0 slice/summary 由 publish 读盘并经 sanitize_summary（以 D0 slice 校验）后传入；
    时间窗按 D0 计算（引证「窗口外」标注以 D0 为准）。概览表不重复列结转工单。
    关注等级按 D0 slice 的 urgency 信号 + D0 summary 的 sentiment 合成（规则 R），
    结转块头 emoji 与正常详情一致。返回 (结转节 markdown, 结转重点关注行)——后者供
    render 顶部「零、重点关注」节合并，使跨多日未完结的结转单也在顶部列出。"""
    start_str, end_str = window_of(d0_date, tz_of(tz_label))
    attention = _attention_map(d0_slice, d0_summary)
    blocks = []
    for tid in carry_tids:
        t = d0_slice["tickets"][tid]
        s = (d0_summary or {}).get(tid, {})
        readable = d0_slice.get("subgroup_readable", {}).get(tid)
        eff = _effective(t, s, readable, d0_slice.get("signals", {}).get(tid, {}))
        ev_text = _evidence_text(s, d0_slice, tid, start_str, end_str)
        emoji = attention.get(tid, ("", "", []))[0]
        span = _urgency(d0_slice, tid).get("days_span")
        blocks.append(_carryover_ticket_section(d0_date, tid, t, s, eff, ev_text,
                                                readable, emoji, span))
    head = (f"## 三、零工单说明与昨日结转\n\n窗口内无新工单；"
            f"以下工单结转自 {d0_date}，官方状态仍未完结")
    md = head + ("\n\n" + "\n\n".join(blocks) if blocks else "")
    return md, _attention_rows(d0_slice, attention, carry_tids)


def _rows_and_sections(slice_, summary, attention, start_str, end_str):
    """render 逐工单渲染循环抽出（规则 K）：返回 (概览行列表, 详情块列表)。"""
    rows, sections = [], []
    for tid in slice_["ticket_order"]:
        t = slice_["tickets"][tid]
        s = (summary or {}).get(tid, {})
        readable = slice_["subgroup_readable"].get(tid)
        eff = _effective(t, s, readable, slice_.get("signals", {}).get(tid, {}))
        ev_text = _evidence_text(s, slice_, tid, start_str, end_str)
        emoji = attention[tid][0]
        span = _urgency(slice_, tid).get("days_span") or 0
        rows.append(_overview_row(tid, t, eff, readable,
                                  slice_.get("probe_errors", {}).get(tid, ""), span, emoji))
        sections.append(_ticket_section(tid, t, s, eff, ev_text, readable, emoji, span))
    return rows, sections


def _render_values(customer, date_str, tz, tz_label, slice_, attention,
                   rows, sections, zero, followup, watermark, carry_rows):
    """模板占位符 → 值映射抽出（规则 K）；渲染用逐 token str.replace（规则 G，禁 format）。
    carry_rows＝结转单的重点关注行，与当日行合并后交 _attention_section（结转的跨多日
    未完结单也要在顶部列出，不能只在结转详情块显示）。"""
    start_str, end_str = window_of(date_str, tz)
    attn_rows = _attention_rows(slice_, attention) + (carry_rows or [])
    return {
        "ticket_date_compact": date_str.replace("-", ""), "customer_name": customer["name"],
        "window_start": start_str, "window_end": end_str, "timezone": tz_label,
        "generated_at": datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S"),
        "source_group": customer["service_group_name"],
        "attention_section": _attention_section(attn_rows),
        "overview_rows": "\n".join(rows) if rows else "| — | — | — | — | — | — | — | — | — |",
        "watermark": watermark,
        "ticket_sections": "\n\n".join(sections), "zero_section": zero,
        "followup_section": followup,
    }


def render(customer, date_str, slice_, summary, followup="", watermark="",
           tz_label="+08:00", carryover=("", [])):
    """模板渲染纯函数：timezone 由调用方从 cfg 取后传入，本函数不读 config。
    carryover＝(结转节 markdown, 结转重点关注行) 二元组（publish 经 carryover_section
    备好后传入）：md 非空则替换默认零工单说明节，行并入顶部「零、重点关注」；概览表
    仍保持零行占位（结转工单不入当日概览表）。关注等级（规则 R）经 _attention_map
    合成，注入「零、重点关注」节 + 概览列 + 详情头 emoji。"""
    with open(TEMPLATE_PATH, encoding="utf-8") as fh:
        tpl = fh.read()
    tz = tz_of(tz_label)
    start_str, end_str = window_of(date_str, tz)
    attention = _attention_map(slice_, summary)
    rows, sections = _rows_and_sections(slice_, summary, attention, start_str, end_str)
    carry_md, carry_rows = carryover or ("", [])
    zero = ""
    if not slice_["ticket_order"]:
        zero = carry_md or (
            "## 三、零工单说明\n\n窗口内无工单事件（无建单/完结卡片；催单事件已作关注等级硬信号，见 reference）。")
    values = _render_values(customer, date_str, tz, tz_label, slice_, attention,
                            rows, sections, zero, followup, watermark, carry_rows)
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
