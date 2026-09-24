---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/create-a-gateway-instance
fetch_date: 2026-09-21
product: AI Gateway
slug: create-a-gateway-instance
body_sha256: 7ccd2971a5fd1695e2d9cdee8d559fb240af7b08ed71774b34843c5538e63850
body_bytes: 14377
migration_status: current
---

本文介绍如何创建AI 网关实例。  

## 操作步骤
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 单击**创建实例** ，在AI网关购买页面中选择相关配置，然后单击**立即购买**。

   <table> <thead> <tr> <td> <p><b>配置项</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>商品类型</b></p> </td> <td> <p>支持<b>专享实例（按量付费）</b>、<b>专享实例（包年包月）</b>与<b>Serverless（按量付费）</b>，关于三种类型的计费方式请参考<a href="https://help.aliyun.com/document_detail/2881286.html">专享实例计费说明</a>。</p> </td> </tr> <tr> <td> <p><b>地域</b></p> </td> <td> <p>选择网关的<a href="https://help.aliyun.com/document_detail/2883382.html">地域</a>。</p> <div> <div> <i></i> </div> <div> <strong>重要 </strong> <p>资源创建成功后，不能更换地域。</p> </div> </div> </td> </tr> <tr> <td> <p><b>网关名称</b></p> </td> <td> <p>自定义设置网关的名称。推荐用环境或环境加业务领域命名，例如test、order-prod等，最大长度为64个字符。</p> </td> </tr> <tr> <td> <p><b>网关规格</b></p> </td> <td> <p>根据实际需求选择节点规格，不同网关规格下的容量规格请参考<a href="https://help.aliyun.com/document_detail/2922542.html">网关类型</a>。Serverless版本无网关规格。</p> </td> </tr> <tr> <td> <p><b>资源组</b></p> </td> <td> <p>支持默认资源组或已有资源组。如需创建新的资源组，单击<b>创建资源组</b>。</p> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <p>使用资源组对云账号下的资源做分类分组管理，以组为单元进行权限管理、资源部署、资源监控等，而无需单独处理各个资源。</p> </div> </div> </td> </tr> <tr> <td> <p><b>网络访问类型</b></p> </td> <td> <p>支持<b>公网</b>、<b>私网</b>、<b>公网+私网</b>三种访问类型。</p> <ul> <li> <p>公网：公网访问网关时，将会产生相应的公网流量费用，公网流量将基于云数据传输CDT进行统一计费和出账，采用BGP（多线）模式，详情可参考\&nbsp;<a href="https://help.aliyun.com/document_detail/410942.html">公网流量</a>。</p> </li> <li> <p>私网：私网无流量费用。</p> </li> <li> <p>公网+私网：</p> <p>公网访问网关时，将会产生相应的公网流量费用，公网流量将基于云数据传输CDT进行统一计费和出账，采用BGP（多线）模式。访问私网无流量费用。</p> </li> </ul> </td> </tr> <tr> <td> <p><b>专有网络</b></p> </td> <td> <p>选择网关实例运行所在的专有网络环境。如需创建新的专有网络，请前往<a href="https://vpc.console.aliyun.com/vpc/%7B\&amp;regionId%7D/vpcs?spm=5176.29272261.commonbuy2container.11.1e77778bWLg4Fw">专有网络管理控制台</a>完成创建。</p> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <ul> <li> <p>网关所在的VPC与服务所在的VPC需保持一致。</p> </li> <li> <p>在选择VPC时，会显示是否存在容器或Nacos集群，避免误选VPC。</p> </li> </ul> </div> </div> </td> </tr> <tr> <td> <p><b>可用区选择</b></p> </td> <td> <section> <p>选择<b>自动分配</b>或<b>手动选择</b>。</p> <ul> <li> <p><b>自动分配</b>：选择一个交换机，系统会自动分配2个可用区部署网关节点。</p> </li> <li> <p><b>手动选择</b>：手动选择部署网关节点的可用区和交换机。</p> </li> </ul> </section> </td> </tr> <tr> <td> <p><b>交换机</b></p> </td> <td> <p>选择网关实例运行的交换机。如需创建新的交换机，您可以前往<a href="https://vpc.console.aliyun.com/vpc/%7B\&amp;regionId%7D/vpcs?spm=5176.29272261.commonbuy2container.11.1e77778bWLg4Fw">专有网络管理控制台</a>创建。</p> </td> </tr> <tr> <td> <p><b>日志服务</b></p> </td> <td> <p>选中<b>使用日志服务（SLS）</b>，开通日志服务SLS并开启网关日志投递功能，提供日志分析和仪表盘。相关内容，请参见<a href="https://help.aliyun.com/document_detail/2796809.html">开启网关日志投递</a>。</p> </td> </tr> <tr> <td> <p><b>服务关联角色</b></p> </td> <td> <p>已自动创建。允许AI网关访问其他云产品等服务。</p> </td> </tr> </tbody> </table>
