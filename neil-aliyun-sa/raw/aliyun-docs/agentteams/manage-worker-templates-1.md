---
source_url: https://help.aliyun.com/zh/agentteams/manage-worker-templates-1
fetch_date: 2026-09-20
product: AgentTeams
slug: manage-worker-templates-1
body_sha256: a3e371f6b17207613997d41b8c64eabf3acdfcaf828225b57a7e12534af58747
body_bytes: 1597
migration_status: migrated-legacy
---

当团队中多个 Worker 需要使用相同配置时，逐个手动配置效率低且容易出错。Worker 模板基于 AgentSpec 规范，提供可复用的配置模板，支持一次定义、多次创建，快速部署具有相同配置的 Worker。本文介绍如何创建、查看、编辑和删除 Worker 模板。  

## **导入**Worker 模板
1. 登录 AgentTeams[控制台](https://agentteams.console.aliyun.com/)。

2. 在实例详情页左侧导航栏，点击**Worker 模版**。

3. 点击**导入模版**。

4. 选择方式：

   1. **上传压缩包**：将本地已打包为ZIP格式的模板上传到控制台。

   2. **导入预置模板**：搜索预置的 Worker 模板并导入。

5. 点击**确认导入**。

## 创建并管理Worker 模板
1. 登录 AgentTeams[控制台](https://agentteams.console.aliyun.com/)。

2. 在实例详情页左侧导航栏，点击**Worker 模版**。

3. 点击**创建模版**，配置以下信息。

   <table> <thead> <tr> <td> <p><b>参数</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>名称</b></p> </td> <td> <p>Worker名称。</p> </td> </tr> <tr> <td> <p><b>文件</b></p> </td> <td> <p>定义SOUL.MD和AGENT.MD文件的内容。</p> </td> </tr> <tr> <td> <p><b>Skill 绑定</b></p> </td> <td> <p>选择绑定的技能。</p> </td> </tr> </tbody> </table>
4. 在**Worker 模版**页面，查看已创建的Worker 模板条目。

   1. 点击**编辑**，可以编辑信息。

   2. 点击**删除**，可以删除已创建的Worker 模板。