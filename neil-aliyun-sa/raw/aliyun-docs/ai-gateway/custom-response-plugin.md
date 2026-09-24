---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/custom-response-plugin
fetch_date: 2026-09-21
product: AI Gateway
slug: custom-response-plugin
body_sha256: e694242217318ce388c3033432e2b039987cd88fe7bbe5be4620ec6a89a398be
body_bytes: 3171
migration_status: current
---

custom-response插件支持配置自定义的响应，包括自定义HTTP应答状态码、HTTP应答头，以及HTTP应答Body。可以用于Mock响应，也可以用于判断特定状态码后给出自定义应答，例如在触发网关限流策略时实现自定义响应。本文介绍如何配置custom-response插件。  

## **插件类型**
传输协议。

## 配置字段
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>status_code</p></td> <td><p>number</p></td> <td><p>选填。</p></td> <td><p>200</p></td> <td><p>自定义HTTP应答状态码。</p></td> </tr> <tr> <td><p>headers</p></td> <td><p>array of string</p></td> <td><p>选填。</p></td> <td><p>-</p></td> <td><p>自定义HTTP应答头，Key和 Value 用<code>=</code>分隔。</p></td> </tr> <tr> <td><p>body</p></td> <td><p>string</p></td> <td><p>选填。</p></td> <td><p>-</p></td> <td><p>自定义HTTP应答Body。</p></td> </tr> <tr> <td><p>enable_on_status</p></td> <td><p>array of number</p></td> <td><p>选填。</p></td> <td><p>-</p></td> <td><p>匹配原始状态码，生成自定义响应，不填写时，不判断原始状态码。</p></td> </tr> </tbody> </table>

## 配置示例
### Mock应答场景

```
HELPCODEESCAPE-plaintext
status_code: 200
headers:
- Content-Type=application/json
- Hello=World
body: "{\"hello\":\"world\"}"
```

根据该配置，请求将返回自定义应答如下。

```
HELPCODEESCAPE-plaintext
HTTP/1.1 200 OK
Content-Type: application/json
Hello: World
Content-Length: 17

{"hello":"world"}
```

### 触发限流时自定义响应

```
HELPCODEESCAPE-plaintext
enable_on_status: 
- 429
status_code: 302
headers:
- Location=https://example.com
```

触发网关限流时一般会返回429状态码，这时请求将返回自定义应答如下。

```
HELPCODEESCAPE-plaintext
HTTP/1.1 302 Found
Location: https://example.com
```

从而实现基于浏览器302重定向机制，将限流后的用户引导到其他页面，比如可以是一个CDN上的静态页面。

如果希望触发限流时，正常返回其他应答，参考Mock应答场景配置相应的字段即可。

### 对特定路由或域名开启

在`route-a`和`route-b`两个路由做如下插件配置：

```
HELPCODEESCAPE-yaml
body: "{\"hello\":\"world\"}"
```

在`*.example.com`和`test.com`两个域名做如下插件配置：

```
HELPCODEESCAPE-yaml
  enable_on_status: 
  - 429
  status_code: 200
  headers:
  - Content-Type=application/json
  body: "{\"errmsg\": \"rate limited\"}"
```

**说明**

* `route-a`和`route-b`即在创建网关路由时填写的路由名称，当匹配到这两个路由时，将使用此段配置。

* `*.example.com`和`test.com`用于匹配请求的域名，当发现域名匹配时，将使用此段配置。

* 配置的匹配生效顺序，将按照规则的排列顺序，匹配第一个规则后生效对应配置，后续规则将被忽略。