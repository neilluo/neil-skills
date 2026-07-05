# 子代理

> 来源: https://docs.qoder.com/zh/cli/subagent

## 定义

子代理（Subagent）是专门处理某类任务的 Agent，拥有独立的系统提示词、工具集合、模型配置、权限模式、运行限制和 Hook。

## 核心价值

| 价值 | 说明 |
|------|------|
| 保持主会话聚焦 | 独立对话上下文，中间过程不混入主会话 |
| 提升专业任务质量 | 专用提示词、工具白名单、模型配置 |
| 复用团队工作流 | 用户级和项目级可反复使用、随项目共享 |
| 控制工具和权限边界 | 每个 Subagent 独立权限模式 |
| 支持复杂任务编排 | 可并发执行、后台运行 |

## 内置 Subagent

| 名称 | 能力 |
|------|------|
| general-purpose | 通用研究型，复杂搜索、多文件分析 |
| Explore | 只读代码探索，查找文件、搜索符号 |
| Plan | 只读方案设计，梳理实现路径 |
| qoder-guide | 回答 Qoder CLI 使用问题 |
| SaveMemory | 管理跨会话记忆 |

## 来源和优先级（从低到高）

| 优先级 | 来源 | 入口 |
|--------|------|------|
| 最低 | 内置 | Qoder CLI 提供 |
| ↑ | Plugin | 插件目录 agents/ |
| ↑ | 用户级 | ~/.qoder/agents/ |
| 最高 | 项目级 | .qoder/agents/ |

## 配置格式

```markdown
---
name: api-reviewer
description: API 设计审查专家
model: performance
permission_mode: default
tools:
  allowed: [Read, Grep, Glob, WebFetch]
  disallowed: [Write, Bash]
max_turns: 30
---

# System Prompt
你是一个 API 设计审查专家...
```

## 使用方式

- TUI：`/agents` 查看/创建/管理
- Headless：`qodercli agents list`
- 自然语言调用："使用 api-reviewer subagent 审查这个 API 设计"
- 并发执行：Qoder CLI 可一次调度多个 Subagent 并行工作
