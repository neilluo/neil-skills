# AI 网关专题页家族 · 装配质量与引用完整性 lint

生成：2026-09-21 ｜ 生成器：`scripts/lint-aigw-pages.py`（机械可判定项，确定性、可复算）

## 为什么这一半是脚本而不是 agent

首派的一致性评审 agent（R2）任务书含 5 个维度，跑 **59 分钟 / 120 次工具调用后死于模型服务错误、产物为 0**。
其中 **B 交叉引用完整性** 与 **D 装配质量** 是纯机械可判定的，交给 agent 既慢又会死；
改由本脚本承担（L1~L8）。**语义维度**（同一事实跨页口径一致性 / 与既有页面冲突 / SA 可用性）
才需要 agent，且必须**窄范围单派**。

## 结果

| 级别 | 条数 | 含义 |
|---|---|---|
| 🔴 P0 | 0 | 必须修：断链、超拆分阈值 |
| 🟠 P1 | 0 | 应修：章节号引用不存在、装配残留、页眉缺要素、章节号重复/缺失 |
| 🟡 P2 | 0 | 观感与可维护性：表格列数不一致、缺代号指针 |

## L8 `W1`~`W7` 分工代号残留计数

代号是蒸馏批次的内部分工标识，**主页 §0.6 已提供对照表解析器**（与 `aliyun-agentcore.md` 里
约 26 处 `RULINGS §x` 引用的既有约定同形），故保留不算缺陷，但计数留档以便后续决定是否改写：

| 文件 | `W1`~`W7` 出现次数 |
|---|---|
| `aliyun-ai-gateway.md` | 95 |
| `aliyun-ai-gateway-ops.md` | 53 |
| `aliyun-ai-gateway-mcp-agent.md` | 47 |
| `aliyun-ai-gateway-billing.md` | 37 |
| `aliyun-ai-gateway-auth.md` | 31 |
| `aliyun-ai-gateway-plugins.md` | 31 |
| `aliyun-ai-gateway-traffic.md` | 15 |
| **合计** | **309** |

## 家族规模（实测）

| 文件 | 行数 | 表数 |
|---|---|---|
| `aliyun-ai-gateway.md` | 1413 | 60 |
| `aliyun-ai-gateway-billing.md` | 963 | 43 |
| `aliyun-ai-gateway-traffic.md` | 1347 | 71 |
| `aliyun-ai-gateway-auth.md` | 1247 | 37 |
| `aliyun-ai-gateway-mcp-agent.md` | 1411 | 66 |
| `aliyun-ai-gateway-plugins.md` | 1541 | 66 |
| `aliyun-ai-gateway-ops.md` | 1549 | 68 |
| **合计** | **9471** | **411** |
