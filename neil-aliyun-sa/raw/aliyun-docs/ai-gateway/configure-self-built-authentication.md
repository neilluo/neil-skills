---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/configure-self-built-authentication
fetch_date: 2026-09-21
product: AI Gateway
slug: configure-self-built-authentication
body_sha256: b08578f2b7fc4e598500e1d94901cc19914e18795f7522ec596e696202e0ff01
body_bytes: 17267
migration_status: current
---

AI 网关支持自定义鉴权服务，方便在网关入口处完成鉴权，避免每个后端服务都接入鉴权服务。本文介绍如何为AI 网关配置自建认证鉴权。  

## 背景信息
服务端通常根据客户端请求携带的凭证信息（即Token）来保护对外暴露的API接口的通信安全。Token形式没有严格规定，一般根据实际业务场景决定。

* 如果Token采用的是JSON WEB Token (JWT)，那么在任何时间、任何地点都可以利用公钥来对Token的签名进行验签，无需访问一个中心化的鉴权服务。

* 如果Token的形式是业务方自定义的格式，则服务端收到请求后，必须额外访问中心化的鉴权服务来完成鉴权操作，以此保护API接口的通信安全。AI 网关支持自定义鉴权。

下面以一个示例来说明AI 网关接入自建的鉴权服务后的请求处理流程。  
![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2748830871/CAEQWhiBgID7rtTyuhkiIGVlYzJjNmE5MzljNzQ4OGM5YWQ0MzVjNGU0YjgzMGFl5270113_20250610175717.393.svg)

1. 客户端向网关发起认证请求，例如登录操作。

2. 网关将认证请求直接转发给认证服务。

3. 认证服务读取请求中的验证信息（例如用户名、密码）进行验证，验证通过后返回凭证信息（Token）给网关，由网关响应给客户端。

4. 客户端向网关发起业务请求，例如下单操作/order，请求中携带上一步中身份认证成功后颁发的Token。

5. 网关通过截取原始业务请求的Path（包含Query Parameters）、HTTP方法（GET、POST等）和Token来形成一个新的请求报文，向接入的自建鉴权服务发起鉴权请求。您需要在网关控制台配置Token所在的HTTP Header，另外您可以根据需要开启允许携带原始请求的Body。

   假设自建鉴权服务的鉴权API是/validateToken，那么鉴权请求的真实Path是鉴权API加上原始业务请求的Path后的结果，即/validateToken/order。
6. 鉴权服务收到鉴权请求后，既可以根据Token完成校验Token合法性的操作，又可以根据原始业务请求的Path完成鉴权操作。

   * 如果您鉴权服务的鉴权响应可以修改HTTP状态码，那么您可以利用HTTP状态码来反映鉴权结果。

     * 鉴权服务返回HTTP状态码为200，表明Token合法且Token有权限访问该后端资源。网关继续将原始业务请求转发给受保护的后端服务，收到业务响应后再次转发给客户端，完成下单操作。

     * 鉴权服务返回HTTP状态码为401或者403，表明Token不合法或Token无权限访问该后端资源。网关直接返回鉴权服务的响应给客户端，此次下单操作失败。

   * 如果您的鉴权服务受业务本身限制要求鉴权响应的HTTP状态码统一为200，那么您可以利用内置的HTTP头部`x-mse-external-authz-check-result`。

     * 鉴权服务的响应头部`x-mse-external-authz-check-result`的结果为`true`，表明Token合法或Token有权限访问该后端资源。网关继续将原始业务请求转发给受保护的后端服务，收到业务响应后再次转发给客户端，完成下单操作。

     * 鉴权服务的响应头部`x-mse-external-authz-check-result`的结果为`false`，表明Token不合法或Token无权限访问该后端资源。网关直接返回鉴权服务的响应给客户端，此次下单操作失败。

## 创建自建认证鉴权
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击目标**实例ID**。

4. 在左侧导航栏，单击**安全管理** \> **全局认证鉴权**。

