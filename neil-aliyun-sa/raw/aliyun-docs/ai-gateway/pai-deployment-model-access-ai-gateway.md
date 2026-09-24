---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/use-cases/pai-deployment-model-access-ai-gateway
fetch_date: 2026-09-21
product: AI Gateway
slug: pai-deployment-model-access-ai-gateway
body_sha256: ab9b3face4c6724d4e7af1cf265e44624512e6cd2d9e1f92360fff92582b9683
body_bytes: 4661
migration_status: current
---

本文主要介绍如何通过AI 网关访问部署在人工智能平台PAI 的模型。  

## **前提条件**
* 已通过PAI 部署模型，具体操作请参见[一键部署模型](https://help.aliyun.com/document_detail/2865727.html#69e7328d091nn)。

* 已创建AI 网关实例，具体操作请参见[创建网关实例](https://help.aliyun.com/document_detail/2881527.html)。

**重要**

当使用私网地址访问模型时，请确保AI 网关实例与人工智能平台PAI 部署的模型处于同一VPC。

## 操作步骤
### 步骤一：创建AI 服务

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击目标**实例ID**。

4. 在左侧导航栏，单击**服务** ，并单击**服务**页签。

5. 单击**创建服务** ，在**创建服务**面板，参考如下信息配置AI 服务：

   <table> <thead> <tr> <td> <p><b>配置项</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>服务来源</b></p> </td> <td> <p>选择<b>AI服务</b>。</p> </td> </tr> <tr> <td> <p><b>服务名称</b></p> </td> <td> <p>填写创建网关服务的名称，如pai。</p> </td> </tr> <tr> <td> <p><b>大模型供应商</b></p> </td> <td> <p>选择AI 服务所提供的大模型供应商。本示例选择<b>PAI-EAS</b>。若无EAS通过PAI 部署模型，具体操作请参见<a href="https://help.aliyun.com/document_detail/2865727.html#69e7328d091nn">一键部署模型</a>。</p> </td> </tr> <tr> <td> <p><b>工作空间</b></p> </td> <td> <p>人工智能平台PAI工作空间，例如<code>pai_xqrj0u0t\*\*\*\*\*\*</code>。</p> </td> </tr> <tr> <td> <p><b>EAS服务</b></p> </td> <td> <p>选择通过PAI 部署模型的名称，例如<code>Qwen3-32B</code><b>。</b></p> </td> </tr> <tr> <td> <p><b>连接类型</b></p> </td> <td> <p>选择与PAI 部署模型的连接类型，包含公网和私网两种。本示例选择私网。</p> </td> </tr> <tr> <td> <p><b>API-KEY</b></p> </td> <td> <p>已自动获取通过PAI 部署模型的API-KEY。</p> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <p>该API-KEY用于在AI 网关与PAI-EAS服务之间进行身份验证，AI 网关将自动获取API-KEY并与PAI-EAS服务建立通信。</p> </div> </div> </td> </tr> <tr> <td> <p><b>健康检查</b></p> </td> <td> <p>是否开启服务健康状态检查。</p> </td> </tr> </tbody> </table>

### 步骤二：创建Model API

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击目标**实例ID**。

4. 在左侧导航栏，单击**Model API** ，然后单击**创建Model API**。

5. 在**创建Model API**面板中，配置基本信息如下：

   * **Base Path**：API的基本路径。

   * **服务列表** ：选择上述步骤：[创建AI 服务](#ef3045bf987zd)中新建的AI 服务。

6. 单击**确定**完成创建 Model API 。

### 步骤三：调试Model API

1. 单击目标 Model API **操作** 列下的**调试**按钮进行测试。

2. 在**调试** 控制面板中，**模型选择** 在PAI 中部署的模型，在右侧**模型返回**页签下与大模型进行对话。

   **重要**

   在模型返回页签下，使用的是`/v1/chat/completions`对话接口，如需使用其他接口，您可选择**CURL命令** 或**原始输出**的方式通过 curl 、SDK 调试。
3. 【示例】您可以使用**CURL命令** 调用`completions`，具体操作步骤如下：

   1. 在**CURL命令**页签下，复制AI 网关提供的代码示例。

   2. 将代码示例中提供的`url`接口替换为`/v1/completions`**。**

   3. 将代码示例中提供的`data(body)`部分修改为`/v1/completions`需要的格式：

   ```
   HELPCODEESCAPE-bash
   curl --location 'http://env-cxxx-cn-wulanchabu.alicloudapi.com/v1/completions' \
     --header 'Content-Type: application/json' \
     --data '{"model": "DeepSeek-R1-Distill-Qwen-1.5B","prompt": "can you help me with"}'
   {"id":"cmpl-d057e88b-ebb0-456f-89d6-79d431ed0ed9","object":"text_completion","created":1739929451,"model":"DeepSeek-R1-Distill-Qwen-1.5B","choices":[{"index":0,"text":" this math problem?\n\nI think about the idea of moving the focus point of the","logprobs":null,"finish_reason":"length","stop_reason":null,"prompt_logprobs":null}],"usage":{"prompt_tokens":6,"total_tokens":22,"completion_tokens":16,"prompt_tokens_details":null}}
   ```