---
source_url: https://help.aliyun.com/zh/agentcore/managing-the-mcp-server
fetch_date: 2026-09-20
product: AgentCore
slug: managing-the-mcp-server
body_sha256: 30077fba47fde74c03b11063967e800372a70d197a6186794e3dbde64fd420d1
body_bytes: 3719
migration_status: current   # 见 FETCH-CONTRACT §3
---

构建智能体应用时，Agent 常需要调用外部工具或访问第三方数据源来完成复杂任务。通过为Workspace配置 MCP（Model Context Protocol）Server，可以为 Agent 扩展标准化的工具集成能力，对接各类外部服务。本文介绍如何创建、查看、编辑和删除 MCP 服务。  

## **创建并管理MCP Server**
1. 登录 [AgentCore](https://agentcore.console.aliyun.com/)控制台。

2. 在Workspace详情页左侧导航栏，点击**工具管理**。

3. 点击创建工具，配置以下信息。

   <table> <thead> <tr> <td> <p>参数</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>工具类型</p> </td> <td> <p>工具的类型。MCP：Model Context Protocol 工具，支持连接远程 MCP 服务和 HTTP 转 MCP。虚拟 MCP：将已有的 MCP 工具重新组装成新的 MCP 服务，提升工具选择效率，即将上线。</p> </td> </tr> <tr> <td> <p>创建方式</p> </td> <td> <p>工具类型为 MCP 时可选。连接 MCP 服务：对接已有的远程 MCP 服务。HTTP 转 MCP：将 HTTP 接口转换为 MCP 工具。</p> </td> </tr> <tr> <td> <p>工具名称</p> </td> <td> <p>工具的名称。</p> </td> </tr> <tr> <td> <p>描述</p> </td> <td> <p>工具的描述信息，不超过 1000 个字符。</p> </td> </tr> <tr> <td> <p>URL</p> </td> <td> <p>MCP 服务的访问地址，例如 mcp.example.com 或 127.0.0.1。请确保该地址网络可达。</p> </td> </tr> <tr> <td> <p>MCP Transport</p> </td> <td> <p>MCP 服务使用的传输协议，可选 SSE 或 Streamable HTTP。</p> </td> </tr> </tbody> </table>
4. 进行认证配置。

   <table> <thead> <tr> <td> <p>参数</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>启用认证</p> </td> <td> <p>是否为该工具启用认证。关闭时不展示认证参数；打开后需完成以下配置。</p> </td> </tr> <tr> <td> <p>认证方式</p> </td> <td> <p>认证使用的凭证类型，例如 API Key。</p> </td> </tr> <tr> <td> <p>凭证来源</p> </td> <td> <p>凭证在请求中的携带位置，例如自定义 HTTP header。</p> </td> </tr> <tr> <td> <p>Header 名称</p> </td> <td> <p>凭证来源为自定义 HTTP header 时需填写，即携带凭证的请求头名称，例如 Authorization、X-Api-Key。</p> </td> </tr> <tr> <td> <p>API Key</p> </td> <td> <p>凭证的取值，需按目标服务要求的格式填写，例如 Bearer 加空格加密钥。</p> </td> </tr> </tbody> </table>
5. 点击**立即创建**进行创建。

## 管理MCP工具
### 查看MCP工具详情

点击**详情**可以查看MCP工具配置。

#### **基本信息**

<table> <thead> <tr> <td> <p>字段</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>名称</p> </td> <td> <p>工具的名称。</p> </td> </tr> <tr> <td> <p>连接类型</p> </td> <td> <p>工具的连接类型，例如远程连接。</p> </td> </tr> <tr> <td> <p>描述</p> </td> <td> <p>工具的描述信息，未填写时显示\&nbsp;-。</p> </td> </tr> </tbody> </table>

#### **MCP 配置**

<table> <thead> <tr> <td> <p>字段</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>URL</p> </td> <td> <p>MCP 服务的访问地址。</p> </td> </tr> <tr> <td> <p>MCP Transport</p> </td> <td> <p>MCP 服务使用的传输协议，取值为 SSE 或 Streamable HTTP。</p> </td> </tr> </tbody> </table>

### 删除MCP工具

在概览页面，点击**删除**删除该MCP工具。

### 编辑MCP工具

在概览页面，点击编辑配置以编辑该工具。