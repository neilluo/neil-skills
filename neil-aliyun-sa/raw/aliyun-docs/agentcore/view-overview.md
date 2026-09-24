---
source_url: https://help.aliyun.com/zh/agentcore/view-overview
fetch_date: 2026-09-20
product: AgentCore
slug: view-overview
body_sha256: 45c499d2930a13f1c0cb991cc5ac75687f97af0deb108fddcf19d029c4cff188
body_bytes: 5010
migration_status: current   # 见 FETCH-CONTRACT §3
---

当Workspace运行一段时间后，需要了解 Agent 的运行状态。AgentCore 提供概览，实时展示 Agent 统计、团队用量分布和 Token 消耗趋势，帮助快速定位问题和优化资源配置。  

## 进入概览
1. 登录 [AgentCore](https://agentcore.console.aliyun.com/)控制台。

2. 在详情页左侧导航栏，点击**概览**。

## 指标说明
概览从**运行健康** 、**用量统计** 和**协作摘要**三个维度展示监控数据，帮助全面掌握Workspace运行情况。

### 运行健康

展示当前Workspace下所有 Agent 的运行状态和统计数据。

#### 概览

<table> <thead> <tr> <td><p><b>字段</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>Agent 总数</p></td> <td><p>展示Workspace下 Agent 的总数。</p></td> </tr> </tbody> </table>

#### Agent 状态分布

<table> <thead> <tr> <td><p><b>字段</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>运行中</b></p></td> <td><p>正常运行的Agent 个数。</p></td> </tr> <tr> <td><p><b>异常</b></p></td> <td><p>异常状态的Agent 个数。</p></td> </tr> <tr> <td><p><b>停止</b></p></td> <td><p>处于停止状态的Agent 个数。</p></td> </tr> </tbody> </table>

#### **资源摘要**

<table> <thead> <tr> <td><p><b>字段</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>模型</b></p></td> <td><p>展示 Workspace 下已配置的模型数量。</p></td> </tr> <tr> <td><p><b>工具</b></p></td> <td><p>展示 Workspace 下已创建的 MCP 工具数量。</p></td> </tr> <tr> <td><p><b>Skill</b></p></td> <td><p>展示 Workspace 下已创建的 Skill 数量。</p></td> </tr> <tr> <td><p><b>凭证</b></p></td> <td><p>展示 Workspace 下已创建的凭证数量。</p></td> </tr> </tbody> </table>

### 用量统计

展示当前Workspace下所有 Agent 团队的运行状态和统计数据。
<table> <thead> <tr> <td><p><b>字段</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>时间范围</b></p></td> <td><p>设置统计数据的时间范围，默认为当日。调整后单击刷新图标更新数据。</p></td> </tr> <tr> <td><p><b>调用次数</b></p></td> <td><p>展示所选时间范围内的调用总次数。</p></td> </tr> <tr> <td><p><b>Token 用量</b></p></td> <td><p>展示所选时间范围内消耗的 Token 总量。</p></td> </tr> <tr> <td><p><b>调用趋势</b></p></td> <td><p>以折线图展示所选时间范围内调用次数随时间的变化。</p></td> </tr> <tr> <td><p><b>Token 用量趋势</b></p></td> <td><p>以折线图展示所选时间范围内 Token 用量随时间的变化。</p></td> </tr> </tbody> </table>

### 协作摘要

展示当前Workspace下模型调用的统计数据。
<table> <thead> <tr> <td><p><b>字段</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>Team 数</b></p></td> <td><p>展示Workspace下 Team 的总数。</p></td> </tr> <tr> <td><p><b>今日会话</b></p></td> <td><p>展示Workspace下当日的会话总数。</p></td> </tr> </tbody> </table>

## 产品近期活动
<table> <thead> <tr> <td><p><b>字段</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>活动卡片</b></p></td> <td><p>突出展示最近的 3 条活动，单击卡片可跳转至活动详情页。</p></td> </tr> <tr> <td><p><b>活动名称</b></p></td> <td><p>展示活动的名称，例如创建 Agent、部署广场 Skill、开通协作空间。</p></td> </tr> <tr> <td><p><b>发生时间</b></p></td> <td><p>展示活动的发生时间，按时间倒序排列。</p></td> </tr> </tbody> </table>

可通过右下角的翻页按钮查看更多。

## AgentLoop
创建Workspace时会自动绑定AgentLoop，可以查看AgentLoop的相关信息。

## VPC
可以设置绑定VPC。点击绑定VPC后，配置：
<table> <thead> <tr> <td><p>参数</p></td> <td><p>说明</p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>绑定 VPC</p></td> <td><p>是否为 Workspace 配置私有网络资源。关闭时不展示以下参数；打开后需完成 VPC 与交换机配置。</p></td> </tr> <tr> <td><p>VPC</p></td> <td><p>必填。选择 Workspace 使用的专有网络。</p></td> </tr> <tr> <td><p>交换机</p></td> <td><p>必填。选择 VPC 后可选。</p></td> </tr> </tbody> </table>  
**说明**

需选择至少 2 个交换机，并确保覆盖至少 2 个不同可用区。

## 相关文档
* [AgentCore 产品概述](https://help.aliyun.com/document_detail/3052303.html)

* [管理 Workspace](https://help.aliyun.com/document_detail/3052311.html)

* [管理 Agent](https://help.aliyun.com/document_detail/3052293.html)

<br />