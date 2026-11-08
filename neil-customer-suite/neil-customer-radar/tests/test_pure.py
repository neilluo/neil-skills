"""纯函数单测（离线，不碰网络/dws）：日期归一、列匹配、对账门、stat_dates、gate 定稿。"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "scripts"))

from neil_radar import collect, gate, questions as q  # noqa: E402


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

    def test_sum_metric_dedupes_duplicate_rows(self):
        """回归 B5：ChatBI 非确定，同(客户,日期)可能回多行；分子不去重会翻倍致假降级。

        曾直接 sum → 重复行使 ratio≈2 → 对账门必挂 → 触发不必要降级（连带 B2/B4 把
        好数据换坏数据）。修法：按 (身份键, stat_date) 后写覆盖，口径对齐 store.py。"""
        dup = [
            {"customer_key": "haidilao", "stat_date": "20261106", "net_total": 100.0},
            {"customer_key": "haidilao", "stat_date": "20261106", "net_total": 100.0},  # 重复行
            {"customer_key": "hesi", "stat_date": "20261106", "net_total": 50.0},
        ]
        self.assertEqual(gate.sum_metric(dup, "20261106", "net_total"), 150.0,
                         "重复行未去重 = B5 未修（应 100+50，非 100+100+50）")

    def test_sum_metric_first_non_none_wins_on_conflict(self):
        """同(客户,日期)两行都非 None 时取**首个**（与 questions._merge_into 值级合并同口径）。"""
        conflict = [
            {"customer_key": "haidilao", "stat_date": "20261106", "net_total": 100.0},
            {"customer_key": "haidilao", "stat_date": "20261106", "net_total": 120.0},
        ]
        self.assertEqual(gate.sum_metric(conflict, "20261106", "net_total"), 100.0)

    def test_sum_metric_none_does_not_overwrite_real_value(self):
        """末行 None 禁覆盖前面的真值（稀疏行防御网；曾因后写覆盖丢真值）。"""
        conflict = [
            {"customer_key": "haidilao", "stat_date": "20261106", "net_total": 100.0},
            {"customer_key": "haidilao", "stat_date": "20261106", "net_total": None},
        ]
        self.assertEqual(gate.sum_metric(conflict, "20261106", "net_total"), 100.0)
        # 顺序颠倒亦然：真值在末行也要被首个非 None 逻辑捞回
        reversed_rows = [
            {"customer_key": "haidilao", "stat_date": "20261106", "net_total": None},
            {"customer_key": "haidilao", "stat_date": "20261106", "net_total": 70.0},
        ]
        self.assertEqual(gate.sum_metric(reversed_rows, "20261106", "net_total"), 70.0)

    def test_dedupe_keeps_anonymous_rows(self):
        """无身份键的行（纯 {stat_date, metric}）逐行保全，禁因缺键而静默吞真实值。"""
        anon = [{"stat_date": "20261106", "net_total": 3.0},
                {"stat_date": "20261106", "net_total": 4.0}]
        self.assertEqual(gate.sum_metric(anon, "20261106", "net_total"), 7.0)


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

    def test_fixed_key_uses_fixed_name_not_key(self):
        """回归 B4：降级回行无客户列时 report_customer_name 必须填 fixed_name（报表真名），
        禁让 customer_key（如 'haidilao'）污染客户名字段（2026-11-08 15天回填实测污染）。"""
        rows = [{"统计日期": "20261106", "公网络流量/GB": "42"}]
        recs, _, _ = q.parse_grouped_rows(
            rows, self.metrics, {}, fixed_key="haidilao",
            fixed_name="海鸿达(北京)餐饮管理有限公司")
        self.assertEqual(recs[0]["customer_key"], "haidilao")
        self.assertEqual(recs[0]["report_customer_name"], "海鸿达(北京)餐饮管理有限公司",
                         "客户名被 customer_key 污染 = B4 未修")

    def test_total_row_dropped_without_customer_col(self):
        """回归 B4：降级场景回行**全行无客户列**时，合计行仍须靠整行扫描丢弃，
        否则会把全网合计（如 999999）当成某客户的值。

        此处刻意不含任何 CUSTOMER_CANDIDATES 列，逼代码走 _row_is_total 分支
        （若并集里出现「客户名称」，cust_col 非空就测不到该分支）。"""
        rows = [{"统计日期": "20261106", "维度": "合计", "公网络流量/GB": "999999"},
                {"统计日期": "20261106", "维度": "海鸿达", "公网络流量/GB": "42"}]
        recs, unk, _ = q.parse_grouped_rows(
            rows, self.metrics, {}, fixed_key="haidilao", fixed_name="海鸿达")
        vals = [r["net_total"] for r in recs]
        self.assertNotIn(999999.0, vals, "合计行未被丢弃 = B4 未修")
        self.assertEqual(vals, [42.0])

    def test_total_row_still_dropped_with_customer_col(self):
        """对照：有客户列时仍按列值判合计（原路径不被 _row_is_total 破坏）。"""
        rows = [{"统计日期": "20261106", "客户名称": "合计", "公网络流量/GB": "999999"},
                {"统计日期": "20261106", "客户名称": "海鸿达(北京)餐饮管理有限公司",
                 "公网络流量/GB": "42"}]
        recs, _, _ = q.parse_grouped_rows(rows, self.metrics, self.cmap)
        self.assertEqual([r["net_total"] for r in recs], [42.0])

    def test_degrade_metrics_keep_aliases(self):
        """回归 B2：降级路径的 metrics 必须带 aliases（3-tuple），否则报表真名
        与 config field 不一致的指标（net_up: 报表『公网络上行流量/GB』）恒匹配不上。
        2026-11-08 15天回填实测 net_up 60/60 格全丢即此因。"""
        metrics3 = [("net_up", "公网上行流量/GB", ("公网络上行流量/GB",))]
        rows = [{"统计日期": "20261106", "客户名称": "海鸿达(北京)餐饮管理有限公司",
                 "公网络上行流量/GB": "12358"}]   # 报表用 alias 名
        cmap = {"海鸿达(北京)餐饮管理有限公司": "haidilao"}
        recs, _, missing = q.parse_grouped_rows(rows, metrics3, cmap)
        self.assertEqual(recs[0]["net_up"], 12358.0, "alias 未命中 = B2 未修")
        self.assertEqual(missing, [])

    def test_degrade_metrics_without_alias_misses(self):
        """对照：不带 alias 的 2-tuple 在报表用 alias 名时必丢（证明 B2 的必要性）。"""
        metrics2 = [("net_up", "公网上行流量/GB")]   # 无 alias
        rows = [{"统计日期": "20261106", "客户名称": "海鸿达(北京)餐饮管理有限公司",
                 "公网络上行流量/GB": "12358"}]
        cmap = {"海鸿达(北京)餐饮管理有限公司": "haidilao"}
        recs, _, missing = q.parse_grouped_rows(rows, metrics2, cmap)
        self.assertIsNone(recs[0]["net_up"])
        self.assertEqual(missing, ["公网上行流量/GB"])

    def test_missing_cols_reported(self):
        rows = [{"统计日期": "20261106", "客户名称": "海鸿达(北京)餐饮管理有限公司"}]
        recs, _, missing = q.parse_grouped_rows(rows, self.metrics, self.cmap)
        self.assertEqual(missing, ["公网络流量/GB"])
        self.assertIsNone(recs[0]["net_total"])

    def test_multi_block_col_union(self):
        """多 sqlDatas 块拼接时列名取全行并集（rows[0] 无指标列不代表全部块）。

        合并后同(客户,日期)收敛成**一条完整 record**：第一块的 None 被第二块的真值填上，
        禁产出「一条全 None + 一条有值」的半空重复行（review 2026-11-08 B5/B8）。"""
        rows = [{"统计日期": "20261106", "客户名称": "海鸿达(北京)餐饮管理有限公司"},
                {"stat_date": "20261106", "客户名称": "海鸿达(北京)餐饮管理有限公司",
                 "公网络流量/GB": "7"}]
        recs, _, missing = q.parse_grouped_rows(rows, self.metrics, self.cmap)
        self.assertEqual(missing, [])
        self.assertEqual(len(recs), 1, "同(客户,日期)必须合并成唯一 record")
        self.assertEqual(recs[0]["net_total"], 7.0)

    def test_sparse_rows_merge_non_none_wins(self):
        """B5/B8 根因回归：ChatBI 把同一格的不同指标**拆成多个稀疏行**返回，
        必须值级合并（各指标取首个非 None），禁 None 覆盖真值、禁逐行 append 膨胀。
        实测 15 天回填曾因此产出 holdings 172 行（应 60）、unknown 1202 行（应 338）。"""
        rows = [
            {"统计日期": "20261106", "客户名称": "海鸿达(北京)餐饮管理有限公司",
             "公网络流量/GB": "100", "公网上行流量/GB": None},
            {"统计日期": "20261106", "客户名称": "海鸿达(北京)餐饮管理有限公司",
             "公网络流量/GB": None, "公网上行流量/GB": "40"},
            {"统计日期": "20261105", "客户名称": "海鸿达(北京)餐饮管理有限公司",
             "公网络流量/GB": "90", "公网上行流量/GB": "30"},
        ]
        metrics = [("net_total", "公网络流量/GB"), ("net_up", "公网上行流量/GB")]
        recs, unk, _ = q.parse_grouped_rows(rows, metrics, self.cmap)
        self.assertEqual(len(recs), 2, "3 稀疏行应收敛成 2 格（11-06 / 11-05）")
        self.assertEqual(unk, [])
        d = {r["stat_date"]: r for r in recs}
        self.assertEqual(d["20261106"]["net_total"], 100.0, "None 覆盖了真值")
        self.assertEqual(d["20261106"]["net_up"], 40.0, "第二块的真值未合并进来")
        self.assertEqual(d["20261105"]["net_total"], 90.0)
        self.assertEqual(d["20261105"]["net_up"], 30.0)

    def test_unknown_rows_also_merged(self):
        """unknown（config 外客户）同样按(名,日期)合并，禁逐行 append 暴增。"""
        rows = [{"统计日期": "20261106", "客户名称": "北京直客通科技有限公司",
                 "公网络流量/GB": "934"},
                {"统计日期": "20261106", "客户名称": "北京直客通科技有限公司",
                 "公网络流量/GB": None}]
        recs, unk, _ = q.parse_grouped_rows(rows, self.metrics, self.cmap)
        self.assertEqual(recs, [])
        self.assertEqual(len(unk), 1, "unknown 同格必须合并")
        self.assertEqual(unk[0]["net_total"], 934.0)

    def test_cid_mode_merges_sparse_rows(self):
        """maas（cid_mode）同样按(cid,日期)合并稀疏行。"""
        rows = [{"统计日期": "20261106", "cid": 110133.0, "日收入": "1984",
                 "日折算调用量": None},
                {"统计日期": "20261106", "cid": 110133.0, "日收入": None,
                 "日折算调用量": "1018808751"}]
        metrics = [("maas_gaap", "日收入"), ("maas_calls", "日折算调用量")]
        recs, _, _ = q.parse_grouped_rows(rows, metrics, {}, cid_mode=True)
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0]["maas_cid"], "110133")
        self.assertEqual(recs[0]["maas_gaap"], 1984.0)
        self.assertEqual(recs[0]["maas_calls"], 1018808751.0)


class TestFinalizeGate(unittest.TestCase):
    """回归 B6：降级后 gate 结论必须冻结为首次权威判定，禁出现 passed=true&degraded=true。"""

    def test_freezes_first_verdict(self):
        first = {"passed": False, "ratio": 0.9577, "grouped_sum": 41600.8,
                 "report_total": 43437.9, "stat_date": "20261106", "metric": "net_total"}
        out = collect.finalize_gate(first, 60)
        self.assertFalse(out["passed"], "降级只因首次对账失败触发，禁把 passed 改成 True")
        self.assertEqual(out["ratio"], 0.9577, "触发降级的真实 ratio 不得被覆盖丢失")
        self.assertTrue(out["degraded"])
        self.assertEqual(out["degraded_rows"], 60)

    def test_degraded_implies_not_passed_invariant(self):
        """不变式：degraded=True ⇒ passed=False（实测矛盾态 ratio 0.9577 却 degraded）。"""
        out = collect.finalize_gate({"passed": False, "ratio": 0.9}, 12)
        self.assertTrue(out["degraded"])
        self.assertFalse(out["passed"])
        self.assertNotEqual((out["degraded"], out["passed"]), (True, True))

    def test_does_not_mutate_input(self):
        """纯函数：禁就地改入参（cmd_collect 里 first_gate 还要被别处引用）。"""
        first = {"passed": False, "ratio": 0.9, "degraded": False}
        collect.finalize_gate(first, 5)
        self.assertFalse(first["degraded"], "入参被就地修改")
        self.assertNotIn("degraded_rows", first)

    def test_no_degrade_rows_is_still_degraded(self):
        """降级问数无回行时 degraded 仍须为 True（review P1-4），rows=0。"""
        out = collect.finalize_gate({"passed": False, "ratio": 0.5}, 0)
        self.assertTrue(out["degraded"])
        self.assertEqual(out["degraded_rows"], 0)


class TestMissingRowGaps(unittest.TestCase):
    """回归 B7：缺**行**（客户×统计日）必须被检出，否则 holdings 静默落盘不完整。

    _supplement_missing 只补缺列（AGENTS.md 第6条）；holdings 段没有对账门兜底，
    2026-11-08 实测 15 天回填 holdings 仅 27/60 行且无任何告警。"""

    CFG = {"customers": [
        {"key": "haidilao", "report_customer_name": "海鸿达(北京)餐饮管理有限公司"},
        {"key": "hesi", "report_customer_name": "北京合思汇智信息技术有限公司"},
        {"key": "noName", "report_customer_name": None},
    ]}
    METRICS = [("ecs_vcpu", "ecs_vcpu保有量/核"), ("db_instances", "数据库保有实例数/个")]

    def test_detects_missing_rows(self):
        dates = ["20261104", "20261105", "20261106"]
        recs = [{"customer_key": "haidilao", "stat_date": "20261106", "ecs_vcpu": 9206.0},
                {"customer_key": "hesi", "stat_date": "20261106", "ecs_vcpu": 2746.0}]
        gaps = collect.missing_row_gaps(self.CFG, dates, recs, "holdings", self.METRICS)
        # 2 客户 × 3 日 = 6 格，已有 2 格 → 缺 4
        self.assertEqual(len(gaps), 4)
        self.assertEqual({(g["customer_key"], g["stat_date"]) for g in gaps},
                         {("haidilao", "20261104"), ("haidilao", "20261105"),
                          ("hesi", "20261104"), ("hesi", "20261105")})

    def test_row_present_but_all_none_is_still_a_gap(self):
        """B7 残留缺陷（实测）：补问回来的行可能**存在但全 None**（hesi 后 8 天 6 指标全空）。
        只判「行是否存在」会误判已补齐 → 不记 failure、静默落盘空行。"""
        dates = ["20261106"]
        recs = [{"customer_key": "haidilao", "stat_date": "20261106",
                 "ecs_vcpu": None, "db_instances": None},
                {"customer_key": "hesi", "stat_date": "20261106", "ecs_vcpu": 2746.0}]
        gaps = collect.missing_row_gaps(self.CFG, dates, recs, "holdings", self.METRICS)
        self.assertEqual([(g["customer_key"], g["stat_date"]) for g in gaps],
                         [("haidilao", "20261106")],
                         "全 None 行未被判为缺行 = B7 残留缺陷未修")

    def test_partial_value_counts_as_present(self):
        """只有一个指标有值即算该行已补齐（禁因部分列为 None 反复补问）。"""
        dates = ["20261106"]
        recs = [{"customer_key": "haidilao", "stat_date": "20261106",
                 "ecs_vcpu": 9206.0, "db_instances": None}]
        gaps = collect.missing_row_gaps(self.CFG, dates, recs, "holdings", self.METRICS)
        self.assertNotIn("haidilao", {g["customer_key"] for g in gaps},
                         "部分列有值仍被判缺行 = 会反复补问")
        # hesi 无任何行，仍应报缺（CFG 有两个客户）
        self.assertEqual({g["customer_key"] for g in gaps}, {"hesi"})

    def test_duplicate_rows_any_value_wins(self):
        """同 (客户,日期) 多行时任一行有值即算有值。"""
        dates = ["20261106"]
        recs = [{"customer_key": "haidilao", "stat_date": "20261106", "ecs_vcpu": None},
                {"customer_key": "haidilao", "stat_date": "20261106", "ecs_vcpu": 9206.0}]
        gaps = collect.missing_row_gaps(self.CFG, dates, recs, "holdings", self.METRICS)
        self.assertNotIn("haidilao", {g["customer_key"] for g in gaps})

    def test_row_has_value_pure(self):
        self.assertFalse(collect.row_has_value({"ecs_vcpu": None}, self.METRICS))
        self.assertTrue(collect.row_has_value({"ecs_vcpu": 1.0}, self.METRICS))
        self.assertFalse(collect.row_has_value({"ecs_vcpu": 0.0, "db_instances": None},
                                              [("db_instances", "x")]))
        self.assertTrue(collect.row_has_value({"db_instances": 0.0},
                                             [("db_instances", "x")]),
                        "0 是有效值（缺行≠0），禁当缺失")

    def test_no_gaps_when_complete(self):
        dates = ["20261104", "20261105"]
        recs = [{"customer_key": k, "stat_date": d, "ecs_vcpu": 1.0}
                for k in ("haidilao", "hesi") for d in dates]
        self.assertEqual(collect.missing_row_gaps(self.CFG, dates, recs, "holdings",
                                                 self.METRICS), [])

    def test_empty_records_reports_all_expected(self):
        dates = ["20261104", "20261105"]
        gaps = collect.missing_row_gaps(self.CFG, dates, [], "holdings", self.METRICS)
        self.assertEqual(len(gaps), 4, "空记录=全缺，禁因无行而判为无缺")

    def test_skips_customers_without_report_name(self):
        """无 report_customer_name 的客户（如仅 devata cid 的 kunqi）不问数，禁列进缺行。"""
        dates = ["20261106"]
        gaps = collect.missing_row_gaps(self.CFG, dates, [], "holdings", self.METRICS)
        self.assertNotIn("noName", {g["customer_key"] for g in gaps})

    def test_gap_carries_report_name_for_question(self):
        """缺行条目须带报表真名，供补问构造问句与 fixed_name（禁污染客户名，B4）。"""
        gaps = collect.missing_row_gaps(self.CFG, ["20261106"], [], "holdings", self.METRICS)
        h = next(g for g in gaps if g["customer_key"] == "haidilao")
        self.assertEqual(h["report_customer_name"], "海鸿达(北京)餐饮管理有限公司")

    def test_no_metrics_falls_back_to_row_existence(self):
        """metrics 为空时退化为只判行存在（兼容无指标上下文调用）。"""
        dates = ["20261106"]
        recs = [{"customer_key": "haidilao", "stat_date": "20261106", "ecs_vcpu": None},
                {"customer_key": "hesi", "stat_date": "20261106", "ecs_vcpu": None}]
        # 不传 metrics → 全 None 的行也算存在，不报缺（与传 metrics 的行为相反）
        self.assertEqual(collect.missing_row_gaps(self.CFG, dates, recs, "holdings"), [])
        # 对照：传 metrics 时同样的行会被判缺
        gaps = collect.missing_row_gaps(self.CFG, dates, recs, "holdings", self.METRICS)
        self.assertEqual({g["customer_key"] for g in gaps}, {"haidilao", "hesi"})


if __name__ == "__main__":
    unittest.main()
