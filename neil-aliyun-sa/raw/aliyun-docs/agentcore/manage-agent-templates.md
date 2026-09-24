---
source_url: https://help.aliyun.com/zh/agentcore/manage-agent-templates
fetch_date: 2026-09-20
product: AgentCore
slug: manage-agent-templates
body_sha256: 6a7b1cc857cd765e0e187bd402b0d6f7c4b47254de9e9b5f7536e4f7a70388c7
body_bytes: 1648
migration_status: current   # 见 FETCH-CONTRACT §3
---

当团队中多个 Agent 需要使用相同配置时，逐个手动配置效率低且容易出错。Agent 模板基于 AgentSpec 规范，提供可复用的配置模板，支持一次定义、多次创建，快速部署具有相同配置的 Agent。本文介绍如何创建、查看和删除 Agent 模板。  

## **导入**Agent 模板
1. 登录 [AgentCore](https://agentcore.console.aliyun.com/)控制台。

2. 在Workspace详情页左侧导航栏，点击 **Agent 模板**。

3. 点击**导入模版**。

4. **上传压缩包**，将本地已打包为ZIP格式的模板上传到控制台。

5. 点击**确认导入**。

## 创建并管理Agent 模板
1. 登录 AgentCore 控制台。

2. 在Workspace详情页左侧导航栏，点击**Agent 模板**。

3. 点击**创建模版**，配置以下信息。

   <table> <thead> <tr> <td><p><b>参数</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>名称</b></p></td> <td><p>Agent名称。</p></td> </tr> <tr> <td><p><b>文件</b></p></td> <td><p>定义SOUL.md和AGENT.md文件的内容。</p></td> </tr> <tr> <td><p><b>Skill 绑定</b></p></td> <td><p>选择绑定的技能。</p></td> </tr> <tr> <td><p><b>SubAgent</b></p></td> <td><p>选择Agent可用的SubAgent。需要配置名称和SubAgent的AGENTS.md。最多可配置20个SubAgent。</p></td> </tr> </tbody> </table>
4. 配置完成后，点击**立即创建**。

5. 在**Agent 模板**页面，查看已创建的Agent 模板条目。

   1. 点击**详情**，可以查看信息。

   2. 点击**删除**，可以删除已创建的Agent 模板。

<br />