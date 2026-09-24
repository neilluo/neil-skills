---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/parameter-access-control
fetch_date: 2026-09-21
product: AI Gateway
slug: parameter-access-control
body_sha256: 0fde97d27239e6851ff2cf14a0b595f087e16a56a841bb81f2be1067c0590d51
body_bytes: 6371
migration_status: current
---

参数访问控制插件配置参考。  

## **功能说明**
`param-access-control`插件实现了基于请求参数和上下文条件进行精确访问控制，可用于实现复杂的请求验证和访问管理场景。

## 运行属性
* 插件执行阶段：鉴权阶段。

* 插件执行优先级：310。

## 配置字段
<table> <thead> <tr> <td><p><b>参数</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>parameters</b></p></td> <td><p>object</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>定义需要使用的参数，支持从Header、Query、Path中提取。</p></td> </tr> <tr> <td><p><b>rules</b></p></td> <td><p>array of rule</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>定义判断规则和处理逻辑。</p></td> </tr> </tbody> </table>

### parameters字段配置说明

<table> <thead> <tr> <td><p><b>参数</b></p></td> <td><p><b>格式</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>Header</p></td> <td><p><code>Header:参数名</code></p></td> <td><p>从请求头提取参数。</p></td> </tr> <tr> <td><p>Query</p></td> <td><p><code>Query:参数名</code></p></td> <td><p>从查询参数提取参数。</p></td> </tr> <tr> <td><p>Path</p></td> <td><p><code>Path:序号</code></p></td> <td><p>从路径中提取第n段内容，序号从1开始。</p></td> </tr> <tr> <td><p>Path</p></td> <td><p><code>Path</code></p></td> <td><p>获取完整路径。</p></td> </tr> </tbody> </table>

### rules字段配置说明

<table> <thead> <tr> <td><p><b>参数</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>name</p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>规则名称。</p></td> </tr> <tr> <td><p>condition</p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>判断条件。</p></td> </tr> <tr> <td><p>ifTrue</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>-</p></td> <td><p>条件为真时的处理指令（ALLOW/DENY）。</p></td> </tr> <tr> <td><p>ifFalse</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>-</p></td> <td><p>条件为假时的处理指令（ALLOW/DENY）。</p></td> </tr> <tr> <td><p>statusCode</p></td> <td><p>number</p></td> <td><p>选填</p></td> <td><p>403</p></td> <td><p>DENY时返回的HTTP状态码。</p></td> </tr> <tr> <td><p>responseHeaders</p></td> <td><p>object</p></td> <td><p>选填</p></td> <td><p>-</p></td> <td><p>DENY时返回的响应头。</p></td> </tr> <tr> <td><p>responseBody</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>-</p></td> <td><p>DENY时返回的响应体。</p></td> </tr> </tbody> </table>

## 支持的运算符和函数
<table> <thead> <tr> <td><p><b>运算符/函数</b></p></td> <td><p><b>描述</b></p></td> <td><p><b>示例</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>==</p></td> <td><p>等于</p></td> <td><p><code>userType == 'admin'</code></p></td> </tr> <tr> <td><p>!=</p></td> <td><p>不等于</p></td> <td><p><code>status != 'inactive'</code></p></td> </tr> <tr> <td><p>\&gt;</p></td> <td><p>大于</p></td> <td><p><code>version \&gt; '2.0'</code></p></td> </tr> <tr> <td><p>\&gt;=</p></td> <td><p>大于等于</p></td> <td><p><code>level \&gt;= '3'</code></p></td> </tr> <tr> <td><p>\&lt;</p></td> <td><p>小于</p></td> <td><p><code>priority \&lt; '5'</code></p></td> </tr> <tr> <td><p>\&lt;=</p></td> <td><p>小于等于</p></td> <td><p><code>quota \&lt;= '100'</code></p></td> </tr> <tr> <td><p>contains</p></td> <td><p>包含子串</p></td> <td><p><code>path.contains('api')</code></p></td> </tr> <tr> <td><p>matches</p></td> <td><p>正则匹配</p></td> <td><p><code>url.matches('\*.jpg')</code></p></td> </tr> <tr> <td><p>startsWith</p></td> <td><p>前缀匹配</p></td> <td><p><code>path.startsWith('/api')</code></p></td> </tr> <tr> <td><p>endsWith</p></td> <td><p>后缀匹配</p></td> <td><p><code>filename.endsWith('.jpg')</code></p></td> </tr> <tr> <td><p>\&amp;\&amp;</p></td> <td><p>逻辑与</p></td> <td><p><code>userType == 'admin' \&amp;\&amp; level \&gt;= '3'</code></p></td> </tr> <tr> <td><p>\|\|</p></td> <td><p>逻辑或</p></td> <td><p><code>path.startsWith('/api') \\\|\\\| path.startsWith('/v2')</code></p></td> </tr> <tr> <td><p>!</p></td> <td><p>逻辑非</p></td> <td><p><code>!(status == 'inactive')</code></p></td> </tr> </tbody> </table>

## 配置示例
插件通过配置规则（rules）来控制请求访问，规则按照配置顺序依次执行直到遇到ALLOW或DENY指令。每个规则必须至少配置ifTrue或ifFalse其中之一，建议为DENY操作设置明确的状态码和响应信息。以下示例展示了常见的使用场景：

### 基于用户身份的访问控制

```
HELPCODEESCAPE-yaml
parameters:
  userType: "Header:userType"
  userId: "Path:1"

rules:
  - name: admin-access
    condition: "userType == 'admin'"
    ifTrue: "ALLOW"
  - name: user-access
    condition: "userId == '123'"
    ifFalse: "DENY"
    statusCode: 403
    responseBody: "Access Denied"
```

根据该配置，满足以下条件的请求将被允许：

```
HELPCODEESCAPE-bash
# 管理员访问任意路径
curl http://example.com/any/path? -H "userType: admin"

# 用户访问自己的资源
curl http://example.com/123/profile
```

而以下请求将被拒绝：

```
HELPCODEESCAPE-bash
# 用户访问他人资源
curl http://example.com/456/profile
```

### 基于API版本的访问控制

```
HELPCODEESCAPE-yaml
parameters:
  apiVersion: "Header:Api-Version"
  path: "Path"

rules:
  - name: version-check
    condition: "path.contains('/v2/') && apiVersion < '2.0'"
    ifTrue: "DENY"
    statusCode: 400
    responseHeaders:
      Content-Type: application/json
    responseBody: '{"error": "Please upgrade to API version 2.0 or above"}'
```