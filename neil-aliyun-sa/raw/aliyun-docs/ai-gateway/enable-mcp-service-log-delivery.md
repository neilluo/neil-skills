---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/enable-mcp-service-log-delivery
fetch_date: 2026-09-21
product: AI Gateway
slug: enable-mcp-service-log-delivery
body_sha256: 696f2e3177256a30d7f5d51fe453477ec100d9313f0fa6a0fc532f8b31477468
body_bytes: 9425
migration_status: current
---

日志投递功能是AI 网关结合阿里云日志服务SLS提供的服务。开启日志投递后，您可以通过分析AI 网关的访问日志了解用户行为和地域分布，以便排查问题。本文介绍如何为MCP服务开启日志投递。  

## 开启日志投递
**说明**

* AI产品不收取日志费用，但日志服务SLS将根据您的使用量收费。关于SLS的计费方式，请参见[按使用功能计费](https://help.aliyun.com/document_detail/48220.html)。

* 日志投递的开启状态是网关实例级别的。

1. 在AI 网关控制台的[实例](https://apigw.console.aliyun.com/?/cn-hangzhou/consumer-manage#/cn-hangzhou/ai-gateway)页面，选择您实例所在的地域。

2. 进入目标实例页面，选择左侧导航栏的**MCP管理**。

3. 单击目标服务卡片，然后单击**日志**页签。

4. MCP服务提供了**网关请求日志** 和**MCP服务日志**两种查询分析日志的功能。

   > MCP服务日志仅支持带有 `HTTP转MCP`标签可以查询分析日志。
   > **网关请求日志** 和 **MCP服务日志**如果都使用默认开启日志投递服务，日志服务创建的Project是同一个，只是Logstore不同。
   * **网关请求日志：**支持两种方式开启网关日志投递动能。

     * 方式一：在创建实例时，选择使用日志服务（SLS）。

     * 方式二：单击**立即开启日志投递功能** ，在**开启日志投递功能** 对话框，您可以选择**使用默认** 日志服务Project，日志服务会为您创建一个默认的日志服务Project。您也可以选择**使用已有** 的日志服务Project，然后单击**确定**。

   * **MCP服务日志：** 单击**立即开启日志投递功能** ，在**开启日志投递功能** 对话框，您可以选择**使用默认** 日志服务Project，日志服务会为您创建一个默认的日志服务Project。您也可以选择**使用已有** 的日志服务Project，然后单击**确定**。

5. 单击**网关请求日志常用查询条件** 或**MCP服务日志常用查询条件** 后的**查看** 按钮，展开常用查询语句。您可复制并粘贴查询语句到日志服务的搜索栏查询相关内容，关于更多查询与分析的信息，请参见[查询与分析快速指引](https://help.aliyun.com/document_detail/90762.html#task-tqc-ddm-gfb)。

   **日志字段说明**  
   <table> <thead> <tr> <td> <p><b>字段名</b></p> </td> <td> <p><b>类型</b></p> </td> <td> <p><b>含义</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>__time__</p> </td> <td> <p>long</p> </td> <td> <p>日志产生的时间。</p> </td> </tr> <tr> <td> <p>cluster_id</p> </td> <td> <p>string</p> </td> <td> <p>购买的网关实例。</p> </td> </tr> <tr> <td> <p>ai_log</p> </td> <td> <p>json</p> </td> <td> <p>针对Model API/Agent API/MCP API设计的日志字段，字段格式为json。其他类型的API此字段为空。</p> <ul> <li> <p>api: ai api的名称。</p> </li> <li> <p>cache_status: Model API中开启内容缓存时该字段会反映请求是否命中缓存。</p> </li> <li> <p>consumer: 开启消费者鉴权后，此字段会记录当前请求的消费者身份。</p> </li> <li> <p>fallback_from: Model API中开启fallback策略时，此字段记录请求从哪一条路由fallback过来。</p> </li> <li> <p>input_token: LLM请求输入token数。</p> </li> <li> <p>llm_first_token_duration: LLM请求首包RT。</p> </li> <li> <p>llm_service_duration: LLM请求整体RT。</p> </li> <li> <p>model: LLM请求的模型名称。</p> </li> <li> <p>output_token: LLM请求输出token数。</p> </li> <li> <p>response_type: LLM请求流式/非流式。</p> </li> <li> <p>safechack_status: LLM请求内容安全检测状态。</p> </li> <li> <p>token_ratelimit_status: LLM请求是否被限流拦截。</p> </li> </ul> </td> </tr> <tr> <td> <p>authority</p> </td> <td> <p>string</p> </td> <td> <p>请求报文中的Host Header。</p> </td> </tr> <tr> <td> <p>bytes_received</p> </td> <td> <p>long</p> </td> <td> <p>请求的Body大小（不包含Header）。</p> </td> </tr> <tr> <td> <p>bytes_sent</p> </td> <td> <p>long</p> </td> <td> <p>响应的Body大小（不包含Header）。</p> </td> </tr> <tr> <td> <p>downstream_local_address</p> </td> <td> <p>string</p> </td> <td> <p>网关Pod地址。</p> </td> </tr> <tr> <td> <p>downstream_remote_address</p> </td> <td> <p>string</p> </td> <td> <p>连接到网关的Client端地址。</p> </td> </tr> <tr> <td> <p>duration</p> </td> <td> <p>long</p> </td> <td> <p>请求的整体耗时。包含从网关收到来自下游的第一个字节开始，到发送出最后一个响应字节为止的时间段。单位毫秒。</p> </td> </tr> <tr> <td> <p>method</p> </td> <td> <p>string</p> </td> <td> <p>HTTP方法。</p> </td> </tr> <tr> <td> <p>path</p> </td> <td> <p>string</p> </td> <td> <p>HTTP请求中的Path。</p> </td> </tr> <tr> <td> <p>protocol</p> </td> <td> <p>string</p> </td> <td> <p>HTTP的协议版本。</p> </td> </tr> <tr> <td> <p>request_duration</p> </td> <td> <p>long</p> </td> <td> <p>从网关收到来自下游的第一个字节开始，到收到来自下游的最后一个字节为止的时间段。单位毫秒。</p> </td> </tr> <tr> <td> <p>request_id</p> </td> <td> <p>string</p> </td> <td> <p>网关会为每次请求产生一个ID，并放在Header的<span><code>x-request-id</code></span>中，后端可以根据这个字段记录并进行排查。</p> </td> </tr> <tr> <td> <p>requested_server_name</p> </td> <td> <p>string</p> </td> <td> <p>SSL连接时使用的Server Name。</p> </td> </tr> <tr> <td> <p>response_code_details</p> </td> <td> <p>string</p> </td> <td> <p>提供与响应码相关的额外信息。例如via_upstream表示响应码是由后端服务返回的，route_not_found表示请求没有匹配的路由。</p> </td> </tr> <tr> <td> <p>response_tx_duration</p> </td> <td> <p>long</p> </td> <td> <p>从网关收到来自上游的第一个字节开始，到给下游发送出最后一个字节为止的时间段。单位毫秒。</p> </td> </tr> <tr> <td> <p>route_name</p> </td> <td> <p>string</p> </td> <td> <p>路由名。</p> </td> </tr> <tr> <td> <p>start_time</p> </td> <td> <p>string</p> </td> <td> <p>请求开始时间。格式：UTC。</p> </td> </tr> <tr> <td> <p>trace_id</p> </td> <td> <p>string</p> </td> <td> <p>Trace ID。</p> </td> </tr> <tr> <td> <p>upstream_cluster</p> </td> <td> <p>string</p> </td> <td> <p>上游集群。</p> </td> </tr> <tr> <td> <p>upstream_host</p> </td> <td> <p>string</p> </td> <td> <p>上游IP。</p> </td> </tr> <tr> <td> <p>upstream_local_address</p> </td> <td> <p>string</p> </td> <td> <p>本地连接上游的地址。</p> </td> </tr> <tr> <td> <p>upstream_service_time</p> </td> <td> <p>long</p> </td> <td> <p>上游服务处理请求的耗时（毫秒），包括网关访问上游服务的网络耗时和上游服务自身处理耗时两部分。</p> </td> </tr> <tr> <td> <p>upstream_transport_failure_reason</p> </td> <td> <p>string</p> </td> <td> <p>上游链接失败的原因。</p> </td> </tr> <tr> <td> <p>user_agent</p> </td> <td> <p>string</p> </td> <td> <p>HTTP Header中的UserAgent。</p> </td> </tr> <tr> <td> <p>x_forwarded_for</p> </td> <td> <p>string</p> </td> <td> <p>HTTP Header中的<span><code>x-forwarded-for</code></span>，通常用来表示HTTP请求端真实IP。</p> </td> </tr> </tbody> </table>

## 请求失败原因说明
请求失败的原因主要通过日志中`Response_Flag`的值判断。以下是关于`Response_Flag`不同值的说明。  
**说明**

下游指客户端，上游指后端服务。

* UH：上游集群中，没有健康的上游主机。

* UF：上游连接失败。

* NR：给定请求未配置路由。

* URX：请求被拒绝，因为达到了上游重试限制（HTTP）或最大连接尝试次数（TCP）。

* NC：无法找到上游集群。日志中出现 `cluster_not_found` 时，按以下步骤排查：

  1. 确认路由关联的 AI 服务中，模型提供商及后端服务地址配置正确且可用。

  2. 确认 AI 服务已绑定到网关实例，且后端服务的健康检查状态正常。

  3. 确认网关所在 VPC 的网络可访问后端服务地址。若后端服务为公网域名，需在该 VPC 中配置 NAT 网关和 SNAT 条目，否则网关无法访问公网地址。

  4. 确认上述配置变更已发布并生效。

* DT：请求或连接超过了`max_connection_duration`或`max_downstream_connection_duration`。

* DC：下游连接终止。

* LH：本地服务未通过健康检查请求。

* UT：上游请求超时。

* LR：连接本地重置。

* UR：上游远程重置。

* UC：上游连接终止。

* DI：请求处理被延迟一段时间，该延迟时间由故障注入指定。

* FI：请求被故障注入指定的响应码中止。

* RL：请求在本地被HTTP速率限制过滤器限制，除了429响应码之外。

* UAEX：请求被外部授权服务拒绝。

* RLSE：请求被拒绝，因为速率限制服务出现错误。

* IH：请求被拒绝，因为在严格检查的标头中设置了无效值。

* SI：Stream流空闲超时。

* DPE：下游请求存在HTTP协议错误。

* UPE：上游响应存在HTTP协议错误。

* UMSDR：上游请求达到了最大流程持续时间。

* OM：超负荷管理器终止了请求。