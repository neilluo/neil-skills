---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/managing-the-model-api
fetch_date: 2026-09-21
product: AI Gateway
slug: managing-the-model-api
body_sha256: 63ba448ec121ab7ce14bd8fb8f8838786c4e1bc0b69ead789782017cb4008778
body_bytes: 23549
migration_status: current
---

Model API适用于面向人工智能应用开发的团队，提供了更加灵活和智能的AI网关配置和调试能力。它可以用于各种AI代理、AI观测、消费者鉴权、内容安全防护等插件的预置。本文主要介绍了如何创建、编辑、调试和删除Model API。  

## **创建Model API**
1. 打开[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)**实例** 页面，在顶部菜单栏选择目标实例所在地域，并单击目标**实例ID**。

2. 在左侧导航栏，单击**Model API** ，然后单击**创建Model API**。

3. 选择使用场景，并单击对应场景的**创建**按钮。

   不同的场景会影响后续**协议** 可选项与系统自动创建的**默认路由**，当前支持：
   * **文本生成**（Text）：支持 OpenAI 兼容协议和 Anthropic 协议

   * **图片生成**（Image）

   * **视频生成**（Video）

   * **语音合成**（Audio）

   * **向量化（Embedding）**

   * **文本排序（Rerank）**

   * **其他**（Others）

