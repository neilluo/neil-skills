# Worker Hook 生命周期

> QoderWake 数字员工的 8 阶段 Hook 注入链，是安全防护、记忆管理、上下文准备的核心执行机制，通过拦截 QoderCLI 的工具调用和会话事件实现行为控制。

## 概述

QoderWake 为每个数字员工（Waker）自动生成 `.qoder-plugin/hooks/hooks.json` 配置，将 Daemon 级能力（权限守卫、记忆、变更追踪）注入到底层 QoderCLI 的执行流程中。这是 QoderWake 控制 AI 行为的关键「缝合点」。

Hook 通过 CLI 内部子命令 `qoderwake __plugin_hook <hook_name> <event>` 执行。

## 完整 Hook 链

| 执行顺序 | 阶段 | Hook 名称 | 功能 | 超时 |
|----------|------|-----------|------|------|
| 1 | SessionStart | `qoderwake_context_prepare` | 准备工作上下文（项目信息、身份卡注入） | 5s |
| 2 | SessionStart | `qoderwake_memory` | 加载相关记忆到 Agent context | 5s |
| 3 | PreToolUse (*) | `qoderwake_permission_guard` | 安全规则检查（28条规则） | 305s |
| 4 | PreToolUse (*) | `qoderwake_change_tracker` | 记录即将发生的变更 | 5s |
| 5 | PreToolUse (ask_user) | `ask-user-question` | 拦截用户提问并路由 | 2s |
| 6 | PostToolUse (*) | `qoderwake_change_tracker` | 记录已完成的变更 | 5s |
| 7 | UserPromptSubmit (*) | `qoderwake_remote_input_files` | 远程文件注入（大文件传输） | 120000s |
| 8 | PostCompact | `qoderwake_memory` (async) | 压缩后记忆整理与沉淀 | 2s |

## 各 Hook 详解

### 1. qoderwake_context_prepare（SessionStart）

在会话启动时注入：
- 数字员工身份卡（IDENTITY.md / PERSONA.md / BIBLE.md）
- 项目信息和工作目录配置
- Output Style 行为规范

### 2. qoderwake_memory（SessionStart + PostCompact）

双阶段记忆管理：
- **SessionStart**：从 `agent.sqlite` 检索相关记忆注入 context
- **PostCompact**（异步）：当 context 压缩时，将重要信息沉淀为长期记忆

### 3. qoderwake_permission_guard（PreToolUse）

核心安全门禁，超时 **305 秒**（含用户确认等待时间）：
- 加载 [[waker-tool-guard]] 规则库
- 匹配工具调用参数
- 决策：放行 / 阻断 / 等待用户确认

### 4. qoderwake_change_tracker（PreToolUse + PostToolUse）

变更追踪双向记录：
- **Pre**：记录「准备做什么」
- **Post**：记录「实际做了什么」
- 用于审计、回滚、变更报告

### 5. ask-user-question（PreToolUse: ask_user）

仅匹配 `ask_user` 工具：
- 拦截 Agent 的用户提问请求
- 通过 Channel（钉钉/飞书）路由到正确的用户
- 等待用户回复后返回给 Agent

### 6. qoderwake_remote_input_files（UserPromptSubmit）

超长超时（120000s ≈ 33小时）：
- 处理用户通过 IM 发送的大文件
- 下载并注入到 Agent workspace
- 支持断点续传

## 执行机制

```bash
# Hook 实际执行方式
qoderwake __plugin_hook qoderwake_permission_guard pre-tool-use
qoderwake __plugin_hook qoderwake_context_prepare session-start
qoderwake __plugin_hook qoderwake_memory session-start
qoderwake __plugin_hook qoderwake_memory post-compact
qoderwake __pre_tool_use_hook ask-user-question
```

## 设计要点

1. **超时差异化**：安全检查 305s（含人工确认）、记忆加载 5s（快速）、文件传输 33h（极长）
2. **通配符匹配**：`(*)` 表示匹配所有工具调用，`(ask_user)` 表示仅匹配特定工具
3. **异步标记**：PostCompact 的 memory hook 标记为 async，不阻塞主流程
4. **顺序保证**：同阶段多 Hook 按配置顺序串行执行（permission_guard 先于 change_tracker）

## 交叉引用

- [[waker-tool-guard]] — permission_guard 使用的 28 条安全规则详情
- [[waker-permission]] — Waker 整体权限模型
- [[waker-memory]] — 记忆系统的上层设计
- [[cli-hook-system]] — QoderCLI 底层 Hook 引擎（30 事件 + 5 Handler）
- [[desktop-hook-system]] — Desktop IDE 的 Hook 系统（与 CLI 共享引擎）

## 来源

- ~/.qoderwake/data/workers/<agent-id>/.qoder-plugin/hooks/hooks.json [reverse-engineering] 2026-06-30
- QoderCLI 1.0.16 Hook 引擎实测验证 [verified-by-api] 2026-06-28
