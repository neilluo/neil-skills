---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/bot-detect-plug-ins
fetch_date: 2026-09-21
product: AI Gateway
slug: bot-detect-plug-ins
body_sha256: 38b0087efe89a1421f53549210412507a610c3ea1bc7d4c99479c258d394f5a4
body_bytes: 2744
migration_status: current
---

bot-detect插件可以用于识别并阻止互联网爬虫对站点资源的爬取。本文介绍如何配置bot-detect插件。  

## **插件类型**
安全防护。

## 配置字段
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>allow</b></p></td> <td><p>array of string</p></td> <td><p>选填。</p></td> <td><p>-</p></td> <td><p>配置匹配User-Agent请求头的正则表达式，匹配命中时将允许其访问。</p></td> </tr> <tr> <td><p><b>deny</b></p></td> <td><p>array of string</p></td> <td><p>选填。</p></td> <td><p>-</p></td> <td><p>配置匹配User-Agent请求头的正则表达式，匹配命中时将屏蔽请求。</p></td> </tr> <tr> <td><p><b>blocked_code</b></p></td> <td><p>number</p></td> <td><p>选填。</p></td> <td><p>403</p></td> <td><p>配置请求被屏蔽时返回的HTTP状态码。</p></td> </tr> <tr> <td><p><b>blocked_message</b></p></td> <td><p>string</p></td> <td><p>选填。</p></td> <td><p>-</p></td> <td><p>配置请求被屏蔽时返回的HTTP应答Body。</p></td> </tr> </tbody> </table>  
**说明**

`allow`和`deny`字段可以均不配置，则执行默认的爬虫判断逻辑，通过配置`allow`字段可以将原本命中默认爬虫判断逻辑的请求放行，通过配置`deny`字段可以增加额外的爬虫判断逻辑。

## 配置示例
### 放行原本命中爬虫规则的请求

```
HELPCODEESCAPE-plaintext
allow:
- ".*Go-http-client.*"
```

若不做该配置，默认的Golang网络库请求会被视作爬虫，被禁止访问。

### 增加爬虫判断

```
HELPCODEESCAPE-plaintext
deny:
- "spd-tools.*"
```

根据该配置，下列请求将被禁止访问。

```
HELPCODEESCAPE-plaintext
curl http://example.com -H 'User-Agent: spd-tools/1.1'
curl http://exmaple.com -H 'User-Agent: spd-tools'
```

### 对特定路由或域名开启

在`route-a`和`route-b`两个路由做空配置保存。

在`*.example.com`和`test.com`两个域名做如下插件配置：

```
HELPCODEESCAPE-yaml
  allow:
  - ".*Go-http-client.*"
```

**说明**

* `route-a`和`route-b`即在创建网关路由时填写的路由名称，因为没有做额外配置，当匹配到这两个路由时，将使用内置的默认规则来识别爬虫。

* `*.example.com`和`test.com`用于匹配请求的域名，当发现域名匹配时，将使用此段配置。

* 配置的匹配生效顺序，将按照规则的排列顺序，匹配第一个规则后生效对应配置，后续规则将被忽略。