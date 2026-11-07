#!/usr/bin/env python3
"""Data-driven Excalidraw architecture renderer for neil-kunpeng-expert.

Consumes arch.json (contract: docs/arch_schema.md) and emits an Excalidraw v2
JSON file.  Pure python3 stdlib; deterministic output (stable ids + seeds).

Layout (three zoom levels, per excalidraw-diagram-skill methodology):
  L1  meta.summary_flow  -> horizontal chain: ellipse / rectangles / ellipse
  L2  lines[]            -> one swim-lane rectangle per LINE (light fill +
                            colored stroke), header = name + group + cost
  L3  layers             -> six ordered columns per lane; COMP cards stacked
                            vertically; P0/P1/P2 risk badges on card corners
  shared / infra lanes render full-width below the product lanes.
  cross_links            -> bound arrows between COMP cards (orthogonal
                            routing) + midpoint label on a white plate.

Element fields follow references/element-templates.md of
excalidraw-diagram-skill verbatim (roughness 0, opacity 100, fontFamily 3,
text == originalText, bound arrows registered in target boundElements).
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Palette (single source of truth: excalidraw-diagram-skill
# references/color-palette.md).  Every pair below is copied verbatim from the
# "Shape Colors (Semantic)" table; comments record the palette row used.
# ---------------------------------------------------------------------------
LINE_COLORS: Dict[str, Tuple[str, str]] = {
    # enter  -> palette "Start/Trigger"   fill #fed7aa / stroke #c2410c
    "enter": ("#fed7aa", "#c2410c"),
    # framia -> palette "AI/LLM"          fill #ddd6fe / stroke #6d28d9
    "framia": ("#ddd6fe", "#6d28d9"),
    # game   -> palette "Tertiary"        fill #93c5fd / stroke #1e3a5f
    "game": ("#93c5fd", "#1e3a5f"),
    # concat -> palette "Decision"        fill #fef3c7 / stroke #b45309
    "concat": ("#fef3c7", "#b45309"),
    # work   -> palette "End/Success"     fill #a7f3d0 / stroke #047857
    "work": ("#a7f3d0", "#047857"),
    # platform -> palette "Inactive/Disabled" pair, solid stroke here
    "platform": ("#dbeafe", "#1e40af"),
    # infra  -> palette "Secondary"       fill #60a5fa / stroke #1e3a5f
    "infra": ("#60a5fa", "#1e3a5f"),
}
DEFAULT_LANE_COLOR = ("#dbeafe", "#1e40af")  # palette Inactive/Disabled pair

# Risk badge colors: palette Error / Start-Trigger / Decision rows.
RISK_COLORS = {
    "P0": ("#fecaca", "#b91c1c"),  # palette "Error"
    "P1": ("#fed7aa", "#c2410c"),  # palette "Start/Trigger" (orange)
    "P2": ("#fef3c7", "#b45309"),  # palette "Decision" (yellow)
}

# Text hierarchy colors (palette "Text Colors (Hierarchy)").
TXT_TITLE = "#1e40af"
TXT_SUBTITLE = "#3b82f6"
TXT_BODY = "#64748b"
TXT_ON_LIGHT = "#374151"

# Structural / arrow colors (palette "Default Stroke & Line Colors").
ARROW_STRUCT = "#1e3a5f"
LINK_COLORS = {"data": "#1e3a5f", "ai": "#6d28d9", "msg": "#b45309"}

LAYER_ORDER = ["接入", "计算", "数据", "消息", "AI", "观测"]

# Layout constants ------------------------------------------------------------
MARGIN = 80
LANE_GAP = 40
LANE_PAD_X = 16
LANE_HDR_H = 56
COL_GAP = 28
COL_HDR_H = 28
CARD_GAP = 14
CARD_PAD_X = 12  # -> card width = max(line widths) + 24
CARD_NAME_FS = 14
CARD_SUB_FS = 11
CARD_H = 70
BADGE_H = 18
BADGE_FS = 11
SUMMARY_FS = 14
SUMMARY_H = 52
SUMMARY_GAP = 52
SUMMARY_MAX_W = 250
TITLE_FS = 24
SUBTITLE_FS = 12
GUTTER = 56  # reserved right-hand routing channel inside every lane


# ---------------------------------------------------------------------------
# Text metrics.  Excalidraw fontFamily 3 renders Latin/digits in Cascadia
# (monospace) and CJK in a full-width face.  Per docs/arch_schema.md the
# estimate is CJK ~= fontSize, Latin ~= 0.6*fontSize; a 6% safety factor is
# applied on top (calibrated against canvas measureText of the real fonts).
# ---------------------------------------------------------------------------
def _char_w(ch: str, fs: float) -> float:
    return fs if ord(ch) >= 0x2000 else 0.6 * fs


def text_w(s: str, fs: float) -> float:
    return sum(_char_w(c, fs) for c in s) * 1.06


def text_h(lines: int, fs: float) -> float:
    return lines * fs * 1.25


def trunc(s: str, n: int = 24) -> str:
    return s if len(s) <= n else s[: n - 1] + "…"


def wrap(s: str, fs: float, max_w: float) -> List[str]:
    """Greedy char-wise wrap (CJK-safe) into at most two lines; line 2 truncates."""
    if text_w(s, fs) <= max_w:
        return [s]
    lines: List[str] = []
    cur = ""
    for ch in s:
        if cur and text_w(cur + ch, fs) > max_w:
            lines.append(cur)
            cur = ch
            if len(lines) == 2:
                break
        else:
            cur += ch
    if len(lines) < 2:
        lines.append(cur)
    # line 2 keeps any remainder, then truncates to fit max_w
    second = lines[1] + s[len(lines[0]) + len(lines[1]):]
    while second and text_w(second, fs) > max_w:
        second = second[:-1]
    lines[1] = second + ("…" if second != s[len(lines[0]):] else "")
    return lines


# ---------------------------------------------------------------------------
# Element factories (field-for-field copies of element-templates.md)
# ---------------------------------------------------------------------------
class Builder:
    def __init__(self) -> None:
        self.elements: List[Dict[str, Any]] = []
        self._seed = 100000

    def seed(self) -> int:
        self._seed += 7
        return self._seed

    def _base(self, typ: str, eid: str, x: float, y: float, w: float, h: float,
              stroke: str, bg: str, sw: int = 2) -> Dict[str, Any]:
        return {
            "type": typ,
            "id": eid,
            "x": x, "y": y, "width": w, "height": h,
            "strokeColor": stroke,
            "backgroundColor": bg,
            "fillStyle": "solid",
            "strokeWidth": sw,
            "strokeStyle": "solid",
            "roughness": 0,
            "opacity": 100,
            "angle": 0,
            "seed": self.seed(),
            "version": 1,
            "versionNonce": self.seed(),
            "isDeleted": False,
            "groupIds": [],
            "boundElements": None,
            "link": None,
            "locked": False,
        }

    def rect(self, eid: str, x: float, y: float, w: float, h: float,
             stroke: str, bg: str, sw: int = 2,
             roundness: Optional[int] = 3) -> Dict[str, Any]:
        el = self._base("rectangle", eid, x, y, w, h, stroke, bg, sw)
        el["boundElements"] = []
        if roundness is not None:
            el["roundness"] = {"type": roundness}
        self.elements.append(el)
        return el

    def ellipse(self, eid: str, x: float, y: float, w: float, h: float,
                stroke: str, bg: str, sw: int = 2) -> Dict[str, Any]:
        el = self._base("ellipse", eid, x, y, w, h, stroke, bg, sw)
        el["boundElements"] = []
        el["roundness"] = {"type": 2}
        self.elements.append(el)
        return el

    def text(self, eid: str, x: float, y: float, s: str, fs: float,
             color: str, align: str = "left", valign: str = "top",
             container: Optional[str] = None) -> Dict[str, Any]:
        lines = s.split("\n")
        w = max(text_w(ln, fs) for ln in lines)
        h = text_h(len(lines), fs)
        el = self._base("text", eid, x, y, w, h, color, "transparent", 1)
        el.update({
            "text": s,
            "originalText": s,
            "fontSize": fs,
            "fontFamily": 3,
            "textAlign": align,
            "verticalAlign": valign,
            "containerId": container,
            "lineHeight": 1.25,
        })
        self.elements.append(el)
        return el

    def arrow(self, eid: str, x: float, y: float, points: List[List[float]],
              stroke: str, start_id: Optional[str] = None,
              end_id: Optional[str] = None, sw: int = 2) -> Dict[str, Any]:
        # 契约：x/y 为箭头锚点绝对坐标，points 为相对 (x, y) 的偏移（调用方负责）。
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        el = self._base("arrow", eid, x, y, max(xs) - min(xs), max(ys) - min(ys),
                        stroke, "transparent", sw)
        el.update({
            "points": points,
            "startBinding": {"elementId": start_id, "focus": 0, "gap": 2} if start_id else None,
            "endBinding": {"elementId": end_id, "focus": 0, "gap": 2} if end_id else None,
            "startArrowhead": None,
            "endArrowhead": "arrow",
        })
        self.elements.append(el)
        return el

    def bind(self, shape: Dict[str, Any], text_id: Optional[str] = None,
             arrow_id: Optional[str] = None) -> None:
        if shape["boundElements"] is None:
            shape["boundElements"] = []
        if text_id:
            shape["boundElements"].append({"id": text_id, "type": "text"})
        if arrow_id:
            shape["boundElements"].append({"id": arrow_id, "type": "arrow"})

    def by_id(self, eid: str) -> Dict[str, Any]:
        for el in self.elements:
            if el["id"] == eid:
                return el
        raise KeyError(eid)


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
def fmt_cost(v: Optional[float]) -> str:
    if v is None:
        return "成本未拆分"
    return f"¥{int(round(v)):,}/月"


def card_lines(comp: Dict[str, Any]) -> Tuple[str, str]:
    name = comp.get("name") or comp.get("id", "")
    sub = trunc(comp.get("evidence") or "", 24)
    cost = fmt_cost(comp.get("cost"))
    return name, (f"{sub}\n{cost}" if sub else cost)


def card_size(name: str, sub: str) -> Tuple[float, float]:
    # +26 on the name line keeps the risk badge (top-right) off the text.
    w = max(text_w(name, CARD_NAME_FS) + 26,
            max((text_w(ln, CARD_SUB_FS) for ln in sub.split("\n")), default=0)
            + 2 * CARD_PAD_X)
    return w, CARD_H


def layout_lane(b: Builder, line: Dict[str, Any], lx: float, ly: float,
                lane_w: Optional[float], card_ids: Dict[str, str],
                info: Optional[Dict[str, Any]] = None,
                lane_idx: int = 0) -> Tuple[float, float]:
    """Render one swim lane at (lx, ly). Returns (height, width).

    When ``info`` is given, per-comp routing corridors (row gaps, column
    gaps, lane padding band) are recorded there for the link router.
    """
    lid = line["id"]
    fill, stroke = LINE_COLORS.get(line.get("color", ""), DEFAULT_LANE_COLOR)
    layers = line.get("layers") or {}
    present = [k for k in LAYER_ORDER if layers.get(k)]

    col_widths: List[float] = []
    col_cards: List[List[Dict[str, Any]]] = []
    for key in present:
        comps = layers[key]
        widths = [card_size(*card_lines(c))[0] for c in comps] or [120]
        col_widths.append(max(max(widths), 120))
        col_cards.append(comps)

    content_w = (sum(col_widths) + COL_GAP * max(len(present) - 1, 0)
                 if present else 0)
    hdr_name = line.get("name") or lid
    hdr_meta = f"{line.get('group', '')} · 月均 {fmt_cost(line.get('cost_month'))}"
    hdr_w = max(text_w(hdr_name, 18), text_w(hdr_meta, SUBTITLE_FS))
    width = max(lane_w or 0, content_w + 2 * LANE_PAD_X + GUTTER,
                hdr_w + 2 * LANE_PAD_X)

    col_h: List[float] = []
    for comps in col_cards:
        h = sum(CARD_H + CARD_GAP for _ in comps)
        col_h.append(h - CARD_GAP if comps else 0)
    body_h = (COL_HDR_H + max(col_h, default=0) + 24) if present else 40
    height = LANE_HDR_H + body_h

    b.rect(f"lane_{lid}", lx, ly, width, height, stroke, fill, 2)
    b.text(f"lane_{lid}_name", lx + LANE_PAD_X, ly + 10, hdr_name, 18, stroke)
    b.text(f"lane_{lid}_meta", lx + LANE_PAD_X, ly + 10 + 26, hdr_meta,
           SUBTITLE_FS, TXT_BODY)

    cx = lx + LANE_PAD_X
    cy0 = ly + LANE_HDR_H
    pad_y = ly + height - 12  # lane bottom padding band (clean corridor)
    col_gap_xs: List[float] = []
    for ci, (key, cw, comps) in enumerate(zip(present, col_widths, col_cards)):
        b.text(f"col_{lid}_{key}", cx, cy0, key, 14, stroke)
        col_gap_xs.append(cx + cw + COL_GAP / 2)
        yy = cy0 + COL_HDR_H
        for ri, comp in enumerate(comps):
            name, sub = card_lines(comp)
            cw_i, _ = card_size(name, sub)
            card = b.rect(f"card_{comp['id']}", cx, yy, cw, CARD_H,
                          stroke, "#ffffff", 1)
            # Card body text stays free-floating INSIDE the card: Excalidraw
            # containers bind exactly one text, cards need two blocks.
            b.text(f"card_{comp['id']}_name", cx + CARD_PAD_X, yy + 9,
                   name, CARD_NAME_FS, TXT_ON_LIGHT)
            b.text(f"card_{comp['id']}_sub", cx + CARD_PAD_X, yy + 33, sub,
                   CARD_SUB_FS, TXT_BODY)
            card_ids[comp["id"]] = card["id"]
            if info is not None:
                gap_above = (cy0 + COL_HDR_H / 2 if ri == 0
                             else yy - CARD_GAP / 2)
                gap_below = (pad_y if ri == len(comps) - 1
                             else yy + CARD_H + CARD_GAP / 2)
                info[comp["id"]] = {
                    "lane": lane_idx, "col": ci, "row": ri,
                    "ncols": len(present), "nrows": len(comps),
                    "col_x": cx, "col_w": cw,
                    "gap_above": gap_above, "gap_below": gap_below,
                    "pad_y": pad_y, "row0": ri == 0,
                }
            yy += CARD_H + CARD_GAP
        cx += cw + COL_GAP
    if info is not None:
        info.setdefault("_lanes", {})[lane_idx] = {
            "x": lx, "y": ly, "w": width, "h": height,
            "col_gap_xs": col_gap_xs, "pad_y": pad_y,
            "gutter_x": lx + width - GUTTER / 2,
        }
    return height, width


def route_link(si: Dict[str, Any], di: Dict[str, Any],
               s_el: Dict[str, Any], d_el: Dict[str, Any],
               lanes: Dict[int, Dict[str, Any]],
               trunk_x: float) -> Tuple[List[List[float]], Tuple[float, float]]:
    """Manhattan route through reserved corridors only: column gaps (full
    height, empty), lane bottom padding bands, and a trunk channel in the
    white margin right of every lane.  Links never cross a card.
    Returns absolute points and the label anchor."""
    sl, dl = lanes[si["lane"]], lanes[di["lane"]]

    def exit_x(i: Dict[str, Any], lane: Dict[str, Any]) -> float:
        return (lane["col_gap_xs"][i["col"]] if i["col"] < i["ncols"] - 1
                else lane["gutter_x"])

    def entry_x(i: Dict[str, Any], lane: Dict[str, Any]) -> Tuple[float, str]:
        if i["col"] > 0:
            return lane["col_gap_xs"][i["col"] - 1], "l"
        if i["col"] < i["ncols"] - 1:
            return lane["col_gap_xs"][i["col"]], "r"
        return lane["gutter_x"], "r"

    scy = s_el["y"] + s_el["height"] / 2
    tcy = d_el["y"] + d_el["height"] / 2
    sx = s_el["x"] + s_el["width"]
    ex_x, e_side = entry_x(di, dl)
    t_edge = d_el["x"] if e_side == "l" else d_el["x"] + d_el["width"]
    s_exit = exit_x(si, sl)

    pts: List[List[float]] = [[sx, scy], [s_exit, scy], [s_exit, sl["pad_y"]]]
    if si["lane"] != di["lane"]:
        pts += [[trunk_x, sl["pad_y"]], [trunk_x, dl["pad_y"]]]
    pts += [[ex_x, dl["pad_y"]], [ex_x, tcy], [t_edge, tcy]]

    out = [pts[0]]
    for p in pts[1:]:
        if abs(p[0] - out[-1][0]) > 0.5 or abs(p[1] - out[-1][1]) > 0.5:
            out.append(p)
    # label anchor: midpoint of the horizontal run along the target lane's
    # bottom padding band (the plate is drawn just BELOW it, in the empty
    # inter-lane gap, so it never covers a card)
    best = None
    for a, c in zip(out, out[1:]):
        if abs(a[1] - c[1]) < 0.5 and abs(a[1] - dl["pad_y"]) < 0.5:
            best = ((a[0] + c[0]) / 2, a[1])
    if best is None:
        best = (out[-1][0], out[-1][1])
    return out, best


def build(arch: Dict[str, Any]) -> Dict[str, Any]:
    b = Builder()
    meta = arch.get("meta") or {}
    card_ids: Dict[str, str] = {}

    # ---- title block (free-floating typography, no containers) ----
    title = f"{meta.get('customer', '')} · {meta.get('brand', '')} 云架构"
    months = "、".join(meta.get("months") or [])
    subtitle = (f"cid {meta.get('cid', '-')} · uid {meta.get('uid', '-')} · "
                f"完整月 {months or '-'} · 生成于 {meta.get('generated_at', '-')}")
    b.text("doc_title", 0, 0, title.strip(), TITLE_FS, TXT_TITLE)
    b.text("doc_subtitle", 0, 36, subtitle, SUBTITLE_FS, TXT_BODY)

    # ---- Level 1: summary flow chain ----
    flow = arch.get("summary_flow") or []
    node_texts = [wrap(s, SUMMARY_FS, SUMMARY_MAX_W) for s in flow]
    node_ws = [max(max(text_w(ln, SUMMARY_FS) for ln in t) + 32, 120)
               for t in node_texts]
    for i, t in enumerate(node_texts):  # ellipses: text sits in the inscribed band
        if i == 0 or i == len(node_texts) - 1:
            lw = max(text_w(ln, SUMMARY_FS) for ln in t)
            node_ws[i] = max(lw * (1.5 if len(t) > 1 else 1.0) + 48, 140)
    y_sum = 84
    x = 0.0
    prev: Optional[Dict[str, Any]] = None
    for i, (lines, w) in enumerate(zip(node_texts, node_ws)):
        h = SUMMARY_H if len(lines) == 1 else SUMMARY_H + 18
        if i == 0:
            node = b.ellipse(f"sum_node_{i}", x, y_sum, w, h,
                             "#c2410c", "#fed7aa")  # palette Start/Trigger
        elif i == len(flow) - 1:
            node = b.ellipse(f"sum_node_{i}", x, y_sum, w, h,
                             "#047857", "#a7f3d0")  # palette End/Success
        else:
            node = b.rect(f"sum_node_{i}", x, y_sum, w, h,
                          "#1e3a5f", "#93c5fd")  # palette Tertiary
        t = b.text(f"sum_node_{i}_t", x, y_sum, "\n".join(lines), SUMMARY_FS,
                   TXT_ON_LIGHT, align="center", valign="middle",
                   container=node["id"])
        b.bind(node, t["id"])
        if prev is not None:
            sx, sy = prev["x"] + prev["width"], prev["y"] + prev["height"] / 2
            ex, ey = node["x"], node["y"] + node["height"] / 2
            ar = b.arrow(f"sum_arrow_{i}", sx, sy,
                         [[0, 0], [ex - sx, ey - sy]],
                         ARROW_STRUCT, prev["id"], node["id"])
            b.bind(prev, arrow_id=ar["id"])
            b.bind(node, arrow_id=ar["id"])
        prev = node
        x += w + SUMMARY_GAP

    # ---- Level 2/3: product swim lanes (natural width) then full-width
    # shared/infra lanes below them (per docs/arch_schema.md) ----
    product = list(arch.get("lines") or [])
    extra = [arch[k] for k in ("shared", "infra") if arch.get(k)]

    info: Dict[str, Any] = {}
    y = y_sum + SUMMARY_H + 24 + 60
    idx = 0
    widths: List[float] = []
    for line in product:
        h, w = layout_lane(b, line, 0.0, y, None, card_ids, info, idx)
        widths.append(w)
        y += h + LANE_GAP
        idx += 1
    full_w = max(widths, default=600)
    for line in extra:
        h, _w = layout_lane(b, line, 0.0, y, full_w, card_ids, info, idx)
        y += h + LANE_GAP
        idx += 1
    lanes_geo = info.get("_lanes", {})
    trunk_x = max((g["x"] + g["w"] for g in lanes_geo.values()), default=0) + 28
    lane_id_by_idx = {i: ln.get("id") for i, ln in enumerate(product + extra)}

    # ---- cross links 在 normalize 之后绘制（见文件末尾 normalize 块后的第二段）----
    cross_links_pending = list(arch.get("cross_links") or [])

    # ---- risk badges on card corners ----
    badge_count = 0
    for line in product + extra:
        for r in line.get("risks") or []:
            cid = card_ids.get(r.get("target", ""))
            if not cid:
                continue
            card = b.by_id(cid)
            fill, stroke = RISK_COLORS.get(r.get("level", "P2"),
                                           RISK_COLORS["P2"])
            label = r.get("level", "P2")
            bw = text_w(label, BADGE_FS) + 14
            bx = card["x"] + card["width"] - bw + 6
            by = card["y"] - BADGE_H / 2
            badge = b.rect(f"badge_{badge_count}_{cid}", bx, by, bw, BADGE_H,
                           stroke, fill, 1)
            bt = b.text(f"badge_{badge_count}_{cid}_t", bx, by, label,
                        BADGE_FS, stroke, align="center", valign="middle",
                        container=badge["id"])
            b.bind(badge, bt["id"])
            badge_count += 1

    # ---- center the Level-1 chain over the lane block ----
    nodes = [e for e in b.elements
             if e["id"].startswith("sum_node_") and e["type"] in ("rectangle", "ellipse")]
    if nodes and lanes_geo:
        chain_w = max(e["x"] + e["width"] for e in nodes) - min(e["x"] for e in nodes)
        lane_right = max(g["x"] + g["w"] for g in lanes_geo.values())
        delta = (lane_right - chain_w) / 2
        if delta > 1:
            for e in b.elements:
                if e["id"].startswith(("sum_node_", "sum_arrow_")):
                    e["x"] += delta

    # ---- normalize: translate bbox min to (MARGIN, MARGIN) ----
    minx = miny = float("inf")
    maxx = maxy = float("-inf")
    for el in b.elements:
        if el["type"] in ("arrow", "line"):
            for px, py in el["points"]:
                minx = min(minx, el["x"] + px)
                miny = min(miny, el["y"] + py)
                maxx = max(maxx, el["x"] + px)
                maxy = max(maxy, el["y"] + py)
        else:
            minx = min(minx, el["x"])
            miny = min(miny, el["y"])
            maxx = max(maxx, el["x"] + el["width"])
            maxy = max(maxy, el["y"] + el["height"])
    dx, dy = MARGIN - minx, MARGIN - miny
    for el in b.elements:
        el["x"] += dx
        el["y"] += dy

    # ---- cross links: lane-level trunk routing（normalize 之后，用最终坐标）----
    # 泳道间依赖是"线对线"关系；竖线只走所有泳道右侧白边 trunk 通道（每 link
    # 偏移 8px），横线只走泳道外缘到 trunk 的白边段，零穿越、不绑定（绑定箭头
    # 会被渲染器重路由覆盖手工点）。
    lane_els = [e for e in b.elements
                if e["type"] == "rectangle" and e["id"].startswith("lane_")]
    if cross_links_pending and lane_els:
        trunk_x = max(e["x"] + e["width"] for e in lane_els) + 28
        label_jobs: List[Tuple[str, float, float]] = []
        for i, link in enumerate(cross_links_pending):
            s_info = info.get(link.get("from", ""))
            d_info = info.get(link.get("to", ""))
            s_id = lane_id_by_idx.get(s_info["lane"]) if s_info else None
            d_id = lane_id_by_idx.get(d_info["lane"]) if d_info else None
            s_el = b.by_id("lane_%s" % s_id) if s_id else None
            d_el = b.by_id("lane_%s" % d_id) if d_id else None
            if not s_el or not d_el:
                continue
            sy = s_el["y"] + s_el["height"] / 2
            dy2 = d_el["y"] + d_el["height"] / 2
            sx = s_el["x"] + s_el["width"]
            dx2 = d_el["x"] + d_el["width"]
            tx = trunk_x + i * 8
            pts = [[sx, sy], [tx, sy], [tx, dy2], [dx2, dy2]]
            color = LINK_COLORS.get(link.get("kind", "data"), ARROW_STRUCT)
            rel = [[p[0] - pts[0][0], p[1] - pts[0][1]] for p in pts]
            b.arrow(f"link_{i}", pts[0][0], pts[0][1], rel, color, None, None)
            if link.get("label"):
                label_jobs.append((link["label"], tx, (sy + dy2) / 2))
        placed: List[Tuple[float, float, float, float]] = []
        for i, (label, mx, my) in enumerate(label_jobs):
            lw = text_w(label, 11)
            px = mx + 6
            py = my - 9
            while any(not (px + lw + 10 < x0 or px > x1
                           or py + 18 < y0 or py > y1)
                      for x0, x1, y0, y1 in placed):
                py += 20
            placed.append((px, px + lw + 10, py, py + 18))
            b.rect(f"link_{i}_plate", px, py,
                   lw + 10, 18, "#ffffff", "#ffffff", 1, roundness=None)
            b.text(f"link_{i}_label", px + 5, py + 2, label, 11, TXT_BODY)

    return {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": b.elements,
        "appState": {"viewBackgroundColor": "#ffffff", "gridSize": 20},
        "files": {},
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", help="arch.json path (see docs/arch_schema.md)")
    ap.add_argument("-o", "--output", required=True, help="output .excalidraw")
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as fh:
        arch = json.load(fh)
    if "lines" not in arch:
        print("ERROR: arch.json missing required key 'lines'", file=sys.stderr)
        return 2
    out = build(arch)
    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print(f"wrote {args.output} ({len(out['elements'])} elements)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
