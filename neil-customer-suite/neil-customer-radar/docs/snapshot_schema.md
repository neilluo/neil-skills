# snapshot.json 契约 v1（neil-customer-radar 采集层 → 存储/分析/看板层的唯一接口）

版本：v1（2026-11-07）。采集层 `collect.py` 产出、`store.py`/`analyze.py`/`render_dashboard.py` 消费。
改任何字段前先改本文件；渲染与分析只认 v1，遇未知 schema_version 报错退出，禁静默兼容。

## 顶层结构

```jsonc
{
  "meta": {
    "schema_version": "v1",
    "run_date": "2026-11-07",          // 跑批日（本地时区 +08:00）
    "stat_dates": ["20261025", "...", "20261106"],  // 本次覆盖的统计日（升序）
    "generated_at": "ISO8601",
    "sources": ["fbi:616045", "fbi:dataset:76050019"],
    "gate": {                          // 合计对账门（分组问数完整性）
      "stat_date": "20261106",
      "metric": "net_total",
      "grouped_sum": 123456.0,         // 分组问数各行求和
      "report_total": 123400.0,        // 报表匿名合计行（=全客户合计）
      "ratio": 1.0005,                 // grouped_sum / report_total
      "passed": true,                  // |ratio-1| <= gate_tolerance 才 true
      "degraded": false                // true = 对账失败已降级逐客户问数
    },
    "failures": [ {"scope": "traffic-grouped", "message": "..."} ]
  },
  "traffic":  [ {"customer_key","report_customer_name","stat_date",
                 "net_total","net_down","net_up","line_out","line_in"} ],   // 数值 float|null
  "holdings": [ {"customer_key","report_customer_name","stat_date",
                 "ecs_vcpu","ecs_instances","oss_storage","db_instances","db_cpu","db_disk"} ],
  "products": [ {"customer_key","report_customer_name","stat_date",
                 "product","instances"} ],        // 产品存在性证据（新启用/停用检测输入）
  "maas":     [ {"maas_cid","report_customer_name","stat_date","maas_gaap","maas_calls"} ]
}
```

## 口径约定

1. **stat_date 为报表统计日**（YYYYMMDD 字符串，日期列带时间戳时取头 8 位 + strptime 校验，weekly 陷阱 12）。
   跑批日 D 通常只能拿到 D-1 及更早的完整统计日。**stat_dates = 本次请求的完整窗口**
   （collect 无条件写入）；窗口内某客户缺行的统计日由 analyze 的 data_gap 事件暴露，不在采集层补零。
2. **数值一律 float 或 null**：parse_number 归一（去千分位/星号），'-'/'--'/空 → null。禁字符串数值入库。
   maas 行以 maas_cid 为身份键（dataset 76050019 维度是 cid，无 customer_key）。
3. **customer_key 以 config/customers.json 为准**；报表回的客户名经 `report_customer_name` 精确匹配
   （禁包含匹配——weekly 陷阱 5：日值列与 `_周均值` 兄弟列、相似客户名都会静默绑错）。
   报表出现而 config 没有的客户：行携带指标值进 unknown 列表（对账门全量求和需要），
   落盘 `outputs/unknown-<run_date>.json` 供人核对入表，不进 meta.failures、不自动入 config。
4. **products 段 = holdings 指标派生的产品族存在性**（collect._derive_products：值>0 即该族在用，
   product 取值 ∈ ecs_vcpu/ecs_instances/oss_storage/db_instances/db_cpu/db_disk）。
   实测 616045 组件无产品名维度（仅产品团队码，2026-11-07 probe），产品级存在性走 kunpeng 账单深钻；
   analyze 的新启用/停用检测基于本段+holdings 零→非零，禁宣称产品名级覆盖。
5. **gate 只校 traffic.net_total 一个指标**（代表性足够且报表有匿名合计行）；tolerance 默认 0.05，
   写 config `thresholds.gate_tolerance`。**求和口径 = 分组问数全量行（config 内 + unknown 行）**，
   因为报表合计行是 28 客户全量；unknown 行携带指标值仅用于对账，存储/分析只消费 config 内行。
   对账失败 → 该统计日 traffic 降级逐客户问数（degraded=true）。
6. **maas 段按 maas_cid 过滤**（dataset 76050019 维度是 cid）；config 中 maas_cid 为 null 的客户不进 maas 段。
7. 文件落盘：`outputs/snapshot-<run_date>.json`（重跑覆盖幂等）；历史序列 = 该目录按 run_date 升序。

## 消费方约束

- store.py：只写 traffic+holdings+products+maas 四段进 AI 表格（快照表按 stat_date 单键 upsert）。
- analyze.py：读历史序列算信号；信号证据必须引用本契约字段（customer_key/stat_date/原始值），禁引用渲染层产物。
- render_dashboard.py：整包内嵌最新 snapshot + 近 N 天序列；不读 AI 表格（表格是人对账视图，非分析源）。