5. 在**全局认证鉴权** 页面，单击**创建鉴权** ，然后在**创建鉴权** 面板，配置网关鉴权相关参数，最后单击**确定**。

   <table> <thead> <tr> <td> <p><b>配置项</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>开启</b></p> </td> <td> <p>是否开启AI 网关鉴权。</p> </td> </tr> <tr> <td> <p><b>鉴权名称</b></p> </td> <td> <p>自定义AI 网关鉴权的名称。</p> </td> </tr> <tr> <td> <p><b>鉴权类型</b></p> </td> <td> <p>选择<b>自建的鉴权服务</b>。</p> </td> </tr> <tr> <td> <p><b>鉴权服务</b></p> </td> <td> <p>选择鉴权的后端服务，可以在服务管理中添加。相关内容，请参见<a href="https://help.aliyun.com/document_detail/250960.html#task-2081185">添加服务</a>。</p> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <ul> <li> <p>仅支持选择HTTP协议的服务，不支持Dubbo等其他协议的服务。</p> </li> <li> <p>如果具有多个端口的K8s Service，则默认取第一个端口。如果您希望使用其他端口，需要在容器服务中创建一个额外的K8s Service且只使用目标端口。</p> </li> </ul> </div> </div> </td> </tr> <tr> <td> <p><b>鉴权API</b></p> </td> <td> <p>设置鉴权服务提供的鉴权API的Path，API的Path需是前缀匹配。</p> <div> <p>例如，您的鉴权服务基于SpringMVC构建，对外开放的鉴权API为/check，那么处理/check/<b>的请求设置如下：</b></p> <pre>HELPCODEESCAPE-java<br>@RequestMapping("/check/")<br>public ResponseEntity\&lt;RestResult\&lt;String\&gt;\&gt; check(){}</pre> </div> </td> </tr> <tr> <td> <p><b>Token位置</b></p> </td> <td> <p>设置Token在请求报文中的Header位置，常见的有Authorization和Cookie。您可以选择<b>下拉选择</b>或<b>手动输入</b>的方式设置Token位置。</p> </td> </tr> <tr> <td> <p><b>鉴权请求中允许携带的头部</b></p> </td> <td> <p>如果需要额外携带客户端请求中的头部，那么需要在字段中按需配置头部。</p> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <p>Host、Method、Path和Content-Length头部会被默认添加，您无需手动添加。</p> </div> </div> </td> </tr> <tr> <td> <p><b>鉴权响应中允许保留的头部</b></p> </td> <td> <p>如果需要将鉴权响应中的头部添加到客户端请求中，那么需要在字段中按需配置头部。</p> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <p>如果客户端请求中已经有该头部，那么其值将会被覆盖。</p> </div> </div> </td> </tr> <tr> <td> <p><b>鉴权请求中允许携带Body</b></p> </td> <td> <p>勾选<b>鉴权请求中允许携带Body</b>后，鉴权请求会包含原始请求的Body。</p> <p>其中，<b>Body最大字节数</b>表示允许鉴权请求携带Body的最大字节数。单位：字节。</p> </td> </tr> <tr> <td> <p><b>超时时间</b></p> </td> <td> <p>设置等待鉴权服务返回结果的最大等待时间。单位：秒，默认超时时间为10秒。</p> </td> </tr> <tr> <td> <p><b>模式</b></p> </td> <td> <p>支持宽松模式和严格模式，建议您使用宽松模式。</p> <ul> <li> <p><b>宽松模式</b>：当鉴权服务不可用时（鉴权服务建立连接失败或者返回5xx请求），网关接受客户端请求。</p> </li> <li> <p><b>严格模式</b>：当鉴权服务不可用时（鉴权服务建立连接失败或者返回5xx请求），网关拒绝客户端请求。</p> </li> </ul> </td> </tr> <tr> <td> <p><b>简单条件</b></p> </td> <td> <p>在<b>授权</b>右侧单击<b>简单条件</b>。简单条件授权模式支持<b>白名单模式</b>和<b>黑名单模式</b>。</p> <ul> <li> <p><b>白名单模式</b>：白名单中的Hosts和Paths无需校验即可访问，其余Hosts和Paths都需要校验。</p> </li> <li> <p><b>黑名单模式</b>：黑名单中的Hosts和Paths需要校验，其余Hosts和Paths可直接访问。</p> </li> </ul> <div> <p>单击<b>规则条件</b>，设置请求域名、路径和请求头。</p> <ul> <li> <p><b>域名</b>：请求访问的域名，即Hosts。</p> </li> <li> <p><b>路径（Path）</b>：请求访问的接口Path，即Paths。</p> </li> <li> <p><b>路径匹配条件</b>：Path支持精确匹配、前缀匹配和正则匹配。</p> <ul> <li> <p><b>精确匹配</b>：输入完整的Path，例如/app/v1/order。</p> </li> <li> <p><b>前缀匹配</b>：输入Path的前缀，并且末尾填一个\*。例如，匹配所有以/app开头的请求，那么需设置为/app/\*。</p> </li> <li> <p><b>正则匹配</b>：正则匹配的语法遵循Google Re2规范。详细信息，请参见<a href="https://github.com/google/re2/wiki/Syntax">Re2语法</a>。</p> </li> </ul> <p><b>大小写敏感</b>：若选中此项，路径匹配值会区分大小写。</p> </li> <li> <p><b>请求头（Header）</b>：请求访问的头部信息，即Header。单击<b>请求头</b>配置，可以配置多个Header，各个Header之间是与的关系。</p> <ul> <li> <p><b>HeaderKey</b>：Header字段名。</p> </li> <li> <div> <p><b>条件</b>：Header支持的匹配条件。</p> <ul> <li> <p><b>等于</b>：请求Header集合中指定Key的值与输入值相等。</p> </li> <li> <p><b>不等于</b>：请求Header集合中指定Key的值与输入值不相等。</p> </li> <li> <p><b>存在</b>：请求Header集合中存在输入Key值。</p> </li> <li> <p><b>不存在</b>：请求Header集合中不存在输入Key值。</p> </li> <li> <p><b>包含</b>：请求Header集合中指定Key的值包含输入值。</p> </li> <li> <p><b>不包含</b>：请求Header集合中指定Key的值不包含输入值。</p> </li> <li> <p><b>前缀</b>：请求Header集合中指定Key的值以输入值为前缀。</p> </li> <li> <p><b>后缀</b>：请求Header集合中指定Key的值以输入值为后缀。</p> </li> <li> <p><b>正则</b>：请求Header集合中指定Key的值匹配输入的正则表达式，正则匹配的语法遵循Google Re2规范。详细信息，请参见<a href="https://github.com/google/re2/wiki/Syntax">Re2语法</a>。</p> </li> </ul> </div> </li> <li> <p><b>值</b>：Header字段的取值。</p> </li> </ul> </li> </ul> </div> </td> </tr> <tr> <td> <p><b>复杂条件</b></p> </td> <td> <p>在<b>授权</b>右侧单击<b>复杂条件</b>。</p> <p>复杂条件授权支持通过YAML配置Envoy的permission数据结构来配置基于与/或/非组合条件逻辑的授权规则。当满足配置的条件时执行鉴权逻辑；不满足条件的请求无需鉴权即可访问。</p> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <ul> <li> <p>完整的permission数据结构字段说明，请参见<a href="https://www.envoyproxy.io/docs/envoy/v1.20.3/api-v3/config/rbac/v3/rbac.proto#envoy-v3-api-msg-config-rbac-v3-permission">Envoy官方文档</a>。</p> </li> <li> <p>配置示例请参见<a href="https://help.aliyun.com/document_detail/2807799.html#1fadb527163f9">复杂条件授权示例</a>。</p> </li> </ul> </div> </div> </td> </tr> </tbody> </table>  
   返回**全局认证鉴权**页面查看鉴权信息，如果已包含新建的网关鉴权信息，说明网关自建认证鉴权新建成功。

