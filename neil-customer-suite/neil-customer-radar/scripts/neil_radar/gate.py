"""对账门：分组问数完整性校验（纯函数）。分组问数各行求和 vs 报表匿名合计行，
|ratio-1| <= tolerance 才放行；失败由 collect 降级逐客户问数。禁静默放过。"""

DEFAULT_GATE_TOLERANCE = 0.05


def gate_pure(grouped_sum, report_total, tolerance=DEFAULT_GATE_TOLERANCE):
    """返回 gate 片段（stat_date/metric 由调用方补）。任一输入 None → passed=False。"""
    if grouped_sum is None or report_total is None:
        return {"grouped_sum": grouped_sum, "report_total": report_total,
                "ratio": None, "passed": False}
    if report_total == 0:
        return {"grouped_sum": grouped_sum, "report_total": report_total,
                "ratio": None, "passed": grouped_sum == 0}
    ratio = grouped_sum / report_total
    return {"grouped_sum": grouped_sum, "report_total": report_total,
            "ratio": round(ratio, 6), "passed": abs(ratio - 1.0) <= tolerance}


def identity_of(record):
    """记录身份键：customer_key > maas_cid > report_customer_name。

    ChatBI 自然语言→SQL 非确定，同一(客户,统计日)可能回多行（review 2026-11-08 B5）。
    与 store.merged_by_date 的「同键后写覆盖」口径保持一致，禁各算各的。"""
    return (record.get("customer_key")
            or record.get("maas_cid")
            or record.get("report_customer_name"))


def dedupe_records(records, metric_key):
    """同 (身份键, stat_date) 多行收敛成一行，**非 None 值优先**（禁 None 覆盖真值）。

    parse_grouped_rows 已保证每格唯一 record（值级合并），此处是防御网：万一上游漏合并，
    末行 None 也不得覆盖前面的真值。口径与 questions._merge_into、
    analyze.series_from_snapshots 一致。
    无身份键的行（如纯 {stat_date, metric} 记录）用序号兜底**逐行保全**——
    丢数据比不去重更糟，禁因缺身份键而静默吞掉真实值。
    返回 {key: value}，value 为 None 的行不参与（缺行≠0）。"""
    out = {}
    for i, r in enumerate(records):
        ident = identity_of(r)
        key = ident if ident is not None else ("__anon__", i)
        val = r.get(metric_key)
        if out.get(key) is None and val is not None:
            out[key] = val
        elif key not in out:
            out[key] = val
    return {k: v for k, v in out.items() if v is not None}


def sum_metric(records, stat_date, metric_key):
    """records 中 stat_date 当天 metric_key 非 None 值求和；无行 → None。

    先按 (身份键, stat_date) 去重再求和（review 2026-11-08 B5）：曾因直接 sum
    使 ChatBI 回的重复行把分子翻倍 → ratio≈2 → 对账门必挂 → 触发不必要降级，
    而降级链自带 B2/B4 会把好数据换成坏数据（等于「门一响就换坏数据」）。"""
    day_rows = [r for r in records if r.get("stat_date") == stat_date]
    if not day_rows:
        return None
    vals = list(dedupe_records(day_rows, metric_key).values())
    return sum(vals) if vals else None
