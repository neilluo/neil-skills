"""分析层单测（纯函数，离线）：新启用/停用/网络异动/事件 ID 确定性。"""
import datetime as dt
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "scripts"))

from neil_radar import analyze as az  # noqa: E402

TH = {"net_wow_pct": 30.0, "net_sustain_days": 3, "line_out_drop_pct": 50.0,
      "new_product_confirm_days": 2, "stop_confirm_days": 3, "maas_wow_pct": 30.0}


def _snap(dates, key, **vals):
    rows = []
    for d in dates:
        row = {"customer_key": key, "report_customer_name": "X", "stat_date": d}
        row.update({m: vals.get(m, {}).get(d) for m in vals})
        rows.append(row)
    return {"meta": {"schema_version": "v1", "stat_dates": dates}, "traffic": rows,
            "holdings": [], "products": [], "maas": []}


class TestNewStop(unittest.TestCase):
    def test_new_product(self):
        dates = ["20261101", "20261102", "20261103"]
        db = {"20261101": 0, "20261102": 5, "20261103": 5}
        series = az.series_from_snapshots([_snap(dates, "c1", db_instances=db)], "c1")
        evs = az.detect_new_stop(series, TH)
        self.assertEqual([e["event_type"] for e in evs], ["new_product"])
        self.assertEqual(evs[0]["event_date"], "20261102")

    def test_product_stop(self):
        dates = ["20261101", "20261102", "20261103", "20261104", "20261105"]
        db = {"20261101": 5, "20261102": 0, "20261103": 0, "20261104": 0}
        series = az.series_from_snapshots([_snap(dates, "c1", db_instances=db)], "c1")
        evs = [e for e in az.detect_new_stop(series, TH) if e["event_type"] == "product_stop"]
        self.assertEqual(len(evs), 1)
        self.assertEqual(evs[0]["event_date"], "20261102")

    def test_no_signal_on_stable(self):
        dates = ["20261101", "20261102", "20261103"]
        db = {d: 5 for d in dates}
        series = az.series_from_snapshots([_snap(dates, "c1", db_instances=db)], "c1")
        self.assertEqual(az.detect_new_stop(series, TH), [])


class TestNetAnomaly(unittest.TestCase):
    @staticmethod
    def _dates(n):
        d0 = dt.date(2026, 10, 21)
        return [(d0 + dt.timedelta(days=i)).strftime("%Y%m%d") for i in range(n)]

    def test_sustained_drop(self):
        dates = self._dates(17)
        vals = {d: (100.0 if i < 10 else 40.0) for i, d in enumerate(dates)}
        evs = az.detect_net_anomaly({"net_total": vals}, TH)
        self.assertTrue(any(e["event_type"] == "net_anomaly" for e in evs))

    def test_line_out_zero_is_p1(self):
        dates = self._dates(17)
        vals = {d: (50.0 if i < 10 else 0.001) for i, d in enumerate(dates)}
        evs = az.detect_net_anomaly({"line_out": vals}, TH)
        p1 = [e for e in evs if e["metric"] == "line_out"]
        self.assertTrue(p1 and p1[0]["level"] == "P1")

    def test_stable_no_signal(self):
        dates = self._dates(17)
        self.assertEqual(az.detect_net_anomaly({"net_total": {d: 100.0 for d in dates}}, TH), [])


class TestEventId(unittest.TestCase):
    def test_deterministic(self):
        cust = {"key": "c1", "radar": {"daily_watch": True}}
        dates = ["20261101", "20261102", "20261103"]
        db = {"20261101": 0, "20261102": 5, "20261103": 5}
        snaps = [_snap(dates, "c1", db_instances=db)]
        a = az.analyze_customer(cust, snaps, TH)
        b = az.analyze_customer(cust, snaps, TH)
        self.assertEqual([e["event_id"] for e in a], [e["event_id"] for e in b])
        self.assertTrue(a[0]["event_id"].startswith("c1:new_product:db_instances:"))


class TestSeriesSemantics(unittest.TestCase):
    def test_none_does_not_overwrite(self):
        s1 = _snap(["20261101", "20261102"], "c1", db_instances={"20261101": 5, "20261102": 5})
        s2 = _snap(["20261102", "20261103"], "c1", db_instances={"20261102": None, "20261103": 0})
        series = az.series_from_snapshots([s1, s2], "c1")
        self.assertEqual(series["db_instances"]["20261102"], 5)
        self.assertEqual(series["db_instances"]["20261103"], 0)

    def test_maas_keys_no_double_prefix(self):
        snap = {"meta": {"schema_version": "v1", "stat_dates": ["20261106"]},
                "traffic": [], "holdings": [], "products": [],
                "maas": [{"maas_cid": "c1", "stat_date": "20261106",
                          "maas_gaap": 100.0, "maas_calls": 1.0}]}
        series = az.series_from_snapshots([snap], "c1")
        self.assertEqual(series["maas_gaap"]["20261106"], 100.0)
        self.assertNotIn("maas_maas_gaap", series)

    def test_moving_avg_needs_full_window(self):
        vals = {f"2026110{i}": 10.0 for i in range(1, 5)}
        self.assertIsNone(az.moving_avg(vals, "20261107"))
        full = {az._plus_days("20261107", -i): 10.0 for i in range(7)}
        self.assertEqual(az.moving_avg(full, "20261107"), 10.0)

    def test_zero_run_calendar_days(self):
        # 1103 缺观测 → 连续性在 1104 断 → 两段 (1102,1102)/(1104,1105) 均 <3 天 → 无 run
        vals = {"20261101": 5, "20261102": 0, "20261104": 0, "20261105": 0}
        self.assertEqual(az._zero_runs(vals, sorted(vals), 3), [])
        # 日历日连续 4 天零值 → 单 run
        vals2 = {"20261101": 5, "20261102": 0, "20261103": 0, "20261104": 0, "20261105": 0}
        self.assertEqual(az._zero_runs(vals2, sorted(vals2), 3), [("20261102", "20261105")])

    def test_net_anomaly_cooldown(self):
        dates = TestNetAnomaly._dates(24)
        vals = {d: (100.0 if i < 10 else 40.0) for i, d in enumerate(dates)}
        evs = az.detect_net_anomaly({"net_total": vals}, TH)
        starts = [e["event_date"] for e in evs]
        self.assertEqual(len(starts), len(set(starts)))
        self.assertLessEqual(len(evs), 2)


if __name__ == "__main__":
    unittest.main()
