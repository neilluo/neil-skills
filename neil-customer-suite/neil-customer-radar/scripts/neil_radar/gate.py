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


def sum_metric(records, stat_date, metric_key):
    """records 中 stat_date 当天 metric_key 非 None 值求和；无行 → None。"""
    vals = [r.get(metric_key) for r in records
            if r.get("stat_date") == stat_date and r.get(metric_key) is not None]
    return sum(vals) if vals else None
