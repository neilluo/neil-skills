"""纯函数单测（离线，不碰网络/dws）：日期归一、列匹配、对账门、stat_dates。"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "scripts"))

from neil_radar import gate, questions as q  # noqa: E402


class TestNormalizeDate(unittest.TestCase):
    def test_timestamp_head(self):
        self.assertEqual(q.normalize_date("2026-11-06 00:00:00"), "20261106")

    def test_compact(self):
        self.assertEqual(q.normalize_date("20261106"), "20261106")

    def test_slash(self):
        self.assertEqual(q.normalize_date("2026/11/6"), "20261106")

    def test_invalid(self):
        self.assertIsNone(q.normalize_date("not-a-date"))
        self.assertIsNone(q.normalize_date(None))


class TestPickCol(unittest.TestCase):
    def test_exact_only(self):
        self.assertEqual(q.pick_col(["客户名称", "公网络流量/GB"], q.CUSTOMER_CANDIDATES), "客户名称")
        self.assertIsNone(q.pick_col(["客户名称周均值"], q.CUSTOMER_CANDIDATES))


class TestPickMetricCol(unittest.TestCase):
    def test_slash_to_underscore(self):
        names = ["stat_date", "客户名称", "公网络流量_GB", "公网络流量_GB(展示值)"]
        self.assertEqual(q.pick_metric_col(names, "公网络流量/GB"), "公网络流量_GB")

    def test_excludes_display(self):
        names = ["公网络流量_GB(展示值)"]
        self.assertIsNone(q.pick_metric_col(names, "公网络流量/GB"))

    def test_no_substring_fallback(self):
        names = ["公网络流量_GB_周均值"]
        self.assertIsNone(q.pick_metric_col(names, "公网络流量/GB"))


class TestStatDates(unittest.TestCase):
    def test_window(self):
        self.assertEqual(q.stat_dates("2026-11-07", 3), ["20261104", "20261105", "20261106"])


class TestGate(unittest.TestCase):
    def test_pass(self):
        g = gate.gate_pure(1000.0, 1000.0)
        self.assertTrue(g["passed"])

    def test_fail_ratio(self):
        g = gate.gate_pure(500.0, 1000.0)
        self.assertFalse(g["passed"])

    def test_none_inputs(self):
        self.assertFalse(gate.gate_pure(None, 1000.0)["passed"])
        self.assertFalse(gate.gate_pure(1.0, None)["passed"])

    def test_zero_total(self):
        self.assertTrue(gate.gate_pure(0.0, 0.0)["passed"])
        self.assertFalse(gate.gate_pure(5.0, 0.0)["passed"])

    def test_sum_metric(self):
        recs = [{"stat_date": "20261106", "net_total": 3.0},
                {"stat_date": "20261106", "net_total": None},
                {"stat_date": "20261105", "net_total": 9.0}]
        self.assertEqual(gate.sum_metric(recs, "20261106", "net_total"), 3.0)
        self.assertIsNone(gate.sum_metric(recs, "20261101", "net_total"))


class TestParseGroupedRows(unittest.TestCase):
    def setUp(self):
        self.cmap = {"海鸿达(北京)餐饮管理有限公司": "haidilao"}
        self.metrics = [("net_total", "公网络流量/GB")]

    def test_basic(self):
        rows = [{"统计日期": "2026-11-06 00:00:00", "客户名称": "海鸿达(北京)餐饮管理有限公司",
                 "公网络流量/GB": "43,438"}]
        recs, unk, _ = q.parse_grouped_rows(rows, self.metrics, self.cmap)
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0]["customer_key"], "haidilao")
        self.assertEqual(recs[0]["net_total"], 43438.0)
        self.assertEqual(unk, [])

    def test_unknown_customer(self):
        rows = [{"统计日期": "20261106", "客户名称": "陌生公司", "公网络流量/GB": "1"}]
        recs, unk, _ = q.parse_grouped_rows(rows, self.metrics, self.cmap)
        self.assertEqual(recs, [])
        self.assertEqual(unk[0]["report_customer_name"], "陌生公司")
        # 对账门需要 unknown 行携带指标值（全量求和口径）
        self.assertEqual(unk[0]["net_total"], 1.0)

    def test_missing_date_col(self):
        rows = [{"客户名称": "海鸿达(北京)餐饮管理有限公司", "公网络流量/GB": "1"}]
        recs, unk, _ = q.parse_grouped_rows(rows, self.metrics, self.cmap)
        self.assertEqual((recs, unk), ([], []))

    def test_cid_mode(self):
        rows = [{"统计日期": "20261106", "cid": "110133", "日收入": "1,200.5"}]
        recs, unk, _ = q.parse_grouped_rows(rows, [("maas_gaap", "日收入")], {}, cid_mode=True)
        self.assertEqual(recs[0]["maas_cid"], "110133")
        self.assertEqual(recs[0]["maas_gaap"], 1200.5)

    def test_cid_float_normalized(self):
        rows = [{"统计日期": "20261106", "cid": 110133.0, "日收入": "1"}]
        recs, _, _ = q.parse_grouped_rows(rows, [("maas_gaap", "日收入")], {}, cid_mode=True)
        self.assertEqual(recs[0]["maas_cid"], "110133")

    def test_total_row_dropped(self):
        rows = [{"统计日期": "20261106", "客户名称": "合计", "公网络流量/GB": "99999"},
                {"统计日期": "20261106", "客户名称": "海鸿达(北京)餐饮管理有限公司",
                 "公网络流量/GB": "1"}]
        recs, unk, _ = q.parse_grouped_rows(rows, self.metrics, self.cmap)
        self.assertEqual(len(recs), 1)
        self.assertEqual(unk, [])

    def test_fixed_key_degrade(self):
        rows = [{"统计日期": "20261106", "公网络流量/GB": "42"}]
        recs, unk, _ = q.parse_grouped_rows(rows, self.metrics, {}, fixed_key="haidilao")
        self.assertEqual(recs[0]["customer_key"], "haidilao")
        self.assertEqual(recs[0]["net_total"], 42.0)

    def test_missing_cols_reported(self):
        rows = [{"统计日期": "20261106", "客户名称": "海鸿达(北京)餐饮管理有限公司"}]
        recs, _, missing = q.parse_grouped_rows(rows, self.metrics, self.cmap)
        self.assertEqual(missing, ["公网络流量/GB"])
        self.assertIsNone(recs[0]["net_total"])

    def test_multi_block_col_union(self):
        rows = [{"统计日期": "20261106", "客户名称": "海鸿达(北京)餐饮管理有限公司"},
                {"stat_date": "20261106", "客户名称": "海鸿达(北京)餐饮管理有限公司",
                 "公网络流量/GB": "7"}]
        recs, _, missing = q.parse_grouped_rows(rows, self.metrics, self.cmap)
        self.assertEqual(missing, [])
        self.assertEqual(recs[1]["net_total"], 7.0)


if __name__ == "__main__":
    unittest.main()
