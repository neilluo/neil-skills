---
source_url: https://help.aliyun.com/zh/agentteams/managing-the-mcp-server
fetch_date: 2026-09-20
product: AgentTeams
slug: managing-the-mcp-server
body_sha256: 2bde9737297723d1d8a2ea3c55546ed444df716fe5b8f912eae207bf9e5219fb
body_bytes: 2214
migration_status: migrated-legacy
---

<br />

构建智能体应用时，Worker 常需要调用外部工具或访问第三方数据源来完成复杂任务。通过为实例配置 MCP（Model Context Protocol）Server，可以为 Worker 扩展标准化的工具集成能力，对接各类外部服务。本文介绍如何创建、查看、编辑和删除 MCP 服务。

## **创建并管理MCP Server**
1. 登录 AgentTeams[控制台](https://agentteams.console.aliyun.com/)。

2. 在实例详情页左侧导航栏，点击**MCP Server**。

3. 点击**创建 MCP Server**，配置以下信息。

   <table> <thead> <tr> <td> <p><b>参数</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>名称</b></p> </td> <td> <p>MCP Server的名称。</p> </td> </tr> <tr> <td> <p><b>类型</b></p> </td> <td> <p>选择HTTP TO MCP，或者<b>直接代理</b>。</p> </td> </tr> <tr> <td> <p><b>启用认证</b></p> </td> <td> <p>选择是否启用认证，并配置<b>认证类型</b>和<b>凭证</b>。</p> </td> </tr> </tbody> </table>
   1. 对于HTTP TO MCP，配置以下信息。

      <table> <thead> <tr> <td> <p><b>参数</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>端点地址</b></p> </td> <td> <p>MCP Server的端点地址，需要确保该端点地址网络可达。</p> </td> </tr> <tr> <td> <p><b>Swagger 配置</b></p> </td> <td> <p>上传 Swagger 配置文件。</p> </td> </tr> </tbody> </table>
   2. 对于**直接代理**，配置以下信息。

      <table> <thead> <tr> <td> <p><b>参数</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>URL</b></p> </td> <td> <p>MCP Server的URL，需要确保该URL网络可达。</p> </td> </tr> <tr> <td> <p><b>MCP Transport</b></p> </td> <td> <p>选择协议类型为SSE或Streamable HTTP。</p> </td> </tr> </tbody> </table>
4. 点击**创建**。

5. 在**MCP Server**页面，查看已创建的MCP Server条目。

   1. 点击右侧的**编辑**，可以编辑信息。

   2. 点击右侧的**删除**，可以删除已创建的MCP Server条目。