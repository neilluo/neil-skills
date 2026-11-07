"""看板层：outputs 历史 snapshot+events → 单文件 HTML（数据内嵌，无外部依赖）。
重生式刷新：输入文件内容 hash 不变则不重写（AGENTS.md 15 条）。
不做 QW Pages 托管（发布要桌面确认弹窗，卡死无人值守 cron）。"""
import glob
import hashlib
import json
import os
import time

HTML_PATH_NAME = "dashboard.html"
HASH_PATH_NAME = ".dashboard_hash"

PAGE = """<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>客户资源雷达</title><style>
body{font:14px/1.6 -apple-system,"PingFang SC",sans-serif;margin:0;background:#f6f7f9;color:#1f2329}
header{background:#fff;padding:16px 24px;border-bottom:1px solid #e5e6eb}
h1{font-size:18px;margin:0} .meta{color:#86909c;font-size:12px}
main{padding:24px;max-width:1100px;margin:0 auto}
.card{background:#fff;border-radius:8px;padding:16px 20px;margin-bottom:16px}
.card h2{font-size:15px;margin:0 0 8px} table{border-collapse:collapse;width:100%;font-size:13px}
th,td{border-bottom:1px solid #f0f0f0;padding:6px 8px;text-align:right}
th:first-child,td:first-child{text-align:left}
.ev{padding:8px 12px;border-left:3px solid #f53f3f;background:#fff7f5;margin:6px 0;border-radius:4px}
.ev.P2{border-color:#ff7d00;background:#fff7e8}.ev.info{border-color:#86909c;background:#f7f8fa}
.none{color:#86909c}</style></head><body>
<header><h1>客户资源雷达</h1><div class="meta" id="meta"></div></header><main id="app"></main>
<script>const D=__DATA__;
const fmt=v=>v==null?'-':Number(v).toLocaleString('zh-CN',{maximumFractionDigits:1});
document.getElementById('meta').textContent='生成 '+D.generated_at+' ｜ 快照 '+D.snapshots.length+' 份 ｜ 统计日 '+D.stat_dates.join(', ');
let html='';
if(D.degraded.length){html+='<div class="ev P1"><b>采集降级</b> 以下跑批日对账门未过、流量走了逐客户兜底：'+D.degraded.join(', ')+'</div>';}
for(const c of D.customers){
  html+='<div class="card"><h2>'+c.name+' <span class="meta">'+c.key+'</span></h2>';
  const evs=D.events[c.key]||[];
  html+= evs.length? evs.map(e=>'<div class="ev '+e.level+'"><b>'+e.event_type+'</b> '+e.event_date+' ｜ '+e.metric+'<br><span class="meta">'+e.evidence+'</span></div>').join('') : '<div class="none">当前无动态信号</div>';
  const rows=c.rows;
  if(rows.length){html+='<table><tr><th>统计日</th><th>公网流量GB</th><th>下行</th><th>上行</th><th>专线出</th><th>专线入</th><th>ECS核</th><th>DB实例</th><th>MaaS GAAP元</th></tr>';
    for(const r of rows){html+='<tr><td>'+r.stat_date+'</td><td>'+fmt(r.net_total)+'</td><td>'+fmt(r.net_down)+'</td><td>'+fmt(r.net_up)+'</td><td>'+fmt(r.line_out)+'</td><td>'+fmt(r.line_in)+'</td><td>'+fmt(r.ecs_vcpu)+'</td><td>'+fmt(r.db_instances)+'</td><td>'+fmt(r.maas_gaap)+'</td></tr>';}
    html+='</table>';}
  html+='</div>';}
document.getElementById('app').innerHTML=html;</script></body></html>"""


def _load_history(out_dir):
    snapshots = []
    for path in sorted(glob.glob(os.path.join(out_dir, "snapshot-*.json"))):
        with open(path, encoding="utf-8") as fh:
            snap = json.load(fh)
        if snap.get("meta", {}).get("schema_version") != "v1":
            continue
        snapshots.append(snap)
    return snapshots


def _merge_customer_rows(snapshots, customer):
    by_date = {}
    for snap in snapshots:
        for section in ("traffic", "holdings", "maas"):
            for row in snap.get(section, []):
                ident = row.get("customer_key") or row.get("maas_cid")
                if ident not in (customer["key"], customer.get("maas_cid")):
                    continue
                target = by_date.setdefault(row["stat_date"], {"stat_date": row["stat_date"]})
                for key, val in row.items():
                    if key not in ("customer_key", "report_customer_name",
                                   "stat_date", "maas_cid"):
                        target[key] = val
    return [by_date[d] for d in sorted(by_date)]


def build_payload(cfg, snapshots, events):
    stat_dates = sorted({d for s in snapshots for d in s.get("meta", {}).get("stat_dates", [])})
    degraded = [s["meta"]["run_date"] for s in snapshots
                if s.get("meta", {}).get("gate", {}).get("degraded")]
    return {"generated_at": time.strftime("%Y-%m-%d %H:%M +08:00"),
            "snapshots": snapshots, "stat_dates": stat_dates, "degraded": degraded,
            "customers": [{"key": c["key"], "name": c["name"],
                           "rows": _merge_customer_rows(snapshots, c)}
                          for c in cfg.get("customers", [])],
            "events": events}


def cmd_dashboard(args):
    from . import config as cfgmod
    cfg = cfgmod.load_config(args.config)
    out_dir = args.out_dir or os.path.join(cfgmod.SUITE_DIR, "neil-customer-radar", "outputs")
    snapshots = _load_history(out_dir)
    events = {}
    epaths = sorted(glob.glob(os.path.join(out_dir, "events-*.json")))
    if epaths:
        with open(epaths[-1], encoding="utf-8") as fh:
            events = json.load(fh).get("events", {})
    payload = build_payload(cfg, snapshots, events)
    html = PAGE.replace("__DATA__", json.dumps(payload, ensure_ascii=False))
    # hash 只算数据部分（generated_at 带时间戳，否则每次必变、重生式失效）
    data_digest_src = json.dumps({k: v for k, v in payload.items()
                                  if k != "generated_at"},
                                 ensure_ascii=False, sort_keys=True)
    digest = hashlib.sha256(data_digest_src.encode("utf-8")).hexdigest()
    hpath = os.path.join(out_dir, HASH_PATH_NAME)
    old = open(hpath, encoding="utf-8").read().strip() if os.path.exists(hpath) else ""
    if digest == old and not args.force:
        print(json.dumps({"dashboard": "unchanged", "path": os.path.join(out_dir, HTML_PATH_NAME)}))
        return 0
    with open(os.path.join(out_dir, HTML_PATH_NAME), "w", encoding="utf-8") as fh:
        fh.write(html)
    with open(hpath, "w", encoding="utf-8") as fh:
        fh.write(digest)
    print(json.dumps({"dashboard": "written", "path": os.path.join(out_dir, HTML_PATH_NAME)}))
    return 0
