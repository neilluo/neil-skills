---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/degraphql-plugin
fetch_date: 2026-09-21
product: AI Gateway
slug: degraphql-plugin
body_sha256: 547ec5eabc15cecd8f96a5b56edeb7875f868eb3eeb3df052a742a3c2c3df5c7
body_bytes: 5165
migration_status: current
---

`de-graphql`插件通过将URIs映射到GraphQL查询，从而可以将GraphQL上游转换为传统服务进行访问。  

## 运行属性
插件执行阶段：`认证阶段` 插件执行优先级：`430`

## 参数配置
<table> <thead> <tr> <td><p><b>参数</b></p></td> <td><p><b>描述</b></p></td> <td><p><b>默认</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>gql</code></p></td> <td><p>graphql 查询</p></td> <td><p>不能为空</p></td> </tr> <tr> <td><p><code>endpoint</code></p></td> <td><p>graphql 查询端点</p></td> <td><p><code>/graphql</code></p></td> </tr> <tr> <td><p><code>timeout</code></p></td> <td><p>查询连接超时，单位毫秒</p></td> <td><p><code>5000</code></p></td> </tr> <tr> <td><p><code>domain</code></p></td> <td><p>服务域名，当服务来源是DNS配置</p></td> <td><p></p></td> </tr> </tbody> </table>

## 插件使用
<https://github.com/alibaba/higress/issues/268>

### 测试配置

```
HELPCODEESCAPE-yaml
apiVersion: networking.higress.io/v1
kind: McpBridge
metadata:
  name: default
  namespace: higress-system
spec:
  registries:
  - domain: api.github.com
    name: github
    port: 443
    type: dns
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    higress.io/destination: github.dns
    higress.io/upstream-vhost: "api.github.com"
    higress.io/backend-protocol: HTTPS
  name: github-api
  namespace: higress-system
spec:
  ingressClassName: higress  
  rules:
  - http:
      paths:
      - backend:
          resource:
            apiGroup: networking.higress.io
            kind: McpBridge
            name: default
        path: /api
        pathType: Prefix
---
apiVersion: extensions.higress.io/v1alpha1
kind: WasmPlugin
metadata:
  name: de-graphql-github-api
  namespace: higress-system
spec:
  matchRules:
  - ingress:
    - github-api
    config:
      timeout: 5000
      endpoint: /graphql
      domain: api.github.com
      gql: |
           query ($owner:String! $name:String!){
              repository(owner:$owner, name:$name) {
                name
                forkCount
                description
             }
           }
  url: oci://higress-registry.cn-hangzhou.cr.aliyuncs.com/plugins/de-graphql:1.0.0
```

### 测试结果

```
HELPCODEESCAPE-yaml
curl "http://localhost/api?owner=alibaba&name=higress" -H "Authorization: Bearer some-token"

{
"data": {
	"repository": {
		"description": "Next-generation Cloud Native Gateway",
		"forkCount": 149,
		"name": "higress"
	}
}
}
```

## GraphQL介绍
### GraphQL 端点

REST API 有多个端点，GraphQL API 只有一个端点。

```
HELPCODEESCAPE-bash
https://api.github.com/graphql
```

### 与 GraphQL 通信

由于 GraphQL 操作由多行 JSON 组成，可以使用 curl 或任何其他采用 HTTP 的库。

在 REST 中，HTTP 谓词确定执行的操作。 在 GraphQL 中，执行查询要提供 JSON 请求体，因此 HTTP 谓词为 POST。 唯一的例外是内省查询，它是一种简单的 GET 到终结点查询。

### GraphQL POST 请求参数

标准的 GraphQL POST 请求情况如下：

* 添加 HTTP 请求头： Content-Type: application/json

* 使用 JSON 格式的请求体

* JSON 请求体包含三个字段

  * query：查询文档，必填

  * variables：变量，选填

  * operationName：操作名称，选填，查询文档有多个操作时必填

  ```
  HELPCODEESCAPE-json
  {
    "query": "{viewer{name}}",
    "operationName": "",
    "variables": {
      "name": "value"
    }
  }
  ```

### GraphQL 基本参数类型

* 基本参数类型包含： String, Int, Float, Boolean

* \[类型\]代表数组，例如：\[Int\]代表整型数组

* GraphQL 基本参数传递

  * 小括号内定义形参，注意：参数需要定义类型

  * !（叹号）代表参数不能为空

    ```
    HELPCODEESCAPE-go
    query ($owner : String!, $name : String!) {
      repository(owner: $owner, name: $name) {
        name
        forkCount
        description
      }
    }
    ```

### GitHub GraphQL 测试

使用 curl 命令查询 GraphQL，使用有效 JSON 请求体发出 POST 请求。 有效请求体必须包含一个名为 query 的字符串。

```
HELPCODEESCAPE-json
curl https://api.github.com/graphql -X POST \
-H "Authorization: bearer <PAT>" \
-d "{\"query\": \"query { viewer { login }}\"}"

{
  "data": {
    "viewer": {
      "login": "2456868764"
    }
  }
}
```

```
HELPCODEESCAPE-json
curl 'https://api.github.com/graphql' -X POST \
-H 'Authorization: bearer <PAT>' \
-d '{"query":"query ($owner: String!, $name: String!) {\n  repository(owner: $owner, name: $name) {\n    name\n    forkCount\n    description\n  }\n}\n","variables":{"owner":"2456868764","name":"higress"}}'

{
  "data": {
    "repository": {
      "name": "higress",
      "forkCount": 149,
      "description": "Next-generation Cloud Native Gateway | 下一代云原生网关"
    }
  }
}
```

## 参考文档
* <https://github.com/graphql/graphql-spec>

* <https://docs.github.com/zh/graphql/guides/forming-calls-with-graphql>

* <https://github.com/altair-graphql/altair>

<br />