## 查看并管理鉴权服务
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击目标**实例ID**。

4. 在左侧导航栏，单击**安全管理** \> **全局认证鉴权**。

5. 在**认证鉴权** 页面，单击目标鉴权规则**操作** 列的**详情** ，可查看当前服务的**基本信息** 和**认证配置** ，也可查看并管理**授权信息**。

   详情页展示三个区域：**基本信息** 中类型为**自建的鉴权服务** ；**认证配置** 包含**鉴权服务** 、**鉴权API** 、**Token位置** 、**超时时间** 、**不可用模式** 、**允许携带Body** 、**允许的请求头部** 和**允许的响应头部** 字段；**授权信息** 区域显示当前为**白名单模式** ，多行规则条件之间为"或"关系，每行规则内的多个匹配项之间为"与"关系，表格包含**请求域名** 、**请求Path匹配项** 、**大小写敏感** 、**请求Header匹配项** 和**操作**列。

   您可在**授权信息** 区域，单击**创建授权信息** 。在对话框中输入**请求域名** 和**请求Path** ，并选择**匹配方式** ，然后单击**确定**新增授权规则。

## 相关操作
您还可以执行以下其他操作，管理网关的认证鉴权：

* 开启鉴权：在**全局认证鉴权** 页面，单击目标鉴权规则**操作** 列的**开启**，使认证鉴权信息生效。

