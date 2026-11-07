#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render_arch_html.py —— arch.json(v2) → 单文件 HTML 架构图

布局（docs/arch_schema.md v2）：
  标题/meta 条 → summary_flow 链 → edge 顶带 → 业务泳道(lines，置顶)
  → 平台共享层(shared) → 基础设施(infra，沉底)
  泳道内：入口|计算|数据 三列 grid ＋ observe 横条（贯穿三列）＋ 依赖 chips

用法：python3 scripts/render_arch_html.py arch.json -o out.html
零第三方依赖；输出自包含单文件（CSS 内联，无外链）。
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from typing import Any, Dict, List

LINE_COLORS: Dict[str, tuple] = {
    "enter":   ("#fff4e8", "#c2410c", "#e8833a"),
    "framia":  ("#f3efff", "#6d28d9", "#8b5cf6"),
    "game":    ("#eaf3ff", "#1e3a5f", "#3b82f6"),
    "concat":  ("#fffbe8", "#92400e", "#f59e0b"),
    "work":    ("#e9fbf3", "#065f46", "#10b981"),
    "platform": ("#eef2fb", "#334155", "#64748b"),
    "infra":   ("#e8f6f5", "#0f766e", "#14b8a6"),
    "edge":    ("#f5f7fa", "#475569", "#94a3b8"),
}
COLOR_MAP = {"enter": "enter", "framia": "framia", "game": "game",
             "concat": "concat", "work": "work", "anycap": "work",
             "shared": "platform", "infra": "infra"}
BADGE = {"P0": ("#dc2626", "#fef2f2"), "P1": ("#d97706", "#fffbeb"),
         "P2": ("#a16207", "#fefce8")}
COL_TITLES = {"入口": "入口（接入 / 网关）", "计算": "计算（容器 / Serverless）",
              "数据": "数据 / 消息", "AI": "AI / 模型路由",
              "核心库": "核心库", "消息流": "消息 / 流", "分析同步": "分析 / 同步",
              "治理注册": "治理 / 注册", "容器网络": "容器 / 网络 / 出口"}


def esc(s: Any) -> str:
    return html.escape(str(s if s is not None else ""))


def money(v: Any, client: bool = False) -> str:
    if client:
        return ""
    if v is None:
        return "成本未拆分"
    return f"¥{int(v):,}/月"


def card_html(c: Dict[str, Any], risks_by_target: Dict[str, List[Dict]],
              client: bool = False, masks: List[str] = None) -> str:
    badges = ""
    for r in risks_by_target.get(c.get("id", ""), []):
        fg, bg = BADGE.get(r["level"], BADGE["P2"])
        badges += (f'<span class="badge" style="color:{fg};background:{bg};'
                   f'border:1px solid {fg}">{esc(r["level"])}</span>')
    ev = c.get("evidence") or ""
    for m in (masks or []):
        ev = ev.replace(m, "•••")
    if client:
        import re as _re
        ev = _re.sub(r"cost 最小的 \d+ 张卡[:：]\s*", "", ev)
        ev = _re.sub(r"成本未拆分\s*", "", ev)
    ev = esc(ev)
    if len(ev) > 34:
        ev = ev[:33] + "…"
    note = c.get("note") or ""
    if client:
        import re as _re2
        note = _re2.sub(r"cost 最小的 \d+ 张卡[；;]?\s*", "", note)
        note = _re2.sub(r"长尾合并（\s*）", "长尾合并", note)
    note = esc(note)
    sub = ev + (f"｜{note}" if note else "")
    cost = money(c.get("cost"), client)
    cost_html = f'<div class="ccost">{cost}</div>' if cost else ""
    return (f'<div class="card">{badges}<div class="cname">{esc(c.get("name"))}'
            f'</div><div class="csub">{sub}</div>{cost_html}</div>')


