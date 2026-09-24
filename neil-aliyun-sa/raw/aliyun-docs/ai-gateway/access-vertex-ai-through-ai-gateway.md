---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/use-cases/access-vertex-ai-through-ai-gateway
fetch_date: 2026-09-21
product: AI Gateway
slug: access-vertex-ai-through-ai-gateway
body_sha256: a734c02713a6abc9f0c757e175e1f95012befcef41a23b65463feca7038d5916
body_bytes: 42868
migration_status: current
---

本文介绍如何通过阿里云 AI 网关快速接入 Google Vertex AI，实现对 Gemini 等模型的统一管理和调用。

## 背景说明
Google Vertex AI 是 Google Cloud 提供的企业级 AI 平台，支持 Gemini、PaLM 等多种先进的大语言模型。通过阿里云 AI 网关接入 Vertex AI，您可以：

* **统一接入**：通过 OpenAI 兼容协议访问 Vertex AI，无需适配原生 API

* **灵活鉴权**：支持 GCP Service Account 和 Vertex AI Express Mode 两种鉴权方式

* **协议转换**：支持 AI 网关自动协议转换或使用 Vertex AI 原生兼容端点

* **高可用保障**：结合 AI 网关的 Fallback 能力实现跨供应商容灾

## 前提条件
* 已创建专有网络 VPC 并绑定公网 NAT 网关，具体操作请参见[专有网络与交换机](https://help.aliyun.com/document_detail/2881389.html)和[公网访问](https://help.aliyun.com/document_detail/106263.html)。

* 已创建 AI 网关实例，具体操作请参见[创建网关实例](https://help.aliyun.com/document_detail/2881527.html)。

* 已获取 Google Cloud 项目的访问凭证（Service Account Key 或 Vertex AI Express Mode API Key）。

## 场景概览
<table> <thead> <tr> <td><p><b>场景</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><a href="#80dc114d1dplg">场景一：GCP Service Account 模式接入</a></p></td> <td><p>使用 GCP Service Account 密钥进行身份验证，支持完整的 Vertex AI 功能和 OpenAI 协议兼容方式选择</p></td> </tr> <tr> <td><p><a href="#f34d41f3f9ptg">场景二：Vertex AI Express Mode 接入</a></p></td> <td><p>使用 Vertex AI 提供的快速模式，通过 API Key 直接接入，配置更简单</p></td> </tr> <tr> <td><p><a href="#2508c33020wag">场景三：Vertex AI REST API 接入</a></p></td> <td><p>代理 Vertex AI 原生 REST API，适用于 Imagen、Veo 等非 Gemini 系列模型</p></td> </tr> <tr> <td><p><a href="#6d52e237d0giq">场景四：Google GenAI SDK 模式接入</a></p></td> <td><p>使用 Google 官方 GenAI SDK 接入，客户端自行完成 OAuth 认证，通过网关进行请求观测和计量（不推荐）</p></td> </tr> <tr> <td><p><a href="#e51d121ae5jcs">场景五：多模态理解场景接入</a></p></td> <td><p>使用 Gemini 模型通过 Chat Completions 接口理解和分析图片、视频等多模态内容</p></td> </tr> <tr> <td><p><a href="#cd5559befanqr">场景六：图片生成场景接入</a></p></td> <td><p>使用 Gemini Nano Banana Pro 等模型通过 OpenAI 兼容协议进行图片生成、编辑和变体</p></td> </tr> </tbody> </table>

*** ** * ** ***

## 场景一：GCP Service Account 模式接入
GCP Service Account 是 Google Cloud 的标准身份验证方式，适用于需要完整 Vertex AI 功能的企业级应用场景。

### 1. 准备 GCP Service Account

在开始配置之前，您需要在 Google Cloud Console 中创建 Service Account 并下载 JSON 密钥文件。

1. 登录 [Google Cloud Console](https://console.cloud.google.com/)。

2. 在左侧导航栏，选择 **IAM 和管理** \> **服务账号**。

3. 单击 **创建服务账号**，填写服务账号名称和描述。

4. 为服务账号分配 **Vertex AI User** 角色（或更高权限）。

5. 单击 **KEY**，选择创建，下载密钥JSON文件。

**说明** 密钥文件包含敏感信息，请妥善保管。JSON 文件格式示例如下：

```
HELPCODEESCAPE-json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-sa@your-project.iam.gserviceaccount.com",
  "token_uri": "https://oauth2.googleapis.com/token"
}
```

对于 GCP Service Account 的管理，详见[Google官方文档](https://docs.cloud.google.com/iam/docs/service-account-overview)。

### 2. 创建 AI 服务

1. 登录 [AI 网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择 **实例**，并在顶部菜单栏选择地域。

3. 在 **实例** 页面，单击目标 **实例 ID**。

4. 在左侧导航栏，单击 **服务** ，并单击 **服务** 页签。

5. 单击 **创建服务** ，在 **创建服务** 面板，参考如下信息配置 AI 服务：

<table> <thead> <tr> <td><p><b>配置项</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>服务来源</b></p></td> <td><p>选择 <b>AI 服务</b></p></td> </tr> <tr> <td><p><b>服务名称</b></p></td> <td><p>填写服务名称，如 <code>vertex-ai</code></p></td> </tr> <tr> <td><p><b>大模型供应商</b></p></td> <td><p>选择 <b>Vertex AI</b></p></td> </tr> <tr> <td><p><b>鉴权方式</b></p></td> <td><p>选择 <b>GCP Service Account</b></p></td> </tr> <tr> <td><p><b>GCP Service Account KEY</b></p></td> <td><p>粘贴完整的 Service Account JSON 密钥内容</p></td> </tr> <tr> <td><p><b>vertexLocation</b></p></td> <td><p>Vertex AI 服务区域，默认值为 <code>global</code>。可选择其他区域如 <code>us-central1</code>、<code>europe-west4</code> 等</p></td> </tr> <tr> <td><p><b>vertexProjectId</b></p></td> <td><p>GCP 项目 ID（只读），系统会自动从 JSON 密钥中解析 <code>project_id</code> 字段</p></td> </tr> <tr> <td><p><b>OpenAI 协议兼容方式</b></p></td> <td><p>选择协议转换方式（详见下方说明）</p></td> </tr> </tbody> </table>

**OpenAI 协议兼容方式说明**：
<table> <thead> <tr> <td><p><b>选项</b></p></td> <td><p><b>描述</b></p></td> <td><p><b>适用场景</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>AI 网关转换</b></p></td> <td><p>通过 AI 网关在请求和响应阶段进行协议转换。网关会将 OpenAI 格式的请求转换为 Vertex AI 原生格式，并将响应转换回 OpenAI 格式</p></td> <td><p>需要使用 Vertex AI 原生功能（如特定安全设置）的场景</p></td> </tr> <tr> <td><p><b>Vertex AI 原生兼容端点</b></p></td> <td><p>使用 Vertex AI 提供的 OpenAI 兼容 Chat Completions 端点，直接接收 OpenAI 格式请求</p></td> <td><p>如需要获取 Vertex AI 独有的<code>extra_content</code>等字段，选用此模式</p></td> </tr> </tbody> </table>

**重要提示**：

* 如果 JSON 密钥格式不正确或缺少必要字段，系统会显示相应的错误提示。

* `vertexProjectId` 为只读字段，前端会自动解析 JSON 密钥中的 `project_id`。

* **使用「Vertex AI 原生兼容端点」模式时** ，请求体中的 `model` 参数需要添加 Provider 前缀 `google/`。例如：原本使用 `gemini-3-flash-preview` 需要改为 `google/gemini-3-flash-preview`。

关于「Vertex AI 原生兼容端点」模式支持的参数及模型，详见[Google官方文档](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/migrate/openai/overview)。

### 3. 创建 Model API

1. 登录 [AI 网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择 **实例**，并在顶部菜单栏选择地域。

3. 在 **实例** 页面，单击目标 **实例 ID**。

4. 在左侧导航栏，单击 **Model API** ，然后单击 **创建 Model API**。

5. 在 **创建 Model API** 面板中，配置基本信息如下：

   * **域名**：建议配置自定义域名（使用默认环境域名存在限流）。

   * **Base Path** ：API 的基本路径，如 `/gemini`。

   * **模型类型** ：选择 **文本生成**。

   * **协议** ：选择 **OpenAI 兼容**。

   * **路由配置** ：需要勾选 `/v1/chat/completions` 路由。

   * **AI 请求观测**：开启。

   * **服务模型**：单模型服务。

   * **服务列表**：

     * **服务名称**：选择上一步中配置的 Vertex AI 服务。

     * **模型名称** ：选择透传，或指定具体模型如 `gemini-2.0-flash`。

6. 单击 **确定** 完成创建。

### 4. 调试 Model API

1. 单击目标 Model API **操作** 列下的 **调试** 按钮进行测试。

2. 在 **调试** 控制面板中，**模型名称** 输入 Gemini 系列模型（如 `gemini-3-flash-preview`），在右侧 **模型返回** 页签下与大模型进行对话。

**重要** 在模型返回页签下，使用的是 `/v1/chat/completions` 对话接口，如需使用其他接口，您可选择 **CURL 命令** 或 **原始输出** 的方式通过 curl、SDK 调试。

**CURL 调用示例**：

```
HELPCODEESCAPE-bash
curl -X POST "http://your-gateway-domain/gemini/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3-flash-preview",
    "messages": [
      {"role": "user", "content": "你好，请介绍一下你自己"}
    ],
    "stream": false
  }'
```

*** ** * ** ***

## 场景二：Vertex AI Express Mode 接入
Vertex AI Express Mode 是 Google 提供的快速接入方式，通过 API Key 即可直接访问 Vertex AI 服务，无需配置 Service Account，适合快速验证和轻量级应用场景。

### 1. 获取 Vertex AI Express Mode API Key

获取API-KEY的方式请参考文档 [Vertex AI in express mode](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/express-mode/overview)。

**说明** Express Mode API Key 可能有使用限制，详情请参考 Google 官方文档。

### 2. 创建 AI 服务

1. 登录 [AI 网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择 **实例**，并在顶部菜单栏选择地域。

3. 在 **实例** 页面，单击目标 **实例 ID**。

4. 在左侧导航栏，单击 **服务** ，并单击 **服务** 页签。

5. 单击 **创建服务** ，在 **创建服务** 面板，参考如下信息配置 AI 服务：

<table> <thead> <tr> <td><p><b>配置项</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>服务来源</b></p></td> <td><p>选择 <b>AI 服务</b></p></td> </tr> <tr> <td><p><b>服务名称</b></p></td> <td><p>填写服务名称，如 <code>vertex-express</code></p></td> </tr> <tr> <td><p><b>大模型供应商</b></p></td> <td><p>选择 <b>Vertex AI</b></p></td> </tr> <tr> <td><p><b>鉴权方式</b></p></td> <td><p>选择 <b>Vertex AI Express Mode</b></p></td> </tr> <tr> <td><p><b>API-KEY</b></p></td> <td><p>填写从 Google AI Studio 获取的 API Key</p></td> </tr> </tbody> </table>

**说明** Express Mode 配置方式与其他大模型供应商（如 OpenAI、Claude）类似，只需填写 API Key 即可。

### 3. 创建 Model API

1. 在左侧导航栏，单击 **Model API** ，然后单击 **创建 Model API**。

2. 在 **创建 Model API** 面板中，配置基本信息如下：

   * **域名**：建议配置自定义域名（使用默认环境域名存在限流）。

   * **Base Path** ：API 的基本路径，如 `/gemini`。

   * **模型类型** ：选择 **文本生成**。

   * **协议** ：选择 **OpenAI 兼容**。

   * **路由配置** ：需要勾选 `/v1/chat/completions` 路由。

   * **AI 请求观测**：开启。

   * **服务模型**：单模型服务。

   * **服务列表**：

     * **服务名称**：选择上一步中配置的 Vertex AI Express 服务。

     * **模型名称**：选择透传。

3. 单击 **确定** 完成创建。

### 4. 调试 Model API

1. 单击目标 Model API **操作** 列下的 **调试** 按钮进行测试。

2. 在 **调试** 控制面板中，选择 Gemini 模型进行对话测试。

*** ** * ** ***

## 场景三：Vertex AI REST API 接入
本场景介绍如何通过 AI 网关代理 Vertex AI 原生 REST API，适用于使用 Imagen 4、Veo 3 等非 Gemini 系列模型的场景。与前两个场景不同，此模式使用 Vertex AI 原生协议而非 OpenAI 兼容协议。

### 适用场景

* 使用 Imagen 4 等图片生成模型

* 使用 Veo 3 等视频生成模型

* 使用通过 Vertex AI Model Garden 托管的第三方模型

* 需要直接调用 Vertex AI 原生 REST API 的场景

### 1. 创建 AI 服务

创建 AI 服务的步骤与场景一或场景二类似，关键差异如下：

1. 登录 [AI 网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择 **实例**，并在顶部菜单栏选择地域。

3. 在 **实例** 页面，单击目标 **实例 ID**。

4. 在左侧导航栏，单击 **服务** ，并单击 **服务** 页签。

5. 单击 **创建服务** ，在 **创建服务** 面板，参考如下信息配置 AI 服务：

<table> <thead> <tr> <td><p><b>配置项</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>服务来源</b></p></td> <td><p>选择 <b>AI 服务</b></p></td> </tr> <tr> <td><p><b>服务名称</b></p></td> <td><p>填写服务名称，如 <code>vertex-rest-api</code></p></td> </tr> <tr> <td><p><b>大模型供应商</b></p></td> <td><p>选择 <b>Vertex AI</b></p></td> </tr> <tr> <td><p><b>鉴权方式</b></p></td> <td><p>选择 <b>GCP Service Account</b> 或 <b>Vertex AI Express Mode</b>（参考场景一、场景二）</p></td> </tr> <tr> <td><p><b>模型协议</b></p></td> <td><p><b>选择「原生协议」</b></p></td> </tr> </tbody> </table>

**重要提示**：

* **模型协议必须选择「原生协议」**，表示使用 Vertex AI 原生 REST API 格式。

* 选择「原生协议」后，将不会显示「OpenAI 协议兼容方式」选项，因为此模式不进行协议转换。

### 2. 创建 Model API

1. 在左侧导航栏，单击 **Model API** ，然后单击 **创建 Model API**。

2. 在 **创建 Model API** 面板中，配置基本信息如下：

   * **域名**：建议配置自定义域名（使用默认环境域名存在限流）。

   * **Base Path** ：API 的基本路径，如 `/vertex-api`。

   * **使用场景**：根据您的需求选择（此处仅是控制台的分类辅助，混用也不会有问题）：

     * **文本生成**：适用于 Llama 等文本模型

     * **图片生成**：适用于 Imagen 4 等图片生成模型

     * **视频生成**：适用于 Veo 3 等视频生成模型

   * **协议** ：选择 **VertexAI**。

   * **路由配置**：选择 VertexAI 协议后，网关会自动配置以下两条内置路由：

     <table> <thead> <tr> <td><p><b>路由路径</b></p></td> <td><p><b>用途</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>/{api-version}/publishers/{publisher}/models/{model}:{action}</code></p></td> <td><p>Express Mode 使用的路径格式</p></td> </tr> <tr> <td><p><code>/{api-version}/projects/{project}/locations/{location}/publishers/{publisher}/models/{model}:{action}</code></p></td> <td><p>Service Account 模式使用的路径格式</p></td> </tr> </tbody> </table>
   * **服务模型**：单模型服务。

   * **服务列表**：

     * **服务名称** ：选择上一步中创建的 AI 服务（如 `vertex-rest-api`）。

     * **模型名称**：选择透传。

3. 单击 **确定** 完成创建。

### 3. 调用示例

配置完成后，您可以使用 Vertex AI 原生 REST API 格式进行调用。

**使用 Imagen 4 生成图片（Express Mode）**：

```
HELPCODEESCAPE-bash
curl -X POST "https://your-gateway-domain/vertex-api/v1/publishers/google/models/imagen-4.0-generate-preview-06-06:predict" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "instances": [
      {
        "prompt": "一只可爱的橘猫在阳光下打盹"
      }
    ],
    "parameters": {
      "sampleCount": 1,
      "aspectRatio": "1:1"
    }
  }'
```

**使用 Veo 3 生成视频（Express Mode）**：

```
HELPCODEESCAPE-bash
curl -X POST "https://your-gateway-domain/vertex-api/v1/publishers/google/models/veo-3.0-generate-preview:predictLongRunning" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "instances": [
      {
        "prompt": "一只橘猫在草地上奔跑的慢动作视频"
      }
    ],
    "parameters": {
      "aspectRatio": "16:9",
      "durationSeconds": 8
    }
  }'
```

### 支持的模型

<table> <thead> <tr> <td><p><b>模型类别</b></p></td> <td><p><b>模型示例</b></p></td> <td><p><b>Publisher</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>图片生成</p></td> <td><p>Imagen 4 (<code>imagen-4.0-generate-preview-06-06</code>)</p></td> <td><p>google</p></td> </tr> <tr> <td><p>视频生成</p></td> <td><p>Veo 3 (<code>veo-3.0-generate-preview</code>)</p></td> <td><p>google</p></td> </tr> <tr> <td><p>文本生成</p></td> <td><p>Llama 4 (<code>llama-4-maverick-17b-128e-instruct-maas</code>)</p></td> <td><p>meta</p></td> </tr> </tbody> </table>

**说明** 具体支持的模型列表请参考 [Google官方文档](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models)。

*** ** * ** ***

## 场景四：Google GenAI SDK 模式接入
> **不推荐使用**：此模式下网关仅作为透明代理，无法使用 AI 服务中配置的鉴权信息，功能受限。建议使用场景一、场景二或场景三的接入方式，可获得更完整的功能支持。

如果您使用 Google 官方提供的 `google-genai` SDK 进行开发，可以通过此模式将 SDK 请求代理到 AI 网关，实现请求观测和计量功能。

**重要说明** ：由于 GenAI SDK 的鉴权方式是客户端先向 Google 认证服务器发起 OAuth 2.0 认证请求，再进行模型推理 API 调用，因此在此模式下**无法使用 AI 服务中配置的鉴权信息**。网关仅作为透明代理，用于观测和计量推理 API 的调用。

### 1. 创建 DNS 服务

由于 SDK 自行完成鉴权，您需要创建一个 DNS 类型的服务直接指向 Vertex AI 后端。

1. 登录 [AI 网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择 **实例**，并在顶部菜单栏选择地域。

3. 在 **实例** 页面，单击目标 **实例 ID**。

4. 在左侧导航栏，单击 **服务** ，并单击 **服务** 页签。

5. 单击 **创建服务** ，在 **创建服务** 面板，参考如下信息配置 DNS 服务：

<table> <thead> <tr> <td><p><b>配置项</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>服务来源</b></p></td> <td><p>选择 <b>DNS 域名</b></p></td> </tr> <tr> <td><p><b>服务名称</b></p></td> <td><p>填写服务名称，如 <code>vertex-dns</code></p></td> </tr> <tr> <td><p><b>服务地址</b></p></td> <td><p>填写 Vertex AI API 地址，可选择以下两种格式：<br>• <code>aiplatform.googleapis.com:443</code>（全局端点）<br>• <code>{location}-aiplatform.googleapis.com:443</code>（区域端点，如 <code>us-central1-aiplatform.googleapis.com:443</code>）</p></td> </tr> <tr> <td><p><b>TLS 模式</b></p></td> <td><p>选择 <b>单向</b></p></td> </tr> <tr> <td><p><b>SNI</b></p></td> <td><p>默认与填入的域名一致，无需手动修改</p></td> </tr> </tbody> </table>

**说明**

* 使用全局端点 `aiplatform.googleapis.com:443` 适用于 Express Mode。

* 使用区域端点 `{location}-aiplatform.googleapis.com:443` 适用于 Service Account 模式，需根据您的 GCP 项目所在区域填写。

### 2. 创建 Model API

1. 在左侧导航栏，单击 **Model API** ，然后单击 **创建 Model API**。

2. 在 **创建 Model API** 面板中，配置基本信息如下：

   * **域名**：建议配置自定义域名（使用默认环境域名存在限流）。

   * **Base Path** ：API 的基本路径（可选），如 `/vertex`。

   * **模型类型** ：选择 **文本生成** 或 **图片生成**。

   * **协议** ：选择 **VertexAI**。

   * **路由配置**：选择 VertexAI 协议后，网关会自动配置以下两条内置路由：

     \| **路由路径** \| **用途** \|

     \|------------------------------------------------------------------------------------------------\|---------\|

     \| `/{api-version}/publishers/{publisher}/models/{model}:{action}` \| Express Mode 使用的路径格式 \|

     \| `/{api-version}/projects/{project}/locations/{location}/publishers/{publisher}/models/{model}:{action}` \| Service Account 模式使用的路径格式 \|
   * **服务模型**：单模型服务。

   * **服务列表**：

     * **服务名称** ：选择上一步中创建的 DNS 服务（如 `vertex-dns`）。

     * **模型名称**：选择透传。

3. 单击 **确定** 完成创建。

### 3. 配置 GenAI SDK

在您的 Python 代码中，将 GenAI SDK 的 `base_url` 指向 AI 网关地址：

```
HELPCODEESCAPE-python
from google import genai

# 配置 API Key（Express Mode）或使用默认凭证（Service Account）
API_KEY = "your-api-key"

# 网关地址 = 域名 + Base Path（如果配置了的话）
# 示例：如果域名为 your-gateway-domain.com，Base Path 为 /vertex
base_url = "https://your-gateway-domain.com/vertex"

# 创建客户端，将请求代理到 AI 网关
client = genai.Client(
    vertexai=True,  # 目前仅支持 vertexai=True
    api_key=API_KEY,
    http_options={
        'base_url': base_url,
    },
)

# 调用模型
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="你好，请介绍一下你自己",
)

print(response.text)
```

**配置说明**：
<table> <thead> <tr> <td><p><b>参数</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>vertexai</code></p></td> <td><p>必须设置为 <code>True</code>，表示使用 Vertex AI 后端</p></td> </tr> <tr> <td><p><code>api_key</code></p></td> <td><p>Express Mode 的 API Key，或留空使用默认的 Service Account 凭证</p></td> </tr> <tr> <td><p><code>base_url</code></p></td> <td><p>AI 网关的访问地址，格式为 <code>https://{域名}{Base Path}</code></p></td> </tr> </tbody> </table>

**使用 Service Account 模式**：

如果使用 Service Account 进行认证，可以通过环境变量配置凭证：

```
HELPCODEESCAPE-bash
# 设置 Service Account 密钥文件路径
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

```
HELPCODEESCAPE-python
from google import genai

# Service Account 模式下无需设置 api_key
base_url = "https://your-gateway-domain.com/vertex"

client = genai.Client(
    vertexai=True,
    http_options={
        'base_url': base_url,
    },
)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="你好，请介绍一下你自己",
)

print(response.text)
```

### 4. 验证接入效果

配置完成后，您可以在 AI 网关控制台查看请求的观测数据：

1. 在左侧导航栏，单击 **观测分析** \> **日志中心**。

2. 查看通过 GenAI SDK 发起的请求记录，包括：

   * 请求路径

   * 响应状态码

   * 响应时间

   * Token 用量（如果响应中包含）

**说明** 由于鉴权在客户端完成，网关无法进行鉴权配置代理。如需完整的AI网关使用体验，建议使用场景一、场景二或场景三的接入方式。

*** ** * ** ***

## 场景五：多模态理解场景接入
本场景介绍如何使用 Gemini 模型通过 Chat Completions 接口理解和分析图片、视频等多模态内容。多模态理解基于文本对话接口，因此可以复用场景一或场景二中创建的 AI 服务和 Model API。

### 配置要点

* **AI 服务** ：选择 **Vertex AI** 作为大模型供应商，GCP Service Account 或 Express Mode 均可

* **Model API** ：使用场景选择 **文本生成** ，协议选择 **OpenAI 兼容** ，路由需要勾选 `/v1/chat/completions`

### 图片理解

**方式一：使用图片 URL**

```
HELPCODEESCAPE-python
from openai import OpenAI

client = OpenAI(
    base_url="http(s)://{your-domain}/{model-api-base-path}/v1"
)

completion = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "这道题怎么解答？"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"
                    },
                },
            ],
        }
    ],
)

print(completion.choices[0].message.content)
```

**方式二：使用 Base64 编码图片**

```
HELPCODEESCAPE-python
import base64
from openai import OpenAI

client = OpenAI(
    base_url="http(s)://{your-domain}/{model-api-base-path}/v1"
)

# 将本地图片编码为 Base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# 指定图片路径
image_path = "<your-image-path>"
base64_image = encode_image(image_path)

completion = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "这张图片里有什么？"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        }
    ],
)

