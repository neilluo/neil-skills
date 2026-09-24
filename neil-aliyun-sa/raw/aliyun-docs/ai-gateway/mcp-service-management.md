---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/getting-started/mcp-service-management
fetch_date: 2026-09-21
product: AI Gateway
slug: mcp-service-management
body_sha256: 0c9cc817ea326b2f329820193080c71a7779ded6ece84fa4427f1ed8f58e7007
body_bytes: 11442
migration_status: current
---

MCP（Model Context Protocol）是一项开源协议，旨在标准化应用程序向大语言模型（LLM）提供上下文的方式，类似于为AI应用提供了一个"USB-C接口"，以便模型能够灵活、安全地连接各种数据源和工具。本文主要介绍了如何创建及使用MCP服务。  

## 功能描述
MCP服务管理提供RESTful API至MCP服务的平滑迁移能力，支持SSE、Streamable HTTP两种协议访问，并集成基于消费者身份的鉴权认证机制，为企业级API治理提供技术支撑。

此外，MCP 支持直接代理模式 ，适用于原生支持 MCP 协议的服务。该模式能够实现高效的流式通信和上下文保持，特别适合高并发、长连接的场景，例如 AI 推理、多模型协同等。

同时，MCP 还可与 Nacos Registry 深度集成，通过 Nacos 提供的 MCP Router 功能，实现服务注册发现及协议自动转换，支持存量 HTTP 服务"零改动"升级为 MCP 协议接口，结合 Higress AI 网关实现服务的动态治理与智能路由。

## 创建网关托管MCP服务
1. 在AI 网关控制台的[实例](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)页面，选择您实例所在的地域。

2. 进入目标实例页面，选择左侧导航栏的**MCP 管理**。

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

      3. （可选）开启后端服务认证：可以添加认证鉴权配置。认证方式配置说明如下。

      <table> <thead> <tr> <td> <p><b>参数</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>Basic</b></p> </td> <td> <p>将用户名和密码以username: password的形式进行Base64编码后，放在HTTP请求头的Authorization字段中发送。</p> </td> </tr> <tr> <td> <p><b>Bearer</b></p> </td> <td> <p>客户端先通过登录接口获取一个令牌，通常是JWT。以后每次请求都在Authorization头中带上该令牌。令牌通常是临时的，可以设置有效期。</p> </td> </tr> <tr> <td> <p><b>API Key</b></p> </td> <td> <p>由服务端分配给客户端一个唯一字符串作为访问凭据，客户端在每次请求时通过Header或Query参数提交。</p> </td> </tr> </tbody> </table>

      ##### **方式二：**自定义YAML

      1. 您可以通过自定义YAML手动创建MCP工具。

      2. 单击**YAML示例**，您可以针对生成的YAML示例进行修改。

      3. （可选）开启后端服务认证：可以添加认证鉴权配置。认证方式配置说明如下。

      <table> <thead> <tr> <td> <p><b>参数</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>Basic</b></p> </td> <td> <p>将用户名和密码以username: password的形式进行Base64编码后，放在HTTP请求头的Authorization字段中发送。</p> </td> </tr> <tr> <td> <p><b>Bearer</b></p> </td> <td> <p>客户端先通过登录接口获取一个令牌，通常是JWT。以后每次请求都在Authorization头中带上该令牌。令牌通常是临时的，可以设置有效期。</p> </td> </tr> <tr> <td> <p><b>API Key</b></p> </td> <td> <p>由服务端分配给客户端一个唯一字符串作为访问凭据，客户端在每次请求时通过Header或Query参数提交。</p> </td> </tr> </tbody> </table>
   3. 单击**确认** ，可以在**工具**页签看到工具列表及工具描述信息。

## 同步Nacos MCP服务
### 前提条件

* 目前只支持注册在MSE Nacos铂金版3.0及以上版本中的MCP服务同步到AI网关。

  * 升级网关引擎版本至2.1.6及以上。  
  1. 在AI 网关控制台的[实例](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)页面，选择您实例所在的地域。

  2. 进入目标实例页面，在**基本信息** 页签的**运行信息** 区域，查看网关**引擎版本**。

  3. （可选）如果不是最新版，可单击**升级至新版本**，升级到最新版。

  > 网关升级过程大约需要持续 5\~10 分钟。升级过程对短连接无损，对长连接可能会有重建过程。建议在业务低峰期执行此操作。

### 操作步骤

Nacos铂金版创建的服务类型为HTTP转化MCP的MCP服务和标准MCP服务的同步操作相同，具体操作如下所示：