4. 在**确认订单** 页面中，检查AI网关配置详情后，单击**立即购买**。

   **说明**

   网关实例创建过程预计需要1～5分钟时间。
5. 返回AI网关**实例** 页面，查看已创建的网关信息无误且**运行状态** 为**运行中**，表示网关创建成功。

## 高级功能
在创建网关实例时，如需利用日志数据进行监控和分析，或需要对请求响应进行压缩，降低网关流量时，请参考如下操作进行配置。其中开启Gzip硬件加速只能在创建网关实例时进行开启，不支持创建后开启，日志服务无限制。

### 开启Gzip硬件加速

Gzip硬件加速是指通过专用硬件设备来实现数据的快速压缩和解压缩技术。通过将Gzip格式的解压缩任务从CPU卸载到专用硬件设备上，显著提升处理效率并降低CPU负载。  
**说明**

Serverless版不支持Gzip硬件加速。

#### **操作步骤**

1. 在AI网关购买页面，完成创建网关实例的同时，需要进行如下配置完成后单击**立即购买**：

   * **地域** ：Gzip硬件加速支持的地域为**杭州、北京、上海、深圳、乌兰察布、中国香港和新加坡**。

     > 目前在支持的地域中，存在部分可用区不支持的情况，具体以产品购买页为准。
   * **网关规格** ：选择**aigw.medium.x1**以上规格。

   * **Gzip硬件加速**：勾选启用Gzip硬件加速。

   * **可用区** ：勾选**支持Gzip硬件加速**的可用区，并选择交换机。

2. 实例创建成功后，单击目标实例名称ID/名称，单击左侧导航栏的**参数配置** ，在**网关引擎参数** 区域编辑**EnableGzipHardwareAccelerate**参数。

   **说明**

   若在购买时未勾选**启用 Gzip 硬件加速**，则无法开启此配置。
3. 开启后，需要客户端能够处理Gzip压缩的数据，对于支持的客户端需要在请求头中添加`Accept-Encoding: gzip`。

#### **性能参考**

##### **开启Gzip压缩后，与开启前相比能节省多少流量？**

在使用 Gzip 进行压缩时，压缩比（即压缩后数据大小与压缩前数据大小的比值）很大程度上受到数据本身的影响。压缩比越低，代表压缩的效果越好，压缩比越高，代表压缩的效果越差。

通常来说：如果数据中存在大量重复模式或结构（如文本中的字母、单词和标点），Gzip 压缩效果会更好，压缩比更低。相反，对于随机性高、熵值大的数据（如图片、视频、已压缩文件等），由于其内部重复性较低，压缩比通常较高，压缩效果有限。

不同的客户由于其业务属性不同，在使用Gzip压缩时的压缩比也有较大差异。根据核心地域内已启用 Gzip 的实例统计，大部分实例的压缩比集中在 10% 到 50% 之间，意味着开启 Gzip 后，这些用户平均可节省 50% 以上的流量。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2542502571/p983591.png)