def lane_html(line: Dict[str, Any], risks_by_target: Dict[str, List[Dict]],
              col_keys: List[str], deps: List[Dict[str, Any]],
              lane_id_map: Dict[str, str], client: bool = False,
              masks: List[str] = None) -> str:
    ck = COLOR_MAP.get(line.get("id", ""), line.get("color", "platform"))
    bg, stroke, accent = LINE_COLORS.get(ck, LINE_COLORS["platform"])
    cols = ""
    for key in col_keys:
        comps = (line.get("layers") or {}).get(key) or []
        title = COL_TITLES.get(key, key)
        cards = "".join(card_html(c, risks_by_target, client, masks) for c in comps) or \
            '<div class="empty">—</div>'
        cols += (f'<div class="col"><div class="colt">{esc(title)} '
                 f'<span class="cnt">{len(comps)}</span></div>{cards}</div>')
    obs = line.get("observe") or []
    obs_html = ""
    if obs:
        chips = ""
        for c in obs:
            ev = c.get("evidence") or ""
            for m in (masks or []):
                ev = ev.replace(m, "•••")
            chips += (f'<span class="ochip">{esc(c.get("name"))}'
                      f'<i>{esc(ev[:26])}</i>'
                      + (f'<i>{money(c.get("cost"))}</i>' if not client else '')
                      + '</span>')
        obs_html = (f'<div class="observe"><span class="otag">观测（横切）</span>'
                    f'<div class="ochips">{chips}</div></div>')
    dep_html = ""
    if deps:
        items = "".join(
            f'<span class="dep">⤓ {esc(d.get("label") or d.get("kind"))} '
            f'→ {esc(lane_id_map.get(d.get("to_lane", ""), d.get("to_lane", "")))}</span>'
            for d in deps)
        dep_html = f'<div class="deps">{items}</div>'
    cost = line.get("cost_month")
    cost_html = ""
    if not client:
        cost_s = f"月均 ¥{int(cost):,}" if cost else "月均 —"
        cost_html = f'<span class="lcost">{cost_s}</span>'
    return (f'<section class="lane" style="background:{bg};border-color:{stroke}">'
            f'<header style="border-left:6px solid {accent}">'
            f'<span class="lname" style="color:{stroke}">{esc(line.get("name"))}</span>'
            f'<span class="lgrp">{esc(line.get("group"))}</span>'
            f'{cost_html}</header>'
            f'<div class="cols" style="grid-template-columns:repeat({len(col_keys)},1fr)">'
            f'{cols}</div>{obs_html}{dep_html}</section>')


def biz_col_html(line: Dict[str, Any], risks_by_target: Dict[str, List[Dict]],
                 deps: List[Dict[str, Any]], lane_id_map: Dict[str, str],
                 client: bool = False, masks: List[str] = None) -> str:
    """业务层内的一条产品线 = 一个并列列（peer column）。

    列内竖排 入口/计算/数据 三个子块 ＋ 观测横条 ＋ 依赖 chips；
    六条产品线同处一个「业务层」带内并排，表达同级关系。
    """
    ck = COLOR_MAP.get(line.get("id", ""), line.get("color", "platform"))
    bg, stroke, accent = LINE_COLORS.get(ck, LINE_COLORS["platform"])
    blocks = ""
    for key in ("入口", "计算", "数据"):
        comps = (line.get("layers") or {}).get(key) or []
        cards = "".join(card_html(c, risks_by_target, client, masks)
                        for c in comps) or '<div class="empty">—</div>'
        blocks += (f'<div class="bblock"><div class="colt">'
                   f'{esc(COL_TITLES.get(key, key))} '
                   f'<span class="cnt">{len(comps)}</span></div>{cards}</div>')
    obs = line.get("observe") or []
    obs_html = ""
    if obs:
        chips = ""
        for c in obs:
            ev = c.get("evidence") or ""
            for m in (masks or []):
                ev = ev.replace(m, "•••")
            chip_cost = "" if client else f'<i>{money(c.get("cost"))}</i>'
            chips += (f'<span class="ochip">{esc(c.get("name"))}'
                      f'<i>{esc(ev[:18])}</i>{chip_cost}</span>')
        obs_html = (f'<div class="observe"><span class="otag">观测</span>'
                    f'<div class="ochips">{chips}</div></div>')
    dep_html = ""
    if deps:
        items = ""
        for d in deps:
            lab = d.get("label") or d.get("kind") or ""
            if len(lab) > 22:
                lab = lab[:21] + "…"
            tgt = lane_id_map.get(d.get("to_lane", ""), d.get("to_lane", ""))
            items += f'<span class="dep">⤓ {esc(lab)} → {esc(tgt)}</span>'
        dep_html = f'<div class="deps">{items}</div>'
    cost = line.get("cost_month")
    cost_html = ""
    if not client:
        cost_html = f'<span class="bcost">¥{int(cost):,}/月</span>' if cost else ""
    return (f'<div class="bizcol" style="background:{bg};border-color:{stroke}">'
            f'<div class="bhead" style="border-left:4px solid {accent}">'
            f'<span class="bname" style="color:{stroke}">{esc(line.get("name"))}</span>'
            f'<span class="bgrp">{esc(line.get("group"))}</span>{cost_html}</div>'
            f'{blocks}{obs_html}{dep_html}</div>')