4. 配置基本信息。

   在弹窗中先完成**请选择使用场景** ，进入**创建Model API**表单后，您可按以下说明进行配置：
   * **协议** ：不同协议对应该场景下的一组内置[默认路由](#cQ04A)，用于快速生成常用的 OpenAI/DashScope/vLLM 等兼容接口。

     **说明**

     协议转换可能会改变 Token 的统计结构。例如，阿里云百炼协议的 input token 统计会包含缓存 token（cache token），而 Anthropic 协议的 input token 统计不包含缓存 token。请在查看可观测指标时留意不同协议的统计口径差异。
   * **API名称**：您可自定义API名称，需注意名称必须全局唯一（同一账号下不可重复），支持英文、数字、下划线"_"、"-"，且不超过64个字符。

   * **域名** ：访问该 API 的域名，支持选择多个。域名与基本路径 `BasePath` 的组合必须唯一。

     > 如果还没有域名，请单击右侧 **添加域名** 按钮完成 [创建](https://help.aliyun.com/document_detail/2881840.html)。
   * **Base Path** ：配置API的基本请求路径，默认为 `/`。可选择是否启用**转发至后端服务时移除**。

     **说明**

     开启**转发至后端服务时移除**后，当请求转发到后端服务时，系统会自动移除请求路径中的BasePath部分。例如：
     * BasePath设置为 /api

     * 原始请求路径 /api/users

     * 实际转发到后端的路径变为 /users

   * **AI请求观测** : 开启后可查看 Metrics、Logging、Tracing 信息。Logging 与 Tracing 依赖 SLS 日志投递服务。可勾选开启**记录请求内容** 与**记录响应内容**，开启后将记录对大模型的请求或大模型返回的Context。

     **重要**

     启用后系统会记录所有 AI 请求内容（包括请求体 body）到访问日志，请妥善配置 SLS 并做好数据安全防护。
   * **大模型服务** : 支持**单模型服务** 、**多模型服务（按模型名称）** 、**多模型服务（按权重）**。

     * **单模型服务** ：选择 1 个 AI 服务，并可设置**模型名称**（可透传或改写）。

     * **多模型服务（按模型名称）** ：根据请求体中的模型名按规则匹配到不同服务；匹配规则支持通配符 `?` 与 `*`，例如 `qwen-*` 可匹配 `qwen-max`、`qwen-long`。

     * **多模型服务（按权重）**：选择多个 AI 服务并设置权重，支持透传或改写模型名。

     * **多服务（按观测指标）**：系统将根据各服务的响应时间、成功率等观测指标自动选择最优服务进行请求路由，无需手动配置权重。

     * **多模型服务（智能路由）** ：系统将根据模型特征为请求自动选择最合适的模型，详情参考[智能路由](#7a64d5c82axyj)。

       **说明**

       多服务（按观测指标）和多模型服务（智能路由）需要将AI网关版本升级至`2.1.15`及以上。
   * **Fallback** : 可**开启**并按顺序配置多条 Fallback 策略（可复用同一服务）。

   * **首包超时**：用于控制流式响应中从请求发送到接收到第一个响应包之间的最大等待时间，适用于对响应延迟敏感的流式交互场景。（单位为毫秒，设为0时表示不启用）。

   * **资源组**：支持选择默认或已有资源组，也可新建。资源组用于对账户资源分组管理、授权与监控。

     > 如需创建新的资源组，您可以单击 **创建资源组**完成创建。
5. 确认配置参数并单击**确定**完成创建。

## 默认路由
在不同**使用场景** 下选择不同**协议** 时，系统将自动创建**默认路由**。

### 文本生成（Text）

#### **协议：OpenAI 兼容（** **OpenAI/v1****）**

<table> <thead> <tr> <td> <p><b>路由名称</b></p> </td> <td> <p><b>路径</b></p> </td> <td> <p><b>方法</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><code>create-chat-completion</code></p> </td> <td> <p><code>/v1/chat/completions</code></p> </td> <td> <p>POST</p> </td> <td> <p>Creates a model response for the given chat conversation。</p> </td> </tr> <tr> <td> <p><code>create-completion</code></p> </td> <td> <p><code>/v1/completions</code></p> </td> <td> <p>POST</p> </td> <td> <p>Creates a completion for the provided prompt and parameters。</p> </td> </tr> </tbody> </table>

#### **协议：Anthropic（** **Anthropic****）**

Anthropic协议专为Claude等Anthropic系列模型设计，提供原生的消息格式和交互方式。该协议适用于需要使用Anthropic原生API格式的应用场景。  
**说明**

支持该协议的大模型供应商包括：阿里云百炼（Qwen）、Claude、月之暗面（Moonshot）、智谱 AI（ZhipuAI）等。以上供应商AI服务自动支持Anthropic协议，无需额外配置。
<table> <thead> <tr> <td> <p><b>路由名称</b></p> </td> <td> <p><b>路径</b></p> </td> <td> <p><b>方法</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><code>create-message</code></p> </td> <td> <p><code>/v1/messages</code></p> </td> <td> <p>POST</p> </td> <td> <p>Creates a message for the given chat conversation using Anthropic's native message format。</p> </td> </tr> </tbody> </table>

### 图片生成（Image）

#### **协议：阿里云百炼图片生成**

<table> <thead> <tr> <td> <p><b>路由名称</b></p> </td> <td> <p><b>路径</b></p> </td> <td> <p><b>方法</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><code>dashscope-text-to-image-synthesis</code></p> </td> <td> <p><code>/api/v1/services/aigc/text2image/image-synthesis</code></p> </td> <td> <p>POST</p> </td> <td> <p>Generate a text-to-image synthesis image。</p> </td> </tr> <tr> <td> <p><code>dashscope-image-to-image-synthesis</code></p> </td> <td> <p><code>/api/v1/services/aigc/image2image/image-synthesis</code></p> </td> <td> <p>POST</p> </td> <td> <p>Generate an image-to-image synthesis image。</p> </td> </tr> <tr> <td> <p><code>dashscope-image-to-image-outpainting</code></p> </td> <td> <p><code>/api/v1/services/aigc/image2image/out-painting</code></p> </td> <td> <p>POST</p> </td> <td> <p>Generate an image-to-image outpainting image。</p> </td> </tr> <tr> <td> <p><code>dashscope-virtual-model-generation</code></p> </td> <td> <p><code>/api/v1/services/aigc/virtualmodel/generation</code></p> </td> <td> <p>POST</p> </td> <td> <p>Generate a virtual model image。</p> </td> </tr> <tr> <td> <p><code>dashscope-background-generation</code></p> </td> <td> <p><code>/api/v1/services/aigc/background-generation/generation</code></p> </td> <td> <p>POST</p> </td> <td> <p>Generate a background generation image。</p> </td> </tr> <tr> <td> <p><code>tasks</code></p> </td> <td> <p><code>/api/v1/tasks</code></p> </td> <td> <p>GET/POST/PUT/PATCH/DELETE</p> </td> <td> <p>Manage asynchronous tasks。</p> </td> </tr> </tbody> </table>

#### **协议：OpenAI 兼容**

<table> <thead> <tr> <td> <p><b>路由名称</b></p> </td> <td> <p><b>路径</b></p> </td> <td> <p><b>方法</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><code>openai-image-generation</code></p> </td> <td> <p><code>/api/v1/images/generations</code></p> </td> <td> <p>POST</p> </td> <td> <p>Generate an image。</p> </td> </tr> <tr> <td> <p><code>openai-image-edit</code></p> </td> <td> <p><code>/api/v1/images/edits</code></p> </td> <td> <p>POST</p> </td> <td> <p>Edit an image。</p> </td> </tr> <tr> <td> <p><code>openai-image-variation</code></p> </td> <td> <p><code>/api/v1/images/variations</code></p> </td> <td> <p>POST</p> </td> <td> <p>Variation an image。</p> </td> </tr> </tbody> </table>

#### **协议：ComfyUI**

<table> <thead> <tr> <td> <p><b>路由名称</b></p> </td> <td> <p><b>路径</b></p> </td> <td> <p><b>方法</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><code>comfyui-websocket</code></p> </td> <td> <p><code>/ws</code></p> </td> <td> <p>GET</p> </td> <td> <p>WebSocket endpoint for real-time communication with the server.</p> </td> </tr> <tr> <td> <p><code>comfyui-embeddings</code></p> </td> <td> <p><code>/embeddings</code></p> </td> <td> <p>GET</p> </td> <td> <p>Retrieve a list of the names of embeddings available.</p> </td> </tr> <tr> <td> <p><code>comfyui-extensions</code></p> </td> <td> <p><code>/extensions</code></p> </td> <td> <p>GET</p> </td> <td> <p>Retrieve a list of the extensions registering a WEB_DIRECTORY.</p> </td> </tr> <tr> <td> <p><code>comfyui-features</code></p> </td> <td> <p><code>/features</code></p> </td> <td> <p>GET</p> </td> <td> <p>Retrieve server features and capabilities.</p> </td> </tr> <tr> <td> <p><code>comfyui-models</code></p> </td> <td> <p><code>/models</code></p> </td> <td> <p>GET</p> </td> <td> <p>Retrieve a list of available model types.</p> </td> </tr> <tr> <td> <p><code>comfyui-models-folder</code></p> </td> <td> <p><code>/models/{folder}</code></p> </td> <td> <p>GET</p> </td> <td> <p>Retrieve models in a specific folder.</p> </td> </tr> <tr> <td> <p><code>comfyui-workflow-templates</code></p> </td> <td> <p><code>/workflow_templates</code></p> </td> <td> <p>GET</p> </td> <td> <p>Retrieve a map of custom node modules and associated template workflows.</p> </td> </tr> <tr> <td> <p><code>comfyui-upload-image</code></p> </td> <td> <p><code>/upload/image</code></p> </td> <td> <p>POST</p> </td> <td> <p>Upload an image.</p> </td> </tr> <tr> <td> <p><code>comfyui-upload-mask</code></p> </td> <td> <p><code>/upload/mask</code></p> </td> <td> <p>POST</p> </td> <td> <p>Upload a mask.</p> </td> </tr> <tr> <td> <p><code>comfyui-view</code></p> </td> <td> <p><code>/view</code></p> </td> <td> <p>GET</p> </td> <td> <p>View an image. Lots of options.</p> </td> </tr> <tr> <td> <p><code>comfyui-view-metadata</code></p> </td> <td> <p><code>/view_metadata/</code></p> </td> <td> <p>GET</p> </td> <td> <p>Retrieve metadata for a model.</p> </td> </tr> <tr> <td> <p><code>comfyui-system-stats</code></p> </td> <td> <p><code>/system_stats</code></p> </td> <td> <p>GET</p> </td> <td> <p>Retrieve information about the system (python version, devices, vram etc).</p> </td> </tr> <tr> <td> <p><code>comfyui-prompt</code></p> </td> <td> <p><code>/prompt</code></p> </td> <td> <p>GET/POST</p> </td> <td> <p>Retrieve current queue status and execution information or submit a prompt to the queue.</p> </td> </tr> <tr> <td> <p><code>comfyui-object-info</code></p> </td> <td> <p><code>/object_info</code></p> </td> <td> <p>GET</p> </td> <td> <p>Retrieve details of all node types.</p> </td> </tr> <tr> <td> <p><code>comfyui-object-info-class</code></p> </td> <td> <p><code>/object_info/{node_class}</code></p> </td> <td> <p>GET</p> </td> <td> <p>Retrieve details of one node type.</p> </td> </tr> <tr> <td> <p><code>comfyui-history</code></p> </td> <td> <p><code>/history</code></p> </td> <td> <p>GET/POST</p> </td> <td> <p>Retrieve the queue history.</p> </td> </tr> <tr> <td> <p><code>comfyui-history-prompt-id</code></p> </td> <td> <p><code>/history/{prompt_id}</code></p> </td> <td> <p>GET</p> </td> <td> <p>Retrieve the queue history for a specific prompt.</p> </td> </tr> <tr> <td> <p><code>comfyui-queue</code></p> </td> <td> <p><code>/queue</code></p> </td> <td> <p>GET/POST</p> </td> <td> <p>Retrieve the current state of the execution queue or manage queue operations.</p> </td> </tr> <tr> <td> <p><code>comfyui-interrupt</code></p> </td> <td> <p><code>/interrupt</code></p> </td> <td> <p>POST</p> </td> <td> <p>Stop the current workflow execution.</p> </td> </tr> <tr> <td> <p><code>comfyui-free</code></p> </td> <td> <p><code>/free</code></p> </td> <td> <p>POST</p> </td> <td> <p>Free memory by unloading specified models.</p> </td> </tr> <tr> <td> <p><code>comfyui-userdata</code></p> </td> <td> <p><code>/userdata</code></p> </td> <td> <p>GET</p> </td> <td> <p>List user data files in a specified directory.</p> </td> </tr> <tr> <td> <p><code>comfyui-userdata-v2</code></p> </td> <td> <p><code>/v2/userdata</code></p> </td> <td> <p>GET</p> </td> <td> <p>Enhanced version that lists files and directories in structured format.</p> </td> </tr> <tr> <td> <p><code>comfyui-userdata-file</code></p> </td> <td> <p><code>/userdata/{file}</code></p> </td> <td> <p>GET/POST/DELETE</p> </td> <td> <p>Retrieve, upload, update or delete a specific user data file.</p> </td> </tr> <tr> <td> <p><code>comfyui-userdata-file-move</code></p> </td> <td> <p><code>/userdata/{file}/move/{dest}</code></p> </td> <td> <p>POST</p> </td> <td> <p>Move or rename a user data file.</p> </td> </tr> <tr> <td> <p><code>comfyui-users</code></p> </td> <td> <p><code>/users</code></p> </td> <td> <p>GET/POST</p> </td> <td> <p>Get user information or create a new user.</p> </td> </tr> </tbody> </table>

### 视频生成（Video）

#### **协议：阿里云百炼视频生成**

<table> <thead> <tr> <td> <p><b>路由名称</b></p> </td> <td> <p><b>路径</b></p> </td> <td> <p><b>方法</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><code>dashscope-video-generation-synthesis</code></p> </td> <td> <p><code>/api/v1/services/aigc/video-generation/video-synthesis</code></p> </td> <td> <p>POST</p> </td> <td> <p>Generate a video-generation synthesis video。</p> </td> </tr> <tr> <td> <p><code>dashscope-image-to-video-synthesis</code></p> </td> <td> <p><code>/api/v1/services/aigc/image2video/video-synthesis</code></p> </td> <td> <p>POST</p> </td> <td> <p>Generate an image-to-video synthesis video。</p> </td> </tr> <tr> <td> <p><code>tasks</code></p> </td> <td> <p><code>/api/v1/tasks</code></p> </td> <td> <p>GET/POST/PUT/PATCH/DELETE</p> </td> <td> <p>Manage asynchronous tasks。</p> </td> </tr> </tbody> </table>

### 语音合成（Audio）

#### **协议：阿里云百炼语音合成**

<table> <thead> <tr> <td> <p><b>路由名称</b></p> </td> <td> <p><b>路径</b></p> </td> <td> <p><b>方法</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><code>dashscope-text-to-audio-synthesis</code></p> </td> <td> <p><code>/api-ws/v1/inference</code></p> </td> <td> <p>GET</p> </td> <td> <p>Generate a text-to-audio synthesis audio。</p> </td> </tr> </tbody> </table>

#### **协议：OpenAI 兼容（** **OpenAI/v1****）**

<table> <thead> <tr> <td> <p><b>路由名称</b></p> </td> <td> <p><b>路径</b></p> </td> <td> <p><b>方法</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><code>openai-audio-speech</code></p> </td> <td> <p><code>/api/v1/audio/speech</code></p> </td> <td> <p>POST</p> </td> <td> <p>Generate speech audio。</p> </td> </tr> </tbody> </table>

### 向量化（Embedding）

#### **协议：OpenAI 兼容（** **OpenAI/v1****）**

<table> <thead> <tr> <td> <p><b>路由名称</b></p> </td> <td> <p><b>路径</b></p> </td> <td> <p><b>方法</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><code>create-embedding</code></p> </td> <td> <p><code>/v1/embeddings</code></p> </td> <td> <p>POST</p> </td> <td> <p>Creates an embedding vector representing the input text。</p> </td> </tr> </tbody> </table>

### 文本排序（Rerank）

#### **协议：阿里云百炼文本排序**

<table> <thead> <tr> <td> <p><b>路由名称</b></p> </td> <td> <p><b>路径</b></p> </td> <td> <p><b>方法</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><code>rerank</code></p> </td> <td> <p><code>/api/v1/services/rerank/text-rerank/text-rerank</code></p> </td> <td> <p>POST</p> </td> <td> <p>Rerank the given documents to be sorted based on query relevance。</p> </td> </tr> </tbody> </table>

#### **协议：vLLM（** **vLLM****）**

<table> <thead> <tr> <td> <p><b>路由名称</b></p> </td> <td> <p><b>路径</b></p> </td> <td> <p><b>方法</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><code>rerank</code></p> </td> <td> <p><code>/v1/rerank</code></p> </td> <td> <p>POST</p> </td> <td> <p>Rerank the given documents to be sorted based on query relevance。</p> </td> </tr> </tbody> </table>

### 其他（Others）

#### **协议：OpenAI 兼容（** **OpenAI/v1****）**

<table> <thead> <tr> <td> <p><b>路由名称</b></p> </td> <td> <p><b>路径</b></p> </td> <td> <p><b>方法</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><code>models</code></p> </td> <td> <p><code>/v1/models</code></p> </td> <td> <p>GET/POST/PUT/PATCH/DELETE</p> </td> <td> <p>Manage models。</p> </td> </tr> <tr> <td> <p><code>files</code></p> </td> <td> <p><code>/v1/files</code></p> </td> <td> <p>GET/POST/PUT/PATCH/DELETE</p> </td> <td> <p>Manage files。</p> </td> </tr> <tr> <td> <p><code>batches</code></p> </td> <td> <p><code>/v1/batches</code></p> </td> <td> <p>GET/POST/PUT/PATCH/DELETE</p> </td> <td> <p>Manage batches。</p> </td> </tr> <tr> <td> <p><code>fine-tuning</code></p> </td> <td> <p><code>/v1/fine_tuning</code></p> </td> <td> <p>GET/POST/PUT/PATCH/DELETE</p> </td> <td> <p>Manage fine-tuning jobs。</p> </td> </tr> </tbody> </table>  
**说明**

兼容性说明：对于支持Anthropic协议的大模型供应商（阿里云百炼、Claude、月之暗面、智谱 AI等），创建AI服务时会自动支持多种协议，包括OpenAI兼容协议和Anthropic协议，用户可根据需要选择合适的协议创建Model API。

## 智能路由
在企业级智能应用场景中，随着大语言模型能力的多样化发展，不同模型在特定领域展现出差异化的优势：

* **代码生成**：Qwen-Coder系列在代码理解和生成方面表现优异。

* **数学推理**：Qwen-Math系列擅长复杂数学问题的求解。

* **翻译任务**：Qwen-MT系列针对多语言翻译进行了专项优化。

* **快速响应**：Qwen-Flash系列在延迟敏感场景下提供极速响应。

* **复杂推理**：Qwen-Max、DeepSeek-R1等模型在复杂逻辑推理上更胜一筹。

然而，在实际应用中面临以下挑战：

1. **用户体验割裂**：用户需要手动选择模型，难以判断哪个模型最适合当前任务。

2. **资源利用不均**：简单任务使用高成本模型造成资源浪费。

3. **开发复杂度高**：应用层需要实现复杂的路由逻辑，增加开发和维护成本。

4. **缺乏统一入口**：多模型部署导致 API 分散，难以统一管理。

为应对以上问题，AI网关设计实现模型语义智能路由功能，通过语义分析自动将用户请求路由到最合适的模型服务，支持以下意图分类
<table> <thead> <tr> <td> <p><b>IntentCode</b></p> </td> <td> <p><b>描述</b></p> </td> <td> <p><b>典型场景</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><code>Coder</code></p> </td> <td> <p>代码编写与调试</p> </td> <td> <p>编程问题、代码生成、Bug修复</p> </td> </tr> <tr> <td> <p><code>Math</code></p> </td> <td> <p>数学计算与推理</p> </td> <td> <p>数学证明、公式推导、统计分析</p> </td> </tr> <tr> <td> <p><code>Translation</code></p> </td> <td> <p>多语言翻译</p> </td> <td> <p>文档翻译、实时翻译、本地化</p> </td> </tr> <tr> <td> <p><code>Flash</code></p> </td> <td> <p>快速简单响应</p> </td> <td> <p>简单问答、信息查询、日常对话</p> </td> </tr> <tr> <td> <p><code>Complex</code></p> </td> <td> <p>复杂逻辑推理</p> </td> <td> <p>深度分析、复杂决策、长文本理解</p> </td> </tr> </tbody> </table>

## 编辑Model API
1. 打开[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)**实例** 页面，在顶部菜单栏选择目标实例所在地域，并单击目标**实例ID**。

2. 在左侧导航栏，单击**Model API** ，单击目标API操作列的**编辑** 。在**编辑Model API** 面板中修改相关参数配置。关于配置参数说明，请参见[创建Model API](#9d7f312e31snz)。

3. 确认配置信息并单击**确定**。

## 调试Model API
**说明**

当前只支持文本生成的`/v1/chat/completions`调试。

1. 打开[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)**实例** 页面，在顶部菜单栏选择目标实例所在地域，并单击目标**实例ID**。

2. 在左侧导航栏，选择**Model API** ，单击目标API操作列的**调试**。

3. 在**调试** 面板中，选择域名和模型，按需开启**流式请求** 开关、配置参数设置和自定义参数。在右侧**模型返回** 页签中，输入调试内容并单击**发送**进行调试。

   其中参数设置包含 **System Prompt** （系统提示词，上限 100 字符）、**max_tokens** （范围 0--8192，默认 1024）、**top_p** （范围 0--1，默认 0.95）和 **temperature** （范围 0--2，默认 1，对结果影响较大，请谨慎调整）。右侧除 **模型返回** 页签外，还提供 **CURL命令** 和 **原始输出** 页签。

## 删除Model API
1. 打开[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)**实例** 页面，在顶部菜单栏选择目标实例所在地域，并单击目标**实例ID**。

2. 在左侧导航栏，选择**Model API** ，单击目标API操作列下的**删除** ，在确认删除的弹框中输入API名称，然后单击**删除**。