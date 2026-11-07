"""分析层（纯函数）：历史 snapshot 序列 → 客户动态事件。
信号只报证据（日期区间+幅度+原始值），禁下结论（suite AGENTS.md 12 条）。
事件 ID 确定性：<customer_key>:<event_type>:<metric>:<start_date>，事件表按 ID 单键幂等；
同一条持续信号只铸一次 ID（run==sustain 触发一次+冷却，review 2026-11-07 P2-14）。"""
import datetime as dt

METRIC_KEYS = ("net_total", "net_down", "net_up", "line_out", "line_in",
               "ecs_vcpu", "ecs_instances", "oss_storage",
               "db_instances", "db_cpu", "db_disk")
HOLDING_KEYS = ("ecs_vcpu", "ecs_instances", "oss_storage",
                "db_instances", "db_cpu", "db_disk")
SCHEMA_VERSION = "v1"


def _plus_days(date_str, n):
    d = dt.datetime.strptime(date_str, "%Y%m%d").date() + dt.timedelta(days=n)
    return d.strftime("%Y%m%d")


def series_from_snapshots(snapshots, customer_key):
    """{metric: {stat_date: value}}；traffic+holdings 按 customer_key、maas 按 maas_cid。
    None 值不覆盖已有真实值（14 天窗口重叠时后快照缺行不得抹掉前快照数据，
    review 2026-11-07 P1-9）；maas 行键已是 maas_gaap/maas_calls，禁再加前缀。"""
    out = {m: {} for m in METRIC_KEYS}
    out["maas_gaap"], out["maas_calls"] = {}, {}
    for snap in snapshots:
        if snap.get("meta", {}).get("schema_version") != SCHEMA_VERSION:
            continue
        for section in ("traffic", "holdings", "maas"):
            id_key = "maas_cid" if section == "maas" else "customer_key"
            for row in snap.get(section, []):
                if row.get(id_key) != customer_key:
                    continue
                for key, val in row.items():
                    if key in ("customer_key", "report_customer_name",
                               "stat_date", "maas_cid") or val is None:
                        continue
                    out.setdefault(key, {})[row["stat_date"]] = val
    return out


def moving_avg(values_by_date, date_str, window=7):
    """完整窗口才出值：任一日缺样本 → None（缺行≠0，review P1-8；
    稀疏数据宁可不报信号也不造假信号）。"""
    vals = [values_by_date.get(_plus_days(date_str, -i)) for i in range(window)]
    if any(v is None for v in vals):
        return None
    return sum(vals) / window


def _day_span(a, b):
    return (dt.datetime.strptime(b, "%Y%m%d") - dt.datetime.strptime(a, "%Y%m%d")).days + 1


def _zero_runs(vals, dates, min_len):
    """日历日零值连续段（缺行不计停用，review P1-10）：返回 [(start, end)]。"""
    runs, start, prev = [], None, None
    for d in dates:
        if vals.get(d) == 0:
            if start and d == _plus_days(prev, 1):
                prev = d
                continue
            if start:
                runs.append((start, prev))
            start = prev = d
        else:
            if start:
                runs.append((start, prev))
                start = prev = None
    if start:
        runs.append((start, prev))
    return [(s, e) for s, e in runs if _day_span(s, e) >= min_len]


def detect_new_stop(series, thresholds):
    """holdings 族：零值锚点后连续非零 = new_product；日历日零值段 ≥stop_days = product_stop。"""
    events = []
    new_days = thresholds.get("new_product_confirm_days", 2)
    stop_days = thresholds.get("stop_confirm_days", 3)
    for key in HOLDING_KEYS:
        vals = series.get(key, {})
        dates = sorted(vals)
        if not dates:
            continue
        pos = [d for d in dates if vals[d]]
        if pos:
            first = pos[0]
            anchored = any(not vals.get(d) for d in dates if d < first)
            if anchored and all(vals.get(_plus_days(first, i)) for i in range(new_days)):
                events.append(_event("new_product", "P2", key, first,
                                       f"{key} 自 {first} 起连续 {new_days} 天非零，首值 {vals[first]}"))
        for start, end in _zero_runs(vals, dates, stop_days):
            events.append(_event("product_stop", "P2", key, start,
                                   f"{key} {start}~{end} 连续 {_day_span(start, end)} 天为 0"))
    return events


def _event(etype, level, metric, start_date, evidence):
    return {"event_id": f"{etype}:{metric}:{start_date}",
            "event_date": start_date, "event_type": etype, "level": level,
            "metric": metric, "evidence": evidence, "status": "open"}


def detect_net_anomaly(series, thresholds):
    """公网 7 日均值环比 |Δ|≥pct 且连续 sustain 天同向（符号一致，review P2-13）；
    专线流出跌>50%/归零=P1。run==sustain 触发一次后冷却，防同信号重复铸事件。"""
    events = []
    pct = thresholds.get("net_wow_pct", 30.0) / 100.0
    sustain = thresholds.get("net_sustain_days", 3)
    drop = thresholds.get("line_out_drop_pct", 50.0) / 100.0
    for key, is_p1 in (("net_total", False), ("line_out", True)):
        vals = series.get(key, {})
        dates = sorted(d for d in vals if vals[d] is not None)
        run, signs, seg_start, emitted = 0, [], None, False
        for d in dates:
            cur, prev = moving_avg(vals, d), moving_avg(vals, _plus_days(d, -7))
            if cur is None or prev in (None, 0):
                run, signs, seg_start, emitted = 0, [], None, False
                continue
            delta = (cur - prev) / prev
            hit = abs(delta) >= pct or (is_p1 and delta <= -drop)
            same = not signs or (signs[-1] > 0) == (delta > 0)
            if hit and same:
                run += 1
                signs.append(delta)
                seg_start = seg_start or d
            else:
                run, signs, seg_start, emitted = 0, [], None, False
                continue
            # 同一连续异动段只铸一次事件（ID 锚段起点，重跑同段 upsert 更新不新增行，
            # review 2026-11-07 P2-14）；段被非异动日打断后重新计段
            if run == sustain and not emitted:
                start = _plus_days(d, -(sustain - 1))
                events.append(_event("net_anomaly", "P1" if is_p1 else "P2", key, start,
                                       f"{key} 7日均值连续 {sustain} 天同向环比 |Δ|≥{pct:.0%}，"
                                       f"{start}~{d} 当期均值 {cur:.1f} vs 前期 {prev:.1f}"))
                emitted = True
    return events


