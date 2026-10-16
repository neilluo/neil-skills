"""发布层：alidocs 文档幂等创建/覆盖更新、回读校验、跨天跟进节与 publish 子命令编排。
create 前必查重（AGENTS.md 规则 I）；per-future 单客户失败隔离（规则 H）；require
只做形状校验、success 判定在调用方显式 raise（规则 A）。扩展时改这里：校验标记改
render.verification_markers；summary/transcripts 读盘形状改 _load_summary_and_texts。
跨天两处：followup_section（前日建单当日完结跟进）与 _carryover_data（当日零新工单
时结转 D0 官方未完结工单，改零工单口径＝render/publish 结转逻辑同批，见规则 L）。
跑批完成标记：cmd_publish 收尾经 _write_run_marker 写 outputs/run-<date>.json，
是 qoder_cron 巡检任务的完成判据；契约：finished_at 为本次 publish 完成时刻。
机械完成判定：check_status（纯读判定，无网络/写）+ cmd_check（check 子命令，
exit 0=今日已完成 / 3=缺失或过期 / 1=其他异常），巡检任务据退出码补偿，
不靠 prompt 推理。"""
import json
import os
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

from .config import OUT_DIR, cfg_tz, doc_title, load_config, select_customers
from .gate import sanitize_summary
from .render import carryover_section, esc_cell, render, verification_markers
from .transport import RETRY_CREATE, RETRY_TRANSPORT, run_dws

FOLLOWUP_DAYS = 7     # 跟进节跨天对账回看天数


def list_nodes(workspace, folder):
    nodes = []
    cursor = ""
    for _ in range(20):
        cmd = ["wiki", "node", "list", "--workspace", workspace, "--folder", folder, "--limit", "50"]
        if cursor:
            cmd += ["--cursor", cursor]
        data = run_dws(cmd, require=lambda d: isinstance(d.get("nodes"), list))
        nodes.extend(data.get("nodes") or [])
        if not data.get("hasMore"):
            break
        cursor = data.get("nextPageToken") or ""
        if not cursor:
            break
    return nodes


def doc_markdown(node_id):
    data = run_dws(["doc", "read", "--node", node_id], require=lambda d: "markdown" in d)
    return data.get("markdown") or ""


def _doc_folder_id(data):
    """从 doc info envelope（顶层/data/result）容错提取所属 folderId。"""
    for node in (data, data.get("data"), data.get("result")):
        if isinstance(node, dict):
            for field in ("folderId", "parentFolderId", "folder_id"):
                if node.get(field):
                    return node[field]
    return ""


def _folder_warning(customer):
    """customer_folder_node 激活（trap#6 重试经 run_dws require）：doc info 校验
    daily_doc_parent_node 的所属 folderId 是否等于配置值；不一致或校验失败
    只在该客户汇报行追加警告，不阻断发布。"""
    expected = customer.get("customer_folder_node")
    if not expected:
        return ""
    folder = customer["daily_doc_parent_node"]
    try:
        data = run_dws(["doc", "info", "--node", folder],
                       require=lambda d: bool(_doc_folder_id(d)))
    except Exception as exc:  # noqa: BLE001 校验失败不阻断发布
        return f"；警告：doc info 校验 folderId 失败（{type(exc).__name__}），未阻断"
    got = _doc_folder_id(data)
    if got != expected:
        return f"；警告：daily_doc_parent_node 的 folderId={got} ≠ 配置 customer_folder_node={expected}"
    return ""


def create_doc_idempotent(title, folder, tmp):
    """create 重试前先查重，防 envelope 抖动或「服务端已建但 CLI 非零」造成同名重复文档。
    外层至多 RETRY_TRANSPORT 轮；单轮内 run_dws 不重试（RETRY_CREATE=1），由查重决策。"""
    for _ in range(RETRY_TRANSPORT):
        try:
            data = run_dws(["doc", "create", "--name", title, "--folder", folder,
                            "--content-file", tmp], retries=RETRY_CREATE,
                           require=lambda d: isinstance(d, dict))
        except Exception:  # noqa: BLE001 非零 rc 也可能服务端已建，先查重再决定
            data = {}
        node_id = (data.get("nodeId") or (data.get("data") or {}).get("nodeId")
                   or (data.get("result") or {}).get("nodeId"))
        if node_id:
            return node_id, "created"
        existing = next((n for n in list_nodes(load_config()["doc_workspace"], folder)
                         if n.get("name") == title), None)
        if existing:
            return existing["nodeId"], "created(查重命中)"
    raise RuntimeError(f"doc create {RETRY_TRANSPORT} 轮均未拿到 nodeId：{title}")


