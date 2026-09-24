---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/the-traffic-tag-plugin
fetch_date: 2026-09-21
product: AI Gateway
slug: the-traffic-tag-plugin
body_sha256: 09d5c8f9e030334a1cb179b9cae5b3d7b6d9978b1c1ba34ad6a527cd18e9dafd
body_bytes: 8159
migration_status: current
---

`traffic-tag` 插件允许根据权重或特定请求内容通过添加特定请求头的方式对请求流量进行染色。它支持复杂的逻辑来确定如何根据用户定义的标准染色流量。  

## 运行属性
插件执行阶段：`默认阶段` 插件执行优先级：`400`

## 配置字段
此部分提供了配置字段的详细描述。
<table> <thead> <tr> <td><p><b>字段名称</b></p></td> <td><p><b>类型</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>是否必填</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>conditionGroups</code></p></td> <td><p>array of object</p></td> <td><p>-</p></td> <td><p>否</p></td> <td><p>定义基于内容的标记条件组，详细结构见条件组配置。</p></td> </tr> <tr> <td><p><code>weightGroups</code></p></td> <td><p>array of object</p></td> <td><p>-</p></td> <td><p>否</p></td> <td><p>定义基于权重的标记条件组，详细结构见权重组配置。</p></td> </tr> <tr> <td><p><code>defaultTagKey</code></p></td> <td><p>string</p></td> <td><p>-</p></td> <td><p>否</p></td> <td><p>默认的标记键名，当未匹配到任何条件时使用。当且仅当同时配置了defaultTagVal时生效</p></td> </tr> <tr> <td><p><code>defaultTagVal</code></p></td> <td><p>string</p></td> <td><p>-</p></td> <td><p>否</p></td> <td><p>默认的标记值，当未匹配到任何条件时使用。当且仅当同时配置了defaultTagKey时生效</p></td> </tr> </tbody> </table>

### 条件组配置

`conditionGroups` 中每一项的配置字段说明如下：
<table> <thead> <tr> <td><p><b>字段名称</b></p></td> <td><p><b>类型</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>是否必填</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>headerName</code></p></td> <td><p>string</p></td> <td><p>-</p></td> <td><p>是</p></td> <td><p>要添加或修改的 HTTP 头名称。</p></td> </tr> <tr> <td><p><code>headerValue</code></p></td> <td><p>string</p></td> <td><p>-</p></td> <td><p>是</p></td> <td><p>HTTP 头的值。</p></td> </tr> <tr> <td><p><code>logic</code></p></td> <td><p>string</p></td> <td><p>-</p></td> <td><p>是</p></td> <td><p>条件组中的逻辑关系，支持\&nbsp;<code>and</code>、<code>or</code>，必须为小写字母。</p></td> </tr> <tr> <td><p><code>conditions</code></p></td> <td><p>array of object</p></td> <td><p>-</p></td> <td><p>是</p></td> <td><p>描述具体的标记条件，详细结构如下。</p></td> </tr> </tbody> </table>

`conditions` 中每一项的配置字段说明如下：
<table> <thead> <tr> <td><p><b>字段名称</b></p></td> <td><p><b>类型</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>是否必填</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>conditionType</code></p></td> <td><p>string</p></td> <td><p>-</p></td> <td><p>是</p></td> <td><p>条件类型，支持\&nbsp;<code>header</code>、<code>parameter</code>、<code>cookie</code>。</p></td> </tr> <tr> <td><p><code>key</code></p></td> <td><p>string</p></td> <td><p>-</p></td> <td><p>是</p></td> <td><p>条件的关键字。</p></td> </tr> <tr> <td><p><code>operator</code></p></td> <td><p>string</p></td> <td><p>-</p></td> <td><p>是</p></td> <td><p>操作符，支持\&nbsp;<code>equal</code>、<code>not_equal</code>、<code>prefix</code>、<code>in</code>、<code>not_in</code>、<code>regex</code>、<code>percentage</code>。</p></td> </tr> <tr> <td><p><code>value</code></p></td> <td><p>array of string</p></td> <td><p>-</p></td> <td><p>是</p></td> <td><p>条件的值，仅当操作符为\&nbsp;<code>in</code>\&nbsp;和\&nbsp;<code>not_in</code>\&nbsp;时支持配置多个值。</p></td> </tr> </tbody> </table>  
**说明**

