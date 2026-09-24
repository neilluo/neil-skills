---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/http-to-mcp-field-configurations
fetch_date: 2026-09-21
product: AI Gateway
slug: http-to-mcp-field-configurations
body_sha256: a97308233f3838682b87320f4cd94f8349ce50be349801205446eacd8aecf074
body_bytes: 35517
migration_status: current
---

本文档提供 HTTP 转 MCP 配置的字段说明与参考，帮助您通过自定义 YAML 为 MCP 服务集成工具。  

## **配置字段**
### 服务器配置

<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>是否必填</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>server.name</p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>MCP 服务器的名称。如果使用插件内置的 MCP 服务器（如 quark-search），只需配置此字段为对应的名称，无需配置 tools 字段。如果是 HTTP to MCP 场景，此字段可以填写任意值。</p></td> </tr> <tr> <td><p>server.config</p></td> <td><p>object</p></td> <td><p>选填</p></td> <td><p>服务器配置，如 API 密钥等。</p></td> </tr> <tr> <td><p>server.securitySchemes</p></td> <td><p>array\[object\]</p></td> <td><p>选填</p></td> <td><p>定义可重用的认证方案，供工具引用。详见<a href="#e042ea49301ir">认证与安全</a>。</p></td> </tr> </tbody> </table>

### 允许的工具配置

<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>是否必填</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>allowTools</p></td> <td><p>array\[string\]</p></td> <td><p>选填</p></td> <td><p>允许调用的工具列表。如不指定，则允许所有工具。</p></td> </tr> </tbody> </table>

### HTTP to MCP 工具配置