##### **已经开启Gzip的情况下，使用硬件加速可以节省多少实例资源？**

开启Gzip硬件加速后，网关将使用专用的硬件设备进行压缩，从而可以节省CPU资源。下面的压测数据对比了在承接相同QPS的流量的情况下，开启Gzip硬件加速的单节点实例，和使用软件Gzip的4节点实例之间的CPU消耗。

例如，压缩的数据是一份大小约为120k的JSON文本：
<table> <thead> <tr> <td> <p>QPS</p> </td> <td> <p>硬件加速gzip/aigw.medium.x1/单节点 CPU消耗</p> </td> <td> <p>软件gzip/aigw.medium.x1/4节点 CPU消耗</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>2000</p> </td> <td> <p>9%</p> </td> <td> <p>11%</p> </td> </tr> <tr> <td> <p>5000</p> </td> <td> <p>26%</p> </td> <td> <p>28%</p> </td> </tr> <tr> <td> <p>10000</p> </td> <td> <p>56%</p> </td> <td> <p>56%</p> </td> </tr> <tr> <td> <p>13000</p> </td> <td> <p>69%</p> </td> <td> <p>72%</p> </td> </tr> </tbody> </table>

从表格数据中可以看到，`开启Gzip硬件加速/单节点`的CPU消耗与`软件Gzip/4节点`的CPU消耗基本上持平。相当于原本需要4个节点才能承载，开启Gzip硬件加速后仅需要1个节点，可以节省大约75%的实例资源。

### 开启网关日志投递

如果需要收集、存储和分析网关运行日志，可以在创建网关实例时开通日志服务（SLS）进行日志分析和大盘监控。

在完成创建网关实例的同时，勾选**使用日志服务（SLS）**，系统将开通日志服务（SLS）并开启网关日志投递功能。