当 `operator` 为 `regex` 时，使用的正则表达式引擎是 [RE2](https://github.com/google/re2)。详情请参阅 [RE2 官方文档](https://github.com/google/re2/wiki/Syntax)。

### 权重组配置

`weightGroups` 中每一项的配置字段说明如下：
<table> <thead> <tr> <td><p>字段名称</p></td> <td><p>类型</p></td> <td><p>默认值</p></td> <td><p>是否必填</p></td> <td><p>描述</p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>headerName</code></p></td> <td><p>string</p></td> <td><p>-</p></td> <td><p>是</p></td> <td><p>要添加或修改的 HTTP 头名称。</p></td> </tr> <tr> <td><p><code>headerValue</code></p></td> <td><p>string</p></td> <td><p>-</p></td> <td><p>是</p></td> <td><p>HTTP 头的值。</p></td> </tr> <tr> <td><p><code>weight</code></p></td> <td><p>integer</p></td> <td><p>-</p></td> <td><p>是</p></td> <td><p>流量权重百分比。</p></td> </tr> </tbody> </table>

### 操作符说明

<table> <thead> <tr> <td><p>操作符</p></td> <td><p>描述</p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>equal</code></p></td> <td><p>精确匹配，值需要完全相等</p></td> </tr> <tr> <td><p><code>not_equal</code></p></td> <td><p>不等匹配，值不相等时满足条件</p></td> </tr> <tr> <td><p><code>prefix</code></p></td> <td><p>前缀匹配，指定值是实际值的前缀时满足条件</p></td> </tr> <tr> <td><p><code>in</code></p></td> <td><p>包含匹配，实际值需要在指定的列表中</p></td> </tr> <tr> <td><p><code>not_in</code></p></td> <td><p>排除匹配，实际值不在指定的列表中时满足条件</p></td> </tr> <tr> <td><p><code>regex</code></p></td> <td><p>正则表达式匹配，按照正则表达式规则匹配</p></td> </tr> <tr> <td><p><code>percentage</code></p></td> <td><p>百分比匹配，原理：<code>hash(get(key)) % 100 \&lt; value</code>\&nbsp;成立时满足条件</p></td> </tr> </tbody> </table>  
**说明**

关于`percentage`和`weight`的区别

* `percentage`操作符：用于条件表达式中，基于指定的百分比和指定的键值对来判断是否执行某个操作。对于一个相同的键值对，多次匹配的结果是幂等的，即这一次命中条件，下一次也会命中。

* `weight`字段：用于定义不同处理路径的流量权重。在基于权重的流量标记中，`weight`确定了某个路径应接收的流量比例。与`percentage`不同的是，由于没有指定固定的对比依据而是基于随机权重分布，同一个请求的多次匹配可能匹配多个结果。

使用`percentage`进行条件匹配时，判断每个请求是否满足特定百分比条件；而`weight`则是静态随机分配整体流量的比例。

## 配置示例
### 例1: 基于内容的匹配

按照下例的配置，满足请求头`role` 的值是`user`、`viewer`、`editor`其中之一且存在查询参数`foo=bar`的请求将被添加请求头`x-mse-tag: gray`。由于配置了`defaultTagKey`和`defaultTagVal`，当未匹配到任何条件时，请求将被添加请求头`x-mse-tag: base`。

```
HELPCODEESCAPE-yaml
defaultTagKey: x-mse-tag
defaultTagVal: base
conditionGroups:
  - headerName: x-mse-tag
    headerValue: gray
    logic: and
    conditions:
      - conditionType: header
        key: role
        operator: in
        value:
          - user
          - viewer
          - editor
      - conditionType: parameter
        key: foo
        operator: equal
        value:
        - bar
```

### 例2: 基于权重的匹配

按照下列配置，请求将有30%几率被添加请求头`x-mse-tag: gray`，30%几率被添加请求头`x-mse-tag: blue`，40%几率不添加请求头。

```
HELPCODEESCAPE-yaml
# 权重总和为100，下例中未配置的40权重将不添加header
weightGroups:
  - headerName: x-mse-tag
    headerValue: gray
    weight: 30
  - headerName: x-mse-tag
    headerValue: blue
    weight: 30
```