<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>是否必填</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>tools</p></td> <td><p>array\[object\]</p></td> <td><p>选填</p></td> <td><p>HTTP to MCP 工具配置列表。</p></td> </tr> <tr> <td><p>tools\[\].name</p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>工具名称。</p></td> </tr> <tr> <td><p>tools\[\].description</p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>工具功能描述。</p></td> </tr> <tr> <td><p>tools\[\].args</p></td> <td><p>array\[object\]</p></td> <td><p>必填</p></td> <td><p>工具参数定义。</p></td> </tr> <tr> <td><p>tools\[\].args\[\].name</p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>参数名称。</p></td> </tr> <tr> <td><p>tools\[\].args\[\].description</p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>参数描述。</p></td> </tr> <tr> <td><p>tools\[\].args\[\].type</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>参数类型（string, number, integer, boolean, array, object）。默认是string。</p></td> </tr> <tr> <td><p>tools\[\].args\[\].required</p></td> <td><p>boolean</p></td> <td><p>选填</p></td> <td><p>参数是否必需。默认是false。</p></td> </tr> <tr> <td><p>tools\[\].args\[\].default</p></td> <td><p>any</p></td> <td><p>选填</p></td> <td><p>参数默认值。</p></td> </tr> <tr> <td><p>tools\[\].args\[\].enum</p></td> <td><p>array</p></td> <td><p>选填</p></td> <td><p>参数允许的值列表。</p></td> </tr> <tr> <td><p>tools\[\].args\[\].items</p></td> <td><p>object</p></td> <td><p>选填</p></td> <td><p>数组项的模式（当type为array时）。</p></td> </tr> <tr> <td><p>tools\[\].args\[\].properties</p></td> <td><p>object</p></td> <td><p>选填</p></td> <td><p>对象属性的模式（当type为object时）。</p></td> </tr> <tr> <td><p>tools\[\].args\[\].position</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>参数在请求中的位置（query, path, header, cookie, body）。</p></td> </tr> <tr> <td><p>tools\[\].requestTemplate</p></td> <td><p>object</p></td> <td><p>必填</p></td> <td><p>HTTP 请求模板。</p></td> </tr> <tr> <td><p>tools\[\].requestTemplate.url</p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>请求 URL 模板。</p></td> </tr> <tr> <td><p>tools\[\].requestTemplate.method</p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>HTTP 方法（GET/POST等）。</p></td> </tr> <tr> <td><p>tools\[\].requestTemplate.headers</p></td> <td><p>array\[object\]</p></td> <td><p>选填</p></td> <td><p>请求头模板。</p></td> </tr> <tr> <td><p>tools\[\].requestTemplate.headers\[\].key</p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>请求头名称。</p></td> </tr> <tr> <td><p>tools\[\].requestTemplate.headers\[\].value</p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>请求头值模板。</p></td> </tr> <tr> <td><p>tools\[\].requestTemplate.body</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>请求体模板（与<code>argsToJsonBody</code>、<code>argsToUrlParam</code>、<code>argsToFormBody</code>互斥）。</p></td> </tr> <tr> <td><p>tools\[\].requestTemplate.argsToJsonBody</p></td> <td><p>boolean</p></td> <td><p>选填</p></td> <td><p>默认是false。当为true时，参数将直接用作JSON请求体（与<code>body</code>、<code>argsToUrlParam</code>、<code>argsToFormBody</code>互斥）。</p></td> </tr> <tr> <td><p>tools\[\].requestTemplate.argsToUrlParam</p></td> <td><p>boolean</p></td> <td><p>选填</p></td> <td><p>默认是false。当为true时，参数将作为查询参数添加到URL中（与<code>body</code>、<code>argsToJsonBody</code>、<code>argsToFormBody</code>互斥）。</p></td> </tr> <tr> <td><p>tools\[\].requestTemplate.argsToFormBody</p></td> <td><p>boolean</p></td> <td><p>选填</p></td> <td><p>默认是false。当为true时，参数将以<code>application/x-www-form-urlencoded</code>格式编码在请求体中（与<code>body</code>、<code>argsToJsonBody</code>、<code>argsToUrlParam</code>互斥）。</p></td> </tr> <tr> <td><p>tools\[\].responseTemplate</p></td> <td><p>object</p></td> <td><p>必填</p></td> <td><p>HTTP 响应转换模板。</p></td> </tr> <tr> <td><p>tools\[\].responseTemplate.body</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>响应体转换模板（与<code>prependBody</code>和<code>appendBody</code>互斥）。</p></td> </tr> <tr> <td><p>tools\[\].responseTemplate.prependBody</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>在响应体前插入的文本（与<code>body</code>互斥）。</p></td> </tr> <tr> <td><p>tools\[\].responseTemplate.appendBody</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>在响应体后插入的文本（与<code>body</code>互斥）。</p></td> </tr> <tr> <td><p>tools\[\].security</p></td> <td><p>object</p></td> <td><p>选填</p></td> <td><p>工具级别安全配置，用于定义 MCP Client 和 MCP Server 之间的认证方式，并支持凭证透传。</p></td> </tr> <tr> <td><p>tools\[\].security.id</p></td> <td><p>string</p></td> <td><p>当\&nbsp;<code>tools\[\].security</code>\&nbsp;配置时必填</p></td> <td><p>引用在\&nbsp;<code>server.securitySchemes</code>\&nbsp;中定义的认证方案 ID。</p></td> </tr> <tr> <td><p>tools\[\].security.passthrough</p></td> <td><p>boolean</p></td> <td><p>选填</p></td> <td><p>是否启用透明认证。默认是false，如果为\&nbsp;<code>true</code>，则从 MCP Client 请求中提取的凭证将用于\&nbsp;<code>requestTemplate.security</code>\&nbsp;定义的认证方案。</p></td> </tr> <tr> <td><p>tools\[\].requestTemplate.security</p></td> <td><p>object</p></td> <td><p>选填</p></td> <td><p>HTTP 请求模板的安全配置，用于定义 MCP Server 和 HTTP API 之间的认证方式。</p></td> </tr> <tr> <td><p>tools\[\].requestTemplate.security.id</p></td> <td><p>string</p></td> <td><p>当\&nbsp;<code>tools\[\].requestTemplate.security</code>\&nbsp;配置时必填</p></td> <td><p>引用在\&nbsp;<code>server.securitySchemes</code>\&nbsp;中定义的认证方案 ID。</p></td> </tr> <tr> <td><p>tools\[\].requestTemplate.security.credential</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>覆盖\&nbsp;<code>server.securitySchemes</code>\&nbsp;中定义的默认凭证。如果同时启用了\&nbsp;<code>tools\[\].security.passthrough</code>，则此字段将被忽略，优先使用透传的凭证。</p></td> </tr> </tbody> </table>

## 认证与安全
MCP Server 插件支持灵活的认证配置，以确保通信安全。

### 定义认证方案 (server.securitySchemes)

您可以在服务器级别定义一组可重用的认证方案。这些方案可被各个工具引用，用于配置 MCP Server 向后端 HTTP API 发起请求时的认证方式。