def build(arch: Dict[str, Any], client: bool = False) -> str:
    meta = arch.get("meta") or {}
    # 对客脱敏掩码：UID 等内部标识在 evidence 串里出现时替换
    masks = [str(meta.get("uid"))] if client else []
    risks_by_target: Dict[str, List[Dict]] = {}
    all_blocks = list(arch.get("lines") or []) + \
        [arch.get("shared"), arch.get("infra")]
    for blk in all_blocks:
        if not blk:
            continue
        for r in blk.get("risks") or []:
            risks_by_target.setdefault(r.get("target", ""), []).append(r)
    lane_id_map = {}
    for blk in all_blocks:
        if blk:
            lane_id_map[blk.get("id", "")] = blk.get("name", "")
    # cross_links → 源泳道依赖 chips
    deps_by_lane: Dict[str, List[Dict]] = {}
    comp_lane: Dict[str, str] = {}
    for blk in all_blocks:
        if not blk:
            continue
        for comps in list((blk.get("layers") or {}).values()) + [blk.get("observe") or []]:
            for c in comps:
                comp_lane[c.get("id", "")] = blk.get("id", "")
    for lk in arch.get("cross_links") or []:
        src = comp_lane.get(lk.get("from", ""))
        dst = comp_lane.get(lk.get("to", ""))
        if src and dst and src != dst:
            deps_by_lane.setdefault(src, []).append(
                {"label": lk.get("label"), "kind": lk.get("kind"), "to_lane": dst})

    flow = "".join(
        f'<span class="fnode{" fend" if i in (0, len(meta.get("summary_flow") or []) - 1) else ""}">'
        f'{esc(n)}</span><span class="farrow">→</span>'
        for i, n in enumerate(meta.get("summary_flow") or []))[:-len('<span class="farrow">→</span>')]

    edge = arch.get("edge") or {}
    edge_note = edge.get("note") or ""
    if client:
        import re as _re
        edge_note = _re.sub(r"[（(]\s*arch_schema[^）)]*[）)]", "", edge_note).strip()
    edge_cards = "".join(card_html(c, risks_by_target, client, masks) for c in edge.get("comps") or [])
    edge_html = (f'<section class="lane edgeband"><header style="border-left:6px solid '
                 f'{LINE_COLORS["edge"][2]}"><span class="lname" style="color:'
                 f'{LINE_COLORS["edge"][1]}">{esc(edge.get("name") or "全球边缘与加速")}'
                 f'</span><span class="lgrp">{esc(edge_note)}</span></header>'
                 f'<div class="edgegrid">{edge_cards}</div></section>')

    biz_cols = ""
    for line in arch.get("lines") or []:
        biz_cols += biz_col_html(line, risks_by_target,
                                 deps_by_lane.get(line.get("id", ""), []),
                                 lane_id_map, client, masks)
    lanes = (f'<section class="bizband"><header><span class="bandname">业务层'
             f'</span><span class="bandsub">六条产品线同层并列 · 各自闭环 '
             f'入口→计算→数据 · 观测横切</span></header>'
             f'<div class="bizgrid">{biz_cols}</div></section>')
    shared = arch.get("shared") or {}
    shared_html = lane_html(shared, risks_by_target,
                            ["入口", "计算", "数据", "AI"],
                            deps_by_lane.get(shared.get("id", ""), []), lane_id_map,
                            client, masks)
    infra = arch.get("infra") or {}
    infra_html = lane_html(infra, risks_by_target,
                           ["核心库", "消息流", "分析同步", "治理注册", "容器网络"],
                           deps_by_lane.get(infra.get("id", ""), []), lane_id_map,
                           client, masks)

    months = "、".join(meta.get("months_complete") or meta.get("months") or [])
    if client:
        # 对客版：不出现任何金额、内部 UID/CID、schema/生成时间等内部口径
        meta_line = (f'账号 {esc(meta.get("account"))}｜账期 '
                     f'{esc(months)}｜组件清单由账单实例维度还原')
    else:
        total = sum((b.get("cost_month") or 0) for b in all_blocks if b)
        meta_line = (f'UID {esc(meta.get("uid"))}｜CID {esc(meta.get("cid"))}｜'
                     f'完整月 {esc(months)}｜业务+共享+基建月均合计 ¥{int(total):,}'
                     f'｜schema {esc(meta.get("schema_version"))}｜生成 '
                     f'{esc(meta.get("generated_at"))}')
    head = (f'<div class="head"><h1>{esc(meta.get("customer"))} · '
            f'{esc(meta.get("brand"))} 云上架构</h1>'
            f'<div class="meta">{meta_line}</div>'
            f'<div class="flow">{flow}</div></div>')

    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(meta.get('customer'))} 云上架构 v2</title>