print(completion.choices[0].message.content)
```

**支持的图片格式**：image/png, image/jpeg, image/webp, image/heic, image/heif

不同模型的支持能力详见[Google官方文档](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models)。

### 视频理解

**说明** ：由于 OpenAI 的接口规范仅定义了 `image_url` 类型，但这不妨碍我们传入视频内容。AI 网关会自动完成兼容性转换，将视频内容正确传递给 Vertex AI。

**方式一：使用视频 URL**

```
HELPCODEESCAPE-python
from openai import OpenAI

client = OpenAI(
    base_url="http(s)://{your-domain}/{model-api-base-path}/v1"
)

completion = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "简要描述视频内容"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                    },
                },
            ],
        }
    ],
)

print(completion.choices[0].message.content)
```

**方式二：使用 Base64 编码视频**

```
HELPCODEESCAPE-python
import base64
from openai import OpenAI

client = OpenAI(
    base_url="http(s)://{your-domain}/{model-api-base-path}/v1"
)

# 将本地视频编码为 Base64
def encode_video(video_path):
    with open(video_path, "rb") as video_file:
        return base64.b64encode(video_file.read()).decode("utf-8")

# 指定视频路径
video_path = "example.mp4"
base64_video = encode_video(video_path)

completion = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "简要描述视频内容"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:video/mp4;base64,{base64_video}",
                    },
                },
            ],
        }
    ],
)

