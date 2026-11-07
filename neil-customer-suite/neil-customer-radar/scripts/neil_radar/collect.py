"""采集编排：分组问数（错开创建+并发轮询）→ 解析归一 → 合计对账门 → 降级逐客户。
产出 outputs/snapshot-<run_date>.json（docs/snapshot_schema.md v1）。
单 scope 失败不中断全批（记 meta.failures）；products 为 probe 式（组件无产品维度
时允许空段+failure，analyze 侧写 data_gap 事件，禁静默）。"""
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

from . import chatbi as cb
from . import config as cfgmod
from . import gate as gatemod
from . import questions as q

POLL_WORKERS = 4


def _span(dates):
    return (dates[0], dates[-1])


def _jobs(cfg, dates, cids):
    span = _span(dates)
    chatbi = cfg["chatbi"]
    rep = chatbi.get("report_id", "616045")
    traf = [(m["key"], m["field"], m.get("aliases", ())) for m in cfg["traffic_metrics"]]
    hold = [(m["key"], m["field"], m.get("aliases", ())) for m in cfg["holding_metrics"]]
    maas = [(m["key"], m["field"], m.get("aliases", ())) for m in cfg["maas_metrics"]]
    dsid = cfg["maas"]["dataset_id"]
    return [
        {"scope": "traffic", "question": q.traffic_question([m[1] for m in traf], span),
         "rid": rep, "rtype": "report", "metrics": traf},
        {"scope": "holdings", "question": q.holdings_question([m[1] for m in hold], span),
         "rid": rep, "rtype": "report", "metrics": hold},
        {"scope": "maas", "question": q.maas_question([m[1] for m in maas], cids, span),
         "rid": dsid, "rtype": "dataset", "metrics": maas, "cid_mode": True},
        {"scope": "gate-total", "question": q.total_question(
            cfgmod.field_of(cfg, "traffic_metrics", "net_total"), dates[-1]),
         "rid": rep, "rtype": "report", "metrics": []},
    ]


def _derive_products(holdings):
    """products 段 = holdings 指标派生的产品族存在性（值>0 即该族在用）。
    616045 无产品名维度（实测 2026-11-07 仅产品团队码），产品级存在性走 kunpeng 账单深钻。"""
    out = []
    for row in holdings:
        for key in ("ecs_vcpu", "ecs_instances", "oss_storage",
                    "db_instances", "db_cpu", "db_disk"):
            val = row.get(key)
            if val:
                out.append({"customer_key": row["customer_key"],
                            "report_customer_name": row["report_customer_name"],
                            "stat_date": row["stat_date"], "product": key, "instances": val})
    return out


def _create_all(chatbi_cfg, out_dir, jobs, stagger):
    for job in jobs:
        try:
            job["answer_id"] = cb.create_chat(
                chatbi_cfg, out_dir, job["question"], job["rid"], job["rtype"])
        except cb.ChatBIError as exc:
            job["answer_id"] = None
            job["error"] = str(exc)
        time.sleep(stagger)
    return jobs


def _poll_all(chatbi_cfg, jobs):
    pending = [j for j in jobs if j.get("answer_id")]
    with ThreadPoolExecutor(max_workers=POLL_WORKERS) as pool:
        values = list(pool.map(lambda j: cb.poll_chat(chatbi_cfg, j["answer_id"]), pending))
    for job, value in zip(pending, values):
        job["result"] = value
    return jobs


DATE_LIKE = ("统计日期", "日期", "stat_date", "dt", "date")


def _first_number(rows):
    """gate-total 回行列名不保证=字段名（可能「总计」）：单行取首个可解析数值，
    排除日期类列（否则 20261106 会被当合计，review 2026-11-07 P1-3）。"""
    if not rows:
        return None
    for name, val in rows[0].items():
        if str(name).strip() in DATE_LIKE:
            continue
        num = cb.parse_number(val)
        if num is not None:
            return num
    return None


