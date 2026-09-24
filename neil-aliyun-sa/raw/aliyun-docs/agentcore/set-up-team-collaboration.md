---
source_url: https://help.aliyun.com/zh/agentcore/set-up-team-collaboration
fetch_date: 2026-09-20
product: AgentCore
slug: set-up-team-collaboration
body_sha256: cee4716635e1d9bf35fd345ffacb9471231b5cf01b550f5410bdbba9c55e0bc2
body_bytes: 5923
migration_status: current
---

本文介绍如何管理、创建、查看、编辑和删除Team。  

## Team 简介
在复杂任务场景下，单个 Agent 往往难以独立完成全部工作。Team 协作支持将多个 Agent 组织为一个协作团队，并通过设置团队负责人（TL）进行统筹，让成员分工协同、共同完成任务，从而提升复杂任务的处理效率。本文介绍如何创建和管理 Team。

## 开通 Team 协作
Team 协作未开通时，在 Team 协作页面进行开通。

### 公网访问

可以通过开关开启/关闭公网访问。开启后，协作客户端可通过公网地址访问。

### VPC 接入

可以通过开关开启/关闭VPC 接入。开启后，协作客户端可通过 VPC 内网地址访问。开启后需选择 VPC 和交换机，请至少选择两个不同可用区的交换机，以保证协作服务的高可用。

公网访问和 VPC 接入至少开启一项。

完成配置后，点击**开通**。  
**重要**

开通协作功能需要购买协作管控面实例。开通时，系统会跳转到购买页，按页面提示创建实例。协作管控面实例按对应产品定价收费。

## 接入管理
### 网络配置

可以对**公网访问** 与**私网访问**分别进行开启/关闭。开启公网访问后，协作客户端可通过公网地址访问；开启私网访问后，协作客户端可通过所选 VPC 的私网地址访问。

公网访问和私网访问至少开启一项。若 Workspace 未绑定有效 VPC，则必须开启公网访问。

### 连接点

可以查看**协作客户端 (WEB)** （Web 控制台端点，提供可视化操作界面）和**协作客户端(API)**（API 接入端点，提供程序化访问接口）的公网及私网url。

## 团队管理
### 创建 Agent 团队

1. 登录[AgentCore](https://agentcore.console.aliyun.com/)控制台。

2. 在Workspace详情页左侧导航栏，点击**Team 协作**。

3. 切换到**团队管理**。

4. 点击**创建Agent团队**。

5. 在**1. 基本信息**区域，配置以下信息。

   <table> <thead> <tr> <td> <p><b>参数</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>团队名称</b></p> </td> <td> <p>Agent团队的名称</p> </td> </tr> <tr> <td> <p><b>团队 Admin</b></p> </td> <td> <p>Agent 团队的管理员（人类用户）。团队 Admin 可以维护团队信息、增删团队成员与团队 Agent、更换 Team Leader。</p> </td> </tr> <tr> <td> <p><b>团队成员</b></p> </td> <td> <p>（可选）为Agent团队添加成员（人类用户）</p> </td> </tr> <tr> <td> <p><b>描述</b></p> </td> <td> <p>（可选）Agent 团队的用途说明。</p> </td> </tr> </tbody> </table>
6. 在**2. Team Leader 配置**区域，配置以下信息。

   <table> <thead> <tr> <td> <p><b>参数</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>Leader 来源</p> </td> <td> <p>取值为<b>选择已有 Agent</b>或<b>新建 Leader Agent</b>。</p> </td> </tr> <tr> <td> <p>Agent</p> </td> <td> <p>选择作为 Leader 的 Agent。选定的 Agent 将作为该团队的 Leader，负责任务拆解与分派；它不会重复出现在团队成员中。</p> </td> </tr> </tbody> </table>
7. 在**3.团队 Agent 配置** 区域，从**可用 Agent** 中选择要加入 Team 的 Agent，选定后展示在**已加入 Agent**中。

   以下 Agent 无法加入团队，控制台会在对应 Agent 上给出提示，可点击**查看详情**了解原因：
   * 未配置 AG-UI 或 OpenAI（Chat Completions）协议的 Agent。需先在该 Agent 的编辑页完成协议配置，才能加入团队。

   * 以自定义代码 / 镜像方式创建的 Agent，暂不支持加入团队。

   * 已作为其他团队 Leader 的 Agent。

   * 已归属其他团队的 Agent，控制台会同时提示其所属团队名称。

   **说明**

   若提示暂时无法确认 Agent 的团队归属，请刷新页面后重新选择。
8. 点击**立即创建**。

### 查看团队信息

点击详情，可以查看团队详细信息。
<table> <thead> <tr> <td> <p><b>字段</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>团队 Admin</p> </td> <td> <p>团队的管理员。</p> </td> </tr> <tr> <td> <p>Leader Agent</p> </td> <td> <p>统筹团队的 Agent。</p> </td> </tr> <tr> <td> <p>成员数</p> </td> <td> <p>团队内的成员个数。</p> </td> </tr> <tr> <td> <p>Agent 数</p> </td> <td> <p>团队内的 Agent 个数。</p> </td> </tr> <tr> <td> <p>创建时间</p> </td> <td> <p>团队的创建时间。</p> </td> </tr> <tr> <td> <p>更新时间</p> </td> <td> <p>团队最近一次更新的时间。</p> </td> </tr> <tr> <td> <p>描述</p> </td> <td> <p>团队的描述信息。</p> </td> </tr> </tbody> </table>

### 编辑团队

点击编辑，可以编辑团队信息。

### 删除团队

点击删除，可以删除已创建的团队。

## 成员管理
在团队详情页的成员管理页签，可以查看团队内的成员。在搜索框中输入用户名，可以筛选成员。
<table> <thead> <tr> <td> <p><b>字段</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>显示名称/用户名</p> </td> <td> <p>成员的显示名称与用户名。</p> </td> </tr> <tr> <td> <p>认证方式</p> </td> <td> <p>成员的认证方式，如本地账号。</p> </td> </tr> <tr> <td> <p>状态</p> </td> <td> <p>成员当前的状态，如活跃。</p> </td> </tr> <tr> <td> <p>邮箱</p> </td> <td> <p>成员的邮箱地址。</p> </td> </tr> </tbody> </table>

### 创建用户

点击创建用户，填写显示名称、用户名和密码，可以新增成员。

### 编辑成员

点击编辑，可以编辑成员信息。

<br />