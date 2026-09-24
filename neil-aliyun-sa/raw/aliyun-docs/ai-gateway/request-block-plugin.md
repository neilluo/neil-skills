---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/request-block-plugin
fetch_date: 2026-09-21
product: AI Gateway
slug: request-block-plugin
body_sha256: f1c917ac45881be99f84d49d65cfd3c29de12679d8f0c746da54f9718b5ef75b
body_bytes: 3928
migration_status: current
---

request-block插件实现了基于URL、请求头等特征屏蔽HTTP请求，可以用于防护部分站点资源不对外部暴露。本文介绍如何配置request-block插件。  

## **插件类型**
安全防护。

## 配置字段
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>block_urls</b></p></td> <td><p>array of string</p></td> <td><p>选填。block_urls，block_headers，block_bodys中至少必填一项。</p></td> <td><p>-</p></td> <td><p>配置用于匹配需要屏蔽URL的字符串。</p></td> </tr> <tr> <td><p><b>block_headers</b></p></td> <td><p>array of string</p></td> <td><p>选填。block_urls，block_headers，block_bodys中至少必填一项。</p></td> <td><p>-</p></td> <td><p>配置用于匹配需要屏蔽请求Header的字符串。</p></td> </tr> <tr> <td><p><b>block_bodys</b></p></td> <td><p>array of string</p></td> <td><p>选填。block_urls，block_headers，block_bodys中至少必填一项。</p></td> <td><p>-</p></td> <td><p>配置用于匹配需要屏蔽请求Body的字符串。</p></td> </tr> <tr> <td><p><b>blocked_code</b></p></td> <td><p>number</p></td> <td><p>选填。</p></td> <td><p>403</p></td> <td><p>配置请求被屏蔽时返回的HTTP状态码。</p></td> </tr> <tr> <td><p><b>blocked_message</b></p></td> <td><p>string</p></td> <td><p>选填。</p></td> <td><p>-</p></td> <td><p>配置请求被屏蔽时返回的HTTP应答Body。</p></td> </tr> <tr> <td><p><b>case_sensitive</b></p></td> <td><p>bool</p></td> <td><p>选填。</p></td> <td><p>true</p></td> <td><p>配置匹配时是否区分大小写。默认区分。</p></td> </tr> </tbody> </table>

## 配置示例
### 屏蔽请求URL路径

```
HELPCODEESCAPE-yaml
block_urls:
- swagger.html
- foo=bar
case_sensitive: false
```

根据该配置，下列请求将被禁止访问。

```
HELPCODEESCAPE-bash
curl http://example.com?foo=Bar
curl http://exmaple.com/Swagger.html
```

### 屏蔽请求Header

```
HELPCODEESCAPE-yaml
block_headers:
- example-key
- example-value
```

根据该配置，下列请求将被禁止访问。

```
HELPCODEESCAPE-bash
curl http://example.com -H 'example-key: 123'
curl http://exmaple.com -H 'my-header: example-value'
```

### 屏蔽请求Body

```
HELPCODEESCAPE-bash
block_bodys:
- "hello world"
case_sensitive: false
```

根据该配置，下列请求将被禁止访问。

```
HELPCODEESCAPE-bash
curl http://example.com -d 'Hello World'
curl http://exmaple.com -d 'hello world'
```

### 对特定路由或域名开启

在`route-a`和`route-b`两个路由做如下插件配置：

```
HELPCODEESCAPE-yaml
  block_bodys: 
  - "hello world"
```

在`*.example.com`和`test.com`两个域名做如下插件配置：

```
HELPCODEESCAPE-yaml
  block_urls: 
  - "swagger.html"
  block_bodys:
  - "hello world"
```

**说明**

* `route-a`和`route-b`即在创建网关路由时填写的路由名称，当匹配到这两个路由时，将使用此段配置。

* `*.example.com`和`test.com`用于匹配请求的域名，当发现域名匹配时，将使用此配置。

* 配置的匹配生效顺序，将按照规则的排列顺序，匹配第一个规则后生效对应配置，后续规则将被忽略。

## 请求Body大小限制
当配置了`block_bodys`时，仅支持小于32MB的请求Body进行匹配。若请求Body大于此限制，并且不存在匹配到的`block_urls`和`block_headers`项时，不会对该请求执行屏蔽操作。

当配置了`block_bodys`时，若请求Body超过全局配置DownstreamConnectionBufferLimits，将返回`413 Payload Too Large`, 请在参数配置页调高此项。注意调高此参数配置后，网关内存使用将有显著增加。