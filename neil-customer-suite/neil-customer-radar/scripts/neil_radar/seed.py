"""播种层：ChatBI 一问拉报表全量客户名称+CID，与 config 出合并报告。
只报告不写 config（入表须人确认——PUBLIC 仓库+客户清单是业务口径）。
alidocs 人工清单表交叉核对由人工/dws 只读执行，不在本脚本内（dws 走宿主执行契约）。"""
import json
import os
import time

from . import chatbi as cb
from . import config as cfgmod
from . import questions as q


def list_customers_question():
    return "列出报表中全部客户名称和CID，按客户名称展示"


def cmd_seed(args):
    cfg = cfgmod.load_config(args.config)
    chatbi_cfg = cfgmod.chatbi_cfg(cfg)
    out_dir = args.out_dir or os.path.join(cfgmod.SUITE_DIR, "neil-customer-radar", "outputs")
    result = cb.ask(chatbi_cfg, out_dir, list_customers_question(),
                    cfg["chatbi"].get("report_id", "616045"), "report")
    rows = cb.rows_from_sql_datas(result) or cb.rows_from_markdown(result)
    names = list(rows[0].keys()) if rows else []
    cname_col = q.pick_col(names, q.CUSTOMER_CANDIDATES)
    cid_col = q.pick_col(names, q.CID_CANDIDATES)
    report = {}
    for row in rows:
        cname = str(row.get(cname_col) or "").strip() if cname_col else ""
        if cname:
            report[cname] = str(row.get(cid_col) or "").strip() if cid_col else None
    configured = {c.get("report_customer_name"): c["key"]
                  for c in cfg["customers"] if c.get("report_customer_name")}
    matched = sorted(set(report) & set(configured))
    new_in_report = sorted(set(report) - set(configured))
    missing_in_report = sorted(set(configured) - set(report))
    payload = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
               "report_total": len(report),
               "report": report,
               "matched": [{"name": n, "key": configured[n], "cid": report[n]} for n in matched],
               "new_in_report": [{"name": n, "cid": report[n]} for n in new_in_report],
               "missing_in_report": [{"name": n, "key": configured[n]} for n in missing_in_report]}
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "seed-report.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
    print(json.dumps({"report": path, "report_total": len(report),
                      "matched": len(matched), "new": len(new_in_report),
                      "missing": len(missing_in_report)}, ensure_ascii=False))
    return 0
