---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/more-policies-and-plugins
fetch_date: 2026-09-21
product: AI Gateway
slug: more-policies-and-plugins
body_sha256: 2de86ee097ea34ed98ed4192430d7e0fbec44e762984ba19323e9891be07a91b
body_bytes: 16275
migration_status: current
---

AI 网关支持对API级进行添加策略和配置插件，提高API的安全性、性能和可维护性。  
**重要**

策略配置修改后即时生效，无需重新发布。

## 操作步骤
1. 打开[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)**实例** 页面，在顶部菜单栏选择目标实例所在地域，并单击目标**实例ID**。

2. 在左侧导航栏，单击**Model API** ，然后单击目标**API名称** 进入**API详情**页面。

3. 单击**策略与插件** 页签，然后在**更多策略与插件** 区域，选择需要配置策略或插件的位置（**入站处理** /**出站处理** ），并单击**启用策略/插件**。

4. 在**启用策略/插件** 面板中，选择策略或插件进行配置。详情请参见[策略配置](#d3f6d3bf2cl8h)和[插件配置](#345f058fc8px5)。

## 策略配置
### 并发控制

并发规则的原理是统计当前网关处理中的请求数之和，当指标达到设定的阈值时立即拦截流量，可配置为后端服务的最大并发处理请求数，实现在高并发下的后端服务可用性保护。  
**操作步骤**  
可在**添加策略** 页签，单击**并发控制** 卡片，在**添加策略**面板配置相关参数。
<table> <thead> <tr> <td> <p><b>配置项</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>是否开启</b></p> </td> <td> <p>开启后，并发规则生效。</p> </td> </tr> <tr> <td> <p><b>总体并发数阈值</b></p> </td> <td> <p>设置<b>总体并发数阈值</b>。</p> </td> </tr> <tr> <td> <p><b>Web fallback 行为</b></p> </td> <td> <p><b>返回指定内容</b></p> </td> <td> <p><b>Http状态码</b></p> </td> <td> <p>设置<b>Http状态码</b>。默认为429。</p> </td> </tr> <tr> <td> <p><b>返回 content-type</b></p> </td> <td> <p>选择<b>返回 content-type</b>为<b>普通文本</b>或<b>JSON</b>。</p> </td> </tr> <tr> <td> <p><b>HTTP 返回文本</b></p> </td> <td> <p>输入返回文本。</p> </td> </tr> <tr> <td> <p><b>返回指定内容</b></p> </td> <td> <p><b>跳转地址</b></p> </td> <td> <p>输入<b>跳转地址</b>。</p> </td> </tr> </tbody> </table>

### 流量控制

流控规则的原理是监控API的QPS指标，当指标达到设定的阈值时立即拦截流量，避免后端服务被瞬时的流量高峰冲垮，从而保障高可用性。  
**操作步骤**  
可在**添加策略** 页签，单击**流量控制** 卡片，在**添加策略**面板配置相关参数。
<table> <thead> <tr> <td> <p><b>配置项</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>是否开启</b></p> </td> <td> <p>开启后，流量控制规则生效。</p> </td> </tr> <tr> <td> <p><b>总体QPS阈值</b></p> </td> <td> <p>设置<b>总体QPS阈值</b>。</p> </td> </tr> <tr> <td> <p><b>Web fallback 行为</b></p> </td> <td> <p><b>返回指定内容</b></p> </td> <td> <p><b>Http状态码</b></p> </td> <td> <p>设置<b>Http状态码</b>。默认为429。</p> </td> </tr> <tr> <td> <p><b>返回 content-type</b></p> </td> <td> <p>选择<b>返回 content-type</b>为<b>普通文本</b>或<b>JSON</b>。</p> </td> </tr> <tr> <td> <p><b>HTTP 返回文本</b></p> </td> <td> <p>输入返回文本。</p> </td> </tr> <tr> <td> <p><b>跳转到指定页面</b></p> </td> <td> <p><b>跳转地址</b></p> </td> <td> <p>输入<b>跳转地址</b>。</p> </td> </tr> </tbody> </table>

### 熔断策略

熔断规则的原理是监控API的响应时间或异常比例，当达到指定的阈值时立即降低依赖优先级。在指定的时间内，系统不会调用该不稳定的资源，避免后端服务受到影响，从而保障后端的高可用性。当指定时间过后，再重新恢复对该资源的调用。  
**操作步骤**  
可在**添加策略** 页签，单击**熔断** 卡片，在**添加策略**面板配置相关参数。
<table> <thead> <tr> <td> <p><b>配置项</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>是否开启</b></p> </td> <td> <p>开启后，熔断规则生效。</p> </td> </tr> <tr> <td> <p><b>统计窗口时长</b></p> </td> <td> <p>统计的时间窗口长度，取值范围为1秒\~120分钟。</p> </td> </tr> <tr> <td> <p><b>最小请求数目</b></p> </td> <td> <p>触发熔断的最小请求数目，若当前统计窗口内的请求数小于此值，即使达到熔断条件规则也不会触发。</p> </td> </tr> <tr> <td> <p><b>阈值类型</b></p> </td> <td> <p>选择以<b>慢调用比例（%）</b>或<b>异常比例（%）</b>作为阈值。</p> <ol> <li> <p>选择以<b>慢调用比例（%）</b>作为阈值，需要设置允许的<b>慢调用RT</b>（即最大的响应时间），请求的响应时间大于该值则统计为慢调用。在降级阈值中设置触发熔断的慢调用比例。规则开启后，在单位统计时长内请求数目大于设置的最小请求数目，并且慢调用的比例大于阈值，则接下来的熔断时长内请求会自动被熔断。经过熔断时长后，熔断器会进入探测恢复状态，若接下来的一个请求响应时间小于设置的慢调用RT，则结束熔断；若大于设置的慢调用RT，则会再次被熔断。</p> </li> <li> <p>选择以<b>异常比例（%）</b>作为阈值，需要在降级阈值中设置触发熔断的异常比例。规则开启后，在单位统计时长内业务异常数目大于设置的最小请求数目，并且异常的比例大于阈值，则接下来的熔断时长内请求会自动被熔断。</p> </li> </ol> </td> </tr> <tr> <td> <p><b>慢调用RT</b></p> </td> <td> <p>设置允许的<b>慢调用RT</b>（即最大的响应时间）。</p> </td> </tr> <tr> <td> <p><b>熔断比例阈值</b></p> </td> <td> <p>触发熔断的慢调用比例阈值，取值范围 0-100（代表 0%-100%）。</p> </td> </tr> <tr> <td> <p><b>熔断时长（s）</b></p> </td> <td> <p>即熔断触发后持续的时间。资源进入熔断状态后，在配置的熔断时长内，请求都会快速失败。</p> </td> </tr> <tr> <td> <p><b>Web fallback 行为</b></p> </td> <td> <p><b>返回指定内容</b></p> </td> <td> <p><b>Http状态码</b></p> </td> <td> <p>设置<b>Http状态码</b>。默认为429。</p> </td> </tr> <tr> <td> <p><b>返回 content-type</b></p> </td> <td> <p>选择<b>返回 content-type</b>为<b>普通文本</b>或<b>JSON</b>。</p> </td> </tr> <tr> <td> <p><b>HTTP 返回文本</b></p> </td> <td> <p>输入返回文本。</p> </td> </tr> <tr> <td> <p><b>跳转到指定页面</b></p> </td> <td> <p><b>跳转地址</b></p> </td> <td> <p>输入<b>跳转地址</b>。</p> </td> </tr> </tbody> </table>

### IP黑白名单策略

IP 黑白名单策略的原理是通过预先配置允许或拒绝访问的 IP 地址列表，控制客户端对服务的访问权限。  
**操作步骤**  
在**添加策略** 页签，单击**IP黑白名单** 卡片，在**添加策略**面板配置相关参数。
<table> <thead> <tr> <td> <p><b>参数</b></p> </td> <td> <p><b>描述</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>开启</b></p> </td> <td> <p>开启后，IP黑白名单策略生效。</p> </td> </tr> <tr> <td> <p><b>名称</b></p> </td> <td> <p>自定义标识名称，用于在多个策略中进行区分和管理。</p> </td> </tr> <tr> <td> <p><b>备注</b></p> </td> <td> <p>策略描述信息，便于识别和管理。</p> </td> </tr> <tr> <td> <p><b>类型</b></p> </td> <td> <p>指定为黑名单或白名单，控制访问策略类型。</p> <ul> <li> <p><b>白名单</b> ：仅允许指定的 IP 地址访问服务，其余默认拒绝。</p> </li> <li> <p><b>黑名单</b> ：阻止特定 IP 地址访问服务，其余默认允许。</p> </li> </ul> </td> </tr> <tr> <td> <p><b>IP地址/地址段</b></p> </td> <td> <p>配置允许或拒绝访问的 IP 地址列表或地址段，支持多个条目，格式如<code>192.168.1.1/24</code>。</p> </td> </tr> </tbody> </table>

### 超时策略

AI 网关提供API级别的超时设置，可以按需为指定API配置网关等待请求响应结果的最大时间。如果网关在设定的时间内未收到后端服务的响应，将向客户端返回一个 HTTP 状态码为 504（Gateway Timeout）的响应结果。  
**操作步骤**  
在**添加策略** 页签，单击**超时** 卡片，在**添加策略**面板配置相关参数。  
**说明**

超时策略配置完成且开启后，请根据实际业务验证服务超时规则是否生效。
<table> <thead> <tr> <td> <p><b>参数</b></p> </td> <td> <p><b>描述</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>开启</b></p> </td> <td> <p>是否开启超时策略。</p> <ul> <li> <p>开启：网关API超时策略生效。</p> </li> <li> <p>关闭：网关API超时策略失效。</p> </li> </ul> </td> </tr> <tr> <td> <p><b>超时时间</b></p> </td> <td> <p>为当前API设置超时时间，单位为秒。</p> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <p>当设置为0或者关闭超时策略时，表示网关会一直等待请求的响应结果。</p> </div> </div> </td> </tr> </tbody> </table>

### 重试策略

AI 网关提供API级别的重试设置，可以对出错的请求进行自动重试。根据需求配置重试条件，例如在连接失败、后端服务不可用，或者接收到指定的HTTP状态码时触发请求重试。  
**API的重试条件**  
当后端服务返回`5xx`错误时，AI 网关按照设置的重试次数对出错的请求自动进行重试。
![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2128830871/CAEQWhiBgMDuyo3_vRkiIDc0ZDhlOTRmZGE4ZDRjYWU5YWJjNmYyZTUzYjhkMDk24430483_20240627165129.604.svg)

* **HTTP协议**的重试条件如下：

  * **5xx** ：如果后端服务返回任何`5xx`响应，或者发生连接断开、重置、读取超时事件，AI 网关将尝试对出错请求进行重试。

    **说明**

    `5xx`包含`connect-failure`和`refused-stream`的条件。
  * **reset**：如果发生连接断开、重置、读取超时事件，AI 网关将尝试对出错请求进行重试。

  * **connect-failure**：如果请求是由连接断开导致的出错，AI 网关将尝试对出错请求进行重试。

  * **refused-stream** ：如果后端服务以`REFUSED_STREAM`错误代码来重置流，AI 网关将尝试对出错请求进行重试。

  * **retriable-status-codes**：如果后端服务响应结果的HTTP状态码匹配上指定的重试状态码，AI 网关将尝试对该请求进行重试。

    **说明**

    只有在重试条件中指定了`retriable-status-codes`，才能使用重试状态码。
* **gRPC协议**的重试条件如下：

  * **cancelled** ：如果后端gRPC服务的响应头部中的gRPC状态码为`cancelled`，AI 网关将尝试对该请求进行重试。

  * **deadline-exceeded** ：如果后端gRPC服务的响应头部中的gRPC状态码为`deadline-exceeded`，AI 网关将尝试对该请求进行重试。

  * **internal** ：如果后端gRPC服务的响应头部中的gRPC状态码为`internal`，AI 网关将尝试对该请求进行重试。

  * **resource-exhausted** ：如果后端gRPC服务的响应头部中的gRPC状态码为`resource-exhausted`，AI 网关将尝试对该请求进行重试。

  * **unavailable** ：如果后端gRPC服务的响应头部中的gRPC状态码为`unavailable`，AI 网关将尝试对该请求进行重试。

**操作步骤**  
可在**添加策略** 页签，单击**重试** 卡片，在**添加策略**面板配置相关参数。  
**说明**

重试策略配置完成且开启后，请根据实际业务验证服务重试规则是否生效。
<table> <thead> <tr> <td> <p><b>参数</b></p> </td> <td> <p><b>描述</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>开启</b></p> </td> <td> <p>是否开启重试策略。</p> <ul> <li> <p>开启：网关API重试策略生效。</p> </li> <li> <p>关闭：网关API重试策略失效。</p> <blockquote> 关闭重试后，网关内部有默认重试配置，重试次数默认为2次，重试条件默认为 <code>connect-failure</code>、 <code>refused-stream</code>、 <code>unavailable</code>、 <code>cancelled</code>、 <code>non_idempotent</code>和 <code>retriable-status-codes</code>。 </blockquote> </li> </ul> </td> </tr> <tr> <td> <p><b>重试次数</b></p> </td> <td> <p>设置对出错请求的最大重试次数。重试次数支持设置0\~10次，建议不超过2次。</p> <blockquote> 重试次数设置为0，表示取消重试。 </blockquote> </td> </tr> <tr> <td> <p><b>重试条件</b></p> </td> <td> <p>选择合适的，支持多选。</p> </td> </tr> <tr> <td> <p><b>重试状态码</b></p> </td> <td> <p>对特定HTTP状态码的响应进行重试，支持配置多种HTTP状态码。</p> <div> <div> <i></i> </div> <div> <strong>重要 </strong> <p><b>重试条件</b>指定<code>retriable-status-codes</code>，才能配置<b>重试状态码</b>。</p> </div> </div> </td> </tr> </tbody> </table>

### Header修改策略

在将请求转发至目标后端服务之前，或在后端服务的响应返回给客户端之前，Header设置功能允许修改原始请求中的头信息。  
**操作步骤**  
可在**添加策略** 页签，单击**Header 修改** 卡片，在**添加策略**面板配置相关参数。
<table> <thead> <tr> <td> <p><b>配置项</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>开启</b></p> </td> <td> <p>是否开启Header修改策略。</p> <ul> <li> <p>开启：开启Header修改策略后，网关会控制请求和响应的Header。</p> </li> <li> <p>关闭：关闭Header修改策略后，网关不会控制请求和响应的Header。</p> </li> </ul> </td> </tr> <tr> <td> <p><b>Header类型</b></p> </td> <td> <p>选择Header类型。</p> <ul> <li> <p><b>请求</b>：表示将会对请求的Header进行设置。</p> </li> <li> <p><b>响应</b>：表示将会对响应的Header进行设置。</p> </li> </ul> </td> </tr> <tr> <td> <p><b>操作类型</b></p> </td> <td> <p>选择操作类型。</p> <ul> <li> <p><b>新增</b>：向请求或响应新增一个Header。</p> <div> <p><b>说明</b></p> <p>如果新增的Header已存在，那么Header Value将会拼接在已有的Header值后面，并通过英文逗号（,）分隔。</p> </div> </li> <li> <p><b>修改</b>：修改请求或响应指定的Header。</p> <div> <p><b>说明</b></p> <ul> <li> <p>如果指定的Header不存在，将会按照Header Key和Header Value进行新增操作。</p> </li> <li> <p>如果指定的Header存在，将会进行覆盖修改操作。</p> </li> </ul> </div> </li> <li> <p><b>删除</b>：删除请求或响应指定的Header。</p> </li> </ul> </td> </tr> <tr> <td> <p><b>Header Key</b></p> </td> <td> <p>输入请求或响应的头部名。</p> </td> </tr> <tr> <td> <p><b>Header Value</b></p> </td> <td> <p>输入请求或响应的头部值。</p> </td> </tr> </tbody> </table>

## 插件配置
1. 单击**添加插件**页签。

2. 在**快捷导航**处，选择要安装的插件类型或者搜索插件名称，单击插件卡片：

   * 如果插件未安装，在安装插件的弹出框中单击**安装并配置**，在启用插件的弹框中配置插件规则，并选择启用状态。

   * 如果插件已安装，在启用插件的弹框中，配置插件规则，并选择启用状态。

3. 单击**确定**，返回API的挂载列表，可以看到API的插件挂载情况和启用状态。

   在挂载列表中，**入站处理** 区域显示 **jwt-auth** （未开启）和 **key-auth** （已启用），**出站处理** 区域显示 **key-auth** （已启用）和 **jwt-auth** （未开启），后端服务地址为 **test.static**，请求流向为前端API → 入站处理 → 后端服务 → 出站处理。