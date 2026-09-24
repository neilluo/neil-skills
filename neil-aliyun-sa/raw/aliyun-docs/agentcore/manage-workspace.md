---
source_url: https://help.aliyun.com/zh/agentcore/manage-workspace
fetch_date: 2026-09-20
product: AgentCore
slug: manage-workspace
body_sha256: d1c5a1292b8bb789c8a3c776c6c3a10f49bf88c5b1d34bce4d5261dbc94caabe
body_bytes: 1411
migration_status: current   # 见 FETCH-CONTRACT §3
---

Workspace 是 AgentCore 中资源隔离和管理的基本单元，模型连接、Agent、Team、Skill、MCP 工具和凭证等资源均归属于某个 Workspace。本文介绍如何创建和切换 Workspace。

## **创建Workspace**
开通 AgentCore 服务时需创建一个 Workspace，开通完成后即可直接使用；后续可根据需要创建更多。

1. 登录 [AgentCore](https://agentcore.console.aliyun.com/)控制台。

2. 点击页面左上角下拉列表框。

3. 在弹出的菜单中，点击**创建Workspace**。

4. 配置Workspace名称。

5. 选择是否绑定VPC，并配置：

   <table> <thead> <tr> <td> <p>参数</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>绑定 VPC</p> </td> <td> <p>是否为 Workspace 配置私有网络资源。关闭时不展示以下参数；打开后需完成 VPC 与交换机配置。</p> </td> </tr> <tr> <td> <p>VPC</p> </td> <td> <p>必填。选择 Workspace 使用的专有网络。</p> </td> </tr> <tr> <td> <p>交换机</p> </td> <td> <p>必填。选择 VPC 后可选。</p> </td> </tr> </tbody> </table>  
   **说明**

   需选择至少 2 个交换机，并确保覆盖至少 2 个不同可用区。
6. 点击**创建**以完成创建。

## 切换Workspace
1. 点击页面左上角下拉列表框。

2. 在弹出的列表中，选择需要进入的Workspace并点击。