def followup_section(date_str, cur_collect, prev_collects, key):
    """纯函数（评审分层归位：不再自行读盘）：前 FOLLOWUP_DAYS 日 collect 里未完结、
    当日窗口内完结的工单 → 跟进节（跨天对账，按客户隔离）。
    prev_collects=[(pdate, collect_json)]，由 cmd_publish 经 _load_prev_collects 提供。"""
    cur = cur_collect["customers"].get(key)
    if cur is None:
        return ""
    rows = []
    for pdate, prev in prev_collects:
        pslice = (prev or {}).get("customers", {}).get(key)
        if not pslice:
            continue
        for tid in pslice.get("ticket_order", []):
            pt = pslice["tickets"][tid]
            ct = cur["tickets"].get(tid)
            if not pt.get("completed_at") and ct and ct.get("completed_at"):
                rows.append(f"| {tid} | {esc_cell(ct['title'])} | {pdate} | {ct['completed_at']} |")
    if not rows:
        return ""
    return ("## 四、前日工单完结跟进\n\n| 工单ID | 标题 | 建单日 | 完结时间 |\n|---|---|---|---|\n"
            + "\n".join(rows))


def _load_prev_collects(date_str, days=FOLLOWUP_DAYS):
    """cmd_publish 专用读盘循环（从 followup_section 移出）→ [(pdate, collect)]。
    坏文件跳过不阻断：publish 整体不因某天前文件损坏而报废（失败隔离精神）。"""
    day = datetime.strptime(date_str, "%Y-%m-%d")
    out = []
    for back in range(1, days + 1):
        pdate = (day - timedelta(days=back)).strftime("%Y-%m-%d")
        ppath = os.path.join(OUT_DIR, f"collect-{pdate}.json")
        if not os.path.exists(ppath):
            continue
        try:
            with open(ppath, encoding="utf-8") as fh:
                out.append((pdate, json.load(fh)))
        except (OSError, ValueError):
            continue
    return out


def _load_summary_and_texts(date_str, key, has_tickets):
    """publish 读盘 → (summary, summary_missing, texts)。
    texts 供 sanitize_summary 做 quote 子串校验（messageId → 原文），
    含子群消息与建单/完结卡原文。"""
    summary, summary_missing = {}, bool(has_tickets)
    spath = os.path.join(OUT_DIR, f"summary-{date_str}-{key}.json")
    if os.path.exists(spath):
        summary_missing = False
        with open(spath, encoding="utf-8") as fh:
            summary = json.load(fh)
    texts = {}
    tpath = os.path.join(OUT_DIR, f"transcripts-{date_str}-{key}.json")
    if os.path.exists(tpath):
        with open(tpath, encoding="utf-8") as fh:
            tr = json.load(fh)
        for tid, t in tr.get("tickets", {}).items():
            bucket = {m["messageId"]: m["text"] for m in (t.get("subgroup_messages") or [])}
            if t.get("create_msg_id"):
                bucket[t["create_msg_id"]] = t.get("create_card_text") or ""
            if t.get("done_msg_id"):
                bucket[t["done_msg_id"]] = t.get("done_card_text") or ""
            texts[tid] = bucket
    return summary, summary_missing, texts


