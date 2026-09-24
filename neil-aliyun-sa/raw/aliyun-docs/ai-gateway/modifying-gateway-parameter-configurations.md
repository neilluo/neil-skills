---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/modifying-gateway-parameter-configurations
fetch_date: 2026-09-21
product: AI Gateway
slug: modifying-gateway-parameter-configurations
body_sha256: ba05db2b0ad89635fa240f95a453393eb8e3208f04e24b26157d3a70cf642541
body_bytes: 6988
migration_status: current
---

为了适应不同场景的变化，您可以对AI网关进行参数调整。通过合理调整参数，可以提升网络的效能、可靠性和安全性，确保网络的稳定运行和用户体验。但是需要注意的是，修改网关参数可能会对网络连接和应用程序的使用产生影响，因此在进行此类操作之前，请了解可修改参数的取值范围及其作用。本文介绍如何修改网关参数以及参数详情。  

## 操作步骤
**说明**

* 为保证实例的稳定运行，仅支持对控制台中开放的参数进行修改，未在控制台中呈现的参数不支持修改。

* 修改网关引擎参数值时，请参考网关引擎参数页面中的取值范围。

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击目标**实例ID**。

4. 在左侧导航栏，选择**参数配置** 。在**网关引擎参数** 区域，单击目标参数**操作** 列下的**编辑** ，根据下表设置您的参数值，并单击**确认**。

   <table> <thead> <tr> <td> <p><b> 参数名称 </b></p> </td> <td> <p><b> 参数类型 </b></p> </td> <td> <p><b> 取值范围 </b></p> </td> <td> <p><b> 默认值 </b></p> </td> <td> <p><b> 参数描述 </b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>DownstreamConnectionBufferLimits</p> </td> <td> <p>int64</p> </td> <td> <p>\[0, 2147483647\]</p> </td> <td> <p>32768</p> </td> <td> <p>作用于网关连接，单条链接的buffer大小，配置后会影响吞吐和网关的内存使用, 单位byte。</p> </td> </tr> <tr> <td> <p>PathWithEscapedSlashes</p> </td> <td> <p>string</p> </td> <td> <ul> <li> <p>KEEP_UNCHANGED</p> </li> <li> <p>REJECT_REQUEST</p> </li> <li> <p>UNESCAPE_AND_REDIRECT</p> </li> <li> <p>UNESCAPE_AND_FORWARD</p> </li> </ul> </td> <td> <p>KEEP_UNCHANGED</p> </td> <td> <p>确定 URI 路径中包含 %2F、%2f、%5C 或 %5c 这些转义的请求的操作, 默认为KEEP_UNCHANGED（保持不变）。</p> </td> </tr> <tr> <td> <p>DownstreamIdleTime</p> </td> <td> <p>int32</p> </td> <td> <p>\[0, 600\]</p> </td> <td> <p>180</p> </td> <td> <p>客户端到网关处于指定的时间内\[0-600\]没有请求，则会断开链接。单位为秒。重启才会生效。</p> </td> </tr> <tr> <td> <p>EnableHardwareAccelerate</p> </td> <td> <p>bool</p> </td> <td> <p>\[true, false\]</p> </td> <td> <p>true</p> </td> <td> <p>将 TLS 证书的验证和卸载转移到硬件中执行，可大幅提高 HTTPS 请求的性能。</p> </td> </tr> <tr> <td> <p>InitialStreamWindowSize</p> </td> <td> <p>int64</p> </td> <td> <p>\[65535, 2147483647\]</p> </td> <td> <p>65535</p> </td> <td> <p>作用于请求环节，网关同客户端使用http2时协商的stream初始窗口大小。单位为byte。</p> </td> </tr> <tr> <td> <p>UpstreamIdleTimeout</p> </td> <td> <p>int32</p> </td> <td> <p>\[0, 600\]</p> </td> <td> <p>30</p> </td> <td> <p>默认到上游的idle时间。单位为秒。</p> </td> </tr> <tr> <td> <p>ZipAlgorithm</p> </td> <td> <p>array</p> </td> <td> <p>\[gzip, brotli\]</p> </td> <td> <p>gzip</p> </td> <td> <p>开启压缩后使用的算法，可以选择brotli，gzip，如果此时EnableGzip未开启，将自动开启EnableGzip选项。</p> </td> </tr> <tr> <td> <p>EnableCustomAuthConfigPush</p> </td> <td> <p>bool</p> </td> <td> <p>\[true, false\]</p> </td> <td> <p>false</p> </td> <td> <p>作用于使用自建的鉴权服务的场景，开启后鉴权规则变更不会引起连接中断，适用于WebSocket和在线业务场景。</p> </td> </tr> <tr> <td> <p>EnableProxyProtocol</p> </td> <td> <p>bool</p> </td> <td> <p>\[true, false\]</p> </td> <td> <p>true</p> </td> <td> <p>是否开启Proxy协议，如果网关入口流量使用NLB接入，如果不开启则无法获取客户端的真实IP，开启后对于非Proxy协议请求没有影响。</p> </td> </tr> <tr> <td> <p>PreserveHeaderFormat</p> </td> <td> <p>bool</p> </td> <td> <p>\[true, false\]</p> </td> <td> <p>false</p> </td> <td> <p>是否保持header头大小写, http1.1规范中 header头不区分大小写进行识别，为了保证与http2规范兼容，默认会统一转化为小写。</p> </td> </tr> <tr> <td> <p>KeepAliveHeaderTimeout</p> </td> <td> <p>int32</p> </td> <td> <p>\[0, 600\]</p> </td> <td> <p>0</p> </td> <td> <p>用于生成Keep-Alive响应头返回给客户端，告知连接的保活时间。单位为秒。例如配置为10时，会返回响应头：'keep-alive: timeout=10'。配置为0时，不会返回该响应头。</p> </td> </tr> <tr> <td> <p>EnableHttp3</p> </td> <td> <p>bool</p> </td> <td> <p>\[true, false\]</p> </td> <td> <p>false</p> </td> <td> <p>是否开启http3。</p> </td> </tr> <tr> <td> <p>AlwaysSetRequestIdInResponse</p> </td> <td> <p>bool</p> </td> <td> <p>\[true, false\]</p> </td> <td> <p>true</p> </td> <td> <p>用于控制在响应中是否始终包含请求ID。</p> </td> </tr> <tr> <td> <p>EnableGzip</p> </td> <td> <p>bool</p> </td> <td> <p>\[true, false\]</p> </td> <td> <p>false</p> </td> <td> <p>作用于请求与响应环节，启用gzip会对请求响应进行压缩，会减少网关流量，增加网关cpu消耗。</p> </td> </tr> <tr> <td> <p>InitialConnectionWindowSize</p> </td> <td> <p>int64</p> </td> <td> <p>\[65535, 2147483647\]</p> </td> <td> <p>1048576</p> </td> <td> <p>作用于请求环节，网关同客户端使用http2时连接级别初始窗口大小。单位为byte。</p> </td> </tr> <tr> <td> <p>DownstreamHttp2MaxConcurrentStream</p> </td> <td> <p>int64</p> </td> <td> <p>\[0, 2147483647\]</p> </td> <td> <p>100</p> </td> <td> <p>作用于请求环节，客户端使用http2时一条链接上最大并发数。</p> </td> </tr> <tr> <td> <p>EnableSlashMerge</p> </td> <td> <p>bool</p> </td> <td> <p>\[true, false\]</p> </td> <td> <p>false</p> </td> <td> <p>作用于请求环节，是否合并请求中多余的'/', 开启后www.a.com//b多余的'/'会被合并，将会同www.a.com/b一致。</p> </td> </tr> <tr> <td> <p>EnableGenerateRequestId</p> </td> <td> <p>bool</p> </td> <td> <p>\[true, false\]</p> </td> <td> <p>true</p> </td> <td> <p>作用于请求范围，根据配置会在请求头中生成requestId，以便追踪请求。</p> </td> </tr> <tr> <td> <p>WebsocketTermGracePeriod</p> </td> <td> <p>int32</p> </td> <td> <p>\[20, 900\]</p> </td> <td> <p>20</p> </td> <td> <p>当网关实例升级、重启等需要关闭连接的场景下，为Websocket连接维持的保活时间。单位为秒。</p> </td> </tr> <tr> <td> <p>XffTrustedNum</p> </td> <td> <p>int32</p> </td> <td> <p>\[0, 10\]</p> </td> <td> <p>0</p> </td> <td> <p>作用于请求环节，网关前可信任的代理个数，会影响网关是否会使用客户端产生的x-forwarded-for和x-request-id等请求头。</p> </td> </tr> </tbody> </table>