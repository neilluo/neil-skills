---
source_url: https://help.aliyun.com/zh/agentteams/manage-workers-and-worker-teams
fetch_date: 2026-09-20
product: AgentTeams
slug: manage-workers-and-worker-teams
body_sha256: 45705c93794f43c2842de389ca57b46900c423bc9e8103339ca95d155d2aa56b
body_bytes: 3387
migration_status: migrated-legacy
---

Worker 是 AgentTeams 平台中 AI 智能体的执行单元，负责关联模型并执行特定的 AI 任务。本文介绍如何创建、查看、编辑和删除 Worker 以及由Worker组成的团队。  

## **管理 Worker 团队**
1. 登录 AgentTeams[控制台](https://agentteams.console.aliyun.com/)。

2. 在实例详情页左侧导航栏，点击**Worker 团队**。

3. 点击**创建 Worker 团队**。

4. 在**1. 基本信息**区域，配置以下信息。

   <table> <thead> <tr> <td> <p><b>参数</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>团队名称</b></p> </td> <td> <p>Worker团队的名称</p> </td> </tr> <tr> <td> <p><b>团队 Admin</b></p> </td> <td> <p>Worker团队的管理员（人类用户）</p> </td> </tr> <tr> <td> <p><b>团队成员</b></p> </td> <td> <p>（可选）为Worker团队添加成员（人类用户）</p> </td> </tr> </tbody> </table>
5. 在**2. Team Leader 配置**区域，配置以下信息。

   <table> <thead> <tr> <td> <p><b>参数</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>创建方式</b></p> </td> <td> <p>选择<b>模版创建</b>或<b>自定义创建</b>。本文以<b>自定义创建</b>为例。</p> </td> </tr> <tr> <td> <p><b>Leader 名称</b></p> </td> <td> <p> Leader名称。</p> </td> </tr> <tr> <td> <p><b>选择模型</b></p> </td> <td> <p>选择已配置的模型。</p> </td> </tr> <tr> <td> <p><b>文件</b></p> </td> <td> <p>定义SOUL.MD和AGENT.MD文件的内容。</p> </td> </tr> <tr> <td> <p><b>技能绑定</b></p> </td> <td> <p>选择绑定的技能。</p> </td> </tr> <tr> <td> <p><b>MCP Server 绑定</b></p> </td> <td> <p>选择绑定的MCP服务。</p> </td> </tr> </tbody> </table>
6. 点击**创建**。

7. 在**Worker 团队**页面，查看已创建的Worker团队。

8. 点击Worker团队条目右侧的**编辑**，可以更改配置信息。

9. 点击Worker团队条目右侧的**删除**，可以删除Worker团队。

## 管理 Worker
1. 登录 AgentTeams[控制台](https://agentteams.console.aliyun.com/)。

2. 在实例详情页左侧导航栏，点击**Worker 管理**。

3. 点击**创建 Worker**，配置以下信息。

   <table> <thead> <tr> <td> <p><b>参数</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>选择创建方式</b></p> </td> <td> <p>选择<b>模版创建</b>或<b>自定义创建</b>。本文以<b>自定义创建</b>为例。</p> </td> </tr> <tr> <td> <p><b>Worker 名称</b></p> </td> <td> <p>Worker名称。</p> </td> </tr> <tr> <td> <p><b>选择模型</b></p> </td> <td> <p>选择已配置的模型。</p> </td> </tr> <tr> <td> <p><b>所属团队</b></p> </td> <td> <p>（可选）选择Woker所属的Worker团队。</p> </td> </tr> <tr> <td> <p><b>文件</b></p> </td> <td> <p>定义SOUL.MD和AGENT.MD文件的内容。</p> </td> </tr> <tr> <td> <p><b>技能绑定</b></p> </td> <td> <p>选择绑定的技能。</p> </td> </tr> <tr> <td> <p><b>MCP Server 绑定</b></p> </td> <td> <p>选择绑定的MCP服务。</p> </td> </tr> </tbody> </table>
4. 点击**立即创建**。

5. 在**Worker 管理**页面，查看已创建的Worker。

6. 点击Worker条目下方的**删除**，可以删除Worker。