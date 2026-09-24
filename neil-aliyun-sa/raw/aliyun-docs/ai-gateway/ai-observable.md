---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/ai-observable
fetch_date: 2026-09-21
product: AI Gateway
slug: ai-observable
body_sha256: 00b748cc15f56928b06c21d92247a93938902f32a8665cdd60385829b28ab52b
body_bytes: 2572
migration_status: current
---

提供AI 可观测基础能力，您可在AI 网关控制台的统计和日志模块中，查看AI 请求和响应信息，便于日志的监控、记录和分析。  
**说明**

[限流](https://help.aliyun.com/document_detail/2873941.html)、[缓存](https://help.aliyun.com/document_detail/2873942.html)、[联网搜索](https://help.aliyun.com/document_detail/2873944.html)策略在处理异常时会透出异常日志，并提供完整策略日志的查看能力。

## **操作步骤**
1. 打开[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)**实例** 页面，在顶部菜单栏选择目标实例所在地域，并单击目标**实例ID**。

2. 在左侧导航栏，单击**Model API** ，然后单击目标**API名称** 进入**API详情**页面。

3. 单击**统计** 页签，您可查看`apig-ai-api-dashboard`，AI 可观测的关键指标包括：

   **重要**

   AI 网关中使用日志服务 SLS 进行日志的采集、分析与展示。如果您还未[开启网关日志投递](https://help.aliyun.com/document_detail/2882057.html)，请单击**立即开通日志投递**功能进行配置。
   * **QPS**：每秒 AI 请求和响应的数量统计，分为 AI 请求的 QPS、流式响应的 QPS 和非流式响应的 QPS。

   * **请求成功率**：即 AI 请求的成功率，可按秒、15 秒、分钟进行统计。

   * **token消耗数/s**：每秒消耗的 token 数量，分为输入 token、输出 token 和总计 token。

   * **请求平均RT/ms**：一段时间内（秒、15 秒、分钟） AI 请求的平均响应时间（ms），分为非流式 RT、流式 RT（流式响应的整体时间）、流式首包 RT（流式响应的首包时间）。

   * **缓存命中情况/s**：一段时间内缓存的命中数和 miss 数统计。

   * **限流请求数/s**：一段时间内被限流的请求和正常请求的统计。

   * **模型token使用统计**：一段时间内不同模型的 token 消耗统计。

   * **消费者token使用统计**：一段时间内不同消费者的 token 消耗统计。

   * **风险类型统计**：被内容安全检测出来的风险，按照风险类型、消费者等维度的统计。

   * **风险消费者统计**：被消费者鉴权检测出来的消费者风险统计。

   * **限流消费者统计**：被限流检测出来的消费者风险。

4. 单击**日志** 页签，您可以通过SQL对查询结果进行统计分析。更多详情，请参见[查询与分析快速指引](https://help.aliyun.com/document_detail/90762.html)。