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


def finalize_gate(first_gate, degraded_rows):
    """降级后的 gate 定稿：结论冻结为**首次分组问数的权威判定**，只补降级元数据。

    B6（2026-11-08 实测）：曾因降级后重算 ratio 用「降级后 config 内行 + 原始全量
    unknown 行」的混合口径（两次不同问数的行拼一起求和无意义），把失败覆盖成
    passed=true → snapshot 出现 passed=true 且 degraded=true 的自相矛盾状态
    （实测 ratio 0.9577 却 degraded），下游无法解释「既对账通过又降级」，
    也丢失了触发降级的真实 ratio。
    不变式：degraded=True ⇒ passed=False（降级只因首次对账失败才触发）。"""
    gate = dict(first_gate)
    gate["degraded"] = True
    gate["degraded_rows"] = degraded_rows
    return gate


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
    """对账门失败 → 逐客户问 traffic 兜底（错开创建+并发轮询，同主链路）。

    降级路径同样要走列集漂移自愈（review 2026-11-08 B6）：曾因 _supplement_missing
    只在降级之前调用一次，降级回来的缺列（如 net_up）无人补救 → 静默 None 落盘。"""
    span = _span(dates)
    # 必须与主链路 _jobs 一样带 aliases（3-tuple）：报表字段命名自身不一致
    # （实测 net_up 真名「公网络上行流量/GB」只能靠 config aliases 命中），
    # 曾因构造 2-tuple 丢 aliases → 降级路径 net_up 恒 None（review 2026-11-08 B2，
    # 2026-11-08 15 天回填实测 60/60 格全丢）。
    traf = [(m["key"], m["field"], m.get("aliases", ()))
            for m in cfg["traffic_metrics"]]
    jobs = []
    for cust in cfg["customers"]:
        cname = cust.get("report_customer_name")
        if not cname:
            continue
        jobs.append({
            "scope": f"traffic-degrade/{cust['key']}",
            "question": (f"统计日期{span[0]}至{span[1]}内，客户{cname}的"
                         f"{'、'.join(m[1] for m in traf)}，按统计日期展示"),
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
        fixed = job["fixed"]
        cmap = {fixed["report_customer_name"]: fixed["key"]}
        # fixed_name 传报表真名：降级回行无客户列时用它填 report_customer_name，
        # 禁让 customer_key（如 "haidilao"）污染客户名字段（review 2026-11-08 B4）
        sub, _, still_missing = q.parse_grouped_rows(rows, job["metrics"], cmap,
                                                    fixed_key=fixed["key"],
                                                    fixed_name=fixed.get("report_customer_name"))
        job["missing_cols"] = still_missing
        # B6：降级回来的行同样走列集漂移补问自愈。曾因 _supplement_missing 只在降级前
        # 调用一次，降级回来的缺列（如 net_up）无人补救 → 静默 None 落盘（实测 60/60 全丢）。
        if still_missing:
            sub, after = _supplement_one(chatbi_cfg, out_dir, dates, job, still_missing,
                                         sub, fixed, failures)
            job["missing_after_supplement"] = after
        recs.extend(sub)
    return recs


def _supplement_one(chatbi_cfg, out_dir, dates, job, missing, recs, fixed, failures):
    """对单个降级 job 补问缺失指标列，按 (customer_key, stat_date) 合并进 recs（只在原值
    None 时填，禁覆盖真值）。返回 (合并后的 recs, 仍缺列清单)。"""
    span = _span(dates)
    fields = [m for m in job["metrics"] if m[1] in missing]
    if not fields:
        return recs, missing
    qtext = q.traffic_question([m[1] for m in fields], span)
    try:
        aid = cb.create_chat(chatbi_cfg, out_dir, qtext, job["rid"], job["rtype"])
        res = cb.poll_chat(chatbi_cfg, aid)
    except cb.ChatBIError as exc:
        failures.append({"scope": f"supplement/{job['scope']}", "message": str(exc)})
        return recs, missing
    rows = cb.rows_from_sql_datas(res) or cb.rows_from_markdown(res)
    cmap = {fixed["report_customer_name"]: fixed["key"]}
    extra, _, still = q.parse_grouped_rows(rows, fields, cmap,
                                           fixed_key=fixed["key"],
                                           fixed_name=fixed.get("report_customer_name"))
    by_key = {(r.get("customer_key"), r["stat_date"]): r for r in extra}
    for rec in recs:
        hit = by_key.get((rec.get("customer_key"), rec["stat_date"]))
        if hit:
            for m in fields:
                if rec.get(m[0]) is None:
                    rec[m[0]] = hit.get(m[0])
    return recs, still


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


def row_has_value(record, metrics):
    """该行是否至少有一个指标值非 None（纯函数，便于单测）。

    B7 残留缺陷（2026-11-08 实测）：补问回来的行可能**存在但全 None**
    （hesi 后 8 天 6 个 holdings 指标全空），只判「行是否存在」会误判为已补齐 →
    不记 failure、静默落盘空行。缺行的定义必须是「该客户该日没有可用值」。"""
    return any(record.get(m[0]) is not None for m in metrics)


def missing_row_gaps(cfg, dates, records, scope, metrics=()):
    """算出 config 客户 × 统计日 的缺行清单（纯函数，便于单测）。

    返回 [{customer_key, report_customer_name, stat_date}]。缺行判定 =
    **没有该 (客户,日期) 行，或该行全部指标值为 None**（见 row_has_value）。
    ChatBI 分组问数的回行集合非确定（AGENTS.md 第5条），漏行不等于客户无数据。
    metrics 为空时退化为只判行存在（兼容无指标上下文的调用）。"""
    want_keys = {c["key"] for c in cfg["customers"] if c.get("report_customer_name")}
    have = {}
    for r in records:
        key = (r.get("customer_key"), r.get("stat_date"))
        # 同键多行时任一行有值即算有值
        have[key] = have.get(key, False) or (
            row_has_value(r, metrics) if metrics else True)
    gaps = []
    for cust in cfg["customers"]:
        ck = cust["key"]
        if ck not in want_keys:
            continue
        for d in dates:
            if not have.get((ck, d)):
                gaps.append({"customer_key": ck,
                             "report_customer_name": cust["report_customer_name"],
                             "stat_date": d})
    return gaps


def _supplement_missing_rows(cfg, chatbi_cfg, out_dir, dates, jobs, parsed, failures,
                             scopes=("holdings",)):
    """行集漂移自愈：缺行（客户×统计日）时逐客户补问，按(客户,日期)合并进 parsed[scope]。

    B7（2026-11-08 实测发现）：_supplement_missing 只补**缺列**（AGENTS.md 第6条），
    不补**缺行**。traffic 段有对账门兜底 → 缺行触发降级逐客户问数被补回；
    holdings 段**没有对账门** → 分组问数漏行时静默落盘不完整
    （实测 15 天回填 holdings 仅 27/60 行，缺 33 格无任何告警）。
    按第6条既有治理原则延伸：缺什么补什么，补不到才记 failure，禁静默不完整。"""
    span = _span(dates)
    for job in jobs:
        scope = job["scope"]
        if scope not in scopes:
            continue
        recs = parsed.get(scope) or []
        metrics = job["metrics"]
        gaps = missing_row_gaps(cfg, dates, recs, scope, metrics)
        if not gaps:
            continue
        # 已有行索引：补问回来的值要**填进**已存在但全 None 的行，禁追加同键重复行
        # （同键两行会污染 gate.dedupe_records 的后写覆盖语义与 store 的单键 upsert 幂等）
        by_key = {}
        for r in recs:
            by_key.setdefault((r.get("customer_key"), r.get("stat_date")), r)
        # 按客户分组补问：一次问一个客户的全部缺失日期，避免逐日扇出（限流面）
        by_cust = {}
        for g in gaps:
            by_cust.setdefault(g["customer_key"], []).append(g)
        added, filled = 0, 0
        still_missing = []
        for ck, cust_gaps in by_cust.items():
            cname = cust_gaps[0]["report_customer_name"]
            qtext = (f"统计日期{span[0]}至{span[1]}内，客户{cname}的"
                     f"{'、'.join(m[1] for m in metrics)}，按统计日期展示")
            try:
                aid = cb.create_chat(chatbi_cfg, out_dir, qtext, job["rid"], job["rtype"])
                res = cb.poll_chat(chatbi_cfg, aid)
            except cb.ChatBIError as exc:
                failures.append({"scope": f"supplement-rows/{scope}/{ck}",
                                 "message": str(exc)})
                still_missing.extend(g["stat_date"] for g in cust_gaps)
                continue
            rows = cb.rows_from_sql_datas(res) or cb.rows_from_markdown(res)
            cmap = {cname: ck}
            extra, _, _ = q.parse_grouped_rows(rows, metrics, cmap,
                                               fixed_key=ck, fixed_name=cname)
            got = {r["stat_date"]: r for r in extra}
            for g in cust_gaps:
                hit = got.get(g["stat_date"])
                # 补问回来仍无值的行不算补齐（否则重演「行在值空」的静默不完整）
                if not hit or not row_has_value(hit, metrics):
                    still_missing.append(g["stat_date"])
                    continue
                existing = by_key.get((ck, g["stat_date"]))
                if existing is None:
                    recs.append(hit)
                    by_key[(ck, g["stat_date"])] = hit
                    added += 1
                else:
                    for m in metrics:
                        if existing.get(m[0]) is None:
                            existing[m[0]] = hit.get(m[0])
                    filled += 1
        parsed[scope] = recs
        job["rows_supplemented"] = added
        job["rows_filled"] = filled
        if still_missing:
            failures.append({"scope": f"supplement-rows/{scope}",
                             "message": (f"补问后仍缺 {len(still_missing)} 行值："
                                         f"{','.join(sorted(set(still_missing))[:8])}"
                                         f"{' …' if len(set(still_missing)) > 8 else ''}")})


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
    # B7：缺**行**自愈。holdings 无对账门，分组问数漏行会静默落盘不完整
    # （实测 15 天回填仅 27/60 行）；traffic 的缺行由下方对账门降级兜底，故此处只补 holdings。
    # 必须在 _assemble 之前：products 段由 holdings 派生（_derive_products），补全后才准。
    _supplement_missing_rows(cfg, chatbi_cfg, out_dir, dates, jobs, parsed, failures,
                             scopes=("holdings",))
    gate_raw = parsed.pop("gate-total", None)
    snapshot = _assemble(cfg, run_date, dates, parsed, gate_raw, failures, unknown)
    # 首次分组问数的对账结论是**权威判定**：degraded 的触发依据就是它失败。
    first_gate = dict(snapshot["meta"]["gate"])
    if not first_gate["passed"]:
        degraded = _degrade_traffic(cfg, chatbi_cfg, out_dir, dates, failures)
        if degraded:
            parsed["traffic"] = degraded
            snapshot = _assemble(cfg, run_date, dates, parsed, gate_raw, failures, unknown)
        else:
            failures.append({"scope": "degrade", "message": "降级逐客户问数仍无回行"})
        # B6：gate 结论冻结为首次判定，禁被二次 _assemble 的混合口径覆盖（见 finalize_gate）
        snapshot["meta"]["gate"] = finalize_gate(first_gate, len(degraded))
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
