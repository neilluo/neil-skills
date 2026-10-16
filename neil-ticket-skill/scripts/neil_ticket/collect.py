"""采集层：主群窗口读取（read_messages）、子群探读（probe_subgroup/_probe_ticket）、
工单 slice 组装（_build_slice）与 collect 子命令编排。翻页一律走 transport._paginate，
dws 一律走 run_dws；单客户失败隔离 per-future try/except（AGENTS.md 规则 H）。
扩展时改这里：探读策略分支（subgroup_policy）在 _probe_ticket；slice 键形状改动
必须与 tests/run-regression.py 手搭 slice 逐键同形（规则 F）。"""
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

from .config import OUT_DIR, cfg_tz, load_config, select_customers, window_of
from .parse import compute_signals, parse_cards
from .transport import RETRY_AUTH, AccessDenied, _paginate, run_dws

LIMIT = 100
MAX_PAGES = 60
PROBE_MAX_PAGES = 6   # 子群探读只取证据链，6 页内配合 PROBE_MSG_CAP 截断足够
PROBE_MSG_CAP = 300   # 单子群保留消息条数上限


def read_messages(cid, start_str, end_str):
    """主群窗口读取：_paginate 通用翻页 + 窗口过滤；返回 (窗口内消息升序, warnings)。"""
    warnings = []
    got = list(_paginate(cid, end_str, start_str, LIMIT, MAX_PAGES, "主群", warnings))
    msgs = [m for m in got if start_str <= m["createTime"] < end_str]
    msgs.sort(key=lambda m: m["createTime"])
    return msgs, warnings


def probe_subgroup(sub_cid, lower_bound=None):
    """返回 (子群消息列表, warnings)；130003 抛 AccessDenied。
    边界=now 保留窗口后消息：它们是「实质状态」的证据链（取舍记录在 reference）；
    lower_bound=建单时间：补跑老日期不翻到建单之前，省页且不损证据链。"""
    warnings = []
    now = datetime.now(cfg_tz()).strftime("%Y-%m-%d %H:%M:%S")
    got = list(_paginate(sub_cid, now, lower_bound, LIMIT, PROBE_MAX_PAGES, "子群",
                         warnings, stop_on_short_page=True, seen_cap=PROBE_MSG_CAP))
    got.sort(key=lambda m: m["createTime"])
    return [{
        "createTime": m["createTime"], "sender": m.get("sender", ""),
        "senderId": m.get("senderId", ""), "text": m.get("text", ""),
        "messageId": m.get("messageId", ""),
    } for m in got[:PROBE_MSG_CAP]], warnings


def resolve_cid_by_name(name):
    cursor = "0"
    for _ in range(5):
        data = run_dws(
            ["chat", "search", "--query", name, "--limit", "20", "--cursor", cursor],
            require=lambda d: isinstance(d.get("result"), dict),
        )
        result = data["result"]
        for group in result.get("groups") or []:
            if group.get("title") == name:
                return group["openConversationId"]
        if not result.get("hasMore"):
            break
        cursor = result.get("nextCursor") or ""
        if not cursor:
            break
    raise RuntimeError(f"群名解析失败：{name}")


def _probe_ticket(ticket, start_str, policy):
    """单工单子群探读 → (transcripts entry, warnings)。policy=customer.subgroup_policy：
    probe_then_fallback（默认）130003 时降级为不可读；fallback_only 跳过探读直接降级。"""
    entry = dict(ticket)
    entry["subgroup_readable"] = None
    entry["probe_error"] = ""
    entry["subgroup_messages"] = []
    warns = []
    if ticket["subgroup_cid"]:
        if policy == "fallback_only":
            entry["subgroup_readable"] = False
            entry["probe_error"] = "策略fallback_only跳过探读"
        else:
            try:
                sub_msgs, probe_warns = probe_subgroup(
                    ticket["subgroup_cid"], lower_bound=ticket["created_at"] or start_str)
                entry["subgroup_messages"] = sub_msgs
                entry["subgroup_readable"] = True
                warns.extend(probe_warns)
            except AccessDenied as exc:
                entry["subgroup_readable"] = False
                entry["probe_error"] = exc.label
    entry["signals"] = compute_signals(ticket, entry["subgroup_messages"])
    return entry, warns


def collect_one(customer, date_str):
    start_str, end_str = window_of(date_str)
    cid = customer.get("service_group_cid") or resolve_cid_by_name(customer["service_group_name"])
    messages, warnings = read_messages(cid, start_str, end_str)
    bot = customer.get("service_bot_name", "阿里云服务台")
    tickets, order, parse_warns = parse_cards(messages, cid, bot)
    warnings.extend(parse_warns)
    transcripts = {"customer_key": customer["key"], "customer_name": customer["name"],
                   "date": date_str, "window": [start_str, end_str], "tickets": {}}
    policy = customer.get("subgroup_policy", "probe_then_fallback")
    for tid in order:
        entry, warns = _probe_ticket(tickets[tid], start_str, policy)
        warnings.extend(warns)
        transcripts["tickets"][tid] = entry
    return cid, tickets, order, transcripts, warnings


