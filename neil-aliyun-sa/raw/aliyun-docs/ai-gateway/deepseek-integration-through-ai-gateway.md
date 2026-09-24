---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/use-cases/deepseek-integration-through-ai-gateway
fetch_date: 2026-09-21
product: AI Gateway
slug: deepseek-integration-through-ai-gateway
body_sha256: 90c21aa15ccf87ee06b8d5659c1b5c5bb031c0ff6f88326e3fceb7dd650e04cd
body_bytes: 7855
migration_status: current
---

本文基于三种AI 模型接入场景，介绍如何通过AI 网关快速实现第三方 DeepSeek 模型的统一接入。  

## 场景概览
<table> <thead> <tr> <td> <p><b>场景</b></p> </td> <td> <p><b>描述</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><a href="#ad5adbe47esdf">集成模型接入AI 网关</a></p> </td> <td> <p>支持通过选择已集成的部分大模型供应商及配置 API-KEY 的方式直接接入使用。</p> </td> </tr> <tr> <td> <p><a href="#4ce27d5d78ds6">通用模型方式接入AI 网关</a></p> </td> <td> <p>支持通过配置自定义AI 服务地址且满足 OpenAI 接入标准的AI 服务。</p> </td> </tr> <tr> <td> <p><a href="#67a05e38adjwn">AI 网关多模型代理</a></p> </td> <td> <p>支持通过网关已集成的部分大模型供应商和配置自定义AI 服务地址接入使用。</p> </td> </tr> </tbody> </table>

