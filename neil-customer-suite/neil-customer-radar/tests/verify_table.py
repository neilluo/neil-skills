"""verify_table.py — 端到端核对：钉钉 AI 表格里的实际记录 vs FBI 616045 报表真值。

这是最后一道验证：不只验「脚本抓的对不对」，而是验「真正落到客户表格里的值对不对」。
表格记录由 agent 通过 dws 从 outputs/table-dump.json 读出（脚本禁 subprocess 调 dws）。

用法:
  1) agent 执行 dws aitable +record-query ... 并把结果存 outputs/table-dump.json
  2) python3 tests/verify_table.py
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RADAR = os.path.dirname(HERE)

# AI 表格 fieldId → (metric_key, 报表列名)
FIELD_MAP = {
    "hFJkuhJ": ("net_total", "公网流量/GB"),
    "5JXSc2r": ("net_down", "公网下行流量/GB"),
    "cZ5c07q": ("net_up", "公网上行流量/GB"),
    "lzqatQz": ("line_out", "专线流出流量/GB"),
    "iQ84XEI": ("line_in", "专线流入流量/GB"),
    "OsfRgbg": ("ecs_vcpu", "ecs_vcpu保有量/核"),
    "iSYrgwW": ("ecs_instances", "ecs_保有实例数/个"),
    "QYKbzYZ": ("oss_storage", "oss存储量/TB"),
    "LMOAP22": ("db_instances", "数据库保有实例数/个"),
    "3YhBVyU": ("db_cpu", "数据库cpu核数/核"),
    "tUn7mgO": ("db_disk", "数据库磁盘/TB"),
}
DATE_FIELD = "HlDl3cP"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dump", default=os.path.join(RADAR, "outputs", "table-dump.json"))
    ap.add_argument("--truth", default=os.path.join(RADAR, "outputs",
                                                   "ground-truth-616045.json"))
    ap.add_argument("--customer", default="haidilao")
    ap.add_argument("--tolerance", type=float, default=1.0)
    a = ap.parse_args(argv)

    with open(a.dump, encoding="utf-8") as fh:
        dump = json.load(fh)
    with open(a.truth, encoding="utf-8") as fh:
        truth = json.load(fh)

    records = dump.get("data", dump).get("records", [])
    labels = truth["_meta"]["day_labels"]
    gt = truth[a.customer]

    match = mismatch = skipped = missing_table = 0
    bad = []
    dates_seen = set()

    for rec in records:
        cells = rec.get("cells", {})
        d = cells.get(DATE_FIELD)
        if not d:
            continue
        dates_seen.add(d)
        if d not in labels:
            skipped += 1
            continue
        idx = labels.index(d)
        for fid, (mk, label) in FIELD_MAP.items():
            raw = cells.get(fid)
            tv = None if raw in (None, "", "null") else float(raw)
            gv_raw = gt.get(label, [None] * len(labels))[idx]
            gv = None if gv_raw in (None, "", "-") else float(str(gv_raw).replace(",", ""))
            if gv is None:
                skipped += 1
                continue
            if tv is None:
                missing_table += 1
                bad.append({"date": d, "metric": mk, "table": None, "report": gv})
                continue
            if abs(round(tv) - round(gv)) <= a.tolerance:
                match += 1
            else:
                mismatch += 1
                bad.append({"date": d, "metric": mk, "table": tv, "report": gv,
                            "delta": round(tv - gv, 4)})

    # 重复键检查
    dups = [d for d in dates_seen if sum(1 for r in records
                                         if r.get("cells", {}).get(DATE_FIELD) == d) > 1]

    print("=" * 74)
    print("端到端核对：钉钉 AI 表格实际记录 vs FBI 616045 报表真值")
    print(f"  客户      : {a.customer}")
    print(f"  表格记录数: {len(records)}  | 日期覆盖: {min(dates_seen)} ~ {max(dates_seen)}")
    print(f"  tolerance : ±{a.tolerance}（报表整数展示 vs 表格精确浮点）")
    print("=" * 74)
    print(f"  ✅ 吻合        : {match}")
    print(f"  ❌ 不一致      : {mismatch}")
    print(f"  ⚠ 表格缺值     : {missing_table}")
    print(f"  ⏭ 跳过（报表无该日/该指标）: {skipped}")
    print(f"  🔁 重复日期键  : {len(dups)}{(' → ' + ','.join(dups)) if dups else ''}")
    print()
    if bad:
        print("明细（前 30 条）：")
        for b in bad[:30]:
            print(f"  {b['date']} {b['metric']:14s} table={b['table']} report={b['report']}")
        print()

    complete_dates = sorted(
        d for d in dates_seen
        if all(cells_ok(cells, fid) for cells in [next(
            r["cells"] for r in records if r["cells"].get(DATE_FIELD) == d)]
            for fid in FIELD_MAP))
    print(f"完整天数（{len(FIELD_MAP)} 个指标全非空）: {len(complete_dates)}")
    print(f"  {', '.join(complete_dates)}")
    print("=" * 74)
    ok = mismatch == 0 and missing_table == 0 and not dups
    print(f"结论: {'PASS' if ok else 'FAIL'}")
    print("=" * 74)
    return 0 if ok else 1


def cells_ok(cells, fid):
    v = cells.get(fid)
    return v not in (None, "", "null")


if __name__ == "__main__":
    raise SystemExit(main())
