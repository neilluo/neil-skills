<!-- source_url: https://www.volcengine.com/docs/6569/1816086 -->
<!-- fetched_date: 2026-09-21 -->
<!-- page_last_modified: 2026-07-21 -->
<!-- summary: 火山引擎 API 网关「MCP 服务」官方全文（经 getDocDetail API 取 Result.MDContent，绕开 SPA JS 壳）。关键取证点：MCP 服务类型含 HTTP 转 MCP / 直接访问 MCP；「HTTP 转换为 MCP 时，仅支持通过 Streamable HTTP 协议访问网关」；MCP Tools 由 Swagger/OpenAPI3 上传生成；自带鉴权为「开启身份认证」= Key Auth 插件（API Key），不是外部认证。 -->

> 文档标题：MCP 服务｜DocumentCode: MCPservice｜FirstPublishedTime: 2025-09-09T03:32:34Z｜UpdatedTime: 2026-07-21T03:05:28Z

MCP（Model Context Protocol）是一项开源协议，旨在标准化应用程序向大语言模型（LLM）提供上下文的方式，以便模型能够灵活、安全地连接各种数据源和工具。本文介绍在如何 API 网关中创建 MCP 服务。

<span id="qOMtbrTU"></span>
## 背景信息

MCP 协议用于简化大语言模型（LLM）与外部工具、API 和服务的交互。通过标准化接口，LLM 能够调用外部 API、运行脚本、访问数据库等，扩展了自身能力边界。MCP 的传输层支持多种协议，确保数据高效、安全传输。其典型应用场景包括智能助手与代理、企业级知识管理、开发者工具与 IDE 集成、多模态数据集成等。此外，MCP 还提供了交互式调试工具，帮助开发者高效测试和调试相关服务器与客户端。

同时，当前在企业内部存在大量的传统 HTTP 应用，虽然 MCP 提供了对应的 SDK，但是仍然需要开发适配的工作。如果能将这些应用转换为 MCP Server，将快速提升 AI Agent 与应用的交互能力。为解决上述问题，API 网关提供 MCP 服务功能，该功能提供 RESTful API 至 MCP 协议的平滑迁移能力，从而能够快速将现有  HTTP 应用转换为 MCP Server。

<span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_dc4a4acac32988fc9383ddf42a86b0bb.png) </span>

<span id="qOMtbrTU"></span>
## 前提条件