print(completion.choices[0].message.content)
```

**支持的视频格式**：video/x-flv, video/quicktime, video/mpeg, video/mpegs, video/mpg, video/mp4, video/webm, video/wmv, video/3gpp

不同模型的支持能力详见[Google官方文档](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models)。

### 代码说明

<table> <thead> <tr> <td><p><b>参数</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>model</code></p></td> <td><p>支持多模态理解的 Gemini 模型，如 <code>gemini-3-flash-preview</code>、<code>gemini-2.0-flash</code> 等</p></td> </tr> <tr> <td><p><code>content</code></p></td> <td><p>消息内容数组，包含文本和媒体（图片/视频）两部分</p></td> </tr> <tr> <td><p><code>type: "text"</code></p></td> <td><p>文本提示，描述您希望模型对媒体内容进行的分析</p></td> </tr> <tr> <td><p><code>type: "image_url"</code></p></td> <td><p>媒体内容，支持图片或视频的 URL 及 Base64 编码格式</p></td> </tr> </tbody> </table>

*** ** * ** ***

## 场景六：图片生成场景接入
本场景介绍如何使用 Vertex AI 的 Gemini Nano Banana Pro（模型 ID：`gemini-3-pro-image-preview`）等模型，通过 OpenAI 兼容协议实现图片生成、图片编辑（Edit）和图片变体（Variation）。

### 配置要点

与场景一或场景二类似，但有以下关键差异：
<table> <thead> <tr> <td><p><b>配置项</b></p></td> <td><p><b>图片生成场景配置</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>AI 服务 - 大模型供应商</b></p></td> <td><p>选择 <b>Vertex AI</b></p></td> </tr> <tr> <td><p><b>AI 服务 - 鉴权方式</b></p></td> <td><p>GCP Service Account 或 Express Mode 均可</p></td> </tr> <tr> <td><p><b>AI 服务 - OpenAI 协议兼容方式</b>（仅 GCP Service Account 模式）</p></td> <td><p><b>必须选择「AI 网关转换」</b></p></td> </tr> <tr> <td><p><b>Model API - 使用场景</b></p></td> <td><p>选择 <b>图片生成</b></p></td> </tr> <tr> <td><p><b>Model API - 协议</b></p></td> <td><p>选择 <b>OpenAI 兼容</b></p></td> </tr> <tr> <td><p><b>Model API - 路由配置</b></p></td> <td><p>按需勾选 <code>/v1/images/generations</code>、<code>/v1/images/edits</code>、<code>/v1/images/variations</code></p></td> </tr> </tbody> </table>

**重要提示** ：在 GCP Service Account 模式下进行图片生成/编辑/变体时，**OpenAI 协议兼容方式必须选择「AI 网关转换」**。这是因为 Vertex AI 原生兼容端点目前仅支持文本对话接口（Chat Completions），而 AI 网关的协议转换支持图片相关接口的转换。

### 接口支持矩阵

<table> <thead> <tr> <td><p><b>接口</b></p></td> <td><p><b>OpenAI SDK 推荐调用方式</b></p></td> <td><p><code><b>image_url</b></code><b>（非文件上传）用法支持情况</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>/v1/images/generations</code></p></td> <td><p><code>client.images.generate()</code>（JSON）</p></td> <td><p>不涉及（该接口通常无需传 <code>image_url</code>）</p></td> </tr> <tr> <td><p><code>/v1/images/edits</code></p></td> <td><p><code>client.images.edit(image=\&lt;file\&gt;)</code>（multipart）</p></td> <td><p>OpenAI SDK 对 <code>image_url</code> 写法不支持；如需 <code>image_url</code> 请使用 HTTP JSON 请求（SDK 的 multipart 文件上传可正常使用）</p></td> </tr> <tr> <td><p><code>/v1/images/variations</code></p></td> <td><p><code>client.images.create_variation(image=\&lt;file\&gt;)</code>（multipart）</p></td> <td><p>OpenAI SDK 对 <code>image_url</code> 写法不支持；如需 <code>image_url</code> 请使用 HTTP JSON 请求（SDK 的 multipart 文件上传可正常使用）</p></td> </tr> </tbody> </table>

### 图片生成（`/v1/images/generations`）

配置完成后，您可以使用 OpenAI Python SDK 调用图片生成接口：

```
HELPCODEESCAPE-python
from openai import OpenAI
from PIL import Image
from io import BytesIO
import base64