**配置字段 (** **server.securitySchemes[]****)**：
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>是否必填</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>id</p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>认证方案的唯一标识符，供工具配置引用。</p></td> </tr> <tr> <td><p>type</p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>认证类型，支持<code>http</code>（用于Basic和 Bearer认证）和<code>apiKey</code>。</p></td> </tr> <tr> <td><p>scheme</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>当<code>type</code>为<code>http</code>时指定具体的方案，如<code>basic</code>或<code>bearer</code>。</p></td> </tr> <tr> <td><p>in</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>当<code>type</code>为<code>apiKey</code>时指定 API 密钥的位置，如<code>header</code>或<code>query</code>。</p></td> </tr> <tr> <td><p>name</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>当<code>type</code>为<code>apiKey</code>时指定 Header 名称或查询参数名称。</p></td> </tr> <tr> <td><p>defaultCredential</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>此方案的默认凭证。例如，对于Basic Auth，可以是<code>user: password</code>；对于Bearer Token，是Token本身；对于API Key，是 Key本身。</p></td> </tr> </tbody> </table>

**示例 (** **server.securitySchemes****)**：

```
HELPCODEESCAPE-yaml
server:
  name: my-api-server
  securitySchemes:
    - id: MyBasicAuth
      type: http
      scheme: basic
      defaultCredential: "admin:secretpassword" # 默认的用户名和密码
    - id: MyBearerToken
      type: http
      scheme: bearer
      defaultCredential: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." # 默认的Bearer Token
    - id: MyApiKeyInHeader
      type: apiKey
      in: header
      name: X-Custom-API-Key # API Key 在名为 X-Custom-API-Key 的 Header 中
      defaultCredential: "abcdef123456" # 默认的 API Key
    - id: MyApiKeyInQuery
      type: apiKey
      in: query
      name: "api_token" # API Key 在名为 api_token 的查询参数中
      defaultCredential: "uvwxyz789012"
```

### 在工具中应用认证方案

定义了 `server.securitySchemes` 后，您可以在每个工具的 `requestTemplate.security` 中通过 `id` 引用这些方案，以指定 MCP Server 调用后端 HTTP API 时使用的认证方式。

* **tools[].requestTemplate.security.id**: 引用 `server.securitySchemes` 中定义的认证方案的 `id`。

* **tools[].requestTemplate.security.credential**: 可选。如果提供，它将覆盖所引用方案中的 `defaultCredential`。这允许您为特定工具使用不同的凭证，即使它们共享相同的认证机制。

**示例：**

```
HELPCODEESCAPE-yaml
tools:
  - name: get-user-details
    # ... 其他工具配置 ...
    requestTemplate:
      url: "https://api.example.com/users/{{.args.userId}}"
      method: GET
      security:
        id: MyBearerToken # 使用上面定义的 MyBearerToken 方案
        # credential: "override_token_for_this_tool" # 可选：为此工具覆盖默认Token
  # ...
  - name: update-inventory
    # ... 其他工具配置 ...
    requestTemplate:
      url: "https://api.example.com/inventory/{{.args.itemId}}"
      method: POST
      security:
        id: MyApiKeyInHeader # 使用 MyApiKeyInHeader 方案
        # 此工具将使用 MyApiKeyInHeader 中定义的 defaultCredential
```

### 透明认证 (Passthrough Authentication)

透明认证功能允许在 MCP Client（例如 AI 助手）调用 MCP Server 时，将提供的凭证直接传递给 MCP Server，以用于后续调用后端 HTTP API 的认证过程。

**配置方式：**

1. **确保相关认证方案已在** **server.securitySchemes****中定义**。这包括客户端用于连接到 MCP Server 的方案，以及 MCP Server 用于连接到后端 HTTP API 的方案。

2. **配置工具级别认证 (** **tools[].security****)** : 在需要透传凭证的工具中，配置 `security` 字段：

   * `id`：引用 `server.securitySchemes` 中定义的、用于 **MCP Client 与 MCP Server 之间**的认证方案。插件将根据此方案从客户端请求中提取凭证，并清理原始请求中的该凭证。

   * `passthrough: true`：启用透明认证。

3. **配置请求模板认证 (** **tools[].requestTemplate.security****)** : 在工具的 `requestTemplate` 中，配置 `security` 字段：

   * `id`: 引用 `server.securitySchemes` 中定义的、用于 **MCP Server 与后端 HTTP API 之间**的认证方案。

   * 当 `tools[].security.passthrough` 为 `true` 时，从客户端提取的凭证将根据此 `requestTemplate.security` 方案应用于对后端 HTTP API 的调用。

**示例：**

假设 MCP Client 使用 Bearer Token 调用 MCP Server，而 MCP Server 需要使用 API Key 调用后端的 HTTP API。

