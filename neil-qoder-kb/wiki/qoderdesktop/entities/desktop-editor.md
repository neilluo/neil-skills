# Editor（编辑器）

> Qoder IDE 的核心 AI 编码工作区，集成 NEXT 代码建议、行间会话与智能会话面板（Ask / Agent 模式）。

## 概述

Editor 是 Qoder Desktop 的主编码视图，将 AI 能力无缝嵌入代码编辑器。开发者无需离开编码现场即可获得实时代码预测、问答与自主编码协作。

## 三大交互入口

| 入口 | 快捷键 | 作用 |
|------|--------|------|
| **NEXT 代码建议** | ⌥P / Alt+P 唤出，Tab 采纳 | 基于光标位置和上下文自动预测下一段代码 |
| **行间会话** | ⌘I / Ctrl+I | 在代码上下文中直接与 AI 对话，生成代码后 ⌘⏎ 应用 |
| **智能会话面板** | ⌘L / Ctrl+L | 右侧面板，选择 Ask 或 Agent 模式处理复杂任务 |

## Ask vs Agent 模式

| 维度 | Ask（智能问答） | Agent（智能体） |
|------|----------------|-----------------|
| 定位 | 问答，不修改代码 | 自主编码，端到端完成任务 |
| 能力 | 基于上下文回答问题、提供建议 | 文件编辑、终端命令、项目搜索、MCP 工具 |
| 适用 | 快速问答、解释代码 | 多文件修改、实现功能、调试修复 |

## 会话独立窗口

支持将进行中的对话拆分到单独窗口运行，适用于多任务并行监控和分屏对照。

## 行为推荐卡片

Agent 完成任务后自动推荐下一步：
- **Review Code Changes** — 审查代码变更
- **Run Feature Test** — 检测到前端文件变更时触发浏览器验证
- **AI Suggestion** — 根据上下文自主生成

## 交叉引用
- [[desktop-quest]] — Quest 独立视窗，面向自主委派
- [[desktop-knowledge-engine]] — 知识引擎，Agent 的记忆来源
- [[desktop-rules]] — 规则系统，引导 Agent 行为
- [[desktop-agent-mode]] — Agent 模式详细机制

## 来源
- raw/qoderdesktop/overview.md [official-docs]
- raw/qoderdesktop/editor.md [official-docs]