* 已创建 API 网关实例，详情请参见 [创建实例](https://www.volcengine.com/docs/6569/85693)。

* （可选）已创建服务，并绑定自定义域名。详情请参见 [创建服务](https://www.volcengine.com/docs/6569/85695)、[绑定自定义域名](https://www.volcengine.com/docs/6569/148261)。

* （可选）已创建消费者，并生成认证鉴权信息。详情请参见 [创建消费者](https://www.volcengine.com/docs/6569/1215179)、[生成认证信息](https://www.volcengine.com/docs/6569/1215181)。

* （可选）当后端服务为容器服务时，需要将待对接集群添加为 Upstream 来源，具体操作可参见 [导入容器集群](https://www.volcengine.com/docs/6569/133830)。


<span id="VMc9Zlo7"></span>
## 使用限制

HTTP 转换为 MCP 时，仅支持通过 Streamable HTTP 协议访问网关。

<span id="VMc9Zlo7"></span>
## 操作步骤


1. 登录 [API 网关控制台](https://console.volcengine.com/veapig)。

2. 在顶部导航栏，选择目标地域。

3. 在左侧导航栏选择 **MCP** **服务**，单击 创建 **MCP 服务**。

   * **基本信息**

   <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_0d64e5ec5c06a8078e531c5bc13e80f0.png) </span>

   
   |配置项 |说明 |
   |---|---|
   |所属实例 |在下拉菜单中选择 MCP 服务所属的网关实例。 |
   |访问域名 |配置 MCP 服务使用的域名，包括：<br><br><br>* **使用已有**：使用已创建服务的域名。当您选择该选项时，需要在弹出的下拉菜单中选择已创建的服务。<br><br>* **新建域名**：新建一个新域名。当您选择该选项时，系统会自动生成一个新域名，新域名的名称为`mcp-service-xxxx`，其中，`xxxx`为随机字符串。 |
   |MCP 服务名称 |配置 MCP 服务的名称，系统会使用该名称创建对应的路由。 |
   |MCP 服务类型 |不同类型的后端服务，支持不同的访问方式。包括：<br><br><br>* **HTTP 转 MCP**：若后端服务为 HTTP Server，则选择该选项。MCP Client 的访问报文会被转换为 HTTP 报文，然后使用 HTTP 协议访问 HTTP Server。<br><br>* **直接访问 MCP**：若后端服务为 MCP Server，则选择该选项。MCP Client 会直接访问后端 MCP Server。<br><br><br><div data-tips="true" data-tips-type="default">说明</div><br><br><br><div data-tips="true" data-tips-type="default">当访问方式选择 <strong>直接访问 MCP</strong> 时，MCP 服务会默认绑定 MCP 会话保持插件。详情请参见 <a href="https://www.volcengine.com/docs/6569/1584319">MCP 会话保持</a>。</div><br> |
   |MCP 传输类型 |当 **MCP 服务类型** 选择 **直接访问 MCP ** 时，需要配置 MCP 传输类型。当前仅支持 **Streamable HTTP**。 |
   |MCP 服务路径 |配置 MCP 服务的访问路径。 |
   

   * **后端配置**

   <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_149c98bd780dd779c27630d49234c50d.png) </span>

   
   |配置项 |说明 |
   |---|---|
   |后端服务 |配置  Upstream 对接的后端服务，包括：<br><br><br>* **选择已有 Upstream**：选择后端服务所在的云资源（容器服务、函数服务、云服务器等）和已存在的 Upstream。<br><br>* **新建 Upstream**：配置指定的后端服务 Upstream。不同类型 Upstream 的配置方式和参数解释，请参见 [Upstream 管理](https://www.volcengine.com/docs/6569/163236)。 |
   

4. 单击 **确定**，完成配置。


<span id="K39No00H"></span>
## 后续配置

<span id="IJfFKSYS"></span>
### 获取访问方式和示例


1. MCP 服务创建完成后，在服务列表中选择目标服务，单击服务名称，进入服务详情页面。

2. 选择 **基本信息** 页签，在 **调用示例** 中即可获得该 MCP 服务的调用域名和调用示例。

   <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_c398422560113fc26b5b8d981c9ff72b.png) </span>

   <div data-tips="true" data-tips-type="default" data-tips-is-title="true" data-wrapper-indent="1">说明   </div>
   

   <div data-tips="true" data-tips-type="default" data-wrapper-indent="1">如果您已安装 TRAE，可以单击 <strong>去 TRAE CN 配置</strong>，跳转至 TRAE 控制台进行快速配置。   </div>
   

<span id="aweTIQpy"></span>
### 开启认证鉴权


1. MCP 服务创建完成后，在服务列表中选择目标服务，单击服务名称，进入服务详情页面。

2. 选择 **基本信息** 页签，并开启 **身份认证** 功能。在弹出的配置页面中，使用 Key Auth 插件配置 API Key 认证鉴权。更多配置详情，请参见 [API Key 认证鉴权](https://www.volcengine.com/docs/6569/1515836)。

   <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_10d65c450957b70cdc7ab419e4df8de9.png) </span>


<span id="zMtRRXmF"></span>
### 添加 MCP Tools

<div data-tips="true" data-tips-type="default" data-tips-is-title="true">说明</div>


<div data-tips="true" data-tips-type="default">仅当 <strong>MCP 服务类型</strong> 选择 <strong>HTTP 转 MCP </strong>时，允许添加 MCP Tools。</div>


MCP 服务创建完成后，支持基于 Swagger 文件添加 MCP Tools。操作步骤如下：


1. MCP 服务创建完成后，在服务列表中选择目标服务，单击服务名称，进入服务详情页面。

2. 选择 MCP Tools 页签，单击 **上传 MCP 配置**。

   <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_4aa77f9ad0e4c2d680fccf4dd94a8326.png) </span>

3. 单击或拖拽文件到控制台，上传 MCP Tools 文件。

   <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_61b0ca91e251ff712e6214580051ecca.png) </span>

4. 单击 **确定**，完成配置。配置完成后，您可以在 MCP Tools 页面中查看已上传的工具详情。

   <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_c643b5168f0f9d3e7d55361c494de3e5.png) </span>


