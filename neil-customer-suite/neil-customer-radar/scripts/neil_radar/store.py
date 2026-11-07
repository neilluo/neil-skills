"""存储层（plan 模式）：snapshot.json → dws 写计划（纯函数，零 subprocess）。
宿主执行契约实测（2026-11-07）：dws 被 Python subprocess 调用会被宿主 guard 拦截，
故本层只产出 argv 清单落盘 outputs/store-plan-<date>.json，由 agent/cron agent
逐条直接执行 dws（禁管道/重定向/后台）。字段名→fieldId 由 agent 先跑
`dws aitable field get` 回读后填入 plan（field_ids 段），脚本不硬编码 fieldId。
幂等口径：快照表按 stat_date 单键 upsert-by-key；事件表按确定性事件 ID 单键。"""
import json
import os
import time

from . import config as cfgmod

SNAP_CELL_MAP = [
    ("traffic", "net_total", "公网流量GB"), ("traffic", "net_down", "公网下行GB"),
    ("traffic", "net_up", "公网上行GB"), ("traffic", "line_out", "专线流出GB"),
    ("traffic", "line_in", "专线流入GB"),
    ("holdings", "ecs_vcpu", "ECSvCPU核"), ("holdings", "ecs_instances", "ECS实例数"),
    ("holdings", "oss_storage", "OSS存储TB"), ("holdings", "db_instances", "DB实例数"),
    ("holdings", "db_cpu", "DB核数"), ("holdings", "db_disk", "DB磁盘TB"),
    ("maas", "maas_gaap", "MaaS日GAAP元"), ("maas", "maas_calls", "MaaS日调用量"),
]
EVENT_CELL_MAP = [("event_date", "事件日期"), ("event_type", "事件类型"),
                  ("level", "级别"), ("metric", "目标指标"),
                  ("evidence", "证据"), ("status", "状态")]


def merged_by_date(snapshot, customer):
    """traffic/holdings 按 customer_key、maas 按 maas_cid 归并到 stat_date。"""
    by_date = {}
    for section in ("traffic", "holdings"):
        for row in snapshot.get(section, []):
            if row.get("customer_key") == customer["key"]:
                by_date.setdefault(row["stat_date"], {})[section] = row
    if customer.get("maas_cid"):
        for row in snapshot.get("maas", []):
            if row.get("maas_cid") == customer["maas_cid"]:
                by_date.setdefault(row["stat_date"], {})["maas"] = row
    return by_date


def plan_for_customer(customer, snapshot, field_ids):
    """field_ids: {字段名: fieldId}（agent 回读填入）。返回 upsert argv 清单。"""
    radar = customer.get("radar", {})
    if not radar.get("base_id") or not radar.get("snapshot_table_id"):
        return []
    key_fid = field_ids.get("快照日期")
    if not key_fid:
        return []
    out = []
    for sdate, sections in sorted(merged_by_date(snapshot, customer).items()):
        cells = {}
        for section, key, fname in SNAP_CELL_MAP:
            row = sections.get(section)
            fid = field_ids.get(fname)
            if row and row.get(key) is not None and fid:
                cells[fid] = row[key]
        if not cells:
            continue
        argv = ["aitable", "+record-upsert-by-key", "--base-id", radar["base_id"],
                "--table-id", radar["snapshot_table_id"], "--key-field-id", key_fid,
                "--key-value", sdate, "--cells", json.dumps(cells, ensure_ascii=False),
                "--yes", "--format", "json"]
        out.append({"argv": argv,
                    "on_unknown": {"action": "query_then_decide",
                                   "query_argv": ["aitable", "+record-query", "--base-id",
                                                  radar["base_id"], "--table-id",
                                                  radar["snapshot_table_id"], "--query", sdate,
                                                  "--format", "json"],
                                   "rule": "查到记录且 cells 正确→不重试；查不到→重试一次；仍查不到→报错停"}})
    return out


def plan_events(customer, events, field_ids):
    radar = customer.get("radar", {})
    if not radar.get("base_id") or not radar.get("events_table_id"):
        return []
    key_fid = field_ids.get("事件ID")
    if not key_fid:
        return []
    out = []
    for ev in events:
        cells = {key_fid: ev["event_id"]}
        for src_key, fname in EVENT_CELL_MAP:
            fid = field_ids.get(fname)
            if ev.get(src_key) is not None and fid:
                cells[fid] = ev[src_key]
        argv = ["aitable", "+record-upsert-by-key", "--base-id", radar["base_id"],
                "--table-id", radar["events_table_id"], "--key-field-id", key_fid,
                "--key-value", ev["event_id"], "--cells",
                json.dumps(cells, ensure_ascii=False), "--yes", "--format", "json"]
        out.append({"argv": argv,
                    "on_unknown": {"action": "query_then_decide",
                                   "query_argv": ["aitable", "+record-query", "--base-id",
                                                  radar["base_id"], "--table-id",
                                                  radar["events_table_id"],
                                                  "--query", ev["event_id"],
                                                  "--format", "json"],
                                   "rule": "查到记录且 cells 正确→不重试；查不到→重试一次；仍查不到→报错停"}})
    return out


def cmd_store(args):
    cfg = cfgmod.load_config(args.config)
    with open(args.snapshot, encoding="utf-8") as fh:
        snapshot = json.load(fh)
    field_ids = {}
    if args.field_ids:
        with open(args.field_ids, encoding="utf-8") as fh:
            blob = json.load(fh)
        field_ids = blob.get("fields", blob)
    keys = args.customers.split(",") if args.customers else None
    plan = []
    for cust in cfgmod.customers(cfg, keys=keys):
        fids = field_ids
        rel = cust.get("radar", {}).get("field_ids_file")
        if rel:
            path_f = os.path.join(cfgmod.SUITE_DIR, rel)
            if os.path.exists(path_f):
                with open(path_f, encoding="utf-8") as fh:
                    blob = json.load(fh)
                fids = blob.get("fields", blob)
        plan.extend(plan_for_customer(cust, snapshot, fids))
    out_dir = args.out_dir or os.path.join(cfgmod.SUITE_DIR, "neil-customer-radar", "outputs")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"store-plan-{snapshot['meta']['run_date']}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
                   "commands": plan}, fh, ensure_ascii=False, indent=1)
    if not plan:
        print("WARN store 计划为空：snapshot 无 config 内客户行或 field_ids 缺失")
    print(json.dumps({"plan": path, "commands": len(plan)}, ensure_ascii=False))
    return 0
