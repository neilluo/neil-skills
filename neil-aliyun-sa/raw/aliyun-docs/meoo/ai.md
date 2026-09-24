> ## Documentation Index
> Fetch the complete documentation index at: https://docs.meoo.com/llms.txt
> Use this file to discover all available pages before exploring further.

# AI 服务

Meoo 提供开箱即用的 AI 大模型服务，当您的应用需要 AI 能力时，Meoo会自动为您集成并生成调用代码，无需手动配置。

## 支持的模型

### 文本对话

| 模型           | 传参值             | 特点                  |
| ------------ | --------------- | ------------------- |
| Qwen3.6-Plus | `qwen3.6-plus`  | 通义千问旗舰版，综合能力强       |
| Qwen3-Max    | `qwen3-max`     | 通义千问增强版，适合复杂推理      |
| Kimi         | `kimi-k2.5`     | 月之暗面出品，长文本处理能力强     |
| Deepseek     | `deepseek-v3.2` | 深度求索出品，代码与推理能力突出    |
| GLM          | `glm-5`         | 智谱 AI 出品，中文理解能力优秀   |
| MiniMax      | `MiniMax-M2.5`  | MiniMax 出品，多模态综合能力强 |

### 视觉理解

| 模型      | 传参值             | 特点          |
| ------- | --------------- | ----------- |
| Qwen VL | `qwen3-vl-plus` | 支持图片内容识别与分析 |

### 图片生成

| 模型             | 传参值              | 特点             |
| -------------- | ---------------- | -------------- |
| Qwen Image 2.0 | `qwen-image-2.0` | 通义图片生成，高质量、速度快 |
| Wan2.7         | `wan2.7-image`   | 万象图片生成，艺术风格丰富  |

## 计费方式

* 文本对话 / 视觉理解：按 Token 用量计费
* 图片生成：按生成张数计费

## 如何使用

Meoo AI 服务是内置服务，您无需手动配置模型或编写鉴权逻辑，只需在对话中描述您的需求，Meoo会自动完成以下步骤：

1. **识别需求** — 判断您的应用是否需要 AI 能力
2. **开通服务** — 自动为您的应用申请 Service AK，并以 `MEOO_PROJECT_API_KEY` 为名写入环境变量
3. **生成代码** — 自动生成 Edge Functions 服务端调用代码，通过 `MEOO_PROJECT_API_KEY` 读取 AK，不会暴露在前端
4. **完成集成** — 自动生成前端调用代码，完成端到端的 AI 功能集成

您可以在 **Cloud → AI** 中查看 AI 服务的使用记录与用量统计。

> 💡 如需在已有应用中追加 AI 功能，直接告诉Meoo您的需求即可，例如："帮我加一个 AI 对话功能"、"帮我实现图片内容识别"。

## 代码调用参考

Meoo会自动生成调用代码，以下为参考示例，实际代码由Meoo根据您的需求生成。

### 文本对话

```typescript theme={null}
const response = await fetch("https://api.meoo.host/meoo-ai/compatible-mode/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${Deno.env.get("MEOO_PROJECT_API_KEY")}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    model: "kimi-k2.5",  // 可替换为其他模型：qwen3.6-plus / qwen3-max / deepseek-v3.2 / glm-5 / MiniMax-M2.5
    messages: [
      { role: "user", content: "你好" }
    ],
    stream: false,
  }),
});

const data = await response.json();
console.log(data.choices[0].message.content);
```

### 视觉理解

```typescript theme={null}
const response = await fetch("https://api.meoo.host/meoo-ai/compatible-mode/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${Deno.env.get("MEOO_PROJECT_API_KEY")}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    model: "qwen3-vl-plus",
    messages: [
      {
        role: "user",
        content: [
          { type: "text", text: "这张图片里有什么？" },
          { type: "image_url", image_url: { url: "https://your-image-url.com/image.png" } },
        ],
      }
    ],
  }),
});

const data = await response.json();
console.log(data.choices[0].message.content);
```

### 图片生成

```typescript theme={null}
const response = await fetch("https://api.meoo.host/meoo-ai/api/v1/services/aigc/image-generation/generation", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${Deno.env.get("MEOO_PROJECT_API_KEY")}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    model: "qwen-image-2.0",  // 或 wan2.7-image
    input: {
      messages: [
        {
          role: "user",
          content: [{ text: "一只坐在窗边的橘猫，暖阳光照射" }],
        }
      ],
    },
    parameters: {
      size: "1024*1024",
    },
  }),
});

const data = await response.json();
```
