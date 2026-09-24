---
source_url: https://help.aliyun.com/zh/agentteams/management-models-and-suppliers-1
fetch_date: 2026-09-20
product: AgentTeams
slug: management-models-and-suppliers-1
body_sha256: 595b86ec7c789fece535395797ae3b18775da2b47fc248649af88c82f636c79e
body_bytes: 2045
migration_status: migrated-legacy
---

AI Worker 运行依赖模型配置。模型管理功能支持接入多个 AI 模型供应商，统一管理 API 端点和认证信息，并在正式使用前验证模型可用性。  

## **配置模型供应商**
1. 登录 AgentTeams[控制台](https://agentteams.console.aliyun.com/)。

2. 在实例详情页左侧导航栏，点击**模型管理**。

3. 点击**模型供应商**标签页。

4. 找到列表中的模型供应商条目，单击**编辑**，配置以下信息。

   <table> <thead> <tr> <td> <p><b>参数</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>模型供应商</b></p> </td> <td> <p>选择模型供应商。</p> </td> </tr> <tr> <td> <p><b>API 端点</b></p> </td> <td> <p>供应商提供的 API 服务地址。建议保持默认，或参考模型供应商的文档。</p> </td> </tr> <tr> <td> <p><b>协议</b></p> </td> <td> <p>选择协议。</p> </td> </tr> <tr> <td> <p><b>API Keys</b></p> </td> <td> <p>模型供应商的 API Key。</p> </td> </tr> </tbody> </table>
5. 点击**保存**。

6. 点击模型供应商条目右侧的**测试** 。点击**测试**，查看测试结果。

## 配置模型
1. 登录 AgentTeams[控制台](https://agentteams.console.aliyun.com/)。

2. 在实例详情页左侧导航栏，点击**模型管理**。

3. 点击**模型**标签页。

4. 找到列表中的模型供应商条目，单击**编辑** 来修改已有模型配置，或者点击**添加模型**来创建模型配置。配置以下信息。

   <table> <thead> <tr> <td> <p><b>参数</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>模型名称</b></p> </td> <td> <p>输入模型名称</p> </td> </tr> <tr> <td> <p><b>模型供应商</b></p> </td> <td> <p>选择模型供应商。</p> </td> </tr> </tbody> </table>
5. 点击**保存** 或**创建**。

6. 点击模型条目右侧的**测试** 。点击**测试**，查看测试结果。

<br />