<style>
:root{{--ink:#1f2937;--sub:#6b7280;--line:#e2e6ea;--bg:#f6f8fa}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);
color:var(--ink);padding:24px 28px 56px;font-size:12px}}
.head h1{{font-size:20px}} .head .meta{{color:var(--sub);font-size:11.5px;margin:6px 0 10px}}
.flow{{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-bottom:16px}}
.fnode{{background:#e3edfb;border:1px solid #93b4e0;border-radius:6px;padding:4px 10px;font-size:11.5px}}
.fnode.fend{{background:#e7f8ef;border-color:#7fcba4;border-radius:14px}}
.farrow{{color:#94a3b8}}
.lane{{border:1px solid;border-radius:10px;margin-bottom:14px;overflow:hidden}}
.lane>header{{display:flex;align-items:baseline;gap:10px;padding:8px 14px;
background:rgba(255,255,255,.55);border-bottom:1px solid var(--line)}}
.lname{{font-weight:700;font-size:13.5px}} .lgrp{{font-size:10.5px;color:var(--sub);
background:rgba(255,255,255,.8);border:1px solid var(--line);border-radius:4px;padding:1px 6px}}
.lcost{{margin-left:auto;font-size:11px;color:var(--sub)}}
.cols{{display:grid;gap:10px;padding:12px 14px 6px}}
.colt{{font-size:11px;font-weight:600;color:var(--sub);margin-bottom:6px;letter-spacing:.3px}}
.colt .cnt{{font-weight:400;background:rgba(255,255,255,.85);border-radius:8px;padding:0 5px;font-size:10px}}
.card{{position:relative;background:#fff;border:1px solid var(--line);border-radius:7px;
padding:6px 9px;margin-bottom:7px}}
.cname{{font-size:11.5px;font-weight:600}} .csub{{font-size:10px;color:var(--sub);
font-family:ui-monospace,Menlo,monospace;margin-top:2px;word-break:break-all}}
.ccost{{font-size:10px;color:#0f766e;margin-top:2px}}
.badge{{position:absolute;top:-6px;right:-4px;font-size:9px;font-weight:700;
border-radius:4px;padding:0 4px;line-height:14px}}
.empty{{color:#cbd5e1;font-size:11px;padding:4px}}
.observe{{margin:2px 14px 10px;padding:7px 10px;background:rgba(255,255,255,.6);
border:1px dashed #b6c2cf;border-radius:7px;display:flex;gap:10px;align-items:flex-start}}
.otag{{font-size:10px;color:var(--sub);white-space:nowrap;padding-top:3px}}
.ochips{{display:flex;flex-wrap:wrap;gap:6px}}
.ochip{{background:#fff;border:1px solid var(--line);border-radius:5px;padding:2px 7px;font-size:10.5px}}
.ochip i{{font-style:normal;color:var(--sub);font-family:ui-monospace,Menlo,monospace;margin-left:5px}}
.deps{{margin:0 14px 12px;display:flex;flex-wrap:wrap;gap:6px}}
.dep{{font-size:10.5px;color:#475569;background:rgba(255,255,255,.75);
border:1px solid #cbd5e1;border-radius:12px;padding:2px 9px}}
.edgeband .edgegrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));
gap:8px;padding:12px 14px}}
.bizband{{border:1px solid #cbd5e1;border-radius:12px;background:#fff;margin-bottom:14px}}
.bizband>header{{display:flex;align-items:baseline;gap:10px;padding:9px 14px;
border-bottom:1px solid var(--line);background:#f8fafc;border-radius:12px 12px 0 0}}
.bandname{{font-weight:700;font-size:14px}} .bandsub{{font-size:11px;color:var(--sub)}}
.bizgrid{{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));
gap:10px;padding:12px 14px 14px;align-items:start;overflow-x:auto}}
.bizcol{{border:1px solid;border-radius:10px;overflow:hidden;min-width:0}}
.bizcol .card{{padding:5px 7px;margin-bottom:5px}}
.bizcol .cname{{font-size:10.8px}} .bizcol .csub{{font-size:9.2px}}
.bizcol .ccost{{font-size:9.2px}}
.bhead{{display:flex;align-items:baseline;gap:7px;padding:7px 10px;
background:rgba(255,255,255,.6);border-bottom:1px solid var(--line);flex-wrap:wrap}}
.bname{{font-weight:700;font-size:12.5px}} .bgrp{{font-size:9.5px;color:var(--sub);
background:rgba(255,255,255,.85);border:1px solid var(--line);border-radius:4px;padding:0 5px}}
.bcost{{margin-left:auto;font-size:10px;color:var(--sub)}}
.bblock{{padding:8px 10px 0}}
.bizcol .observe{{margin:8px 10px 6px}}
.bizcol .deps{{margin:0 10px 10px}}
.bizcol .ochip i{{margin-left:4px}}
</style></head><body>
{head}
{edge_html}
{lanes}
{shared_html}
{infra_html}
</body></html>"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", help="arch.json (schema v2)")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--internal", action="store_true",
                    help="内部版：显示成本/UID/CID（默认对客脱敏，禁默认带钱）")
    a = ap.parse_args()
    with open(a.input, encoding="utf-8") as fh:
        arch = json.load(fh)
    if "lines" not in arch:
        print("ERROR: arch.json missing 'lines'", file=sys.stderr)
        return 2
    ver = (arch.get("meta") or {}).get("schema_version")
    if ver != "v2":
        print(f"ERROR: render_arch_html.py only accepts schema v2, got {ver!r} "
              f"(v1 输入请用 legacy render_excalidraw_arch.py 或重跑 aggregate)",
              file=sys.stderr)
        return 2
    out = build(arch, client=not a.internal)
    if a.internal:
        out = out.replace("<body>",
                          '<body><div style="background:#dc2626;color:#fff;'
                          'font:700 13px/1.6 sans-serif;text-align:center;'
                          'padding:6px 0;position:sticky;top:0;z-index:99">'
                          '内部版：含成本与 UID/CID，禁止对客外发</div>', 1)
    with open(a.output, "w", encoding="utf-8") as fh:
        fh.write(out)
    print(f"wrote {a.output} ({len(out)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
