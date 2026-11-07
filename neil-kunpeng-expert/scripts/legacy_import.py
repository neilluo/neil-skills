#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""legacy_import.py —— 把本会话两份历史存档转成 bills_raw.json（aggregate.py 的标准输入）

用途：离线复现/自证。生产路径是 fetch_bills.js 直接从 usercenter2 页面落 bills_raw.json；
本脚本只服务"用已存档数据重跑聚合与渲染"，保证 skill 不依赖浏览器也能端到端验证。

输入：
  --rg-links   旧格式资源组台账 {groups:{<组>:[{p,id,nk,sp,m:{month:金额},al,tg}]}, aux:{...}}
  --instances  旧格式实例存档 {full:{<pip>:[{id,nick,spec,alloc,reg,zone,ip,pip,rg,tag,com,ct,req,res}]},
                               summ:{...}, C:{fc/gpdb/acs:{roots:{...}}}}
输出：
  --out bills_raw.json  {meta:{uid,months,sources}, instance_rows:[...], group_rows:[...]}

行字段名对齐 aggregate.py 的读取面（month/pipCode/instanceId/instanceNick/instanceSpec/
instanceAllocation/instanceTag/resourceGroupName/requireAmount/commodityName/resName/chargeType）。
残缺月（如只出账到月内某天的 202611）原样带入，由 aggregate --months-complete 决定进不进均值。
"""

from __future__ import annotations

import argparse
import json


def rows_from_rg_links(doc):
    rows = []
    for group, items in (doc.get("groups") or {}).items():
        for it in items:
            for month, amt in (it.get("m") or {}).items():
                rows.append({
                    "month": month,
                    "pipCode": it.get("p"),
                    "instanceId": it.get("id"),
                    "instanceNick": it.get("nk"),
                    "instanceSpec": it.get("sp"),
                    "instanceAllocation": it.get("al"),
                    "instanceTag": it.get("tg"),
                    "resourceGroupName": group,
                    "requireAmount": amt,
                    "commodityName": "",
                    "resName": "",
                    "chargeType": "postpay",
                    "tableType": "INSTANCE_CONSUME_MONTH",
                })
    return rows


def rows_from_instances(doc, partial_month):
    rows = []

    def push(pip, x, req):
        rows.append({
            "month": partial_month,
            "pipCode": pip,
            "instanceId": x.get("id"),
            "instanceNick": x.get("nick"),
            "instanceSpec": x.get("spec"),
            "instanceAllocation": x.get("alloc"),
            "instanceTag": x.get("tag"),
            "resourceGroupName": x.get("rg") or "",
            "requireAmount": req,
            "commodityName": x.get("com") or "",
            "resName": x.get("res") or "",
            "chargeType": x.get("ct") or "postpay",
            "tableType": "INSTANCE_CONSUME_MONTH",
        })

    for pip, items in (doc.get("full") or {}).items():
        for x in items:
            push(pip, x, x.get("req"))

    # summ.ecs：规格|地域|计费 聚合组，sample 实例 id 作为证据行（金额取组均摊，仅证据）
    for key, grp in ((doc.get("summ") or {}).get("ecs") or {}).items():
        spec, reg, ct = (key.split("|") + ["", "", ""])[:3]
        for sid in (grp.get("s") or [])[:3]:
            iid, _, nick = sid.partition("/")
            rows.append({
                "month": partial_month,
                "pipCode": "ecs",
                "instanceId": iid,
                "instanceNick": nick or None,
                "instanceSpec": spec,
                "instanceAllocation": "地域:%s" % reg,
                "instanceTag": "",
                "resourceGroupName": "",
                "requireAmount": round(grp.get("req", 0) / max(grp.get("n", 1), 1), 2),
                "commodityName": "云服务器（按量付费）" if ct == "postpay" else "云服务器ECS(包月)",
                "resName": "",
                "chargeType": ct or "postpay",
                "tableType": "INSTANCE_CONSUME_MONTH",
            })

    # C.<pip>.roots：饱和抽样根集合，作为无金额证据行（fc/gpdb/acs 计算面存在性）
    for pip, blob in (doc.get("C") or {}).items():
        for _, root in (blob.get("roots") or {}).items():
            rid = root.get("0") if isinstance(root, dict) else None
            meta = root.get("1") if isinstance(root, dict) else {}
            if not rid:
                continue
            rows.append({
                "month": partial_month,
                "pipCode": pip,
                "instanceId": rid if pip != "fc" else "acs:fc:ap-southeast-1:0:functions/%s" % rid,
                "instanceNick": None,
                "instanceSpec": None,
                "instanceAllocation": (meta or {}).get("alloc") or "",
                "instanceTag": "",
                "resourceGroupName": "",
                "requireAmount": 0,
                "commodityName": (meta or {}).get("com") or "",
                "resName": "",
                "chargeType": "postpay",
                "tableType": "INSTANCE_CONSUME_MONTH",
            })
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rg-links", default="", help="旧格式资源组台账 json")
    ap.add_argument("--instances", default="", help="旧格式实例存档 json")
    ap.add_argument("--uid", default="1077748325118640")
    ap.add_argument("--customer", default="北京坤启无限科技有限公司")
    ap.add_argument("--brand", default="Converge AI")
    ap.add_argument("--cid", default="1941872709")
    ap.add_argument("--account", default="ubiquantvc.onaliyun.com")
    ap.add_argument("--months", default="202609,202610,202611")
    ap.add_argument("--partial-month", default="202611", help="instances 存档所属残缺月")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    group_rows, instance_rows = [], []
    sources = []
    if a.rg_links:
        group_rows = rows_from_rg_links(json.load(open(a.rg_links)))
        sources.append(a.rg_links)
    if a.instances:
        instance_rows = rows_from_instances(json.load(open(a.instances)), a.partial_month)
        sources.append(a.instances)

    payload = {
        "meta": {"uid": a.uid, "customer": a.customer, "brand": a.brand,
                 "cid": a.cid, "account": a.account,
                 "months": a.months.split(","), "sources": sources},
        "instance_rows": instance_rows,
        "group_rows": group_rows,
    }
    with open(a.out, "w") as f:
        json.dump(payload, f, ensure_ascii=False)
    print("bills_raw: group_rows=%d instance_rows=%d -> %s" % (len(group_rows), len(instance_rows), a.out))


if __name__ == "__main__":
    main()
