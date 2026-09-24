---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/mcp-observable
fetch_date: 2026-09-21
product: AI Gateway
slug: mcp-observable
body_sha256: dca042103a73a396391d144a9fbd736d80646b40ea0010ae0e2635933a4f7cd9
body_bytes: 1438
migration_status: current
---

AI网关提供MCP可观测基础能力，您可在AI网关控制台的统计和日志模块中，查看MCP请求和响应信息，便于日志的监控、记录和分析。  

## 操作步骤
1. 在AI 网关控制台的[实例](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)页面，在顶部菜单栏选择目标实例所在地域。

2. 在**实例**页面，单击目标网关实例ID。

3. 在左侧导航栏单击**MCP 管理** ，然后单击目标**MCP 服务** ，进入目标**MCP服务**详情页面。

4. 单击**统计** 页签，您可查看**apig-mcp-server-dashboard**，MCP 观测的关键指标包括：

   > 如果您还未 [开启MCP服务日志投递](https://help.aliyun.com/document_detail/2929771.html)，您需单击 **立即开通日志投递功能**。开启后您可在网关中使用日志服务 SLS 进行日志的采集、分析与展示。
   * **QPS**：每秒 MCP 请求和响应的数量统计。

   * **请求成功率**：即 MCP 请求的成功率，可按秒、15 秒、分钟进行统计。

   * **请求平均RT/ms**：一段时间内（秒、15 秒、分钟） MCP 请求的平均响应时间（ms）。

   * **MCP tool 请求分布** ：一段时间内不同**MCP tool**的请求分布

5. 单击**日志** 页签，您可以通过SQL对查询结果进行统计分析。更多详情，请参见[查询与分析快速指引](https://help.aliyun.com/document_detail/90762.html)。