## 前提条件
* 创建专有网络VPC并绑定公网NAT网关，具体操作请参见[创建和管理专有网络](https://help.aliyun.com/document_detail/65398.html)和[使用公网NAT网关SNAT功能访问互联网](https://help.aliyun.com/document_detail/203501.html)。

* 基于上述VPC创建AI 网关实例，具体操作请参见[创建网关实例](https://help.aliyun.com/document_detail/2881527.html)。

## 场景一：集成模型接入AI 网关
当前AI 网关中已经集成部分大模型供应商，该类模型可通过选择供应商及配置 API-KEY 直接接入。  
**展开集成的大模型**  
* 阿里云百炼

* DeepSeek

* OpenAI

* Azure

* Claude

* 月之暗面

* 百川智能

* 零一万物

* 智谱AI

* 混元

* 阶跃星辰

* 星火

* 豆包（火山引擎）

* MiniMax

* Gemini

### 1. 创建AI 服务

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击目标**实例ID**。

4. 在左侧导航栏，单击**服务** ，并单击**服务**页签。

5. 单击**创建服务** ，在**创建服务** 面板，参考如下信息配置AI 服务，以**阿里云百炼**配置示例。

   * **服务来源** ：**AI服务**。

   * **服务名称**：填写创建网关服务的名称，如aliyun-deepseek。

   * **大模型供应商** ：选择对应的模型供应商，如**阿里云百炼**。

   * **服务接入点** ：使用阿里云百炼默认配置，如https://dashscope.aliyuncs.com/compatible-model/v1。

   * **API-KEY**：填写模型供应商获取的请求凭证 API-KEY 。

     **说明**

     如果使用**阿里云百炼** ，请在阿里云百炼[API-KEY 获取](https://bailian.console.aliyun.com/?apiKey=1#/api-key)。其他大模型供应商，请咨询对应的服务供应商。

### 2. 创建Model API

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击目标**实例ID**。

4. 在左侧导航栏，单击**Model API** ，然后单击**创建Model API**。

5. 在**创建Model API**面板中，配置基本信息如下：

   * **域名**：建议配置域名（使用默认环境域名下存在限流）。

   * **Base Path**：API的基本路径。

   * **AI请求观测**：开启。

   * **服务模型**：单模型服务。

   * **服务列表**：配置如下：

     * **服务名称**：选择上一步中配置的阿里云百炼 DeepSeek 服务。

     * **模型名称**：选择透传。

### 3. 调试Model API

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击目标**实例ID**。

4. 在左侧导航栏，选择**Model API** ，单击目标 Model API **操作** 列下的**调试** 。在**调试**面板中，配置相关参数进行调试。

5. **模型选择** 为**deepseek-r1** ，在右侧**模型返回**页签下与阿里云百炼的 DeepSeek 进行对话。

   **重要**

   在模型返回页签下，使用的是`/v1/chat/completions`对话接口，如需使用其他接口，您可选择**CURL命令** 或**原始输出**的方式通过 curl 、SDK 调试。

## 场景二：通用模型方式接入AI 网关
您可通过自定义服务地址方式，将通用模型接入AI 网关且支持如下情况。

* 对于AI 网关中**未集成大模型供应商**，且该模型支持 OpenAI 协议。

* 对于通过在阿里云**人工智能平台PAI** 或者**函数计算FC**等方式部署的 DeepSeek 服务。

本场景，可直接参考[通过AI网关接入PAI部署模型](https://help.aliyun.com/document_detail/2870215.html)进行接入。

## 场景三：AI 网关多模型代理
### 1. 创建AI 服务

当前AI 网关支持同时基于已集成模型和通用模型的方式接入，提供多模型代理服务，并支持调用异常情况下 Fallback 。在该场景下，用户使用统一调用方式，同时调用不同的三方模型服务。

**基于** [场景一](#ad5adbe47esdf)**、** [场景二](#4ce27d5d78ds6)**分别完成三个网关AI 服务配置**（阿里云百炼、火山引擎、PAI），火山引擎的服务配置可参考图示配置。

火山引擎的服务配置：**服务来源** 选择**AI服务** ，**服务名称** 填写`bytedance-deepseek`，**大模型供应商** 选择**豆包** ，**服务地址（base_url）** 填写`https://ark.cn-beijing.volces.com`，在**大模型配置** 区域填写对应的**API-KEY** ，并开启**健康检查**。

### 2. 创建Model API

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击目标**实例ID**。

4. 在左侧导航栏，单击**Model API** ，然后单击**创建Model API**。

5. 在**创建Model API**面板中，配置基本信息如下：

   * **服务模型** ：**多模型服务（按模型名称）**。

   * **服务列表**：添加下列多个服务。

     * 选择上一步中配置的阿里云 DeepSeek 服务，模型名称匹配规则配置为`deepseek-*`。

     * 选择上一步中配置的火山引擎 DeepSeek 服务，模型名称匹配规则配置为`ep-*`。

   * **Fallback**：开启。

   * **Fallback列表** ： 选择上一步中配置的 PAI DeepSeek 服务，模型名称配置为`DeepSeek-R1-Distill-Qwen-1.5B`。

   **说明**

   以上配置会按照下列规则执行：
   * 模型为deepseek-\*时调用阿里云 DeepSeek 。

   * 模型为ep-\*时调用火山引擎 DeepSeek 。

   * 在其他模型出错或限流场景下调用 PAI DeepSeek-R1-Distill-Qwen-1.5B（如配置多个Fallback，则按顺序调用）。

### 3. 调试Model API

1. 单击目标 Model API **操作** 列下的**调试** 。在**调试**面板中，配置相关参数进行调试。

   **模型选择** 为`deepseek-v3`、`ep-20250219155230-28l6f`（以火山引擎侧实际获取的模型为准）时，会按照规则响应阿里云百炼、火山引擎。  
   **重要**

   在模型返回页签下，使用的是`/v1/chat/completions`对话接口，如需使用其他接口，您可选择**CURL命令** 或**原始输出**的方式通过 curl 、SDK 调试。
2. 当配置一个**匹配上述模型前缀但错误** 的名称，如`deepseek-abc`，此时阿里云百炼不存在该模型。因此会触发 **Fallback**，调用到PAI DeepSeek。

   在**调试** 页面将模型设置为 `deepseek-abc` 并发送消息"你是谁?"，模型回复自我介绍为深度求索（DeepSeek）公司开发的 DeepSeek-R1 智能助手，确认 Fallback 已生效。