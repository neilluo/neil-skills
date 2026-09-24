---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/model-metadata
fetch_date: 2026-09-21
product: AI Gateway
slug: model-metadata
body_sha256: 83a83a792a36fc7823dc6a6896955fbe14ad0b12d6a4f5a696aa7ee4764fb950
body_bytes: 8625
migration_status: current
---

AI 网关使用模型元信息资源管理隶属于供应商的具体 AI 模型。您可以在 AI 网关实例中创建、编辑和删除模型，配置其 Credits 消耗、Token 上限、能力特性和可用路径等信息，使模型可用于 Model API 和路由配置。  

## 前提条件
* 已[创建网关实例](https://help.aliyun.com/document_detail/2881527.html)。

* 当前实例下至少有一个可用供应商（预置供应商或自定义供应商）。如没有，请先[管理供应商](https://help.aliyun.com/document_detail/3045094.html)。

## 模型元信息概述
模型元信息是隶属于某个供应商的具体 AI 模型实例。每个模型元信息包含：

* **基础信息**：所属供应商、名称、信息来源 URL

* **Credits 信息**：输入/输出/缓存 Token 消耗的 Credits 单价。

* **能力与性能**：最大输入/输出/总 Token 上限，输入/输出模态，能力特性

* **可用路径**：模型支持的 API 路径和协议类型

## 使用限制
使用模型管理功能时，需遵循以下限制：

* 路径必须以 `/` 开头。

* 同一模型内的可用路径不建议重复。

* Credits 消耗参数如填写，必须为大于等于 0 的数字，最多两位小数。

* 如当前实例内无可用供应商，无法创建模型，需先创建供应商或启用预置供应商。

## 查看模型元信息列表
1. 登录[AI 网关控制台](https://apig.console.aliyun.com/?spm=5176.6660585.apigateway_aipost_public_cn-top.i1.29127992temjdc#/ai-gateway-overview)，选择实例所在的地域，并单击目标实例 ID。

2. 单击左侧导航栏中的**模型元信息管理**，进入模型管理页面。

3. 默认展示**模型元信息**页签，查看当前实例下的模型列表。

包含以下列：
<table> <thead> <tr> <td><p><b>列名</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>模型名称</p></td> <td><p>模型的展示名称</p></td> </tr> <tr> <td><p>单价</p></td> <td><p>输入、输出、缓存 Credits 单价（Credits/1M tokens）</p></td> </tr> <tr> <td><p>总 Token 上限</p></td> <td><p>模型的总 Token 上限</p></td> </tr> <tr> <td><p>能力</p></td> <td><p>模型已启用的能力特性数量与全部可选能力特性数量（15 项）的比值，如 5/15。</p></td> </tr> <tr> <td><p>供应商</p></td> <td><p>模型绑定的供应商名称</p></td> </tr> <tr> <td><p>更新时间</p></td> <td><p>最近一次资源更新时间</p></td> </tr> <tr> <td><p>操作</p></td> <td><p>查看、编辑、删除</p></td> </tr> </tbody> </table>

## 创建模型元信息
1. 单击**创建模型元信息**。

   打开创建面板后，按以下折叠面板依次配置参数：  
   **基础信息**  

   ### 基础信息

   以下参数为基础信息，供应商和名称为必填项。
   <table> <thead> <tr> <td><p><b>参数</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>供应商</p></td> <td><p>必填。下拉展示当前实例内所有可用供应商（预置 + 自定义）。如无可用的供应商，无法创建模型并提示先创建供应商或启用预置供应商</p></td> </tr> <tr> <td><p>模型名称</p></td> <td><p>必填。模型的展示名称。</p></td> </tr> </tbody> </table>  
   **Credits 信息**  

   ### Credits 信息

   以下参数为可选配置，用于控制模型调用时的 Credits 消耗。
   <table> <thead> <tr> <td><p><b>参数</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>输入 Token 消耗</p></td> <td><p>选填。单位 Credits/1M tokens，如填写必须为大于等于 0 的数字，最多两位小数。默认值为 0</p></td> </tr> <tr> <td><p>输出 Token 消耗</p></td> <td><p>选填。单位 Credits/1M tokens，如填写必须为大于等于 0 的数字，最多两位小数。默认值为 0</p></td> </tr> <tr> <td><p>缓存 Token 消耗</p></td> <td><p>选填。单位 Credits/1M tokens，如填写必须为大于等于 0 的数字，最多两位小数。默认值为 0</p></td> </tr> </tbody> </table>  
   **能力与性能**  

   ### 能力与性能

   以下参数为可选配置，用于描述模型的能力边界。
   <table> <thead> <tr> <td><p><b>参数</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>最大输入 Token</p></td> <td><p>选填。最大输入 Token 数，如填写必须为大于等于 0 的整数</p></td> </tr> <tr> <td><p>最大输出 Token</p></td> <td><p>选填。最大输出 Token 数，如填写必须为大于等于 0 的整数</p></td> </tr> <tr> <td><p>总 Token 上限</p></td> <td><p>选填。总 Token 上限，如填写必须为大于等于 0 的整数</p></td> </tr> <tr> <td><p>输入模态</p></td> <td><p>选填。多选，可选值：text、image、audio、video</p></td> </tr> <tr> <td><p>输出模态</p></td> <td><p>选填。多选，可选值：text、image、audio、video</p></td> </tr> </tbody> </table>  
   **能力特性**  

   ### 能力特性

   模型支持以下能力特性，按需勾选（多选）。以下参数为可选配置。
   <table> <thead> <tr> <td><p><b>能力特性</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>系统消息</p></td> <td><p>支持 System Prompt</p></td> </tr> <tr> <td><p>结构化输出</p></td> <td><p>支持 Structured Output</p></td> </tr> <tr> <td><p>函数调用</p></td> <td><p>支持 Function Calling</p></td> </tr> <tr> <td><p>工具选择</p></td> <td><p>支持 Tool Choice</p></td> </tr> <tr> <td><p>前缀补全</p></td> <td><p>支持 Prefix Completion</p></td> </tr> <tr> <td><p>Prompt 缓存</p></td> <td><p>支持 Prompt Cache</p></td> </tr> <tr> <td><p>计算机操作</p></td> <td><p>支持 Computer Use</p></td> </tr> <tr> <td><p>PDF 输入</p></td> <td><p>支持 PDF Input</p></td> </tr> <tr> <td><p>视觉理解</p></td> <td><p>支持 Vision</p></td> </tr> <tr> <td><p>图像 Embedding</p></td> <td><p>支持 Image Embedding</p></td> </tr> <tr> <td><p>流式输出</p></td> <td><p>支持 Streaming Output</p></td> </tr> <tr> <td><p>并行函数调用</p></td> <td><p>支持 Parallel Function Calling</p></td> </tr> <tr> <td><p>联网搜索</p></td> <td><p>支持 Web Search</p></td> </tr> <tr> <td><p>推理模式</p></td> <td><p>支持 Reasoning</p></td> </tr> <tr> <td><p>URL 上下文</p></td> <td><p>支持 URL Context</p></td> </tr> </tbody> </table>  
   **可用路径**  

   ### 可用路径

   以下参数为必填项，用于配置模型支持的 API 路径和协议。
   <table> <thead> <tr> <td><p><b>参数</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>路径</p></td> <td><p>必填。模型支持的 API 路径，必须以 <code>/</code> 开头。例如 <code>/v1/chat/completions</code>。同一模型内可用路径不建议重复</p></td> </tr> <tr> <td><p>协议类型</p></td> <td><p>必填。可选：OpenAI Compatible、Anthropic Compatible、Custom</p></td> </tr> </tbody> </table>

   单击**添加路径**可新增一条可用路径。
2. 配置完成后，单击**确定**完成创建。新模型将出现在列表中。

创建成功后，可在模型列表中查看新模型状态，发送测试请求验证路径和 Token 配置是否生效。

## 编辑模型元信息
1. 找到目标模型，单击操作列的**编辑**。

2. 修改需要调整的参数。编辑时可修改以下参数：供应商、名称、Credits 信息（输入/输出/缓存 Token 消耗）、能力与性能（最大输入/输出/总 Token 上限、输入/输出模态）、能力特性、可用路径（路径和协议类型）。

3. 修改完成后单击**确定**保存。

编辑模型名称时，会影响 Model API 和路由中的模型名称候选展示。

## 删除模型元信息
1. 找到目标模型，单击操作列的**删除**。

2. 确认后删除。

删除模型后从列表中移除，但不影响已保存的 Model API 和路由中的模型名称字符串（Model API 中以字符串方式存储的模型名称不会因模型资源删除而失效）。

## 后续步骤
* 将已创建的模型关联到 Model API 配置中，供应用调用。

* 路由配置中选择该模型作为目标模型，实现流量分发。

* 如需添加更多模型，请先[管理供应商](https://help.aliyun.com/document_detail/3045094.html)。