def _parse_one(cfg, job, failures, unknown):
    rows = cb.rows_from_sql_datas(job.get("result")) or cb.rows_from_markdown(job.get("result"))
    if job["scope"] == "gate-total":
        return _first_number(rows)
    cmap = {c["report_customer_name"]: c["key"] for c in cfg["customers"]
            if c.get("report_customer_name")}
    recs, unk, missing = q.parse_grouped_rows(
        rows, job["metrics"], cmap, cid_mode=job.get("cid_mode", False),
        fixed_key=job.get("fixed", {}).get("key"))
    job["missing_cols"] = missing
    unknown.extend(unk)
    if not recs:
        failures.append({"scope": job["scope"], "message": f"回行解析为空（原始行 {len(rows)}）"})
    return recs


def _assemble(cfg, run_date, dates, parsed, gate_raw, failures, unknown):
    # 对账门求和口径 = config 内行 + unknown 行（报表全量），存储/分析只消费 config 内
    traf = parsed.get("traffic") or []
    gsum = gatemod.sum_metric(traf + unknown, dates[-1], "net_total")
    gate = gatemod.gate_pure(gsum, gate_raw, cfg.get("thresholds", {}).get("gate_tolerance", 0.05))
    gate.update({"stat_date": dates[-1], "metric": "net_total", "degraded": False})
    return {"meta": {"schema_version": "v1", "run_date": run_date, "stat_dates": dates,
                     "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
                     "sources": ["fbi:616045", "fbi:dataset:" + str(cfg["maas"]["dataset_id"])],
                     "gate": gate, "failures": failures},
            "traffic": traf, "holdings": parsed.get("holdings") or [],
            "products": _derive_products(parsed.get("holdings") or []),
            "maas": parsed.get("maas") or []}


def _degrade_traffic(cfg, chatbi_cfg, out_dir, dates, failures):
    """对账门失败 → 逐客户问 traffic 兜底（错开创建+并发轮询，同主链路）。"""
    span = _span(dates)
    traf = [(m["key"], m["field"]) for m in cfg["traffic_metrics"]]
    jobs = []
    for cust in cfg["customers"]:
        cname = cust.get("report_customer_name")
        if not cname:
            continue
        jobs.append({
            "scope": f"traffic-degrade/{cust['key']}",
            "question": (f"统计日期{span[0]}至{span[1]}内，客户{cname}的"
                         f"{'、'.join(f for _, f in traf)}，按统计日期展示"),
            "rid": cfg["chatbi"].get("report_id", "616045"), "rtype": "report",
            "metrics": traf, "fixed": cust})
    _create_all(chatbi_cfg, out_dir, jobs, cfg["chatbi"].get("create_stagger_seconds", 8))
    _poll_all(chatbi_cfg, jobs)
    recs = []
    for job in jobs:
        if job.get("error"):
            failures.append({"scope": job["scope"], "message": job["error"]})
            continue
        rows = cb.rows_from_sql_datas(job.get("result")) or cb.rows_from_markdown(job.get("result"))
        cmap = {job["fixed"]["report_customer_name"]: job["fixed"]["key"]}
        sub, _, _ = q.parse_grouped_rows(rows, job["metrics"], cmap,
                                         fixed_key=job["fixed"]["key"])
        recs.extend(sub)
    return recs


def _write_outputs(out_dir, run_date, snapshot, unknown):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"snapshot-{run_date}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(snapshot, fh, ensure_ascii=False, indent=1)
    if unknown:
        upath = os.path.join(out_dir, f"unknown-{run_date}.json")
        with open(upath, "w", encoding="utf-8") as fh:
            json.dump(unknown, fh, ensure_ascii=False, indent=1)
    return path


