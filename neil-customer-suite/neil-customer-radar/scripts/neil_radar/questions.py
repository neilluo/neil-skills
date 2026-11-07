"""问数层：分组问数问题模板 + 回行归一（日期/客户/指标列精确匹配）。
禁包含匹配（weekly 陷阱 5：日值列与 _周均值 兄弟列会静默绑错）；
日期列带时间戳时取头 8 位 + strptime 校验（weekly 陷阱 12）。纯函数，无 I/O。"""
import datetime as dt

from .chatbi import parse_number

DATE_CANDIDATES = ("统计日期", "日期", "stat_date", "dt", "date")
CUSTOMER_CANDIDATES = ("客户名称", "客户", "客户全称")
CID_CANDIDATES = ("cid", "CID", "客户ID")
DISPLAY_SUFFIX = "(展示值)"


def _norm_col(name):
    """sqlDatas 列名归一：报表字段 '/' 被替换为 '_'（实测 公网络流量/GB→公网络流量_GB）。
    归一后仍精确匹配，禁子串兜底（weekly 陷阱 5）。"""
    return str(name or "").replace("/", "_").strip()


def pick_metric_col(names, field, aliases=()):
    """字段名 → 回行列名：归一精确匹配（field 或任一 alias）且排除 (展示值) 兄弟列；
    无命中 → None。报表字段命名自身不一致（实测 下行=公网络下行流量、上行=公网络上行流量，
    2026-11-07），别名走 config metrics.aliases，禁子串兜底。"""
    targets = {_norm_col(field)} | {_norm_col(a) for a in aliases}
    for name in names:
        if str(name).endswith(DISPLAY_SUFFIX):
            continue
        if _norm_col(name) in targets:
            return name
    return None


def stat_dates(run_date, range_days):
    """跑批日 D 往前 range_days 个统计日（D-1..D-range_days），升序 YYYYMMDD。"""
    day = dt.datetime.strptime(run_date, "%Y-%m-%d").date()
    out = []
    for offset in range(range_days, 0, -1):
        out.append((day - dt.timedelta(days=offset)).strftime("%Y%m%d"))
    return out


def normalize_date(raw):
    """'2026-11-06 00:00:00'/'20261106'/'2026/11/6' → '20261106'；非法 → None。"""
    text = str(raw or "").strip()
    head = text[:10].replace("/", "-").replace(".", "-")
    if "-" in head:
        parts = head.split(" ")[0].split("-")
        if len(parts) == 3:
            try:
                return dt.date(int(parts[0]), int(parts[1]), int(parts[2])).strftime("%Y%m%d")
            except ValueError:
                return None
    digits = "".join(ch for ch in text[:10] if ch.isdigit())
    if len(digits) >= 8:
        try:
            dt.datetime.strptime(digits[:8], "%Y%m%d")
            return digits[:8]
        except ValueError:
            return None
    return None


def pick_col(names, candidates):
    """精确匹配候选列名；无命中 → None（调用方记 failure，禁子串兜底）。"""
    for cand in candidates:
        if cand in names:
            return cand
    return None


def _fields_question(fields, dims, span):
    return (f"统计日期{span[0]}至{span[1]}内，每个客户的"
            f"{'、'.join(fields)}，按{'和'.join(dims)}展示")


def traffic_question(fields, span):
    return _fields_question(fields, ("客户名称", "统计日期"), span)


def holdings_question(fields, span):
    return _fields_question(fields, ("客户名称", "统计日期"), span)


def maas_question(fields, cids, span):
    return (f"统计日期{span[0]}至{span[1]}内，cid为{'、'.join(cids)}的"
            f"{'、'.join(fields)}，按cid和统计日期展示")


def maas_question_single(fields, cid, span):
    return maas_question(fields, [cid], span)


def total_question(field, stat_date):
    return f"统计日期{stat_date}的{field}总计是多少"


TOTAL_ROW_NAMES = {"合计", "总计", "小计", "总和", "total", "Total", "TOTAL"}


def _norm_cid(raw):
    """cid 归一：数值型回行 '110133.0' → '110133'（review 2026-11-07 P1-11）。"""
    text = str(raw or "").strip()
    if text.endswith(".0"):
        try:
            return str(int(float(text)))
        except ValueError:
            return text
    return text


def parse_grouped_rows(rows, metric_fields, customer_map, cid_mode=False, fixed_key=None):
    """回行 → (records, unknown, missing_cols)。records 每行 {customer_key|maas_cid,
    report_customer_name, stat_date, <metric_key>: float|None}。
    metric_fields: [(key, field)]；列名归一精确匹配 field（禁子串兜底）。
    fixed_key：降级逐客户问数（回行无客户列）时把全部行归到该 key。
    合计/小计行直接丢弃（review P1-5：进 unknown 会污染对账门求和）。
    列名取全行并集（多 sqlDatas 块拼接时 rows[0] 不代表全部块，review P1-6）。"""
    if not rows:
        return [], [], []
    names = []
    for row in rows:
        for name in row.keys():
            if name not in names:
                names.append(name)
    date_cols = [c for c in DATE_CANDIDATES if c in names]
    cust_col = None if cid_mode else pick_col(names, CUSTOMER_CANDIDATES)
    cid_col = pick_col(names, CID_CANDIDATES) if cid_mode else None
    if not date_cols or (not cust_col and not cid_col and not fixed_key):
        return [], [], []
    col_of = {m[1]: pick_metric_col(names, m[1], m[2] if len(m) > 2 else ())
              for m in metric_fields}
    missing_cols = [m[1] for m in metric_fields if not col_of[m[1]]]
    records, unknown = [], []
    for row in rows:
        sdate = None
        for col in date_cols:
            sdate = normalize_date(row.get(col))
            if sdate:
                break
        if not sdate:
            continue
        if cid_mode:
            cid = _norm_cid(row.get(cid_col))
            rec = {"maas_cid": cid, "report_customer_name": cid, "stat_date": sdate}
        else:
            cname = str(row.get(cust_col) or "").strip() if cust_col else ""
            if cname in TOTAL_ROW_NAMES:
                continue
            key = customer_map.get(cname) if cname else fixed_key
            rec = {"customer_key": key,
                   "report_customer_name": cname or (fixed_key or ""), "stat_date": sdate}
            if not key:
                # unknown 行保留指标值：对账门需全量行求和（config 内+外），存储/分析只消费 config 内
                for m in metric_fields:
                    col = col_of.get(m[1])
                    rec[m[0]] = parse_number(row.get(col)) if col else None
                unknown.append(rec)
                continue
        for m in metric_fields:
            col = col_of.get(m[1])
            rec[m[0]] = parse_number(row.get(col)) if col else None
        records.append(rec)
    return records, unknown, missing_cols