```
HELPCODEESCAPE-yaml
server:
  name: product-api-server
  securitySchemes:
    - id: ClientSideBearer # 客户端使用Bearer Token
      type: http
      scheme: bearer
    - id: BackendApiKey    # 后端API使用X-API-Key
      type: apiKey
      in: header
      name: X-API-Key
      # defaultCredential: "optional_default_backend_key"

tools:
  - name: get-product-securely
    description: "获取产品信息（安全透传）"
    security: # 客户端 -> MCP Server 认证配置
      id: ClientSideBearer # MCP Server期望客户端使用此方案，并会尝试提取此类型的凭证
      passthrough: true   # 允许凭证透传
    args:
      - name: product_id
        description: "产品ID"
        type: string
        required: true
    requestTemplate:
      security: # MCP Server -> 后端 HTTP API 认证配置
        id: BackendApiKey # 后端API需要此方案。透传的凭证将按此方案应用。
      url: "https://api.example.com/products/{{.args.product_id}}"
      method: GET
```

**工作流程：**

1. MCP Client 发起请求到 MCP Server 的 `get-product-securely` 工具，并在 `Authorization` 头中携带 `Bearer <client_token>`。

2. MCP Server 根据 `tools[].security` (id: `ClientSideBearer`) 识别出客户端使用的是 Bearer Token。它会从请求中提取 `<client_token>` 并移除原始的 `Authorization` 头。

3. 因为 `passthrough: true`，提取出的 `<client_token>` 被标记为透传凭证。

4. MCP Server 准备调用后端 HTTP API。它查看 `requestTemplate.security` (id: `BackendApiKey`)。

5. 由于启用了透传，MCP Server 将之前提取的 `<client_token>` 作为凭证值，按照 `BackendApiKey` 方案（即作为名为 `X-API-Key` 的 HTTP Header）添加到对 `https://api.example.com/products/...` 的请求中。

6. 后端 HTTP API 收到请求，其中 `X-API-Key` Header 的值为 `<client_token>`。

**重要**

* 当 `tools[].security.passthrough` 为 `true` 时，`requestTemplate.security.credential` 字段会被忽略，优先使用透传的凭证。

* 透传的凭证值会直接用于 `requestTemplate.security` 指定的认证方案。请确保凭证的格式与目标认证方案兼容。`extractAndRemoveIncomingCredential` 函数会尝试提取核心凭证部分（例如，Bearer token 值，Basic auth 的 base64 编码部分）。

### 透传凭证不生效的排查建议

配置透明认证后，如果 MCP Server 调用后端 HTTP API 时仍在使用 `server.securitySchemes` 中定义的默认凭证（`defaultCredential`），而不是从客户端透传的凭证，请按以下顺序自查配置：

1. **确认工具级别是否已启用透传** ：检查对应工具的 `tools[].security.passthrough` 是否设置为 `true`。该字段必须配置在具体工具的 `security` 节点下，仅在 `server.securitySchemes` 中定义认证方案不会自动启用透传。

2. **确认认证方案与客户端凭证类型一致** ：检查 `tools[].security.id` 引用的 `server.securitySchemes` 方案（例如 `ClientSideBearer`）与客户端/SDK 实际传入的凭证类型是否匹配。例如客户端通过 Bearer Token 调用，则该方案的 `type` 和 `scheme` 需配置为 `http`/`bearer`，否则插件无法从请求中正确提取凭证。

3. **确认 `defaultCredential` 本身是合法凭证** ：透传未生效时，系统会回退使用 `requestTemplate.security` 对应认证方案下配置的 `defaultCredential`。请确认该值是一个真实可用的凭证（例如合法 JWT 格式的 Bearer Token），不要保留模板占位符或示例值。`defaultCredential` 格式非法会导致认证校验失败。

完成以上三项自查后，可重新发起调用并观察后端 HTTP API 收到的凭证是否已替换为透传值。

## 参数类型支持
HTTP to MCP 工具支持多种参数类型，使您可以更精确地定义工具参数：

* **string**: 字符串类型（默认）。

* **number**: 数字类型（浮点数）。

* **integer**: 整数类型。

* **boolean**: 布尔类型（true/false）。

* **array** : 数组类型，使用 `items` 字段定义数组元素的模式。

* **object** : 对象类型，使用 `properties` 字段定义对象属性的模式。

**示例：**