def _supplement_missing(cfg, chatbi_cfg, out_dir, dates, jobs, parsed, failures):
    """列集漂移自愈：traffic/holdings 缺指标列时补一问只问缺的指标，按(客户,日期)合并。
    ChatBI 回行列集非确定（2026-11-07 实测同问两次列集不同），缺列=静默 None 风险。"""
    span = _span(dates)
    cmap = {c["report_customer_name"]: c["key"] for c in cfg["customers"]
            if c.get("report_customer_name")}
    for job in jobs:
        missing = job.get("missing_cols")
        if job["scope"] not in ("traffic", "holdings") or not missing:
            continue
        fields = [m for m in job["metrics"] if m[1] in missing]
        qtext = (q.traffic_question if job["scope"] == "traffic" else q.holdings_question)(
            [m[1] for m in fields], span)
        try:
            aid = cb.create_chat(chatbi_cfg, out_dir, qtext, job["rid"], job["rtype"])
            res = cb.poll_chat(chatbi_cfg, aid)
        except cb.ChatBIError as exc:
            failures.append({"scope": f"supplement/{job['scope']}", "message": str(exc)})
            continue
        rows = cb.rows_from_sql_datas(res) or cb.rows_from_markdown(res)
        recs, _, still = q.parse_grouped_rows(rows, fields, cmap)
        job["missing_after_supplement"] = still
        by_key = {(r["customer_key"], r["stat_date"]): r for r in recs}
        for rec in parsed.get(job["scope"]) or []:
            extra = by_key.get((rec["customer_key"], rec["stat_date"]))
            if extra:
                for m in fields:
                    if rec.get(m[0]) is None:
                        rec[m[0]] = extra.get(m[0])


def cmd_collect(args):
    cfg = cfgmod.load_config(args.config)
    chatbi_cfg = cfgmod.chatbi_cfg(cfg)
    run_date = args.date or time.strftime("%Y-%m-%d")
    days = args.range_days or cfg.get("maas", {}).get("range_days", 14)
    dates = q.stat_dates(run_date, days)
    cids = [c["maas_cid"] for c in cfg["customers"] if c.get("maas_cid")]
    out_dir = args.out_dir or os.path.join(cfgmod.SUITE_DIR, "neil-customer-radar", "outputs")
    jobs = _create_all(chatbi_cfg, out_dir, _jobs(cfg, dates, cids),
                       cfg["chatbi"].get("create_stagger_seconds", 8))
    jobs = _poll_all(chatbi_cfg, jobs)
    failures, unknown, parsed = [], [], {}
    for job in jobs:
        if job.get("error"):
            failures.append({"scope": job["scope"], "message": job["error"]})
            continue
        parsed[job["scope"]] = _parse_one(cfg, job, failures, unknown)
    _supplement_missing(cfg, chatbi_cfg, out_dir, dates, jobs, parsed, failures)
    for job in jobs:
        still = job.get("missing_after_supplement")
        if still:
            failures.append({"scope": job["scope"],
                             "message": f"补问后仍缺列：{','.join(still)}"})
    gate_raw = parsed.pop("gate-total", None)
    snapshot = _assemble(cfg, run_date, dates, parsed, gate_raw, failures, unknown)
    if not snapshot["meta"]["gate"]["passed"]:
        degraded = _degrade_traffic(cfg, chatbi_cfg, out_dir, dates, failures)
        snapshot["meta"]["gate"]["degraded"] = True   # 降级已触发（无论有无回行，review P1-4）
        if degraded:
            parsed["traffic"] = degraded
            snapshot = _assemble(cfg, run_date, dates, parsed, gate_raw, failures, unknown)
            snapshot["meta"]["gate"]["degraded"] = True
        else:
            failures.append({"scope": "degrade", "message": "降级逐客户问数仍无回行"})
    path = _write_outputs(out_dir, run_date, snapshot, unknown)
    empty = not (snapshot["traffic"] or snapshot["holdings"] or snapshot["maas"])
    print(json.dumps({"snapshot": path, "rows": {k: len(snapshot[k]) for k in
          ("traffic", "holdings", "products", "maas")},
          "gate_passed": snapshot["meta"]["gate"]["passed"],
          "failures": len(failures), "unknown_customers": len(unknown)},
          ensure_ascii=False))
    if empty:
        print("ERROR 全 scope 无数据，日批视为失败（cron agent 须推送告警而非静默）")
        return 1
    return 0
