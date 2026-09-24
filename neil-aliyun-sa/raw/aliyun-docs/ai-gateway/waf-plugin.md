---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/waf-plugin
fetch_date: 2026-09-21
product: AI Gateway
slug: waf-plugin
body_sha256: e64675d433c4bf17475eebe6156139099d76dffd98a6e3245f7c31ad9edec67b
body_bytes: 2956
migration_status: current
---

waf插件实现了基于ModSecurity的规则防护引擎，可以根据用户配置的规则屏蔽可疑请求，并支持OWASP CRS，为站点提供基础的防护功能。本文介绍如何配置waf插件。  
**说明**

该插件基于开源ModSecurity规则，默认规则为静态规则，不具备识别最新的安全风险并实时更新规则集的能力，如需获取更强大的安全防护能力，请参见[开启WAF防护](https://help.aliyun.com/document_detail/2796840.html)。

## **插件类型**
安全防护。

## 配置字段
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>useCRS</b></p></td> <td><p>bool</p></td> <td><p>选填。</p></td> <td><p>false</p></td> <td><p>是否开启OWASP CRS，详情可参考<a href="https://github.com/coreruleset/coreruleset/tree/v3.3.2">coreruleset</a>。</p></td> </tr> <tr> <td><p><b>secRules</b></p></td> <td><p>array of string</p></td> <td><p>选填。</p></td> <td><p>-</p></td> <td><p>用户自定义的waf防护规则，语法规则可参考<a href="http://www.modsecurity.cn/chm/">ModSecurity中文手册</a>。</p></td> </tr> </tbody> </table>

## 配置示例
### 默认配置

启用默认配置，进行拦截。

```
HELPCODEESCAPE-bash
useCRS: true
```

启用默认配置，仅观测，不拦截。

```
HELPCODEESCAPE-bash
useCRS: true
secRules:
  - "SecRuleEngine DetectionOnly"
```

### 自定义防护规则

```
HELPCODEESCAPE-bash
useCRS: true
secRules: 
  - "SecRule REQUEST_URI \"@streq /admin\" \"id:101,phase:1,t:lowercase,deny\""
  - "SecRule REQUEST_BODY \"@rx maliciouspayload\" \"id:102,phase:2,t:lowercase,deny\""
```

根据该配置，下列请求将被禁止访问。

```
HELPCODEESCAPE-bash
curl http://example.com/admin
curl http://example.com -d "maliciouspayload"
```

### 对特定路由或域名开启

```
HELPCODEESCAPE-bash
useCRS: true
secRules: 
  - "SecRule REQUEST_URI \"@streq /admin\" \"id:101,phase:1,t:lowercase,deny\""
  - "SecRule REQUEST_BODY \"@rx maliciouspayload\" \"id:102,phase:2,t:lowercase,deny\""
```

在`route-1`路由做如下插件配置：

```
HELPCODEESCAPE-yaml
secRules:
  - "SecAction \"id:102,phase:1,deny\""
```

在`*.example.com`和`test.com`两个域名做如下插件配置：

```
HELPCODEESCAPE-yaml
secRules:
  - "SecAction \"id:102,phase:1,pass\""
```

**说明**

* `route-1`即在创建网关路由时填写的路由名称，当匹配到该路由时，将使用此段配置。

* `*.example.com`和`test.com`用于匹配请求的域名，当发现域名匹配时，将使用此配置。

* 配置的匹配生效顺序，将按照规则的排列顺序，匹配第一个规则后生效对应配置，后续规则将被忽略。