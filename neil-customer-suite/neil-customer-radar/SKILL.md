---
name: neil-customer-radar
description: 重点客户资源雷达日批。从 devata 公共云资源看板（FBI 616045）+ MaaS 数据集（76050019）经 ChatBI 开放 API 分组问数采每客户流量/保有量/收入日序列，幂等写入每客户钉钉 AI 表格快照，跑客户动态分析（新产品启用/产品停用/网络流量异动=迁移信号/MaaS 趋势），有信号才推送，单文件 HTML 看板重生式刷新。当用户提到 客户雷达 / 资源快照 / 客户动态 / 新产品启用 / 产品停用 / 流量异动 / 迁移信号 / 每日快照 / 跑雷达 时使用。画架构图不在此 skill（走 neil-kunpeng-expert，仅主动触发）。
---

# neil-customer-radar

每日把每个客户的云资源使用量记下来，并从中发现客户动态。**全脚本驱动**（ChatBI 开放 API 静态
token，无需浏览器登录态）；dws 写表格由 agent 逐条直接执行（宿主契约禁 subprocess 调 dws）。

- 快照契约：[docs/snapshot_schema.md](docs/snapshot_schema.md)（v1，采集→存储/分析/看板唯一接口）
- 套件纪律：[../AGENTS.md](../AGENTS.md)（凭据/对账门/dws 契约/阈值口径）
- 统一客户表：`../config/customers.json`（唯一事实源；加客户只改它）

## 日批流程（cron 09:30，agent 按序执行）

```bash
cd <suite>/neil-customer-radar/scripts
python3 -m neil_radar.cli collect                 # 1 分组问数+对账门 → outputs/snapshot-<date>.json（全空 exit 1）
python3 -m neil_radar.cli store --snapshot ../outputs/snapshot-<date>.json   # 2 出 dws 写计划
# 3 agent 逐条执行 outputs/store-plan-<date>.json 的 commands[].argv（每条是 argv 数组，
#   按元素原样传参禁 shell 拼串拆词；禁管道/后台）
#   遇 status=unknown（create 路径 read-back 假阳性）：按该条 on_unknown.query_argv 查键，
#   记录与 cells 正确→不重试；查不到→重试一次；仍查不到→报错停（禁盲重放，防双写）
python3 -m neil_radar.cli analyze                 # 4 历史序列出事件 → events-<date>.json + events-plan
# 5 agent 逐条执行 outputs/events-plan-<date>.json 的 commands[].argv（同 3 的处置规则）
python3 -m neil_radar.cli dashboard               # 6 看板重生式刷新（数据无变化不重写）
```

推送（有信号才推，无信号静默）：events-<date>.json 中 level ∈ {P1,P2} 的事件，经
「问问」IM 会话推一条汇总（客户/事件类型/日期区间/幅度证据），禁下「客户在迁云」类结论。

## 能力边界（诚实声明）

- 616045 组件**无产品名维度**：products 段=holdings 派生的产品族存在性；产品级存在性/实例清单
  走 neil-kunpeng-expert 账单深钻（要浏览器登录态，按需触发）。
- 报表缺行客户（流量零值）≠ 停用：存在性以 holdings 为锚。
- ChatBI 自然语言→SQL 有非确定性：合计对账门是唯一防线，失败自动降级逐客户问数。
- 7 日移动平均需 ≥4 天历史：新装客户前几日无信号属预期，非故障。

## 测试

```bash
python3 tests/test_pure.py      # 归一/列匹配/对账门 18 例
python3 tests/test_analyze.py   # 新启用/停用/异动/事件ID 7 例
```