def _build_slice(customer, cid, tickets, order, transcripts, warnings):
    """transcripts → collect-{date}.json 的客户 slice。
    subgroup_msg_ids / subgroup_msg_times 写在 tickets[tid] 内部（ticket 级），
    render 的「（窗口外）」标注从同一层级读取（曾误读 slice 级恒 None，评审 P0）。"""
    tr = transcripts["tickets"]
    return {
        "name": customer["name"], "cid": cid, "ticket_order": order,
        "warnings": warnings,
        "tickets": {tid: {**tickets[tid],
                          "subgroup_msg_ids": [m["messageId"] for m in
                                               tr[tid]["subgroup_messages"]],
                          "subgroup_msg_times": {m["messageId"]: m["createTime"] for m in
                                               tr[tid]["subgroup_messages"]}}
                    for tid in order},
        "probe_errors": {tid: tr[tid]["probe_error"] for tid in order},
        "signals": {tid: tr[tid]["signals"] for tid in order},
        "subgroup_readable": {tid: tr[tid]["subgroup_readable"] for tid in order},
    }


def _auto_join_gap(customer, slice_, date_str):
    """auto_join_expected 激活（原死配置）：预期自动入群，但本批有子群链接的工单
    实测全部降级 → True，由汇报行标注不一致。补跑老日期不告警：入群配置不追溯
    历史子群（2026-10-15 实测：配置生效后 10-13 子群仍 130003）。"""
    if not customer.get("auto_join_expected"):
        return False
    yesterday = (datetime.now(cfg_tz()) - timedelta(days=1)).strftime("%Y-%m-%d")
    if date_str < yesterday:
        return False
    linked = [tid for tid in slice_["ticket_order"]
              if slice_["tickets"][tid].get("subgroup_cid")]
    return bool(linked) and all(slice_["subgroup_readable"].get(tid) is False
                                for tid in linked)


def _report_collect(cfg, collect):
    by_key = {c["key"]: c for c in cfg["customers"]}
    for key, slice_ in collect["customers"].items():
        readable = [f"{tid}:{'读' if slice_['subgroup_readable'][tid] is True else ('降' if slice_['subgroup_readable'][tid] is False else '无链')}"
                    for tid in slice_["ticket_order"]]
        line = f"[collect] {key} 工单 {len(slice_['ticket_order'])} 张 {readable}"
        if _auto_join_gap(by_key.get(key, {}), slice_, collect.get("date", "")):
            line += "（警告：预期自动入群但实测全降级）"
        print(line)


def cmd_collect(args):
    cfg = load_config()
    os.makedirs(OUT_DIR, exist_ok=True)
    auth = run_dws(["chat", "data-auth", "cross-org", "--all", "--grant-type", "timed",
                    "--ttl", "24h", "--yes"], retries=RETRY_AUTH,
                   require=lambda d: isinstance(d, dict))
    if auth.get("success") is not True:  # 规则 A：require 只校验形状，success 判定在调用方
        raise RuntimeError(f"data-auth cross-org 授权未返回 success：{str(auth)[:300]}")
    customers = select_customers(cfg, args.customers)
    collect = {"date": args.date,
               "generated_at": datetime.now(cfg_tz()).strftime("%Y-%m-%d %H:%M:%S"),
               "customers": {}, "errors": {}}
    with ThreadPoolExecutor(max_workers=len(customers)) as pool:
        futs = {pool.submit(collect_one, c, args.date): c for c in customers}
        for fut in futs:
            customer = futs[fut]
            try:
                cid, tickets, order, transcripts, warnings = fut.result()
                with open(os.path.join(OUT_DIR, f"transcripts-{args.date}-{customer['key']}.json"),
                          "w", encoding="utf-8") as fh:
                    json.dump(transcripts, fh, ensure_ascii=False, indent=2)
                collect["customers"][customer["key"]] = _build_slice(
                    customer, cid, tickets, order, transcripts, warnings)
                for warn in warnings:
                    print(f"[collect] {customer['key']} 警告：{warn}")
            except Exception as exc:  # noqa: BLE001 单客户失败隔离（含落盘/组装）
                collect["errors"][customer["key"]] = f"{type(exc).__name__}: {exc}"
                print(f"[collect] {customer['key']} 失败：{exc}")
                continue
    with open(os.path.join(OUT_DIR, f"collect-{args.date}.json"), "w", encoding="utf-8") as fh:
        json.dump(collect, fh, ensure_ascii=False, indent=2)
    _report_collect(cfg, collect)
    if collect["errors"]:
        sys.exit(1)
