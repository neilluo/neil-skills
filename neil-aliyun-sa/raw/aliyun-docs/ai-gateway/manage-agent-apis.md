---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/manage-agent-apis
fetch_date: 2026-09-21
product: AI Gateway
slug: manage-agent-apis
body_sha256: e65019eed1f4aa082359e9ee0868893461214a988f6fedbccf6ed1918707adec
body_bytes: 2613
migration_status: current
---

Agent 网关提供Agent API的管理。Agent API 专为对接阿里云百炼、Dify等平台的Agent设计。通过 Agent API，用户可便捷、安全地将各类智能体能力无缝集成至业务系统，实现智能对话、流程自动化等创新功能，助力企业高效构建智能化应用生态。  

## 创建Agent API
1. 在AI 网关控制台的[实例](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)页面，选择您实例所在的地域。

2. 进入目标实例页面，选择左侧导航栏的**Agent API**。

3. 单击**创建Agent API**，配置以下基本信息：

   * **API名称**：自定义API 名称。

     > Model API和Agent API名称不能相同。
   * **域名**：选择您计划创建Agent API的域名。

   * **Base Path**：自定义API的基本路径。

   * **协议** ：支持**阿里云百炼应用** 、**Dify** 、**自定义** 三种协议，默认选择**阿里云百炼应用**。

     * **阿里云百炼应用**：阿里云百炼推出的大模型应用，智能体、工作流与智能体编排，增加了知识库检索、互联网搜索、工作流设计及智能体协作等功能，显著扩展了大模型的应用范围。

     * **Dify**：Dify的智能体允许用户利用大型语言模型（LLM）的推理能力，构建能够自主设定目标、分解任务、使用工具并逐步完成复杂任务的 AI 应用。

     * **自定义**：适用于您自定义的其他Agent服务。

   * **资源组** ：选择控制台默认的资源组或已有资源组。如需创建新的资源组，您可以单击[创建资源组](https://help.aliyun.com/document_detail/2882591.html#section-0pl-c10-vmx)。

     > 使用资源组对云账号下的资源做分类分组管理，以组为单元进行权限管理、资源部署、资源监控等，而无需单独处理各个资源。

## 编辑Agent API
1. 在AI 网关控制台的[实例](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)页面，选择您实例所在的地域。

2. 进入目标实例页面，选择左侧导航栏的**Agent API**。

3. 单击目标Agent API操作列的**编辑** ，在**编辑Agent API** 面板中修改Agent API**域名** 和**Base Path** ，然后单击**确定**。

## 删除Agent API
1. 在AI 网关控制台的[实例](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)页面，选择您实例所在的地域。

2. 进入目标实例页面，选择左侧导航栏的**Agent API**。

3. 单击目标Agent API操作列的**删除** ，在**确定删除** 对话框中输入当前API名称，然后单击**删除**。