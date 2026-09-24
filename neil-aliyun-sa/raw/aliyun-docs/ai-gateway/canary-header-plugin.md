---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/canary-header-plugin
fetch_date: 2026-09-21
product: AI Gateway
slug: canary-header-plugin
body_sha256: a5a22cfe446a0e084e69a43e8d05320db2496663515643f75daa3cfbde4d9841
body_bytes: 3600
migration_status: current
---

`canary-header`插件实现了按照指定比例为请求添加指定header的功能。请求添加header后会重新匹配路由，配合此插件，可实现基于比例的灰度路由，而无需客户端主动携带灰度header。  

## 配置字段
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>weighted_headers</code></p></td> <td><p>array of object</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>配置要添加的header以及其对应的权重。</p></td> </tr> </tbody> </table>

weighted_headers中每一项的配置字段说明如下：
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>added_key</code></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>要添加的header key。</p></td> </tr> <tr> <td><p><code>added_value</code></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>要添加的header value。</p></td> </tr> <tr> <td><p><code>weight</code></p></td> <td><p>number</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>要添加的header所对应的权重，单位为百分比，所有header的权重之和不能大于100。</p></td> </tr> </tbody> </table>  
**说明**

若路由权重之和不大于100，则不足100的部分代表不会添加任何header的概率。

## 配置示例
## 全局配置
按照如下配置，所有请求中30%的请求会被添加`x-higress-canary:gray`的header，70%的请求会被添加`x-higress-canary:base`的header。

```
HELPCODEESCAPE-yaml
weighted_headers: 
- added_key: x-higress-canary
  added_value: gray
  weight: 30
- added_key: x-higress-canary
  added_value: base
  weight: 70
```

按照如下配置，所有请求中30%的请求会被添加`x-higress-canary:gray`的header，70%的请求不会添加任何header。

```
HELPCODEESCAPE-yaml
weighted_headers: 
- added_key: x-higress-canary
  added_value: gray
  weight: 30
```

## 对特定路由或域名开启
按照如下配置，对于匹配到`route-a`路由的请求，将会有30%的概率被添加`x-higress-canary:gray`的header，70%的概率被添加`x-higress-canary:base`的header。添加header后，请求将会重新匹配路由。例如，此时有一个路由`route-a-gray`，该路由的匹配规则中有一项按header匹配的规则，该规则匹配了`x-higress-canary:gray`。这样将会有30%的请求将会匹配到`route-a-gray`，从而实现了按比例灰度的功能。

```
HELPCODEESCAPE-yaml
# 使用 _rules_ 字段进行细粒度规则配置
_rules_:
# 规则一：按路由名称匹配生效
- _match_route_:
  - route-a
  weighted_headers: 
  - added_key: x-higress-canary
    added_value: gray
    weight: 30
  - added_key: x-higress-canary
    added_value: base
    weight: 70
# 规则二：按域名匹配生效
- _match_domain_:
  - "*.example.com"
  weighted_headers:
  - added_key: x-custom-header
    added_value: gray
    weight: 30
  - added_key: x-custom-header
    added_value: blue
    weight: 30
  - added_key: x-custom-header
    added_value: base
    weight: 40
```