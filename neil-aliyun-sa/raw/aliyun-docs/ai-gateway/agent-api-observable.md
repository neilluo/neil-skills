---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/agent-api-observable
fetch_date: 2026-09-21
product: AI Gateway
slug: agent-api-observable
body_sha256: 1f35979c8026d4834b23d9997c15fb4b9e28a3fe15a6765531409495bea85248
body_bytes: 978
migration_status: current
---

AI网关提供Agent API可观测能力，可在AI网关控制台的统计模块中，查看Agent API相关的请求和响应信息，便于日志的监控、记录和分析。  

## 操作步骤
1. 在AI网关控制台的[实例](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)页面，在顶部菜单栏选择目标实例所在地域。

2. 在**实例** 页面，单击目标**网关实例ID**。

3. 在左侧导航栏单击**Agent API** ，单击目标**API名称**。

4. 选择**统计** 页签，可查看**apig-agent-api-dashboard**，Agent API观测的关键指标包括：

   **说明**

   如果尚未开启网关日志投递功能，单击**立即开通日志投递功能**。选择合适的日志服务Project开启日志投递功能。开启后可在网关中使用日志服务SLS进行日志的采集、分析与展示。
   * **QPS**：每秒Agent API请求和响应的数量统计。

   * **请求成功率**：Agent API请求的成功率。

   *