<span id="IvCbO52U"></span>
## 常见问题

<span id="OA4azxgS"></span>
### 如何上传正确的 MCP 配置文件


* 使用限制

   MCP 配置文件需要符合以下条件：

   
   |类型 |说明 |
   |---|---|
   |语法 |* 代码中不存在 Swagger/OpenAPI 3 语法错误。<br><br>* 代码中必须包含 Swagger/OpenAPI 3 元数据、title 和 version。<br><br>* 建议为每个 Opeartion 设置 operationId。 |
   |请求方法 |* 仅支持 GET、POST、PUT、DELETE、PATCH 。<br><br>* CONNECT、HEAD、OPTIONS 和 TRACE 等请求方法将被忽略。 |
   |请求类型 |* 支持 JSON（application/json）和 Form（application/x\-www\-form\-urlencoded）内容类型。<br><br>* 不支持 application/xml、multipart/form\-data 和 application/octet\-stream 等内容类型。 |
   |请求参数 |* Swagger<br><br>   * 参数的位置为 path、query、header 或 formData 时，array 类型的参数将序列化为逗号分隔值（CSV）。<br><br>   * 参数的数据类型不支持 file。<br><br>* OpenAPI 3.0<br><br>   * 参数的位置为 path、query、header 或 cookie 时，array 类型的参数将序列化为逗号分隔值（CSV）。 |
   |响应 |仅支持解析 200、201 和 default，且仅解析1个。同时存在时，解析的顺序为 200 \> 201 \> default。 |
   

* 代码示例

   JSON 格式的 POST 请求示例如下。

   * Swagger

   ```JSON
   {
     "swagger": "2.0",
     "info": {
       "title": "weather",
       "version": "1.0.0"
     },
     "paths": {
       "/weather/{city}": {
         "get": {
           "operationId": "weather",
           "summary": "Check weather status。",
           "consumes": ["application/json"],
           "parameters": [
             {
               "name": "city",
               "description": "City",
               "type": "string",
               "in": "path",
               "required": true
             },
             {
               "name": "body",
               "in": "body",
               "schema": {
                 "type": "object",
                 "properties": {
                   "date": {
                     "description": "Date",
                     "type": "string"
                   }
                 }
               }
             }
           ],
           "responses": {
             "200": {
               "description": "Weather status",
               "schema": {
                 "type": "object",
                 "properties": {
                   "weather": {
                     "description": "Weather",
                     "type": "string"
                   }
                 }
               }
             }
           }
         }
       }
     }
   }
   ```
   

* OpenAPI 3.0

   ```JSON
   {
     "openapi": "3.0.1",
     "info": {
       "title": "weather",
       "version": "1.0.0"
     },
     "paths": {
       "/weather/{city}": {
         "get": {
           "operationId": "weather",
           "summary": "check the weather",
           "parameters": [
             {
               "name": "city",
               "description": "city",
               "type": "string",
               "schema": {
                 "type": "string"
               },
               "in": "path",
               "required": true
             }
           ],
           "requestBody": {
             "content": {
               "application/json": {
                 "schema": {
                   "type": "object",
                   "properties": {
                     "date": {
                       "description": "Date",
                       "type": "string"
                     }
                   }
                 }
               }
             }
           },
           "responses": {
             "200": {
               "description": "weather",
               "content": {
                 "application/json": {
                   "schema": {
                     "type": "object",
                     "properties": {
                       "weather": {
                         "description": "weather",
                         "type": "string"
                       }
                     }
                   }
                 }
               }
             }
           }
         }
       }
     }
   }
   ```