def detect_maas_trend(series, thresholds):
    pct = thresholds.get("maas_wow_pct", 30.0) / 100.0
    vals = series.get("maas_gaap", {})
    dates = sorted(d for d in vals if vals[d] is not None)
    if not dates:
        return []
    d = dates[-1]
    cur, prev = moving_avg(vals, d), moving_avg(vals, _plus_days(d, -7))
    if cur is None or prev in (None, 0):
        return []
    delta = (cur - prev) / prev
    if abs(delta) < pct:
        return []
    return [_event("maas_trend", "info", "maas_gaap", d,
                   f"MaaS 日GAAP 7日均值 {d} 环比 {delta:+.0%}（{prev:.0f}→{cur:.0f} 元）")]


def detect_data_gap(snapshots, customer, run_date):
    """观测窗口内该客户无行的统计日 → data_gap（事件 ID 锚 run_date，稳定幂等）。"""
    if not snapshots:
        return []
    dates = snapshots[-1].get("meta", {}).get("stat_dates", [])
    have = set()
    for snap in snapshots:
        for section in ("traffic", "holdings"):
            for row in snap.get(section, []):
                if row.get("customer_key") == customer["key"]:
                    have.add(row["stat_date"])
    missing = [d for d in dates if d not in have]
    if not missing:
        return []
    ev = _event("data_gap", "info", "snapshot", run_date,
                f"统计日 {','.join(missing)} 无该客户行（流量零值客户可能不在组件）")
    return [ev]


def analyze_customer(customer, snapshots, thresholds, run_date=""):
    series = series_from_snapshots(snapshots, customer["key"])
    events = (detect_new_stop(series, thresholds) + detect_net_anomaly(series, thresholds)
              + detect_maas_trend(series, thresholds))
    if customer.get("radar", {}).get("daily_watch"):
        events += detect_data_gap(snapshots, customer, run_date)
    for ev in events:
        ev["event_id"] = f"{customer['key']}:{ev['event_type']}:{ev['metric']}:{ev['event_date']}"
    return events


def cmd_analyze(args):
    """读 outputs/snapshot-*.json 历史序列（升序）→ 每客户事件清单落盘 + 事件写计划。"""
    import glob
    import json
    import os
    import time

    from . import config as cfgmod
    from . import store as store_mod

    cfg = cfgmod.load_config(args.config)
    out_dir = args.out_dir or os.path.join(cfgmod.SUITE_DIR, "neil-customer-radar", "outputs")
    snapshots = []
    for path in sorted(glob.glob(os.path.join(out_dir, "snapshot-*.json"))):
        with open(path, encoding="utf-8") as fh:
            snap = json.load(fh)
        if snap.get("meta", {}).get("schema_version") != SCHEMA_VERSION:
            print(f"WARN 跳过未知 schema_version: {os.path.basename(path)}")
            continue
        snapshots.append(snap)
    if not snapshots:
        print("ERROR 无可用 snapshot，分析中止")
        return 1
    run_date = time.strftime("%Y-%m-%d")
    thresholds = cfgmod.thresholds(cfg)
    keys = args.customers.split(",") if args.customers else None
    all_events = {}
    for cust in cfgmod.customers(cfg, keys=keys):
        all_events[cust["key"]] = analyze_customer(cust, snapshots, thresholds, run_date)
    payload = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
               "snapshots": [os.path.basename(p) for p in
                             sorted(glob.glob(os.path.join(out_dir, "snapshot-*.json")))],
               "events": all_events}
    epath = os.path.join(out_dir, f"events-{run_date}.json")
    with open(epath, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
    plan, field_ids = [], {}
    if args.field_ids:
        with open(args.field_ids, encoding="utf-8") as fh:
            blob = json.load(fh)
        field_ids = blob.get("fields", blob)
    for cust in cfgmod.customers(cfg, keys=keys):
        fids = field_ids
        rel = cust.get("radar", {}).get("field_ids_file")
        if rel:
            fpath = os.path.join(cfgmod.SUITE_DIR, rel)
            if os.path.exists(fpath):
                with open(fpath, encoding="utf-8") as fh:
                    fids = json.load(fh).get("fields", {})
        plan.extend(store_mod.plan_events(cust, all_events[cust["key"]], fids))
    n_events = sum(len(v) for v in all_events.values())
    if n_events and not plan:
        print("WARN 有事件但写计划为空（field_ids 缺失？），事件未入表格")
    ppath = os.path.join(out_dir, f"events-plan-{run_date}.json")
    with open(ppath, "w", encoding="utf-8") as fh:
        json.dump({"commands": plan}, fh, ensure_ascii=False, indent=1)
    print(json.dumps({"events_file": epath, "plan": ppath,
                      "counts": {k: len(v) for k, v in all_events.items()},
                      "commands": len(plan)}, ensure_ascii=False))
    return 0