def _carryover_data(key, prev_collects, tz_label="+08:00"):
    """零工单结转（用户 2026-10-15 指令「如果没有工单的话，可以复用一下昨天的」）：
    当日零新工单时，回看 ≤7 天（prev_collects 由 cmd_publish 经 _load_prev_collects
    提供，按近→远排列）找该客户最近一个有工单的日期 D0，取 D0 中官方未完结
    （completed_at 为空）的工单结转。内容复用 D0 的 summary/transcripts，
    effective_status 经 sanitize_summary 以 D0 slice 校验（复用规则 E 门禁，失败
    自动回退规则值并留痕）。D0 无未完结工单或无任何历史 → 返回 ""（维持纯零工单
    说明，不再回看更早日）。返回结转节 markdown（render.carryover_section 纯函数）。"""
    for pdate, prev in prev_collects:
        pslice = (prev or {}).get("customers", {}).get(key)
        if not pslice or not pslice.get("ticket_order"):
            continue
        carry = [tid for tid in pslice["ticket_order"]
                 if not pslice["tickets"].get(tid, {}).get("completed_at")]
        if not carry:
            return ""  # D0 存在但全完结 → 维持零工单说明，不继续回看更早日
        summary, _, texts = _load_summary_and_texts(pdate, key, True)
        summary = sanitize_summary(summary, pslice, texts)
        return carryover_section(pdate, carry, pslice, summary, tz_label)
    return ""  # 无任何历史


def _update_doc(node_id, tmp, force):
    """目标文档已存在：非空且未 --force → 跳过不写；否则 overwrite。返回是否已写入。"""
    existing = doc_markdown(node_id)
    if existing.strip() and not force:
        return False
    data = run_dws(["doc", "update", "--node", node_id, "--mode", "overwrite",
                    "--content-file", tmp, "--yes"],
                   require=lambda d: isinstance(d, dict))
    if data.get("success") is not True:  # 规则 A：require 只校验形状，success 判定在调用方
        raise RuntimeError(f"doc update 未返回 success：node={node_id}")
    return True


def _verify_written(node_id, customer, slice_):
    """回读校验：工单ID 全出现 + verification_markers 文本出现；缺失只汇报不抛。"""
    check = doc_markdown(node_id)
    missing = [tid for tid in slice_["ticket_order"] if tid not in check]
    missing += [label for text, label in verification_markers(customer, slice_)
                if text not in check]
    return "校验通过" if not missing else f"校验缺失 {missing}（node={node_id} 供人工核）"


def publish_one(customer, date_str, collect, force, cfg, prev_collects):
    slice_ = collect["customers"].get(customer["key"])
    if slice_ is None:
        err = collect.get("errors", {}).get(customer["key"], "collect 无该客户")
        return f"[publish] {customer['key']} 跳过：{err}"
    summary, summary_missing, texts = _load_summary_and_texts(
        date_str, customer["key"], bool(slice_["ticket_order"]))
    summary = sanitize_summary(summary, slice_, texts)
    watermark = ("> 注：总结子代理缺失，本篇为规则回退渲染。\n" if summary_missing else "")
    carryover = ("" if slice_["ticket_order"] else
                 _carryover_data(customer["key"], prev_collects,
                                 cfg.get("timezone", "+08:00")))
    md = render(customer, date_str, slice_, summary,
                followup_section(date_str, collect, prev_collects, customer["key"]),
                watermark=watermark, tz_label=cfg.get("timezone", "+08:00"),
                carryover=carryover)
    title = doc_title(cfg, date_str)
    folder = customer["daily_doc_parent_node"]
    nodes = list_nodes(cfg["doc_workspace"], folder)
    target = next((n for n in nodes if n.get("name") == title), None)
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as fh:
        fh.write(md)
        tmp = fh.name
    note = "；总结缺失(回退渲染)" if summary_missing else ""
    note += _folder_warning(customer)
    try:
        if target is None:
            node_id, action = create_doc_idempotent(title, folder, tmp)
        else:
            node_id = target["nodeId"]
            if not _update_doc(node_id, tmp, force):
                return f"[publish] {customer['key']} 跳过：文档已存在且非空 {node_id}"
            action = "overwritten"
        state = _verify_written(node_id, customer, slice_)
        return f"[publish] {customer['key']} {action} node={node_id} {state}{note}"
    finally:
        os.unlink(tmp)


