---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/debug-mcp-services
fetch_date: 2026-09-21
product: AI Gateway
slug: debug-mcp-services
body_sha256: b52b2abef5e915b9236d27d36f1497a4ab07f2aa5ca7cd3d56d1077efe2b181c
body_bytes: 3322
migration_status: current
---

本文介绍如何通过控制台和MCP Inspector调试MCP服务。  

## **通过控制台调试MCP服务**
1. 在AI 网关控制台的[实例](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)页面，选择您实例所在的地域。

2. 进入目标实例页面，选择左侧导航栏的**MCP管理**。

3. 在**MCP 管理**页面，单击目标MCP服务卡片。

4. 单击**调试**页签，控制台会自动跟后端MCP Server建立连接，同时您可以在控制台查看连接建立状态。

   **说明**

   如果连接失败会有对应的错误提示，建连失败的常见原因如下：
   * 如果使用的是AI网关提供的测试域名，存在调用限额，每天整个域名限额1000次。

   * 如果使用的是自定义域名，需要确保此域名在公网可解析，且此域名解析的地址公网可达。

   * 如果开启了消费者鉴权，请确保使用的认证信息正确。

   * 不支持内网域名调试。

   * Serverless 版 **AI 网关** 实例需通过 **NAT 网关** 配置 **SNAT** 才能访问公网。请在 **NAT 网关** 控制台为网关实例所在 **VPC** 的**交换机** 网段添加 **SNAT** 条目并关联 **EIP**，配置完成后重试 MCP 调试。

5. 如果开启了消费者认证，需要选择对应已授权消费者作为请求参数传入。

6. 单击**获取工具**，选择您需要使用的工具，填入工具参数即可在线调试。

   > 如果所选消费者只授权了 [MCP工具级别消费者认证](https://help.aliyun.com/document_detail/2930333.html#4e9068601f0vw)，且仅授权某些工具的情况下，HTTP转MCP的场景中获取工具列表只能看到和调用有权限的工具；直接代理场景调试的时候能看到全部工具，选择授权的工具调用是ok的，没权限的会403。

## 通过MCP Inspector调试MCP服务
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
   npx @modelcontextprotocol/inspector node build/index.js
   Starting MCP inspector...
   ⬜⬜ Proxy server listening on port 6277
   ◇ MCP Inspector is up and running at http://127.xxx.1:6274 ◇
   ```

4. 配置连接信息。

   1. 选择传输类型：`Transport Type`选择`SSE`。

   2. 输入`URL`地址：在MCP管理的**基本信息**页右侧获取。

   3. （可选）若配置了消费者认证，单击`Authentication`安装展开授权配置，并填写消费者身份对应的Token。以如下凭证配置为例，`Header Name`为 `Authorization`不需要修改，在`Bearer Token`中填入 `HereIsToken`。

5. 单击`Connect`进行连接，连接成功后可以看到中间出现`List Tools`按钮，单击`List Tools`获取MCP服务的所有工具。

6. （可选）若要调试具体的工具，点击工具名称，在右侧填写必要的参数，并单击`Run Tool`进行工具调用调试。