"""diff_ground_truth.py — 把 outputs/snapshot-<date>.json 里脚本抓的值
逐格对比 outputs/ground-truth-616045.json（浏览器从 FBI 616045 实读的报表真值）。

判定口径：
  - 报表 UI 显示为整数（四舍五入），脚本存精确浮点 → 用 |round(script)-report| <= 1 判等
  - 报表某日缺列 / 脚本某日缺行 → 记 MISSING，不算不一致
  - 单位一致性：config 声明 unit vs 报表列名后缀（/GB /TB /核 /个）逐项核对

用法: python3 tests/diff_ground_truth.py [--snapshot PATH]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RADAR = os.path.dirname(HERE)
SUITE = os.path.dirname(RADAR)

# 报表列名 → config metrics key（口径与 config/customers.json 完全一致）
METRIC_TO_KEY = {
    "公网流量/GB": "net_total",
    "公网下行流量/GB": "net_down",
    "公网上行流量/GB": "net_up",
    "专线流出流量/GB": "line_out",
    "专线流入流量/GB": "line_in",
    "ecs_vcpu保有量/核": "ecs_vcpu",
    "ecs_保有实例数/个": "ecs_instances",
    "oss存储量/TB": "oss_storage",
    "数据库保有实例数/个": "db_instances",
    "数据库cpu核数/核": "db_cpu",
    "数据库磁盘/TB": "db_disk",
}

# 报表列名后缀 → config 声明的 unit
SUFFIX_UNIT = {"/GB": "GB", "/TB": "TB", "/核": "核", "/个": "个"}


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def parse_report_num(s):
    """报表字符串 '20,793' / '-' / '' → float 或 None。"""
    t = (s or "").strip().replace(",", "")
    if not t or t in ("-", "—", "null", "None"):
        return None
    try:
        return float(t)
    except ValueError:
        return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--snapshot",
                    default=os.path.join(RADAR, "outputs", "snapshot-2026-11-07.json"))
    ap.add_argument("--truth",
                    default=os.path.join(RADAR, "outputs", "ground-truth-616045.json"))
    ap.add_argument("--config",
                    default=os.path.join(SUITE, "config", "customers.json"))
    ap.add_argument("--tolerance", type=float, default=1.0,
                    help="报表整数四舍五入 vs 脚本浮点，允许绝对差（默认 1.0）")
    a = ap.parse_args(argv)

    snap = load_json(a.snapshot)
    truth = load_json(a.truth)
    cfg = load_json(a.config)

    # config unit 表：metric key → 声明 unit
    unit_of = {}
    for section in ("traffic_metrics", "holding_metrics"):
        for m in cfg.get(section, []):
            unit_of[m["key"]] = m.get("unit")

    # 报表日期标签序列（升序索引 → 具体 YYYYMMDD）
    labels = truth["_meta"]["day_labels"]

    # 脚本 snapshot 里每客户每指标每日的值
    script = {}   # (customer_key, metric_key, stat_date) -> float|None
    for section in ("traffic", "holdings"):
        for row in snap.get(section, []):
            ck = row.get("customer_key")
            sd = row.get("stat_date")
            for mk, v in row.items():
                if mk in ("customer_key", "report_customer_name", "stat_date", "maas_cid"):
                    continue
                script[(ck, mk, sd)] = v

    stats = {"match": 0, "mismatch": 0, "missing_script": 0, "missing_report": 0,
             "unit_check": 0, "unit_fail": 0}
    mismatches = []
    missing = []
    unit_fails = []

    for ck, block in truth.items():
        if ck.startswith("_"):
            continue
        for metric_label, day_vals in block.items():
            mk = METRIC_TO_KEY.get(metric_label)
            if not mk:
                continue
            # 单位核对：报表列名后缀 vs config 声明 unit
            suffix = next((s for s in SUFFIX_UNIT if metric_label.endswith(s)), None)
            if suffix:
                stats["unit_check"] += 1
                declared = unit_of.get(mk)
                if declared and declared != SUFFIX_UNIT[suffix]:
                    stats["unit_fail"] += 1
                    unit_fails.append({
                        "customer": ck, "metric": mk,
                        "report_unit": SUFFIX_UNIT[suffix], "config_unit": declared})
            for i, raw in enumerate(day_vals):
                sd = labels[i]
                rv = parse_report_num(raw)
                sv = script.get((ck, mk, sd), "__NO_ROW__")
                if rv is None and sv == "__NO_ROW__":
                    continue
                if rv is None:
                    stats["missing_report"] += 1
                    missing.append({"customer": ck, "metric": mk, "date": sd,
                                    "side": "report", "script": sv})
                    continue
                if sv == "__NO_ROW__" or sv is None:
                    stats["missing_script"] += 1
                    missing.append({"customer": ck, "metric": mk, "date": sd,
                                    "side": "script", "report": rv})
                    continue
                if abs(round(sv) - rv) <= a.tolerance:
                    stats["match"] += 1
                else:
                    stats["mismatch"] += 1
                    mismatches.append({
                        "customer": ck, "metric": mk, "date": sd,
                        "script": sv, "report": rv,
                        "delta": round(sv - rv, 4)})

    print("=" * 72)
    print("脚本抓取 vs 报表真值 逐格 diff")
    print(f"  snapshot : {os.path.basename(a.snapshot)}")
    print(f"  truth    : {os.path.basename(a.truth)}  (FBI 616045 浏览器实读)")
    print(f"  tolerance: ±{a.tolerance}（报表整数四舍五入 vs 脚本浮点）")
    print("=" * 72)
    print(f"  ✅ 吻合        : {stats['match']}")
    print(f"  ❌ 不一致      : {stats['mismatch']}")
    print(f"  ⚠ 脚本缺行     : {stats['missing_script']}")
    print(f"  ⚠ 报表缺列     : {stats['missing_report']}")
    print(f"  单位核对       : {stats['unit_check']} 项，失败 {stats['unit_fail']}")
    print()

    if mismatches:
        print("❌ 不一致明细（前 40 条）：")
        for m in mismatches[:40]:
            print(f"  {m['customer']:10s} {m['metric']:15s} {m['date']}  "
                  f"script={m['script']:>14.4f}  report={m['report']:>12.0f}  "
                  f"Δ={m['delta']:>+12.4f}")
        print()

    if unit_fails:
        print("❌ 单位声明不一致：")
        for u in unit_fails:
            print(f"  {u['customer']} {u['metric']}: 报表={u['report_unit']} "
                  f"config={u['config_unit']}")
        print()

    if missing:
        # 只汇总，不逐条打印（可能几十条）
        from collections import Counter
        by_side = Counter((m["side"], m["metric"]) for m in missing)
        print("⚠ 缺失汇总（side × metric）：")
        for (side, mk), n in sorted(by_side.items()):
            print(f"  {side:8s} {mk:15s} × {n}")
        print()
        dates = sorted({m["date"] for m in missing})
        print(f"  涉及日期：{', '.join(dates[:15])}"
              f"{' …' if len(dates) > 15 else ''}")
        custs = sorted({m["customer"] for m in missing})
        print(f"  涉及客户：{', '.join(custs)}")

    print()
    print("=" * 72)
    verdict = "PASS" if not mismatches and not unit_fails else "FAIL"
    print(f"结论: {verdict}")
    print("=" * 72)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