开启日志投递以后，可前往**观测分析** \>**日志中心**查看网关日志。  
**日志字段说明**  
<table> <thead> <tr> <td> <p><b>字段名</b></p> </td> <td> <p><b>类型</b></p> </td> <td> <p><b>含义</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>__time__</p> </td> <td> <p>long</p> </td> <td> <p>日志产生的时间。</p> </td> </tr> <tr> <td> <p>cluster_id</p> </td> <td> <p>string</p> </td> <td> <p>购买的网关实例。</p> </td> </tr> <tr> <td> <p>ai_log</p> </td> <td> <p>json</p> </td> <td> <p>针对Model API/Agent API/MCP API设计的日志字段，字段格式为json。其他类型的API此字段为空。</p> <ul> <li> <p>api: ai api的名称。</p> </li> <li> <p>cache_status: Model API中开启内容缓存时该字段会反映请求是否命中缓存。</p> </li> <li> <p>consumer: 开启消费者鉴权后，此字段会记录当前请求的消费者身份。</p> </li> <li> <p>fallback_from: Model API中开启fallback策略时，此字段记录请求从哪一条路由fallback过来。</p> </li> <li> <p>input_token: LLM请求输入token数。</p> </li> <li> <p>llm_first_token_duration: LLM请求首包RT。</p> </li> <li> <p>llm_service_duration: LLM请求整体RT。</p> </li> <li> <p>model: LLM请求的模型名称。</p> </li> <li> <p>output_token: LLM请求输出token数。</p> </li> <li> <p>response_type: LLM请求流式/非流式。</p> </li> <li> <p>safechack_status: LLM请求内容安全检测状态。</p> </li> <li> <p>token_ratelimit_status: LLM请求是否被限流拦截。</p> </li> </ul> </td> </tr> <tr> <td> <p>authority</p> </td> <td> <p>string</p> </td> <td> <p>请求报文中的Host Header。</p> </td> </tr> <tr> <td> <p>bytes_received</p> </td> <td> <p>long</p> </td> <td> <p>请求的Body大小（不包含Header）。</p> </td> </tr> <tr> <td> <p>bytes_sent</p> </td> <td> <p>long</p> </td> <td> <p>响应的Body大小（不包含Header）。</p> </td> </tr> <tr> <td> <p>downstream_local_address</p> </td> <td> <p>string</p> </td> <td> <p>网关Pod地址。</p> </td> </tr> <tr> <td> <p>downstream_remote_address</p> </td> <td> <p>string</p> </td> <td> <p>连接到网关的Client端地址。</p> </td> </tr> <tr> <td> <p>duration</p> </td> <td> <p>long</p> </td> <td> <p>请求的整体耗时。包含从网关收到来自下游的第一个字节开始，到发送出最后一个响应字节为止的时间段。单位毫秒。</p> </td> </tr> <tr> <td> <p>method</p> </td> <td> <p>string</p> </td> <td> <p>HTTP方法。</p> </td> </tr> <tr> <td> <p>path</p> </td> <td> <p>string</p> </td> <td> <p>HTTP请求中的Path。</p> </td> </tr> <tr> <td> <p>protocol</p> </td> <td> <p>string</p> </td> <td> <p>HTTP的协议版本。</p> </td> </tr> <tr> <td> <p>request_duration</p> </td> <td> <p>long</p> </td> <td> <p>从网关收到来自下游的第一个字节开始，到收到来自下游的最后一个字节为止的时间段。单位毫秒。</p> </td> </tr> <tr> <td> <p>request_id</p> </td> <td> <p>string</p> </td> <td> <p>网关会为每次请求产生一个ID，并放在Header的<span><code>x-request-id</code></span>中，后端可以根据这个字段记录并进行排查。</p> </td> </tr> <tr> <td> <p>requested_server_name</p> </td> <td> <p>string</p> </td> <td> <p>SSL连接时使用的Server Name。</p> </td> </tr> <tr> <td> <p>response_code_details</p> </td> <td> <p>string</p> </td> <td> <p>提供与响应码相关的额外信息。例如via_upstream表示响应码是由后端服务返回的，route_not_found表示请求没有匹配的路由。</p> </td> </tr> <tr> <td> <p>response_tx_duration</p> </td> <td> <p>long</p> </td> <td> <p>从网关收到来自上游的第一个字节开始，到给下游发送出最后一个字节为止的时间段。单位毫秒。</p> </td> </tr> <tr> <td> <p>route_name</p> </td> <td> <p>string</p> </td> <td> <p>路由名。</p> </td> </tr> <tr> <td> <p>start_time</p> </td> <td> <p>string</p> </td> <td> <p>请求开始时间。格式：UTC。</p> </td> </tr> <tr> <td> <p>trace_id</p> </td> <td> <p>string</p> </td> <td> <p>Trace ID。</p> </td> </tr> <tr> <td> <p>upstream_cluster</p> </td> <td> <p>string</p> </td> <td> <p>上游集群。</p> </td> </tr> <tr> <td> <p>upstream_host</p> </td> <td> <p>string</p> </td> <td> <p>上游IP。</p> </td> </tr> <tr> <td> <p>upstream_local_address</p> </td> <td> <p>string</p> </td> <td> <p>本地连接上游的地址。</p> </td> </tr> <tr> <td> <p>upstream_service_time</p> </td> <td> <p>long</p> </td> <td> <p>上游服务处理请求的耗时（毫秒），包括网关访问上游服务的网络耗时和上游服务自身处理耗时两部分。</p> </td> </tr> <tr> <td> <p>upstream_transport_failure_reason</p> </td> <td> <p>string</p> </td> <td> <p>上游链接失败的原因。</p> </td> </tr> <tr> <td> <p>user_agent</p> </td> <td> <p>string</p> </td> <td> <p>HTTP Header中的UserAgent。</p> </td> </tr> <tr> <td> <p>x_forwarded_for</p> </td> <td> <p>string</p> </td> <td> <p>HTTP Header中的<span><code>x-forwarded-for</code></span>，通常用来表示HTTP请求端真实IP。</p> </td> </tr> </tbody> </table>