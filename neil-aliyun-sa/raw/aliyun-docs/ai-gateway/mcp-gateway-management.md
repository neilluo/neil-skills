---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/mcp-gateway-management
fetch_date: 2026-09-21
product: AI Gateway
slug: mcp-gateway-management
body_sha256: ec7aa8c726c3d0c4da7d7c0ec7c19d68f876dc7c64d793eccb588ab9d2730382
body_bytes: 6094
migration_status: current
---

MCP网关提供MCP服务的管理。MCP（Model Context Protocol）是一项开源协议，旨在标准化应用程序向大语言模型提供上下文的方式，类似于为AI应用提供了一个"USB-C接口"，以便模型能够灵活、安全地连接各种数据源和工具。本文主要介绍了如何创建网关托管MCP服务。  

## 功能描述
MCP服务管理提供RESTful API至MCP服务的平滑迁移能力，支持SSE、Streamable HTTP两种协议访问，并集成基于消费者身份的鉴权认证机制，为企业级API治理提供技术支撑。

此外，MCP 支持直接代理模式 ，适用于原生支持 MCP 协议的服务。该模式能够实现高效的流式通信和上下文保持，特别适合高并发、长连接的场景，例如 AI 推理、多模型协同等。

同时，MCP 还可与 Nacos Registry 深度集成，通过 Nacos 提供的 MCP Router 功能，实现服务注册发现及协议自动转换，支持存量 HTTP 服务"零改动"升级为 MCP 协议接口，结合 Higress AI 网关实现服务的动态治理与智能路由。

## 创建网关托管MCP服务
1. 在AI 网关控制台的[实例](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)页面，选择您实例所在的地域。

2. 进入目标实例页面，选择左侧导航栏的**MCP管理**。

3. 单击**创建MCP服务**，AI 网关提供了以下两种服务协议创建MCP服务：

   * 若后端为MCP Server，则选择MCP协议；

   * 若后端为HTTP Server，则选择HTTP转MCP协议。

   ## MCP直接代理
   ----------

   选择MCP服务协议配置：
   1. **后端服务：**

      1. 选择**服务名称** 并选择**服务协议**为MCP。

      2. 按需选择**MCP Transport**，支持SSE和Streamable HTTP两种传输协议。

      3. 填写路径，路径是实际的后端mcp server的访问path。比如后端mcp server访问端点是xxx.com/sse，路径就填/sse；如果是xxx.com/test/sse，路径就填/test/sse。

   2. **MCP接入点：**

      1. 选择访问MCP 服务使用的域名，支持选择多个域名。

      2. MCP接入点的路径是通过/mcp-servers、/MCP服务名称以及实际的后端MCP Server的访问path拼接成的。创建完成后，进入当前MCP服务的基础信息页面，您可以在**step 1. 生成URL**区域查看实际的访问端点地址。

   创建成功后，MCP服务卡片上会有直接代理的标识。

   ## HTTP转MCP
   -----------

   选择HTTP服务协议配置：
   1. **后端服务：**

      1. 选择**服务名称** 并选择**服务协议**为HTTP。若您没有创建服务，需要新建服务，建议您使用FC或者DNS这类服务进行测试。

      2. 填写描述，描述是必填项，该字段表示MCP工具的功能用途，以提升API的可理解性和AI处理的准确性。

   2. **MCP接入点：**

      1. 选择访问MCP 服务使用的域名，支持选择多个域名。

      2. MCP接入点的路径 (SSE)是通过/mcp-servers、/MCP服务名称以及/sse拼接而成。

      3. MCP接入点的路径 (Streamable HTTP)是通过/mcp-servers和MCP服务名称拼接成的。

   创建成功后，MCP服务卡片上会有直接代理或者HTTP转MCP的标识。

   ### 为MCP服务添加工具

   在创建成功后，您还可以为其添加工具，操作步骤如下：
   1. 单击目标服务卡片，然后单击**添加工具**。

   2. MCP服务目前支持两种添加工具的方式：

      ##### **方式一：基于Swagger文件（推荐使用）**

      1. **导入Swagger，创建或增量更新MCP工具** ：从本地上传OpenAPI文件或将API定义粘贴到编辑框内，然后单击**立即生成**。

      2. **更新及确认MCP工具列表**：可以看到生成的MCP工具描述文件，可以进一步确认及修改其中的信息。

      3. （可选）开启后端服务认证：可以添加认证鉴权配置。认证方式配置说明如下：

         <table> <thead> <tr> <td> <p><b>参数</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>Basic</b></p> </td> <td> <p>将用户名和密码以username: password的形式进行Base64编码后，放在HTTP请求头的Authorization字段中发送。</p> </td> </tr> <tr> <td> <p><b>Bearer</b></p> </td> <td> <p>客户端先通过登录接口获取一个令牌，通常是JWT。以后每次请求都在Authorization头中带上该令牌。令牌通常是临时的，可以设置有效期。</p> </td> </tr> <tr> <td> <p><b>API Key</b></p> </td> <td> <p>由服务端分配给客户端一个唯一字符串作为访问凭据，客户端在每次请求时通过Header或Query参数提交。</p> </td> </tr> </tbody> </table>

      ##### **方式二：**自定义YAML

      1. 您可以通过自定义YAML手动创建MCP工具，详细配置详情，请参见[HTTP to MCP 配置字段参考](https://help.aliyun.com/document_detail/2932676.html)。

      2. 单击**YAML示例**，您可以针对生成的YAML示例进行修改。

      3. （可选）开启后端服务认证：可以添加认证鉴权配置。认证方式配置说明如下：

         <table> <thead> <tr> <td> <p><b>参数</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>Basic</b></p> </td> <td> <p>将用户名和密码以username: password的形式进行Base64编码后，放在HTTP请求头的Authorization字段中发送。</p> </td> </tr> <tr> <td> <p><b>Bearer</b></p> </td> <td> <p>客户端先通过登录接口获取一个令牌，通常是JWT。以后每次请求都在Authorization头中带上该令牌。令牌通常是临时的，可以设置有效期。</p> </td> </tr> <tr> <td> <p><b>API Key</b></p> </td> <td> <p>由服务端分配给客户端一个唯一字符串作为访问凭据，客户端在每次请求时通过Header或Query参数提交。</p> </td> </tr> </tbody> </table>
   3. 单击**确认** ，可以在**工具**页签看到工具列表及工具描述信息。