```
HELPCODEESCAPE-yaml
args:
  - name: query
    description: "搜索关键词"
    type: string
    required: true
  - name: limit
    description: "返回结果数量"
    type: integer
    default: 10
  - name: filters
    description: "过滤条件"
    type: object
    properties:
      category:
        type: string
        enum: ["food", "hotel", "attraction"]
      price:
        type: integer
        minimum: 0
  - name: coordinates
    description: "坐标点列表"
    type: array
    items:
      type: object
      properties:
        lat:
          type: number
        lng:
          type: number
```

## 参数位置控制
HTTP to MCP 工具支持通过 `position` 字段精确控制每个参数在请求中的位置。这使您可以更灵活地构建 API 请求，例如同时使用路径参数、查询参数和请求体参数。

### 支持的位置类型

* **query**: 参数将作为查询参数添加到 URL 中。

* **path** : 参数将替换 URL 中的路径占位符，例如 `/pet/{petId}` 中的 `{petId}`。

* **header**: 参数将作为 HTTP 头添加到请求中。

* **cookie**: 参数将作为 Cookie 添加到请求中。

* **body**: 参数将添加到请求体中（根据内容类型自动格式化为 JSON 或表单）。

### 使用示例

```
HELPCODEESCAPE-yaml
args:
  - name: petId
    description: "宠物ID"
    type: string
    required: true
    position: path
  - name: token
    description: "认证令牌"
    type: string
    required: true
    position: header
  - name: sessionId
    description: "会话ID"
    type: string
    position: cookie
  - name: limit
    description: "返回结果数量"
    type: integer
    default: 10
    position: query
  - name: tags
    description: "标签列表"
    type: array
    position: body
```

在上面的示例中：

* `petId` 将替换 URL 中的 `{petId}` 占位符。

* `token` 将作为 HTTP 头添加到请求中。

* `sessionId` 将作为 Cookie 添加到请求中。

* `limit` 将作为查询参数添加到 URL 中。

* `tags` 将添加到请求体中。

### 与批量参数处理选项的关系

当使用 `position` 指定参数位置时，这些参数将按照指定的位置处理，而不会受到批量参数处理选项（`argsToJsonBody`、`argsToUrlParam`、`argsToFormBody`）的影响。只有未指定 `position` 的参数才会受到这些批量选项的影响。

例如，如果您同时使用了 `position` 和 `argsToJsonBody`：

* 指定了 `position: query` 的参数会添加到 URL 查询字符串中。

* 指定了 `position: header` 的参数会添加到 HTTP 头中。

* 指定了 `position: path` 的参数会替换 URL 中的占位符。

* 指定了 `position: cookie` 的参数会添加到 Cookie 中。

* 指定了 `position: body` 的参数会添加到 JSON 请求体中。

* 未指定 `position` 的参数会通过 `argsToJsonBody` 添加到 JSON 请求体中。

此外，如果在 `requestTemplate` 中明确指定了 `body`，则所有 `position: body` 的参数都将被忽略，以避免冲突。

## 请求参数传递方式
除了使用 `position` 精确控制每个参数的位置外，HTTP to MCP 工具还支持四种批量参数处理方式，这些选项是**互斥的**，只能选择其中一种：

1. **body**: 使用模板手动构建请求体。这是最灵活的方式，允许您完全控制请求体的格式。

   ```
   HELPCODEESCAPE-yaml
   requestTemplate:
     body: |
       {
         "query": "{{.args.query}}",
         "filters": {{toJson .args.filters}},
         "options": {
           "limit": {{.args.limit}}
         }
       }
   ```

2. **argsToJsonBody** : 当设置为 `true` 时，未指定 `position` 的参数将直接作为 JSON 对象发送到请求体中，并自动添加 `Content-Type: application/json; charset=utf-8` 头。

   ```
   HELPCODEESCAPE-yaml
   requestTemplate:
     argsToJsonBody: true
   ```

3. **argsToUrlParam** : 当设置为 `true` 时，未指定 `position` 的参数将作为查询参数添加到 URL 中。

   ```
   HELPCODEESCAPE-yaml
   requestTemplate:
     argsToUrlParam: true
   ```

4. **argsToFormBody** : 当设置为 `true` 时，未指定 `position` 的参数将以 `application/x-www-form-urlencoded` 格式编码在请求体中，并自动添加相应的 Content-Type 头。

   ```
   HELPCODEESCAPE-yaml
   requestTemplate:
     argsToFormBody: true
   ```

这些选项简化了常见 API 调用模式的配置，无需手动构建请求体或 URL 参数。请注意，这四个选项是互斥的，在一个工具配置中只能使用其中一种。如果同时配置了多个选项，系统会报错并拒绝加载该工具配置。