# 创建客户端，指向 AI 网关地址
client = OpenAI(
    base_url="http(s)://{your-domain}/{model-api-base-path}/v1"
)

# 调用图片生成接口
response = client.images.generate(
    model="gemini-3-pro-image-preview",  # Gemini Nano Banana Pro 模型
    prompt="一只可爱的橘猫在阳光下打盹",
    size="1024x1024",
    n=1
)

# 获取生成的图片（base64 编码）
image_data = response.data[0].b64_json
if image_data:
    # 解码并保存图片到本地
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    image.save("output_folder/example-image-cat.png")
    print("图片已保存到 output_folder/example-image-cat.png")
```

**代码说明**：
<table> <thead> <tr> <td><p><b>参数</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>base_url</code></p></td> <td><p>AI 网关的访问地址，格式为 <code>http(s)://{域名}/{Base Path}</code></p></td> </tr> <tr> <td><p><code>model</code></p></td> <td><p>模型 ID，Gemini Nano Banana Pro 的模型 ID 为 <code>gemini-3-pro-image-preview</code></p></td> </tr> <tr> <td><p><code>prompt</code></p></td> <td><p>图片生成的提示词，描述您想要生成的图片内容</p></td> </tr> <tr> <td><p><code>size</code></p></td> <td><p>生成图片的尺寸，如 <code>1024x1024</code>（详见下方尺寸映射表）</p></td> </tr> <tr> <td><p><code>n</code></p></td> <td><p>生成图片的数量</p></td> </tr> </tbody> </table>

**尺寸参数映射**：

由于 OpenAI 接口使用分辨率（如 `1024x1024`）而 Vertex AI 使用宽高比（aspectRatio）+ 分辨率等级（imageSize）的方式，AI 网关会自动进行参数转换。

Vertex AI 支持的宽高比：`1:1`、`3:2`、`2:3`、`3:4`、`4:3`、`4:5`、`5:4`、`9:16`、`16:9`、`21:9`

Vertex AI 支持的分辨率等级：`1k`、`2k`、`4k`
<table> <thead> <tr> <td><p><b>OpenAI size 参数</b></p></td> <td><p><b>Vertex AI aspectRatio</b></p></td> <td><p><b>Vertex AI imageSize</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>256x256</code></p></td> <td><p>1:1</p></td> <td><p>1k</p></td> </tr> <tr> <td><p><code>512x512</code></p></td> <td><p>1:1</p></td> <td><p>1k</p></td> </tr> <tr> <td><p><code>1024x1024</code></p></td> <td><p>1:1</p></td> <td><p>1k</p></td> </tr> <tr> <td><p><code>1792x1024</code></p></td> <td><p>16:9</p></td> <td><p>2k</p></td> </tr> <tr> <td><p><code>1024x1792</code></p></td> <td><p>9:16</p></td> <td><p>2k</p></td> </tr> <tr> <td><p><code>2048x2048</code></p></td> <td><p>1:1</p></td> <td><p>2k</p></td> </tr> <tr> <td><p><code>4096x4096</code></p></td> <td><p>1:1</p></td> <td><p>4k</p></td> </tr> <tr> <td><p><code>1536x1024</code></p></td> <td><p>3:2</p></td> <td><p>2k</p></td> </tr> <tr> <td><p><code>1024x1536</code></p></td> <td><p>2:3</p></td> <td><p>2k</p></td> </tr> <tr> <td><p><code>1024x768</code></p></td> <td><p>4:3</p></td> <td><p>1k</p></td> </tr> <tr> <td><p><code>768x1024</code></p></td> <td><p>3:4</p></td> <td><p>1k</p></td> </tr> <tr> <td><p><code>1280x1024</code></p></td> <td><p>5:4</p></td> <td><p>1k</p></td> </tr> <tr> <td><p><code>1024x1280</code></p></td> <td><p>4:5</p></td> <td><p>1k</p></td> </tr> <tr> <td><p><code>2560x1080</code></p></td> <td><p>21:9</p></td> <td><p>2k</p></td> </tr> </tbody> </table>

**CURL 调用示例**：

```
HELPCODEESCAPE-bash
curl -X POST "https://your-gateway-domain/gemini-image/v1/images/generations" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3-pro-image-preview",
    "prompt": "一只可爱的橘猫在阳光下打盹",
    "size": "1024x1024",
    "n": 1
  }'
