# 模型

> 来源: https://docs.qoder.com/zh/cli/model

## 模型选择方式

### 分级模型（Default）

| 级别 | 说明 | Credit 消耗 |
|------|------|------------|
| Auto（智能路由） | 智能选择最适合的模型 | ~1.0× |
| Ultimate（极致） | 专家级深度推理 | ~1.6× |
| Performance（性能） | 高级推理，高质量 | ~1.1× |
| Efficient（经济） | 标准推理，高性价比 | ~0.3× |
| Lite（轻量） | 基础推理，免费（Team版） | 免费 |

### 前沿模型（New Models）

| 模型名称 | 简介 | Credit 倍率 |
|---------|------|------------|
| Qwen3.7-Max | Agentic 能力全面跃迁 | 0.5× |
| Qwen3.7-Plus | 推理效率多模态跃迁 | 0.1× |
| DeepSeek-V4-Pro | 复杂推理代码生成 | 0.5× |
| DeepSeek-V4-Flash | 速度快成本低 | 0.1× |
| GLM-5.2 | 复杂系统工程长程任务 | 0.6× |
| Kimi-K2.7-Code | 长上下文编码 | 0.3× |
| MiniMax-M3 | 多模态1M上下文 | 0.2× |

### 自定义模型（Custom）

支持供应商：阿里云百炼、DeepSeek、智谱、Kimi、MiniMax、小米 MIMO

## 模型参数配置

### 上下文窗口
200K（标准）、400K（扩展）、1M（最大）

### 思考强度
low / medium / high / xhigh / max

### Fast 模式
部分模型提供 Fast 模式优先提升响应速度。

## 切换模型

- TUI：`/model` 打开选择界面
- 命令行：`--model efficient`、`--reasoning-effort high`、`--context-window 400000`
- 列出可用：`qodercli --list-models`
- 添加自定义：`/model` → Custom 标签页 → Add custom model