* 关闭鉴权：在**全局认证鉴权** 页面，单击目标鉴权规则**操作** 列的**关闭**，关闭网关认证鉴权信息。

* 编辑鉴权：在**全局认证鉴权** 页面，单击目标鉴权规则**操作** 列的**编辑**，可编辑网关认证鉴权信息。

* 删除鉴权：在**全局认证鉴权** 页面，单击目标鉴权规则**操作** 列的**删除**，可删除网关认证鉴权信息。

**说明**

只有在认证鉴权信息关闭的状态下才可执行删除操作。

## 复杂条件授权示例
### 正则匹配域名示例

本示例中，只对exampleA.com和exampleB.com两个域名下前缀匹配路径的请求执行鉴权逻辑。注意此处regex字段配置的正则需要完全匹配，而非部分匹配。

本示例中，test.exampleA.com将无法命中条件，无需鉴权即可访问。  
**说明**

* 正则匹配的语法遵循Google Re2规范。详细信息，请参见[Re2语法](https://github.com/google/re2/wiki/Syntax)。

* 完整的permission数据结构字段说明，请参见[Envoy官方文档](https://www.envoyproxy.io/docs/envoy/v1.20.3/api-v3/config/rbac/v3/rbac.proto#envoy-v3-api-msg-config-rbac-v3-permission)。

```
HELPCODEESCAPE-yaml
permissions:
# and_rules 表示下面的所有 rules 条件同时成立时执行鉴权
- and_rules:
    rules:
      - url_path:
          # 前缀匹配路径
          path:
            prefix: /
      - header:
          # 正则匹配
          safe_regex_match:
            regex: "(exampleA\\.com|exampleB\\.com)"
          # 支持HTTP Pseudo-Header规范，可通过":authority"这个Header来获取域名
          name: ":authority"
```

### 与/或/非多条件组合示例

本示例满足以下条件：

1. exampleA.com/api前缀开头的请求需要鉴权，但是：

   1. exampleA.com/api/appa/bbb不需要鉴权。

   2. exampleA.com/api/appb/ccc不需要鉴权。

2. exampleB.com下所有请求需要鉴权，但是：

   1. exampleB.com/api/appa/bbb不需要鉴权**。**

   2. exampleB.com/api/appb/ccc不需要鉴权**。**

   3. exampleB.com/api/appc前缀开头的不需要鉴权，但是：

      1. exampleB.com/api/appc/bbb/ccc需要鉴权**。**

      2. exampleB.com/api/appc/ccc/ddd需要鉴权**。**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2748830871/CAEQVRiBgIDf0JHPrBkiIDZiNjlmYjQ2OGI0NDQyNmVhMTBlODA3OTA3NzQ2YTRk4977538_20250314160915.530.svg)

对应的YAML配置如下：

```
HELPCODEESCAPE-yaml
permissions:
# or_rules 表示下面的所有 rules 条件中，有任意一个条件成立时执行鉴权
- or_rules:
    rules:
      # and_rules，表示下面所有 rules 同时满足，此 rule 条件才成立
      # 规则一
      - and_rules:
          rules:
            - url_path:
                path:
                  exact: /api/appc/bbb/ccc
            - header:
                exact_match: "exampleB.com"
                name: ":authority"
      # 规则二                
      - and_rules:
          rules:
            - url_path:
                path:
                  exact: /api/appc/ccc/ddd
            - header:
                exact_match: "exampleB.com"
                name: ":authority"
      - and_rules:
          rules:
            # 规则三
            - url_path:
                path:
                  prefix: /api/
            # not_rule 表示下面的配置不满足时，此 rule 条件才成立
            # 规则四
            - not_rule:
                url_path:
                  path:
                    exact: /api/appa/bbb
            # 规则五
            - not_rule:
                url_path:
                  path:
                    exact: /api/appb/ccc                                
            - header:
                exact_match: "exampleA.com"
                name: ":authority"                                
      - and_rules:
          rules:
            # 规则六
            - url_path:
                path:
                  prefix: /
            # not_rule 表示下面的配置不满足时，此 rule 条件才成立
            # 规则七
            - not_rule:
                url_path:
                  path:
                    exact: /api/appa/bbb
            # 规则八
            - not_rule:
                url_path:
                  path:
                    exact: /api/appb/ccc
            # 规则九
            - not_rule:
                url_path:
                  path:
                    prefix: /api/appc/                                         
            - header:
                exact_match: "exampleB.com"
                name: ":authority" 
```