```

### 图片编辑（`/v1/images/edits`）

配置完成后，您可以使用 OpenAI Python SDK 通过 multipart 方式上传原图并执行编辑：

```
HELPCODEESCAPE-python
from openai import OpenAI
from PIL import Image
from io import BytesIO
import base64

client = OpenAI(
    base_url="http(s)://{your-domain}/{model-api-base-path}/v1",
    api_key="YOUR_API_KEY"
)

# 使用文件上传方式调用 Edit 接口（OpenAI SDK 推荐方式）
with open("assets/image-cat.png", "rb") as image_file:
    response = client.images.edit(
        model="gemini-3-pro-image-preview",
        prompt="将猫的品种修改为布偶猫，保持原图姿势",
        image=image_file,
        size="1024x1024",
        n=1
    )

image_data = response.data[0].b64_json
if image_data:
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    image.save("output_folder/edited-image-cat.png")
    print("图片编辑完成，已保存到 output_folder/edited-image-cat.png")
```

#### 使用 HTTP 请求传递 `image_url`（SDK 不支持该写法）

`/v1/images/edits` 在 HTTP JSON 请求中支持传入 data URL。以下示例展示如何将本地图片转为 Base64 后通过 `curl` 直接调用：

```
HELPCODEESCAPE-bash
# 1) 将本地图片转为 Base64（去掉换行）
BASE64_IMAGE=$(base64 < assets/image-cat.png | tr -d '\n')

