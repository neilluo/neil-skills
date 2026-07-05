# CLI Model — 模型系统

> Qoder CLI 的多层模型选择机制，在开发效率、输出质量与成本之间取得最佳平衡。

## 概述

CLI 内置 SOTA 级 AI 模型，提供三种选择方式：分级模型（智能路由）、前沿模型（指定具体模型）、自定义模型（接入第三方 API Key）。每种模型支持上下文窗口、思考强度等参数调节。

## 分级模型（Default）

五档选择器，类似智能汽车驾驶模式：

| 级别 | 定位 | Credit 消耗 | 适用场景 |
|------|------|------------|---------|
| Auto（智能路由） | 智能选择最适模型 | ~1.0× | 日常开发（推荐默认） |
| Ultimate（极致） | 专家级深度推理 | ~1.6× | 复杂系统设计、高难度分析 |
| Performance（性能） | 高级推理高质量 | ~1.1× | 核心功能实现、架构设计 |
| Efficient（经济） | 标准推理高性价比 | ~0.3× | 基础代码生成、单元测试 |
| Lite（轻量） | 基础推理 | 免费 | 快速验证、快问快答（Team 版） |

## 前沿模型（New Models）

| 模型 | 特色 | Credit 倍率 |
|------|------|------------|
| Qwen3.7-Max | Agentic 长程复杂任务 | 0.5× |
| Qwen3.7-Plus | 推理+多模态 | 0.1× |
| DeepSeek-V4-Pro | 复杂推理代码 | 0.5× |
| DeepSeek-V4-Flash | 速度快成本低 | 0.1× |
| GLM-5.2 | 系统工程 | 0.6× |
| Kimi-K2.7-Code | 长上下文编码 | 0.3× |
| MiniMax-M3 | 多模态 1M 上下文 | 0.2× |

## 自定义模型（Custom）

接入第三方供应商 API Key：阿里云百炼、DeepSeek、智谱、Kimi、MiniMax、小米 MIMO。

## 参数配置

| 参数 | 选项 | 调节方式 |
|------|------|---------|
| 上下文窗口 | 200K / 400K / 1M | `/context-window` 或 `--context-window` |
| 思考强度 | low / medium / high / xhigh / max | `/effort` 或 `--reasoning-effort` |
| Fast 模式 | on / off | `/fast` |

## 切换方式

- TUI：`/model` → Default / New Models / Custom 三个标签页
- 命令行：`--model efficient`、`--reasoning-effort high`
- 列出可用：`qodercli --list-models`

## 交叉引用

- [[cli-session]] — 模型在会话中的使用
- [[cli-quickstart]] — 首次使用时的模型选择
- [[cli-vs-cloud-agents]] — 与 Cloud Agents 模型选择的对比

## 来源

- raw/qodercli/model.md [official-docs]