def _write_run_marker(date_str, results, errors):
    """跑批完成标记 outputs/run-<date>.json —— qoder_cron 巡检任务的完成判据。
    契约：finished_at 为本次 publish 完成时刻（配置时区，ISO +08:00）；results 为
    每客户汇报行字符串（成功/跳过/失败全含）；errors 按客户 key 记异常消息。
    写盘失败只打印警告、不影响主流程（规则 H 失败隔离精神）。"""
    try:
        payload = {"date": date_str,
                   "finished_at": datetime.now(cfg_tz()).isoformat(timespec="seconds"),
                   "results": results, "errors": errors}
        with open(os.path.join(OUT_DIR, f"run-{date_str}.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
    except Exception as exc:  # noqa: BLE001 标记写盘失败不得影响主流程
        print(f"[publish] 警告：run 完成标记写盘失败（{type(exc).__name__}: {exc}），不阻断")


def check_status(date_str):
    """机械完成判定（qoder_cron 巡检补偿依据，纯读、无网络/写操作）。
    读 outputs/run-<date>.json：finished_at 的日期（配置时区，tz_of）等于「今天」
    → (True, finished_at 原值)；标记不存在 → (False, "marker_absent")；
    finished_at 非今天 → (False, "stale:finished_at")。
    其他情况（JSON 损坏/缺键/时间格式非法）直接抛异常，由 cmd_check 归 exit 1。"""
    path = os.path.join(OUT_DIR, f"run-{date_str}.json")
    if not os.path.exists(path):
        return False, "marker_absent"
    with open(path, encoding="utf-8") as fh:
        marker = json.load(fh)
    finished_at = marker["finished_at"]
    tz = cfg_tz()
    done_day = datetime.fromisoformat(finished_at).astimezone(tz).date()
    if done_day == datetime.now(tz).date():
        return True, finished_at
    return False, "stale:finished_at"


def cmd_check(args):
    """check 子命令：机械判定当日跑批是否完成，退出码即结论（巡检脚本零推理）。
    exit 0=今日已完成（stdout: DONE finished_at=<值>）；exit 3=缺失/过期
    （stdout: MISSING reason=<marker_absent|stale:finished_at>）；exit 1=其他异常。"""
    try:
        ok, detail = check_status(args.date)
    except Exception as exc:  # noqa: BLE001 判定异常统一 exit 1（stderr 留痕）
        sys.exit(f"[check] 判定异常：{type(exc).__name__}: {exc}")
    if ok:
        print(f"DONE finished_at={detail}")
        return
    print(f"MISSING reason={detail}")
    sys.exit(3)


def cmd_publish(args):
    cfg = load_config()
    if not args.force:  # 机械幂等门：当日已有完成标记则 no-op，防巡检误补偿重跑
        try:
            ok, finished_at = check_status(args.date)
        except Exception:  # noqa: BLE001 标记损坏不阻断发布
            ok = False
        if ok:
            print(f"[publish] ALREADY_DONE 标记存在（finished_at={finished_at}），本次跳过；如需重发用 --force")
            return
    with open(os.path.join(OUT_DIR, f"collect-{args.date}.json"), encoding="utf-8") as fh:
        collect = json.load(fh)
    customers = select_customers(cfg, args.customers)
    prev_collects = _load_prev_collects(args.date)  # 7 天读盘循环自 followup_section 上移
    results, errors = [], {}
    with ThreadPoolExecutor(max_workers=len(customers)) as pool:
        futs = {pool.submit(publish_one, c, args.date, collect, args.force, cfg,
                            prev_collects): c for c in customers}
        for fut in futs:
            key = futs[fut]["key"]
            try:
                line = fut.result()
            except Exception as exc:  # noqa: BLE001 单客户失败隔离
                line = f"[publish] {key} 失败：{type(exc).__name__}: {exc}"
                errors[key] = f"{type(exc).__name__}: {exc}"
            print(line)
            results.append(line)
    # 所有客户处理完毕（成功/跳过/失败均入 results）后写完成标记
    _write_run_marker(args.date, results, errors)