# 2) 通过 image_url(data URL) 调用 edits 接口
curl -X POST "https://your-gateway-domain/{model-api-base-path}/v1/images/edits" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d "{
    \"model\": \"gemini-3-pro-image-preview\",
    \"prompt\": \"将猫的品种修改为布偶猫，保持原图姿势\",
    \"image_url\": {
      \"url\": \"data:image/png;base64,${BASE64_IMAGE}\"
    },
    \"size\": \"1024x1024\",
    \"n\": 1
  }"
```

### 图片变体（`/v1/images/variations`）

配置完成后，您可以使用 OpenAI Python SDK 通过 multipart 方式生成图片变体：

```
HELPCODEESCAPE-python
from openai import OpenAI
from PIL import Image
from io import BytesIO
import base64

client = OpenAI(
    base_url="http(s)://{your-domain}/{model-api-base-path}/v1",
    api_key="YOUR_API_KEY"
)

with open("assets/image-cat.png", "rb") as image_file:
    response = client.images.create_variation(
        model="gemini-3-pro-image-preview",
        image=image_file,
        size="1792x1024",
        n=1
    )

image_data = response.data[0].b64_json
if image_data:
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    image.save("output_folder/variation-image-cat.png")
    print("图片变体生成完成，已保存到 output_folder/variation-image-cat.png")
