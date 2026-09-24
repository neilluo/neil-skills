---
source_url: https://help.aliyun.com/zh/agentteams/view-dashboards-and-monitoring-1
fetch_date: 2026-09-20
product: AgentTeams
slug: view-dashboards-and-monitoring-1
body_sha256: ccaf0dee78b42f8825e2f8f8b8f567935332ffeaebf078c881ee3391c2e02ad7
body_bytes: 4616
migration_status: unknown
---

当实例运行一段时间后，需要了解 Worker 的运行状态、资源消耗和模型调用情况，以便及时发现异常并优化成本。AgentTeams 提供实例级仪表盘，实时展示 Worker 统计、团队用量分布和 Token 消耗趋势，帮助快速定位问题和优化资源配置。  

## 进入仪表盘
1. 登录 AgentTeams[控制台](https://agentteams.console.aliyun.com/)。

2. 在实例详情页左侧导航栏，点击**仪表盘**。

## 监控指标说明
仪表盘从**Worker 统计** 、**任务与团队** 和**模型调用**三个维度展示监控数据，帮助全面掌握实例运行情况。

### Worker 统计

展示当前实例下所有 Worker 的运行状态和统计数据。

#### 概览

<table> <thead> <tr> <td> <p><b>字段</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>Worker 总数</b></p> </td> <td> <p>展示实例下 Worker 的总数</p> </td> </tr> </tbody> </table>

#### **Worker 详情**

<table> <thead> <tr> <td> <p><b>字段</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>名称</b></p> </td> <td> <p>Worker 名称</p> </td> </tr> <tr> <td> <p><b>模型</b></p> </td> <td> <p>Worker 调用的模型</p> </td> </tr> <tr> <td> <p><b>状态</b></p> </td> <td> <p>Worker 状态</p> </td> </tr> <tr> <td> <p><b>任务数量</b></p> </td> <td> <p>Worker 执行任务数量</p> </td> </tr> <tr> <td> <p><b>Token 用量</b></p> </td> <td> <p>Worker Token 用量</p> </td> </tr> <tr> <td> <p><b>LLM 调用次数</b></p> </td> <td> <p>Worker 调用模型次数</p> </td> </tr> </tbody> </table>

### 任务与团队

展示当前实例下所有 Worker 团队的运行状态和统计数据。

#### 概览

<table> <thead> <tr> <td> <p><b>字段</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>总任务数</b></p> </td> <td> <p>展示实例下任务的总数</p> </td> </tr> <tr> <td> <p><b>任务平均耗时</b></p> </td> <td> <p>展示实例下任务的平均耗时</p> </td> </tr> <tr> <td> <p><b>任务平均 Token</b></p> </td> <td> <p>展示实例下任务的平均 Token</p> </td> </tr> </tbody> </table>

#### **任务状态分布**

<table> <thead> <tr> <td> <p><b>字段</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><span><b>Completed</b></span></p> </td> <td> <p>展示实例下已完成的任务数</p> </td> </tr> <tr> <td> <p><span><b>InProgress</b></span></p> </td> <td> <p>展示实例下进行中的任务数</p> </td> </tr> </tbody> </table>

#### **团队详情**

<table> <thead> <tr> <td> <p><b>字段</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>团队</b></p> </td> <td> <p>Worker 团队的名称</p> </td> </tr> <tr> <td> <p><b>Worker 数</b></p> </td> <td> <p>Worker 团队中 Worker 的数量</p> </td> </tr> <tr> <td> <p><b>任务数量</b></p> </td> <td> <p>Worker 团队的任务数量</p> </td> </tr> <tr> <td> <p><b>Token 用量</b></p> </td> <td> <p>Worker 团队的 Token 用量</p> </td> </tr> </tbody> </table>

#### **工具调用分布**

展示工具的**总调用数**和分布情况。

### 模型调用

展示当前实例下模型调用的统计数据。

#### 概览

<table> <thead> <tr> <td> <p><b>字段</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>今日调用次数</b></p> </td> <td> <p>展示今日模型调用的次数，以及较昨日的变动情况</p> </td> </tr> <tr> <td> <p><b>近七天调用次数</b></p> </td> <td> <p>展示近七天模型调用的次数，以及较上周的变动情况</p> </td> </tr> <tr> <td> <p><b>调用频率</b></p> </td> <td> <p>展示每分钟模型调用的平均次数</p> </td> </tr> </tbody> </table>

#### **模型分布**

展示模型调用的分布情况。

#### **Token 总调用量**

展示 Token 总调用量随时间的变化趋势。

#### **Token 调用（按模型统计）**

展示不同模型的 Token 调用量随时间的变化趋势。

## 筛选与分析数据
仪表盘支持按时间范围筛选数据，便于对比不同时段的运行情况。

* **时间范围筛选** ：在面板顶部**仪表盘**区域，选择时间范围，查看指定时段内的监控数据。

* **刷新数据**：点击顶部刷新按钮，获取最新统计数据。