1. 在AI 网关控制台的[实例](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)页面，选择您实例所在的地域。

2. 进入目标实例页面，选择左侧导航栏的**MCP 管理**。

3. 单击**同步 Nacos MCP 服务** ，选择您创建的MSE Nacos类型的[服务来源](https://help.aliyun.com/document_detail/2881570.html)。

4. 选择MCP服务所在的**Nacos 命名空间**，然后选择访问MCP 服务使用的域名，支持选择多个域名。

5. 在选择需要同步的**Nacos MCP 服务** 时，您可以通过**协议类型**区分它的后端类型。

   * mcp-sse：后端是SSE类型mcp server。

   * mcp-streamable：后端是streamable类型的mcp server。

   * http：Nacos上HTTP服务转MCP类型。

6. 同步成功后，MCP服务卡片上除了有直接代理或者HTTP转MCP的标识外，还会新增Nacos托管标识。

## 消费者认证
1. 在AI 网关控制台的[实例](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)页面，选择您实例所在的地域。

2. 进入目标实例页面，选择左侧导航栏的**MCP 管理**。

3. 单击目标服务卡片，然后单击**消费者认证**页签。

4. 单击**配置信息** 右侧的**编辑** ，开启**启用状态** 。配置相关参数后，单击**确认** **。**

   **重要**

   开启消费者认证后，若没有配置授权关系，将无法访问当前API。
   <table> <thead> <tr> <td> <p><b>配置项</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>启用状态</b></p> </td> <td> <p>开启或关闭消费者授权开关，默认关闭。</p> </td> </tr> <tr> <td> <p><b>认证方式</b></p> </td> <td> <p>消费者授权的认证方式目前仅支持<b>API Key</b>认证。</p> <blockquote> API Key是一种简单的认证方式，客户端访问时，需将凭证以指定的方式添加至请求中，网关收到请求后会验证API Key的合法性及权限。 </blockquote> </td> </tr> </tbody> </table>
5. 单击**授权** 并选择消费者，然后单击**添加**。

   若没有消费者，您可单击**消费者** 右侧的选择框，并在下拉列表中单击[创建消费者](https://help.aliyun.com/document_detail/2882031.html)进行创建。

## 调试MCP服务
### 通过控制台直接调试Nacos mcp server

1. 在**MCP管理**页面，单击目标MCP服务卡片。

2. 单击**调试**页签，会在控制台自动跟后端mcp server建立连接。同时您可以在控制台查看连接建立状态，如果连接失败会有对应的文案提示。建立连接失败的常见原因如下：

   * 如果使用的是AI网关提供的测试域名，存在调用限额，每天整个域名限额1000次。

   * 如果使用的是自定义域名，需要确保此域名在公网可解析，且此域名解析的地址公网可达。

   * 如果开启了消费者鉴权，请确保使用的认证信息正确。

3. 如果开启了消费者认证，需要选择对应已授权消费者作为请求参数传入。

4. 单击**获取工具**，选择您需要使用的工具，填入工具参数即可在线调试。

### 通过MCP Inspector调试MCP服务

**说明**

建议在本地启动MCP Inspector进行MCP调试。

MCP Inspector是MCP社区提供的调试工具，可用于MCP服务全流程的调试。

1. [安装Node.js环境](https://nodejs.org/zh-cn/download)。

2. 执行MCP Inspector安装命令：`npx @modelcontextprotocol/inspector node build/index.js`。

3. 访问MCP Inspector界面，例如通过浏览器登录以下地址：`http://127.0.0.1:6274`。

   ```
   HELPCODEESCAPE-text
   Need to install the following packages:
   @modelcontextprotocol/inspector@0.13.0
   Starting MCP inspector...
   ⬡⬡ Proxy server listening on port 6277
   ◇ MCP Inspector is up and running at http://127.xxx.1:6274 ◇
   ```

4. 配置连接信息。

   1. 选择传输类型：`Transport Type`选择`SSE`。

   2. 输入`URL`地址：在MCP管理的**基本信息**页右侧获取。

   3. （可选）若配置了消费者认证，单击`Authentication`安装展开授权配置，并填写消费者身份对应的Token。以以下凭证配置为例，`Header Name`为 `Authorization`不需要修改，在`Bearer Token`中填入 `HereIsToken`。

5. 单击`Connect`进行连接，连接成功后可以看到中间出现`List Tools`按钮，单击`List Tools`获取MCP服务的所有工具。

6. （可选）若要调试具体的工具，点击工具名称，在右侧填写必要的参数，并单击`Run Tool`进行工具调用调试。