```

如果您希望在 Variation 场景中使用 `image_url`（URL 或 data URL）而不是文件上传，也可以直接使用 HTTP JSON 请求：

```
HELPCODEESCAPE-bash
# 1) 将本地图片转为 Base64（去掉换行）
BASE64_IMAGE=$(base64 < assets/image-cat.png | tr -d '\n')

# 2) 通过 image_url(data URL) 调用 variations 接口
curl -X POST "https://your-gateway-domain/{model-api-base-path}/v1/images/variations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d "{
    \"model\": \"gemini-3-pro-image-preview\",
    \"image_url\": {
      \"url\": \"data:image/png;base64,${BASE64_IMAGE}\"
    },
    \"size\": \"1792x1024\",
    \"n\": 1
  }"
```

### 支持的图片生成模型

<table> <thead> <tr> <td><p><b>模型名称</b></p></td> <td><p><b>模型 ID</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>Gemini Nano Banana Pro</p></td> <td><p><code>gemini-3-pro-image-preview</code></p></td> <td><p>Google 最新的图片生成模型，支持高质量图片生成</p></td> </tr> <tr> <td><p>Gemini Nano Banana</p></td> <td><p><code>gemini-2.5-flash-image</code></p></td> <td><p>Google 上一代图片生成模型，支持高质量图片生成</p></td> </tr> </tbody> </table>

**说明** 具体支持的图片生成模型列表请参考 [Google官方文档](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models)。

*** ** * ** ***

## 高级配置
### 多供应商高可用配置

为了实现更高的可用性，您可以配置 Vertex AI 与其他供应商形成 Fallback 关系：

1. 创建多个 AI 服务（如 Vertex AI + 阿里云百炼）。

2. 创建 Model API 时，选择 **多模型服务（按模型名称）**。

3. 配置路由规则：

   * **服务名称** ：vertex-ai，**模型名称匹配规则** ：`gemini*`

   * **服务名称** ：bailian，**模型名称匹配规则** ：`qwen*`

4. 开启 **Fallback**，选择备用服务。

### 安全配置建议

1. **凭证管理**：建议通过引用凭据方式将 Service Account Key 或 API Key 存储在阿里云 KMS 中，避免凭证泄露风险。

2. **访问控制**：配置 IP 白名单或其他访问控制策略，限制 API 访问来源。

3. **限流保护**：设置合理的限流规则，避免意外的高额费用。

*** ** * ** ***

## 常见问题
### 401/403 鉴权失败

* 检查 Service Account JSON 密钥的完整性，确保包含 `private_key`、`client_email`、`token_uri` 等必要字段。

* 确认 Service Account 具有 Vertex AI User 或更高权限。

* 对于 Express Mode，确认 API Key 有效且未过期。

### 404 模型不存在

* 确认使用的模型名称正确，如 `gemini-3-flash-preview`、`gemini-3-pro-preview` 等。

* 检查所选区域是否支持该模型。

### JSON 解析失败

* 确保粘贴的是完整的 Service Account JSON 内容，不要遗漏开头的 `{` 或结尾的 `}`。

* 检查 JSON 格式是否正确，可使用在线 JSON 验证工具进行验证。

### 请求超时

* 检查 VPC 是否正确配置公网 NAT 网关。

* 确认目标区域的网络连通性。

*** ** * ** ***

## 支持的模型
**说明** 具体支持的模型列表请参考 [Google Vertex AI 官方文档](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/overview)。

*** ** * ** ***

## 总结
通过阿里云 AI 网关，您可以轻松接入 Google Vertex AI，享受统一的 API 管理、灵活的鉴权方式和企业级的高可用保障：

* **GCP Service Account 模式**：适用于需要完整 Vertex AI 功能的企业级应用，支持 OpenAI 协议转换

* **Vertex AI Express Mode**：通过 API Key 快速接入，配置简单，适合快速验证

* **Vertex AI REST API 模式**：代理 Vertex AI 原生 REST API，适用于所有模型，常见用于 Imagen、Veo、Claude 等非 Gemini 系列模型

* **多模态理解场景**：使用 Gemini 模型通过 Chat Completions 接口理解和分析图片、视频等多模态内容

* **图片生成/编辑/变体场景**：使用 Gemini Nano Banana Pro 等模型进行生成、编辑和变体，通过 AI 网关协议转换实现 OpenAI 兼容

无论您选择哪种接入方式，AI 网关都能提供可靠的代理服务和丰富的观测能力。

<br />