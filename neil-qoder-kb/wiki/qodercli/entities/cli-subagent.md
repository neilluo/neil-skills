# CLI Subagent — 子代理系统

> 专门处理某类任务的独立 Agent，拥有隔离上下文和定制化能力配置。

## 概述

Subagent 是 Qoder CLI 中处理子任务的独立 Agent 实例。它有自己的系统提示词、工具集合、模型配置、权限模式和运行限制。适合开放式、多步骤、需要判断和汇总的任务。

## 核心价值

| 价值 | 说明 |
|------|------|
| 上下文隔离 | 独立对话上下文，中间搜索/思考不污染主会话 |
| 能力定制 | 专用提示词 + 工具白名单 + 独立模型 + 权限 |
| 并发执行 | 独立任务可同时调度多个 Subagent |
| 后台运行 | 可放到后台执行，完成后通知主会话 |
| 隔离工作区 | 支持在独立 git worktree 中运行 |

## 内置 Subagent

| 名称 | 能力 | 典型场景 |
|------|------|---------|
| general-purpose | 通用研究型 | 复杂搜索、多文件分析、调用链追踪 |
| Explore | 只读代码探索 | 查找文件、搜索符号、理解实现 |
| Plan | 只读方案设计 | 梳理路径、依赖、架构取舍 |
| qoder-guide | CLI 使用指导 | 回答配置/使用问题 |
| SaveMemory | 记忆管理 | 保存/检索跨会话记忆 |

## 来源优先级（从低到高）

1. **内置** — Qoder CLI 提供
2. **Plugin** — 插件 `agents/` 目录
3. **用户级** — `~/.qoder/agents/`
4. **项目级** — `.qoder/agents/`（最高优先）

## 配置格式（Markdown frontmatter + 系统提示词）

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

你是一个 API 设计审查专家...
```

## 使用方式

- 自然语言："使用 api-reviewer subagent 审查这个 API 设计"
- TUI 管理：`/agents` 查看/创建/编辑/启用/禁用
- Headless：`qodercli agents list`
- 重新加载：`/agents reload`

## 交叉引用

- [[cli-skill]] — Skill 提供知识，Subagent 执行任务
- [[cli-workflow-engine]] — 动态工作流使用 Subagent 作为执行单元
- [[cli-plugin]] — 插件可包含 Subagent
- [[cli-permission-model]] — 每个 Subagent 可独立设置权限
- [[managed-agents-threading]] — Cloud Agents 中的多 Agent 对比

## 来源

- raw/qodercli/subagent.md [official-docs]
