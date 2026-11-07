"""Unit tests for scripts/render_excalidraw_arch.py (stdlib unittest only).

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
FIXTURE = ROOT / "tests" / "fixtures" / "arch_fixture.json"

_spec = importlib.util.spec_from_file_location("render_excalidraw_arch", SCRIPT)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)  # type: ignore[union-attr]

ARCH = json.loads(FIXTURE.read_text(encoding="utf-8"))
DOC = mod.build(ARCH)
ELS = DOC["elements"]
BY_ID = {e["id"]: e for e in ELS}


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


if __name__ == "__main__":
    unittest.main(verbosity=2)
