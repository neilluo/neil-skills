"""Unit tests for the two renderers in neil-customer-arch (stdlib unittest only).

覆盖两个渲染器，各喂各的契约 fixture（两者输入 schema 不同，禁混用）：
  - render_excalidraw_arch.py（legacy）  ← arch_fixture.json    （v1 六列结构）
  - render_arch_html.py（主渲染器）      ← arch_fixture_v2.json （v2，aggregate 真实产出结构）

Run:  python3 -m unittest discover -s tests -v      (from skill root)
  or: python3 tests/test_render.py
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "render_excalidraw_arch.py"
HTML_SCRIPT = ROOT / "scripts" / "render_arch_html.py"
# tracked 脱敏孪生 fixture（示例客户 / cid 0000000000 / uid 0000000000000000），
# 使 clean clone 上渲染测试可跑且不依赖 gitignored 的 internal/ 真数据。
# v1 结构（infra=接入/观测、lines 六列）——legacy excalidraw 渲染器的输入契约。
FIXTURE = ROOT / "tests" / "fixtures" / "arch_fixture.json"
# v2 结构（顶层 summary_flow、meta.schema_version=v2、infra 五列、lines 三列 + observe）
# ——对齐 aggregate.py 真实产出，是 HTML 主渲染器的输入契约。
FIXTURE_V2 = ROOT / "tests" / "fixtures" / "arch_fixture_v2.json"

_spec = importlib.util.spec_from_file_location("render_excalidraw_arch", SCRIPT)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)  # type: ignore[union-attr]

_html_spec = importlib.util.spec_from_file_location("render_arch_html", HTML_SCRIPT)
hmod = importlib.util.module_from_spec(_html_spec)
_html_spec.loader.exec_module(hmod)  # type: ignore[union-attr]

ARCH = json.loads(FIXTURE.read_text(encoding="utf-8"))
DOC = mod.build(ARCH)
ELS = DOC["elements"]
BY_ID = {e["id"]: e for e in ELS}
ARCH_V2 = json.loads(FIXTURE_V2.read_text(encoding="utf-8"))
HTML_CLIENT = hmod.build(ARCH_V2, client=True)
HTML_INTERNAL = hmod.build(ARCH_V2, client=False)


def el_bbox(el):
    if el["type"] in ("arrow", "line"):
        xs = [el["x"] + p[0] for p in el["points"]]
        ys = [el["y"] + p[1] for p in el["points"]]
        return min(xs), min(ys), max(xs), max(ys)
    return el["x"], el["y"], el["x"] + el["width"], el["y"] + el["height"]


class TestOutputJson(unittest.TestCase):
    def test_cli_writes_parseable_json(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out.excalidraw"
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), str(FIXTURE), "-o", str(out)],
                capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(data["type"], "excalidraw")
            self.assertEqual(data["version"], 2)
            self.assertEqual(data["appState"]["viewBackgroundColor"], "#ffffff")

    def test_elements_non_empty(self):
        self.assertIsInstance(ELS, list)
        self.assertGreater(len(ELS), 0)

    def test_element_style_contract(self):
        for el in ELS:
            self.assertEqual(el["roughness"], 0, el["id"])
            self.assertEqual(el["opacity"], 100, el["id"])
            if el["type"] == "text":
                self.assertEqual(el["text"], el["originalText"], el["id"])
                self.assertEqual(el["fontFamily"], 3, el["id"])


class TestBindings(unittest.TestCase):
    def test_arrow_binding_ids_exist(self):
        for el in ELS:
            if el["type"] != "arrow":
                continue
            for key in ("startBinding", "endBinding"):
                b = el.get(key)
                if b:
                    self.assertIn(b["elementId"], BY_ID,
                                  f"{el['id']}.{key} -> {b['elementId']}")

    def test_bound_elements_resolve(self):
        for el in ELS:
            for b in el.get("boundElements") or []:
                self.assertIn(b["id"], BY_ID, f"{el['id']} binds {b['id']}")
                target = BY_ID[b["id"]]
                if b["type"] == "text":
                    self.assertEqual(target.get("containerId"), el["id"])
                else:
                    binds = [target.get("startBinding"), target.get("endBinding")]
                    self.assertTrue(any(x and x["elementId"] == el["id"]
                                        for x in binds),
                                    f"arrow {b['id']} not bound back to {el['id']}")

    def test_container_text_single(self):
        seen = {}
        for el in ELS:
            cid = el.get("containerId")
            if cid:
                seen.setdefault(cid, []).append(el["id"])
        for cid, texts in seen.items():
            self.assertEqual(len(texts), 1, f"container {cid} binds {texts}")


class TestGeometry(unittest.TestCase):
    def test_no_element_outside_canvas_bbox(self):
        boxes = [el_bbox(e) for e in ELS if not e.get("isDeleted")]
        minx = min(b[0] for b in boxes)
        miny = min(b[1] for b in boxes)
        maxx = max(b[2] for b in boxes)
        maxy = max(b[3] for b in boxes)
        for el in ELS:
            x0, y0, x1, y1 = el_bbox(el)
            self.assertGreaterEqual(x0, minx - 0.51, el["id"])
            self.assertGreaterEqual(y0, miny - 0.51, el["id"])
            self.assertLessEqual(x1, maxx + 0.51, el["id"])
            self.assertLessEqual(y1, maxy + 0.51, el["id"])
        # normalization: content starts exactly at the 80px margin
        self.assertAlmostEqual(minx, mod.MARGIN, places=1)
        self.assertAlmostEqual(miny, mod.MARGIN, places=1)

    def test_card_text_inside_card(self):
        for el in ELS:
            if not el["id"].startswith("card_") or el["type"] != "rectangle":
                continue
            cx0, cy0, cx1, cy1 = el_bbox(el)
            for suffix in ("_name", "_sub"):
                t = BY_ID.get(el["id"] + suffix)
                if not t:
                    continue
                tx0, ty0, tx1, ty1 = el_bbox(t)
                self.assertGreaterEqual(tx0, cx0 - 0.51, t["id"])
                self.assertLessEqual(tx1, cx1 + 0.51,
                                     f"{t['id']} overflows {el['id']}")
                self.assertGreaterEqual(ty0, cy0 - 0.51, t["id"])
                self.assertLessEqual(ty1, cy1 + 0.51, t["id"])

    def test_lane_text_inside_lane(self):
        for el in ELS:
            if el["type"] != "rectangle" or not el["id"].startswith("lane_"):
                continue
            lx0, ly0, lx1, ly1 = el_bbox(el)
            for t in ELS:
                if t["type"] == "text" and t["id"].startswith(el["id"] + "_"):
                    tx0, ty0, tx1, ty1 = el_bbox(t)
                    self.assertLessEqual(tx1, lx1 + 0.51, t["id"])
                    self.assertLessEqual(ty1, ly1 + 0.51, t["id"])


class TestRisks(unittest.TestCase):
    def test_badge_count_equals_risks(self):
        lines = list(ARCH.get("lines") or [])
        for k in ("shared", "infra"):
            if ARCH.get(k):
                lines.append(ARCH[k])
        expected = sum(len(l.get("risks") or []) for l in lines)
        badges = [e for e in ELS
                  if e["type"] == "rectangle" and e["id"].startswith("badge_")]
        self.assertEqual(len(badges), expected)
        self.assertEqual(expected, 3)  # fixture: P0 + P1 (game) + P2 (infra)

    def test_badge_colors_from_palette(self):
        for e in ELS:
            if e["type"] == "rectangle" and e["id"].startswith("badge_"):
                self.assertIn((e["backgroundColor"], e["strokeColor"]),
                              set(mod.RISK_COLORS.values()))


class TestPalette(unittest.TestCase):
    def test_only_palette_colors(self):
        allowed = set(mod.LINE_COLORS.values()) | set(mod.RISK_COLORS.values())
        allowed |= {("#ffffff", "#ffffff"), ("transparent",)}
        for el in ELS:
            sc, bg = el["strokeColor"], el["backgroundColor"]
            ok = (sc, bg) in allowed or (bg, sc) in allowed \
                or sc in mod.LINK_COLORS.values() or sc == mod.ARROW_STRUCT \
                or sc in (mod.TXT_TITLE, mod.TXT_SUBTITLE, mod.TXT_BODY,
                          mod.TXT_ON_LIGHT) \
                or bg in ("transparent", "#ffffff") \
                or (sc, bg) in ((s, f) for f, s in mod.LINE_COLORS.values())
            self.assertTrue(ok, f"{el['id']}: {sc}/{bg}")


class TestHtmlRenderer(unittest.TestCase):
    """render_arch_html.py（主渲染器）——拆分前零覆盖，此处补上。"""

    def test_summary_flow_from_top_level(self):
        """回归：契约把 summary_flow 放 arch 顶层，曾误读 meta.summary_flow 致概览链恒空。"""
        flow = ARCH_V2.get("summary_flow") or []
        self.assertTrue(flow, "v2 fixture 必须有顶层 summary_flow")
        self.assertFalse((ARCH_V2.get("meta") or {}).get("summary_flow"),
                         "fixture 应贴近 aggregate 真实产出：meta 内不放 summary_flow")
        for node in flow:
            self.assertIn(node, HTML_CLIENT, f"概览链节点漏渲染: {node}")
        self.assertEqual(HTML_CLIENT.count('class="fnode'), len(flow))

    def test_client_version_desensitized(self):
        """AGENTS 第 8 条对客红线：默认脱敏，¥/月均/UID/CID/schema/生成时间零命中。"""
        meta = ARCH_V2["meta"]
        for pat in ("¥", "月均", "UID", "CID", "schema", "generated_at"):
            self.assertNotIn(pat, HTML_CLIENT, f"对客版泄漏内部口径: {pat}")
        for secret in (str(meta.get("uid")), str(meta.get("cid"))):
            if secret and set(secret) != {"0"}:
                self.assertNotIn(secret, HTML_CLIENT, f"对客版泄漏标识: {secret}")
        self.assertNotIn(meta.get("generated_at", ""), HTML_CLIENT)

    def test_internal_version_shows_cost_and_identity(self):
        """内部版（--internal / client=False）必须带成本与 UID/CID，禁与对客版同产物。"""
        self.assertIn("¥", HTML_INTERNAL)
        self.assertIn("UID", HTML_INTERNAL)
        self.assertIn("CID", HTML_INTERNAL)
        self.assertIn(ARCH_V2["meta"]["schema_version"], HTML_INTERNAL)

    def test_risk_badges_rendered(self):
        """回归：v1 fixture 喂 v2 渲染器时 infra 列名不认 → P2 badge 静默丢失。"""
        levels = [r["level"] for b in
                  (list(ARCH_V2.get("lines") or []) +
                   [ARCH_V2.get("shared"), ARCH_V2.get("infra")]) if b
                  for r in (b.get("risks") or [])]
        self.assertEqual(sorted(levels), ["P0", "P1", "P2"])
        for lv in ("P0", "P1", "P2"):
            self.assertIn(f'>{lv}</span>', HTML_CLIENT, f"风险 badge 未渲染: {lv}")

    def test_infra_v2_columns_all_present(self):
        """回归：v2 infra 五列必须全部渲染，缺一列即列名与 aggregate 产出不匹配。"""
        cols = list((ARCH_V2.get("infra") or {}).get("layers") or {})
        self.assertEqual(cols, ["核心库", "消息流", "分析同步", "治理注册", "容器网络"])
        for col, comps in (ARCH_V2["infra"]["layers"]).items():
            for c in comps:
                self.assertIn(c["name"], HTML_CLIENT, f"infra/{col} 卡片漏渲染: {c['name']}")

    def test_layer_order_edge_then_lines_then_shared_then_infra(self):
        """AGENTS 第 2 条：edge 顶带 → 业务泳道 → 共享层 → infra 沉底，禁 infra 上浮。"""
        pos = {k: HTML_CLIENT.find(k) for k in
               ("edgeband", "bizband", "平台共享层", "基础设施")}
        for k, v in pos.items():
            self.assertGreaterEqual(v, 0, f"缺层: {k}")
        self.assertLess(pos["edgeband"], pos["bizband"])
        self.assertLess(pos["bizband"], pos["平台共享层"])
        self.assertLess(pos["平台共享层"], pos["基础设施"])

    def test_cross_links_as_chips_not_svg_arrows(self):
        """AGENTS 第 4 条：跨泳道依赖用 chip 表达，HTML 里不画 SVG 箭头。"""
        self.assertNotIn("<svg", HTML_CLIENT)
        self.assertNotIn("<path", HTML_CLIENT)
        links = ARCH_V2.get("cross_links") or []
        self.assertTrue(links, "v2 fixture 应有 cross_links")
        self.assertIn('class="dep"', HTML_CLIENT)
        for lk in links:
            self.assertIn(lk["label"], HTML_CLIENT, f"依赖 chip 漏渲染: {lk['label']}")

    def test_observe_rendered_as_horizontal_bar_not_column(self):
        """AGENTS 第 3 条：观测是横切横条，禁做第四列。"""
        for line in ARCH_V2["lines"]:
            for c in line.get("observe") or []:
                self.assertIn(c["name"], HTML_CLIENT, f"observe 漏渲染: {c['name']}")
        self.assertIn('class="observe"', HTML_CLIENT)
        self.assertIn("观测（横切）", HTML_CLIENT)

    def test_cli_rejects_v1_input(self):
        """AGENTS 第 5 条：只认 v2，遇 v1 直接报错退出，禁静默兼容。"""
        v1 = json.loads(json.dumps(ARCH_V2))
        v1["meta"].pop("schema_version", None)
        with tempfile.TemporaryDirectory() as td:
            src, out = Path(td) / "v1.json", Path(td) / "o.html"
            src.write_text(json.dumps(v1), encoding="utf-8")
            proc = subprocess.run([sys.executable, str(HTML_SCRIPT), str(src),
                                   "-o", str(out)], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
            self.assertIn("only accepts schema v2", proc.stderr)
            self.assertFalse(out.exists(), "报错后不应产出文件")

    def test_cli_rejects_real_v1_fixture(self):
        """legacy v1 fixture（arch_fixture.json）必须被主渲染器拒绝——两渲染器契约不可混用。"""
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "o.html"
            proc = subprocess.run([sys.executable, str(HTML_SCRIPT), str(FIXTURE),
                                   "-o", str(out)], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)

    def test_cli_internal_flag_adds_banner(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "i.html"
            proc = subprocess.run([sys.executable, str(HTML_SCRIPT), str(FIXTURE_V2),
                                   "-o", str(out), "--internal"],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            html = out.read_text(encoding="utf-8")
            self.assertIn("内部版：含成本与 UID/CID，禁止对客外发", html)

    def test_cli_default_has_no_banner_and_no_cost(self):
        """默认（不加 --internal）必须是对客脱敏件，禁默认带钱。"""
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "c.html"
            proc = subprocess.run([sys.executable, str(HTML_SCRIPT), str(FIXTURE_V2),
                                   "-o", str(out)], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            html = out.read_text(encoding="utf-8")
            self.assertNotIn("禁止对客外发", html)
            self.assertNotIn("¥", html)


class TestDesensitizationRegressions(unittest.TestCase):
    """钉死 2026-11-08 review 查出并修复的 4 个脱敏缺陷。"""

    def test_empty_uid_does_not_corrupt_evidence(self):
        """P0：uid="" 曾使 masks=[""]，str.replace("","•••") 把每字符间插弹号成乱码。"""
        self.assertEqual(hmod.build_masks({"uid": ""}, True), [])
        self.assertEqual(hmod.build_masks({"uid": None}, True), [])
        self.assertEqual(hmod.build_masks({}, True), [])
        broken = json.loads(json.dumps(ARCH_V2))
        broken["meta"]["uid"] = ""
        html = hmod.build(broken, client=True)
        self.assertNotIn("•••d•••c•••", html)
        self.assertNotIn("•••" * 3, html)
        for c in ARCH_V2["edge"]["comps"]:
            self.assertIn(c["evidence"], html, f"evidence 不该被空 mask 打碎: {c['evidence']}")

    def test_valid_uid_still_masked(self):
        """正向：真实 uid 出现在 evidence 串里必须被掩成 •••（旧测试因全 0 fixture 而空转）。"""
        masks = hmod.build_masks({"uid": "1077748325118640",
                                  "cid": "1941872709"}, True)
        self.assertEqual(masks, ["1077748325118640", "1941872709"])
        leaky = json.loads(json.dumps(ARCH_V2))
        leaky["meta"]["uid"] = "1077748325118640"
        leaky["meta"]["cid"] = "1941872709"
        leaky["edge"]["comps"][0]["evidence"] = "归属 1077748325118640 的 CDN"
        html = hmod.build(leaky, client=True)
        self.assertNotIn("1077748325118640", html, "evidence 内嵌 uid 未掩码")
        self.assertIn("归属 ••• 的 CDN", html)

    def test_internal_terminology_scrubbed(self):
        """P1：内部归线方法论与内部文件名禁进对客件。"""
        self.assertEqual(hmod.client_scrub("untagged:命名"), "")
        self.assertEqual(hmod.client_scrub("untagged:VPC"), "")
        self.assertEqual(hmod.client_scrub("饱和抽样存在性证据（金额见 product_rows）"),
                         "存在性证据")
        self.assertEqual(hmod.client_scrub("cost 最小的 3 张卡：r-1"), "r-1")
        # 空括号被剥掉但有意义的文字保留（不是整串清空）
        self.assertEqual(hmod.client_scrub("长尾合并（ ）"), "长尾合并")
        leaky = json.loads(json.dumps(ARCH_V2))
        leaky["lines"][0]["group"] = "untagged:命名"
        leaky["lines"][0]["layers"]["计算"][0]["note"] = "无实例维度·产品级取证"
        html = hmod.build(leaky, client=True)
        self.assertNotIn("untagged", html, "归线兜底值泄漏到对客版")
        self.assertNotIn("无实例维度", html)
        self.assertNotIn("product_rows", html)

    def test_internal_banner_present_at_build_level(self):
        """P1：横幅曾只在 main() 注入，import build() 的调用方拿到带钱版无警示。"""
        self.assertIn(hmod.INTERNAL_BANNER, HTML_INTERNAL)
        self.assertNotIn(hmod.INTERNAL_BANNER, HTML_CLIENT)
        self.assertIn("¥", HTML_INTERNAL)

    def test_missing_risk_level_does_not_crash(self):
        """P1：risks 条目缺 level 曾 r["level"] 硬索引 KeyError 整图渲染失败。"""
        broken = json.loads(json.dumps(ARCH_V2))
        broken["lines"][1]["risks"].append({"target": "game_data_oss", "text": "无 level"})
        html = hmod.build(broken, client=True)   # 不抛异常即通过
        self.assertTrue(html.startswith("<!DOCTYPE html>"))
        # 缺 level 兜底成 P2 badge，且原有 P0/P1 仍在
        for lv in ("P0", "P1", "P2"):
            self.assertIn(f'>{lv}</span>', html)

    def test_line_count_label_matches_data(self):
        """P1：bandsub 曾写死「六条产品线」，喂 2 条 line 也照印，文案与数据恒不符。"""
        self.assertIn(f"{len(ARCH_V2['lines'])} 条产品线同层并列", HTML_CLIENT)
        self.assertNotIn("六条产品线", HTML_CLIENT)


class TestLegacyV2Gap(unittest.TestCase):
    """诚实记录 legacy excalidraw 渲染器未对齐 v2 的现状（AGENTS 第 1 条已降级为 legacy）。

    LAYER_ORDER 仍是 v1 六列（接入/计算/数据/消息/AI/观测），喂 aggregate 真实 v2 产出
    （infra 五列）时列名不匹配 → 组件静默丢失。这不是本次拆分引入，是 v2 迁移遗留。
    下列用例把该缺口钉成显式失败信号：一旦有人升级 legacy 对齐 v2，这两条会自动变红，
    提醒同步删除本类。
    """

    def test_legacy_does_not_read_v2_infra_columns(self):
        self.assertEqual(mod.LAYER_ORDER,
                         ["接入", "计算", "数据", "消息", "AI", "观测"],
                         "legacy LAYER_ORDER 已改动——若已对齐 v2，请删除 TestLegacyV2Gap 并补正向用例")

    def test_legacy_on_v2_input_loses_infra_cards(self):
        doc = mod.build(ARCH_V2)
        texts = " ".join(e.get("text", "") for e in doc["elements"]
                         if e["type"] == "text")
        lost = [c["name"] for c in ARCH_V2["infra"]["layers"]["容器网络"]]
        for name in lost:
            self.assertNotIn(name, texts,
                             f"legacy 现在能渲染 v2 infra 卡片了（{name}）——"
                             "请删除 TestLegacyV2Gap 并补正向用例")


if __name__ == "__main__":
    unittest.main(verbosity=2)
