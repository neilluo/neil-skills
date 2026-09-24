---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/configure-ai-log-policy
fetch_date: 2026-09-21
product: AI Gateway
slug: configure-ai-log-policy
body_sha256: fd880d9d434413eebf69b062dcb76667b8e89fc9730009ab97b3dadd196b5a65
body_bytes: 16380
migration_status: current
---

AI 网关在处理模型请求时会产生大量日志数据。AI 日志策略支持按需选择日志字段、使用内置模板批量添加字段、自定义日志字段及 JSON PATH 配置，从而控制日志记录范围、降低存储成本。此功能对已兼容协议（如 OpenAI、百炼）和自定义 HTTP 协议均适用，但两者的配置能力有所差异。  

## 前提条件
* 已开通阿里云 API 网关服务。

* 已创建 AI 网关实例。具体操作，请参见[创建网关实例](https://help.aliyun.com/document_detail/2881527.html)。

* 已配置至少一个 Model API 或 Agent API。具体操作，请参见[管理Model API](https://help.aliyun.com/document_detail/2859333.html) 和[Agent 网关管理](https://help.aliyun.com/document_detail/2937089.html)。

## 协议类型与配置能力
AI 网关根据 Model API 或 Agent API的协议类型提供不同的日志策略配置能力：
<table> <thead> <tr> <td><p><b>能力</b></p></td> <td><p><b>已兼容协议（如 OpenAI、百炼）</b></p></td> <td><p><b>自定义 HTTP 协议</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>预定义基础字段</p></td> <td><p>支持</p></td> <td><p>不支持</p></td> </tr> <tr> <td><p>内置模板批量添加</p></td> <td><p>支持</p></td> <td><p>支持</p></td> </tr> <tr> <td><p>自定义 JSON PATH 字段</p></td> <td><p>支持</p></td> <td><p>支持</p></td> </tr> <tr> <td><p>字段独立启用/禁用</p></td> <td><p>支持</p></td> <td><p>支持</p></td> </tr> </tbody> </table>

每条 Model API 的路径 （ Path ）拥有独立的字段配置。不同路径下，由于 API 请求或响应结构的不同，同一字段的 JSON PATH 可能有所不同。  
**说明**

已兼容协议中支持预定义基础字段能力的协议与场景：

* Model API：OpenAI和百炼下的文本生成、图片生成场景。

* Agent API：百炼应用。

## 启用 AI 请求日志
1. 登录 [API 网关控制台](https://apig.console.aliyun.com)。

2. 在左侧导航栏，单击**AI 网关** \> **实例**。

3. 在 AI 网关页面，单击目标实例名称，进入实例详情页。

4. 单击 **Model API** 页签，在 Model API 列表中单击目标 Model API 名称。

5. 在 API 详情页，单击**策略与插件**页签。

6. 在**预置策略与插件** 区域，找到**AI 请求日志**面板，开启开关，单击展开。

7. 根据 Model API 的协议类型，配置日志字段：

   * 已兼容协议（如 OpenAI）：参见[配置已兼容协议的日志字段](#sec04compatible)。

   * 自定义 HTTP 协议：参见[配置自定义 HTTP 协议的日志字段](#sec05custom)。

8. 配置完成后，单击**保存**。

## 配置已兼容协议的日志字段
对于使用已兼容协议（如 OpenAI）的 Model API，AI 请求日志面板提供基础字段管理、模板批量添加和自定义字段三项能力。

### 面板布局

<table> <thead> <tr> <td><p><b>区域</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>启用开关</p></td> <td><p>控制 AI 请求日志功能的开启和关闭。</p></td> </tr> <tr> <td><p>Path 列表</p></td> <td><p>显示当前 Model API 支持的所有路径。选择不同路径时，右侧字段配置随之切换。</p></td> </tr> <tr> <td><p>基础字段</p></td> <td><p>基础字段主要覆盖对话、元信息、用量、工具四个分类。</p></td> </tr> <tr> <td><p>自定义字段</p></td> <td><p>手动添加的自定义日志字段。</p></td> </tr> <tr> <td><p>操作按钮</p></td> <td> <ul> <li><p>从模板批量添加：从内置支持模板中批量导入字段。</p></li> <li><p><b>添加自定义字段</b>：手动添加字段。</p></li> </ul></td> </tr> </tbody> </table>  
**说明**

* Path 列表包含当前 API 支持的各个路径，典型的 Path 如 OpenAI 兼容的`/v1/chat/completions`、`/v1/completions`。在后端服务模型为多服务时，一个 Path 可能对应多条路由，同 Path 的多条路由对应使用同一份配置。

* 每个字段可通过行首的开关控件独立启用或禁用。表头显示当前启用数量和总数，如 "基础字段 (14/24)"。单击**仅展示开启的字段**可过滤仅显示已启用的字段。

### 基础字段

主要的基础字段按分类组织如下：
<table> <thead> <tr> <td><p><b>分类</b></p></td> <td><p><b>字段示例</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>对话</p></td> <td><p>question、answer</p></td> <td><p>用户提问和模型响应内容。</p></td> </tr> <tr> <td><p>元信息</p></td> <td><p>request_model、model、chat_id</p></td> <td><p>请求模型名称、响应模型名称、会话 ID。</p></td> </tr> <tr> <td><p>用量</p></td> <td><p>input_token、output_token、total_token、input_token_details、output_token_details、input_tokens_details.cached_tokens、output_tokens_details.reasoning_tokens</p></td> <td><p>请求和响应的 Token 消耗量及明细。</p></td> </tr> <tr> <td><p>工具</p></td> <td><p>tool_use</p></td> <td><p>工具调用信息。</p></td> </tr> </tbody> </table>  
**说明**

* **字段记录位置** ：基础字段统一以固定的 Key（字段名称）写入日志。其中，除 answer、question外，其余基础字段均作为一级字段存放在 `ai_log` 字段下，answer 与 question 已从`ai_log`中单独抽取，作为独立字段存放。

* **系统内置字段**：model、chat_id、input_token、input_token_details、output_token、output_token_details、total_token 为系统内置字段。系统内置字段默认开启，字段提取时优先按已配置的 JSON PATH 进行提取，未配置时按系统内置规则进行默认提取。

* **流式与非流式字段** ：多数响应字段同时支持非流式响应和流式响应两种提取方式，对应不同的 JSON PATH 配置。以 answer 字段为例，在 `/v1/chat/completions` 路径下，非流式响应的提取路径为 `choices.0.message.content`，流式响应的提取路径为 `choices.0.delta.content`。

### JSON PATH 配置

##### **JSON PATH 配置语法**

JSON Path 配置采用 **GJSON** 语法，用于从 API 请求或响应的 JSON 数据中提取指定字段值。

**语法说明：**

* 使用 `.` 访问对象中的字段

* 使用数组下标访问数组元素，下标从 `0` 开始

* 支持多层嵌套访问

例如，`choices.0.message.content` 表示：

* 先获取 `choices` 数组

* 再取第 `0` 个元素

* 然后依次获取其中的 `message.content` 字段值

**示例：**

以下为一个响应示例：

```
HELPCODEESCAPE-json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "我是阿里云开发的一款超大规模语言模型，我叫千问。"
      },
      "finish_reason": "stop",
      "index": 0
    }
  ],
  "object": "chat.completion",
  "usage": {
    "prompt_tokens": 3019,
    "completion_tokens": 104,
    "total_tokens": 3123,
    "prompt_tokens_details": {
      "cached_tokens": 2048
    }
  },
  "model": "qwen-plus",
  "id": "chatcmpl-6ada9ed2-7f33-9de2-8bb0-78bd4035025a"
}
```

对应字段的 JSON PATH 示例：
<table> <thead> <tr> <td><p><b>字段名称</b></p></td> <td><p><b>JSON PATH</b></p></td> <td><p><b>提取结果</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>answer</code></p></td> <td><p><code>choices.0.message.content</code></p></td> <td><p><code>我是阿里云开发的一款超大规模语言模型，我叫千问。</code></p></td> </tr> <tr> <td><p><code>model</code></p></td> <td><p><code>model</code></p></td> <td><p><code>qwen-plus</code></p></td> </tr> <tr> <td><p><code>input_token</code></p></td> <td><p><code>usage.prompt_tokens</code></p></td> <td><p><code>3019</code></p></td> </tr> </tbody> </table>

##### **不同路径或来源下的 JSON PATH 差异**

Model API 可能关联多个路径（如 `/v1/chat/completions`、`/v1/completions`、`/v1/responses`），不同路径和来源下同一字段的 JSON PATH 存在差异。以 question、answer、input_token 三个代表性字段为例：
<table> <thead> <tr> <td><p><b>字段</b></p></td> <td><p><b>来源</b></p></td> <td><p><code><b>/v1/chat/completions</b></code></p></td> <td><p><code><b>/v1/completions</b></code></p></td> <td><p><code><b>/v1/responses</b></code></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>question</p></td> <td><p>请求</p></td> <td><p><code>messages.@reverse.#(role=="user").content</code></p></td> <td><p><code>prompt</code></p></td> <td><p><code>input</code></p></td> </tr> <tr> <td><p>answer</p></td> <td><p>非流式响应</p></td> <td><p><code>choices.0.message.content</code></p></td> <td><p><code>choices.0.text</code></p></td> <td><p><code>output.#(type=="message").content.#(type=="output_text").text</code></p></td> </tr> <tr> <td><p>answer</p></td> <td><p>流式响应</p></td> <td><p><code>choices.0.delta.content</code></p></td> <td><p><code>choices.0.text</code></p></td> <td><p><code>delta</code></p></td> </tr> <tr> <td><p>input_token</p></td> <td><p>非流式响应</p></td> <td><p><code>usage.prompt_tokens</code></p></td> <td><p><code>usage.prompt_tokens</code></p></td> <td><p><code>usage.input_tokens</code></p></td> </tr> <tr> <td><p>input_token</p></td> <td><p>流式响应</p></td> <td><p><code>usage.prompt_tokens</code></p></td> <td><p><code>usage.prompt_tokens</code></p></td> <td><p><code>response.usage.input_tokens</code></p></td> </tr> </tbody> </table>  
**说明**

* 在 Path 列表中切换不同的路径时，对应的基础字段 JSON PATH 会自动更新。修改某个路径下的字段配置不会影响其他路径。

* 如需修改某个字段的 JSON PATH，可在字段所在行的操作列中单击**编辑**，并在弹出的编辑对话框中修改对应的 JSON PATH 值。系统将根据配置的 JSON PATH，从 API 请求或响应中提取相应字段。

### 通过内置模板批量添加字段

AI 请求日志提供内置模板，可批量添加预定义字段。

1. 在 AI 请求日志面板，单击"从模板批量添加"。

2. **选择模板** ，然后勾选需要添加的字段，单击**批量添加**。

内置模板共 15 个，按提供商分为以下两组：

**OpenAI 模板**（6 个）
<table> <thead> <tr> <td><p>场景</p></td> <td><p><b>路径</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>文本生成</p></td> <td><p><code>/v1/chat/completions</code></p></td> </tr> <tr> <td><p><code>/v1/completions</code></p></td> </tr> <tr> <td><p><code>/v1/responses</code></p></td> </tr> <tr> <td><p>图片生成</p></td> <td><p><code>/v1/images/generations</code></p></td> </tr> <tr> <td><p><code>/v1/images/edits</code></p></td> </tr> <tr> <td><p><code>/v1/images/variations</code></p></td> </tr> </tbody> </table>

**百炼模板**（9 个）
<table> <thead> <tr> <td><p>场景</p></td> <td><p><b>路径</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>文本生成</p></td> <td><p><code>/api/v1/services/aigc/text-generation/generation</code></p></td> </tr> <tr> <td><p>图片生成</p></td> <td><p><code>/api/v1/services/aigc/text2image/image-synthesis</code></p></td> </tr> <tr> <td><p><code>/api/v1/services/aigc/image2image/image-synthesis</code></p></td> </tr> <tr> <td><p><code>/api/v1/services/aigc/image2image/out-painting</code></p></td> </tr> <tr> <td><p><code>/api/v1/services/aigc/virtualmodel/generation</code></p></td> </tr> <tr> <td><p><code>/api/v1/services/aigc/background-generation/generation</code></p></td> </tr> <tr> <td><p><code>/api/v1/services/aigc/multimodal-generation/generation</code></p></td> </tr> <tr> <td><p><code>/api/v1/tasks</code></p></td> </tr> <tr> <td><p>Agent应用</p></td> <td><p><code>/api/v1/apps/{app_id}/completion</code></p></td> </tr> </tbody> </table>  
**说明**

* 内置模板提供的可选字段数量显著多于基础字段。以 OpenAI `/v1/chat/completions` 模板为例，可选字段超过 200 个，并按照对话、配置、工具、用量、元信息、候选、标识、缓存、多模态、概率等类别进行组织，便于快速选择和配置。

* 内置模板中的字段配置可作为参考，实际字段定义及含义请以对应协议的 API 文档为准。

### 添加自定义字段

除基础字段和模板字段外，还可以手动添加自定义字段。

1. 在 AI 请求日志面板，单击**添加自定义字段**。

2. 配置以下参数：

   <table> <thead> <tr> <td><p><b>参数</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>字段名称</p></td> <td><p>自定义的字段名称，作为日志中\&nbsp;<code>ai_log</code>\&nbsp;字段下的 Key。</p></td> </tr> <tr> <td><p>来源</p></td> <td><p>字段来源，可选：请求、非流式响应、流式响应。</p></td> </tr> <tr> <td><p>Json Path</p></td> <td><p>从对应来源数据中提取字段值的 JSON Path 路径。</p></td> </tr> <tr> <td><p>描述</p></td> <td><p>字段的用途说明。</p></td> </tr> </tbody> </table>
3. 单击确认按钮完成配置。

自定义字段添加后，显示在**自定义字段** 标签页。可通过操作列的**编辑** 和**删除**管理已有字段。

## 配置自定义 HTTP 协议的日志字段
对于使用自定义 HTTP 协议的 Model API，AI 请求日志不提供带有预定义 JSON Path 的基础字段。需要根据实际规则，自行配置需要记录的字段，并可通过手动添加字段或从模板导入字段的方式完成配置。

配置方式如下：

1. 在 AI 请求日志面板，根据实际协议的请求和响应结构，通过**添加自定义字段**定义需要记录的字段。

2. 为每个字段指定正确的 JSON PATH，确保路径与实际数据结构匹配。

3. 也可以使用模板导入相近协议的模板作为基础，再根据实际协议结构调整 JSON PATH。

## 配置示例
### 示例一：记录 OpenAI 兼容协议的核心日志字段

以下示例展示如何在/v1/chat/completions路径下记录非流式对话内容和 Token 用量，以减少日志大小。

1. 进入目标 Model API 的**策略与插件** 页签，展开 **AI 请求日志**面板。

2. 选择 `/v1/chat/completions` 路径。

3. 在**基础字段**标签页，启用以下字段：

   <table> <thead> <tr> <td><p><b>字段名称</b></p></td> <td><p><b>来源</b></p></td> <td><p><b>分类</b></p></td> <td><p><b>用途</b></p></td> <td><p><b>默认启用</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>question</p></td> <td><p>请求</p></td> <td><p>对话</p></td> <td><p>记录用户提问内容</p></td> <td><p>否</p></td> </tr> <tr> <td><p>answer</p></td> <td><p>非流式响应</p></td> <td><p>对话</p></td> <td><p>记录非流式响应中模型的回答内容</p></td> <td><p>否</p></td> </tr> <tr> <td><p>input_token</p></td> <td><p>非流式响应</p></td> <td><p>用量</p></td> <td><p>记录输入 Token 数</p></td> <td><p>是</p></td> </tr> <tr> <td><p>output_token</p></td> <td><p>非流式响应</p></td> <td><p>用量</p></td> <td><p>记录输出 Token 数</p></td> <td><p>是</p></td> </tr> <tr> <td><p>total_token</p></td> <td><p>非流式响应</p></td> <td><p>用量</p></td> <td><p>记录 Token 总数</p></td> <td><p>是</p></td> </tr> </tbody> </table>
4. 单击**保存**。

### 示例二：使用模板批量添加百炼字段

以下示例展示如何通过内置模板快速添加百炼文本生成协议的日志字段。

1. 进入目标 Model API 的**策略与插件** 页签，展开 **AI 请求日志**面板。

2. 单击从模板批量添加。

3. **选择模板** 为`/api/v1/services/aigc/text-generation/generation`。

4. 勾选需要的字段，单击**批量添加**。

5. 根据实际需求，在字段列表中启用或禁用特定字段，或修改其Json Path。

6. 单击**保存**。

<br />