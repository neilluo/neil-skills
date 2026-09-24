---
source_url: https://help.aliyun.com/zh/agentcore/manage-connectors
fetch_date: 2026-09-20
product: AgentCore
slug: manage-connectors
body_sha256: 28b4dab184e41754ff06376bf7e8c4801329682fc29cb2ff61d1ab84f9937a9a
body_bytes: 2058
migration_status: current   # 见 FETCH-CONTRACT §3
---

连接器用于将其它 Agent 集成到 AgentCore，集成后由 AgentCore 统一托管。本文介绍如何启用连接器并查看连接器状态。  

## 连接器概述
AgentCore 支持通过连接器集成其它 Agent 平台，集成后的 Agent 由 AgentCore 统一托管。当前支持集成 Qoder CLI，即托管 Qoder 类型的 Agent。集成后创建和管理 Agent 的具体操作请参见[管理 Agent](https://help.aliyun.com/document_detail/3052293.html)。

在**连接器** 页面，可以查看当前 Workspace 支持的连接器及其启用状态（**未启用** 或**已启用** ）。Workspace 的创建和管理具体操作请参见[管理 Workspace](https://help.aliyun.com/document_detail/3052311.html)。

## 启用连接器
1. 登录 [AgentCore](https://agentcore.console.aliyun.com/) 控制台。

2. 在 Workspace 详情页左侧导航栏，点击**连接器**。

3. 在**连接器** 页面，找到目标连接器（例如 **Qoder CLI** ），单击**启用**。

4. 在**启用 Qoder CLI**对话框中，配置以下参数。

   <table> <thead> <tr> <td><p><b>参数</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>站点</b></p></td> <td><p>被集成 Qoder 账号所属的站点，支持<b>中国站</b>和<b>国际站</b>。</p></td> </tr> <tr> <td><p><b>组织 ID</b></p></td> <td><p>要集成的 Qoder 组织 ID。</p></td> </tr> <tr> <td><p><b>API 密钥</b></p></td> <td><p>Qoder 控制台的 API 密钥，用于换取 Qoder 访问凭证（SAT）。配置后加密存储于工作空间 Vault。</p></td> </tr> <tr> <td><p><b>服务账号</b></p></td> <td><p>AgentCore 访问 Qoder 所使用的服务账号，包括<b>账号名称</b>和<b>凭证</b>。单击<b>新增服务账号</b>可以添加多个服务账号。</p></td> </tr> </tbody> </table>
5. 单击**连通性校验**，确认配置的站点、组织 ID、API 密钥和服务账号可用。

6. 单击**启用** 。启用完成后，连接器卡片的状态更新为**已启用**。