## 模板语法
HTTP-to-MCP 功能使用 [GJSON Template](https://github.com/higress-group/gjson_template)库进行模板渲染，它结合了 Go 的模板语法和 GJSON 的强大路径语法：

### 请求模板

用于构造 HTTP 请求 URL、头部和正文：

* 访问配置值：`.config.字段名`。

* 访问工具参数：`.args.参数名`。

### 响应模板

用于将 HTTP 响应转换为适合 AI 消费的格式：

* 使用 GJSON 路径语法访问 JSON 响应字段。

* 使用模板函数如 `add`、`upper`、`lower` 等。

* 使用控制结构如 `if`、`range` 等。

GJSON Template 包含了所有[Sprig](https://github.com/Masterminds/sprig)的函数，提供了 70+ 种用于字符串操作、数学运算、日期格式化等的模板函数，功能等同于 Helm 的模板能力。

常用的 Sprig 函数包括：

* **字符串操作** ：`trim`、`upper`、`lower`、`replace`、`plural`、`nospace`

* **数学运算** ：`add`、`sub`、`mul`、`div`、`max`、`min`

* **日期格式化** ：`now`、`date`、`dateInZone`、`dateModify`

* **列表操作** ：`list`、`first`、`last`、`uniq`、`sortAlpha`

* **字典操作** ：`dict`、`get`、`set`、`hasKey`、`pluck`

* **流程控制** ：`ternary`、`default`、`empty`、`coalesce`

* **类型转换** ：`toString`、`toJson`、`toPrettyJson`、`toRawJson`

* **编码/解码** ：`b64enc`、`b64dec`、`urlquery`、`urlqueryescape`

* **UUID 生成** ：`uuidv4`

有关所有可用函数的完整参考，请参阅 [Helm 函数文档](https://helm.sh/docs/chart_template_guide/function_list/)，因为 GJSON Template 包含了相同的函数集。

### GJSON 路径语法

GJSON 提供了强大的 JSON 查询能力：

* **点表示法** ：`address.city`

* **数组索引** ：`users.0.name`

* **数组迭代** ：`users.#.name`

* **数组过滤** ：`users.#(age>=30)#.name`

* **修饰符** ：`users.@reverse.#.name`

* **多路径** ：`{name:users.0.name,count:users.#}`

* **转义字符** ：`path.with\.dot`

对于更复杂的查询，可以使用 `gjson` 函数：

```
HELPCODEESCAPE-plaintext
<!-- 使用 gjson 函数进行复杂查询 -->
活跃用户: {{gjson "users.#(active==true)#.name"}}

<!-- 带有多个条件的数组过滤 -->
30岁以上的活跃开发者: {{gjson "users.#(active==true && age>30)#.name"}}

<!-- 使用修饰符 -->
用户名（倒序）: {{gjson "users.@reverse.#.name"}}

<!-- 迭代过滤结果 -->
管理员:
{{range $user := gjson "users.#(roles.#(==admin)>0)#"}}
 - {{$user.name}} ({{$user.age}})
{{end}}
```

完整的 GJSON 路径语法参考可查看 [GJSON 文档](https://github.com/tidwall/gjson#path-syntax)。

## 配置示例
### 使用内置 MCP 服务器示例：配置 quark-search

```
HELPCODEESCAPE-yaml
server:
  name: "quark-search"
  config:
    apiKey: "xxxx"
```

此配置使用了 Higress 内置的 quark-search MCP 服务器。在这种情况下，只需要指定服务器名称和必要的配置（如 API 密钥），无需配置 tools 字段，因为工具已经在服务器中预定义好了。

### 基础配置示例：转换高德地图 API

```
HELPCODEESCAPE-yaml
server:
  name: HTTP-amap-server
  config:
    apiKey: your-api-key-here
tools:
  - name: maps-geo
    description: "将详细的结构化地址转换为经纬度坐标。支持对地标性名胜景区、建筑物名称解析为经纬度坐标"
    args:
      - name: address
        description: "待解析的结构化地址信息"
        type: string
        required: true
      - name: city
        description: "指定查询的城市"
        type: string
        required: false
      - name: output
        description: "输出格式"
        type: string
        enum: ["json", "xml"]
        default: "json"
    requestTemplate:
      url: "https://HTTPapi.amap.com/v3/geocode/geo"
      method: GET
      argsToUrlParam: true
      headers:
        - key: x-api-key
          value: "{{.config.apiKey}}"
    responseTemplate:
      body: |
        # 地理编码信息
        {{- range $index, $geo := .geocodes }}
        ## 地点 {{add $index 1}}

        - **国家**: {{ $geo.country }}
        - **省份**: {{ $geo.province }}
        - **城市**: {{ $geo.city }}
        - **城市代码**: {{ $geo.citycode }}
        - **区/县**: {{ $geo.district }}
        - **街道**: {{ $geo.street }}
        - **门牌号**: {{ $geo.number }}
        - **行政编码**: {{ $geo.adcode }}
        - **坐标**: {{ $geo.location }}
        - **级别**: {{ $geo.level }}
        {{- end }}
```

此配置将高德地图的地理编码 API 转换为 AI 可调用的工具。当 AI 调用此工具时：

1. 使用提供的地址和城市参数构建 API 请求。

2. 调用高德地图 API。

3. 将 JSON 响应转换为易于阅读的 Markdown 格式。

4. 将格式化后的结果返回给 AI 助手。

### 高级配置示例：带有条件逻辑的复杂响应处理

````
HELPCODEESCAPE-yaml
server:
  name: weather-api-server
  config:
    apiKey: your-weather-api-key
tools:
  - name: get-weather
    description: "获取指定城市的天气预报信息"
    args:
      - name: city
        description: "城市名称"
        type: string
        required: true
      - name: days
        description: "天数(1-7)"
        type: integer
        required: false
        default: 3
      - name: include_hourly
        description: "是否包含每小时预报"
        type: boolean
        default: true
    requestTemplate:
      url: "https://api.weatherapi.com/v1/forecast.json"
      method: GET
      argsToUrlParam: true
      headers:
        - key: x-api-key
          value: "{{.config.apiKey}}"
    responseTemplate:
      body: |
        # {{.location.name}}, {{.location.country}} 天气预报

        **当前温度**: {{.current.temp_c}}°C
        **体感温度**: {{.current.feelslike_c}}°C
        **天气状况**: {{.current.condition.text}}
        **湿度**: {{.current.humidity}}%
        **风速**: {{.current.wind_kph}} km/h

        ## 未来预报
        {{range $index, $day := .forecast.forecastday}}
        ### {{$day.date}} ({{dateFormat "Monday" $day.date_epoch | title}})

        {{if gt $day.day.maxtemp_c 30}}**高温预警!**{{end}}
        {{if lt $day.day.mintemp_c 0}}**低温预警!**{{end}}

        - **最高温度**: {{$day.day.maxtemp_c}}°C
        - **最低温度**: {{$day.day.mintemp_c}}°C
        - **降水概率**: {{$day.day.daily_chance_of_rain}}%
        - **天气状况**: {{$day.day.condition.text}}

        #### 分时预报
        {{range $hour := slice $day.hour 6 24 3}}
        - **{{dateFormat "15:04" $hour.time_epoch}}**: {{$hour.temp_c}}°C, {{$hour.condition.text}}
        {{end}}
        {{end}}
```
````

此示例展示了：

* 使用条件语句（`if`）进行温度警告。

* 使用日期格式化函数 (`dateFormat`)。

* 使用数组切片（`slice`）选择特定时间的天气。

* 嵌套循环遍历多天和多时段的天气数据。

### 使用 PrependBody 和 AppendBody 的示例：OpenAPI 转换

当您想保留原始 API 响应但添加额外的上下文信息时，`prependBody` 和 `appendBody` 字段非常有用。这在将 OpenAPI/Swagger 规范转换为 MCP 工具时特别有价值，因为您可以保留原始 JSON 响应，同时为 AI 助手提供字段含义的说明。

```
HELPCODEESCAPE-yaml
server:
  name: product-api-server
  config:
    apiKey: your-api-key-here
tools:
  - name: get-product
    description: "获取产品详细信息"
    args:
      - name: product_id
        description: "产品ID"
        type: string
        required: true
    requestTemplate:
      url: "https://api.example.com/products/{{.args.product_id}}"
      method: GET
      headers:
        - key: Authorization
          value: "Bearer {{.config.apiKey}}"
    responseTemplate:
      prependBody: |
        # 产品信息

        以下是产品的详细信息，以JSON格式返回。字段说明：

        - **id**: 产品唯一标识符
        - **name**: 产品名称
        - **description**: 产品描述
        - **price**: 产品价格（美元）
        - **category**: 产品类别
        - **inventory**: 库存信息
        - **quantity**: 当前库存数量
        - **warehouse**: 仓库位置
        - **ratings**: 用户评分列表
        - **score**: 评分（1-5）
        - **comment**: 评论内容
      appendBody: |

        您可以使用这些信息来了解产品的详细信息、价格、库存状态和用户评价。
```

此示例展示了：

* 使用 `prependBody` 在原始 JSON 响应前添加字段说明。

* 使用 `appendBody` 在响应末尾添加使用建议。

* 保留原始 JSON 响应，使 AI 助手可以直接访问所有数据。

## 模板语法
模板使用 GJSON Template 语法（<https://github.com/higress-group/gjson_template>），该语法结合 Go 模板和 GJSON 路径语法处理 JSON。模板引擎支持：

1. 基本点表示法访问字段：{{.fieldName}}。

2. 用于复杂查询的 gjson 函数：{{gjson "users.#(active==true)#.name"}}。

3. 所有 Sprig 模板函数（类似 Helm）：{{add}}、{{upper}}、{{lower}}、{{date}} 等。

4. 控制结构：{{if}}、{{range}}、{{with}} 等。

5. 变量赋值：{{$var := .value}}。

对于复杂 JSON 响应，可利用 GJSON 的过滤和查询能力提取关键信息。

## AI 提示词生成模板
在与 AI 助手一起生成 HTTP to MCP 配置的模板时，您可以使用以下提示词：

````
HELPCODEESCAPE-yaml
请帮我创建一个 Higress 的 HTTP-to-MCP 配置，将 HTTP API 转换为 MCP 工具。

## 配置格式
配置应遵循以下格式：
```yaml
server:
  name: HTTP-api-server
  config:
    apiKey: 您的API密钥
tools:
  - name: tool-name
    description: "详细描述这个工具的功能"
    args:
      - name: arg1
        description: "参数1的描述"
        type: string
        required: true
        position: path
      - name: arg2
        description: "参数2的描述"
        type: integer
        required: false
        default: 10
        position: query
      - name: arg3
        description: "参数3的描述"
        type: array
        items:
          type: string
        position: body
      - name: arg4
        description: "参数4的描述"
        type: object
        properties:
          subfield1:
            type: string
          subfield2:
            type: number
    requestTemplate:
      url: "https://api.example.com/endpoint"
      method: POST
      # 以下四个选项互斥，只能选择其中一种
      argsToUrlParam: true  # 将参数添加到URL查询参数
      # 或者
      # argsToJsonBody: true  # 将参数作为JSON对象发送到请求体
      # 或者
      # argsToFormBody: true  # 将参数以表单编码发送到请求体
      # 或者
      # body: |
      #   {
      #     "param1": "{{.args.arg1}}",
      #     "param2": {{.args.arg2}},
      #     "complex": {{toJson .args.arg4}}
      #   }
      headers:
        - key: x-api-key
          value: "{{.config.apiKey}}"
    responseTemplate:
      # 以下三个选项互斥，只能选择其中一种
      body: 
|
 # 结果
 {{- range $index, $item := .items }}
 ## 项目 {{add $index 1}}
 - **名称**: {{ $item.name }}
 - **值**: {{ $item.value }}
 {{- end }}
 # 或者
 # prependBody: |
 #   # API响应说明
 #
 #   以下是原始JSON响应，字段含义如下：
 #   - field1: 字段1的含义
 #   - field2: 字段2的含义
 #
 # appendBody: |
 #
 #   您可以使用这些数据来...
````

### 我的 API 信息

我想转换的 HTTP API 是：\[在此描述您的 API，包括端点、参数和响应格式，或者粘贴 Swagger/OpenAPI 规范\]。

```
HELPCODEESCAPE-plaintext
请根据以上信息生成一个完整的配置，包括：
1. 具有描述性名称和适当的服务器配置。
2. 定义所有必要的参数，并提供清晰的描述和适当的类型、必填/默认值。
3. 选择合适的参数传递方式（argsToUrlParam、argsToJsonBody、argsToFormBody 或自定义 body）。
4. 创建将 API 响应转换为适合 AI 消费的可读格式的 responseTemplate。
```

## 注意事项
### YAML中tools\[\].args的填写规范

`tools[].args`参数用于定义AI网关在接收MCP请求参数后，将其转换并组装为HTTP请求的规范，具体描述了发送至后端服务的HTTP请求中各参数的属性，包括参数类型、参数位置（如路径、请求头、请求体）以及是否为必填参数。

### AI网关在转换时参数取值位置

AI网关接收到MCP请求后，将根据MCP协议规范从请求体对应位置提取参数，暂不支持从其余位置（如请求头，请求体中其他位置）提取参数。

<br />