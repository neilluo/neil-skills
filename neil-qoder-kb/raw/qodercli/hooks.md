# 钩子

> 来源: https://docs.qoder.com/zh/cli/hooks
> 验证: qodercli 1.0.16 本地实测 [2026-06-28]
> 注意: 官网文档仅列出 4 种事件，实测支持全部 30 种（与 Claude Code 完全同构）

## 概述

Hooks 在 Qoder CLI 关键节点介入 Agent 主执行流。通过 JSON 配置在 Agent 执行生命周期的 30 个事件点注入自定义逻辑。支持 5 种 Handler 类型。适合拦截危险操作、发送通知、自动 lint、组织级安全策略、LLM 判断等场景。

## 配置

### 配置文件位置（三个来源合并执行）

```
~/.qoder/settings.json                    # 用户级
${project}/.qoder/settings.json           # 项目级（可提交 git）
${project}/.qoder/settings.local.json     # 项目级本地
```

也可通过 CLI 参数加载：
```bash
qodercli --settings '{"hooks":{...}}' -p "task"
qodercli --settings /path/to/settings.json -p "task"
```

### 配置格式

```json
{
  "hooks": {
    "事件名": [
      {
        "matcher": "匹配条件",
        "hooks": [
          {
            "type": "command",
            "command": "要执行的命令",
            "timeout": 600
          }
        ]
      }
    ]
  }
}
```

## 事件类型（30 种）

### 会话级（1次/session）

| 事件 | 触发时机 | Matcher 过滤 |
|------|---------|-------------|
| SessionStart | 会话开始或恢复 | startup, resume, clear, compact |
| Setup | 使用 --init-only 或 --maintenance 启动时 | init, maintenance |
| SessionEnd | 会话终止 | clear, resume, logout, prompt_input_exit, other |

### 轮次级（1次/turn）

| 事件 | 触发时机 | Matcher 过滤 |
|------|---------|-------------|
| UserPromptSubmit | 用户提交 prompt 后、模型处理前 | 无（始终触发） |
| UserPromptExpansion | 用户输入的命令展开为 prompt 时 | 命令名 |
| Stop | Agent 完成响应 | 无（始终触发） |
| StopFailure | 轮次因 API 错误终止 | rate_limit, overloaded, authentication_failed, ... |
| TeammateIdle | Agent Team 中某成员即将空闲 | 无（始终触发） |

### 工具级（每次工具调用）

| 事件 | 触发时机 | Matcher 过滤 |
|------|---------|-------------|
| PreToolUse | 工具调用前 | 工具名（如 Bash, Edit, Write, mcp__*） |
| PostToolUse | 工具调用成功后 | 工具名 |
| PostToolUseFailure | 工具调用失败后 | 工具名 |
| PostToolBatch | 一批并行工具调用全部完成后 | 无（始终触发） |
| PermissionRequest | 权限对话框出现时 | 工具名 |
| PermissionDenied | auto 模式分类器拒绝工具调用时 | 工具名 |

### 子代理级

| 事件 | 触发时机 | Matcher 过滤 |
|------|---------|-------------|
| SubagentStart | 子代理启动 | agent 类型名 |
| SubagentStop | 子代理完成 | agent 类型名 |
| TaskCreated | 通过 TaskCreate 创建任务 | 无（始终触发） |
| TaskCompleted | 任务标记完成 | 无（始终触发） |

### 上下文管理

| 事件 | 触发时机 | Matcher 过滤 |
|------|---------|-------------|
| PreCompact | 上下文压缩前 | manual, auto |
| PostCompact | 上下文压缩后 | manual, auto |
| InstructionsLoaded | AGENTS.md 或 rules 文件加载时 | session_start, nested_traversal, path_glob_match, include, compact |

### 文件/环境监听

| 事件 | 触发时机 | Matcher 过滤 |
|------|---------|-------------|
| FileChanged | 被监听文件发生磁盘变化 | 文件名列表（用 \| 分隔） |
| CwdChanged | 工作目录变化 | 无（始终触发） |
| ConfigChange | 配置文件变化 | user_settings, project_settings, local_settings, policy_settings, skills |

### 工作树

| 事件 | 触发时机 | Matcher 过滤 |
|------|---------|-------------|
| WorktreeCreate | 通过 --worktree 创建工作树 | 无（始终触发） |
| WorktreeRemove | 工作树被移除（会话结束或子代理完成） | 无（始终触发） |

### MCP 交互

| 事件 | 触发时机 | Matcher 过滤 |
|------|---------|-------------|
| Elicitation | MCP 服务器请求用户输入 | MCP 服务器名 |
| ElicitationResult | 用户响应 MCP elicitation 后 | MCP 服务器名 |

### 展示/通知

| 事件 | 触发时机 | Matcher 过滤 |
|------|---------|-------------|
| Notification | 通知发送时 | permission_prompt, idle_prompt, auth_success, ... |
| MessageDisplay | 助手消息文本流式显示时 | 无（始终触发） |

## Handler 类型（5 种）

| 类型 | 说明 | 通信方式 |
|------|------|----------|
| command | Shell 命令 | stdin 接收 JSON，stdout 返回决策 |
| http | HTTP POST 请求 | 请求体 JSON，响应体返回决策 |
| mcp_tool | 调用已连接 MCP 服务器的工具 | 工具文本输出等同 stdout |
| prompt | 发送 prompt 给 LLM 单轮评估 | 模型返回 yes/no 决策 JSON |
| agent | 启动子代理验证条件 | 子代理可用 Read/Grep/Glob 工具 |

## Handler 通用字段

| 字段 | 必填 | 说明 |
|------|------|------|
| type | 是 | command / http / mcp_tool / prompt / agent |
| if | 否 | 权限规则语法过滤，如 "Bash(rm *)"、"Edit(*.ts)" |
| timeout | 否 | 超时秒数（command/http/mcp_tool 默认 600，prompt 默认 30，agent 默认 60） |
| statusMessage | 否 | 自定义 spinner 消息 |
| once | 否 | true 时仅执行一次后移除（仅 skill frontmatter 有效） |

## Command Handler 特有字段

| 字段 | 说明 |
|------|------|
| command | Shell 命令或可执行文件路径 |
| args | 参数列表（设置后使用 exec form，跳过 shell） |
| async | true 时后台执行不阻塞 |
| asyncRewake | true 时后台执行，退出码 2 唤醒 Claude |
| shell | bash（默认）或 powershell |

## HTTP Handler 特有字段

| 字段 | 说明 |
|------|------|
| url | POST 请求目标 URL |
| headers | 额外 HTTP 头（支持 $VAR 环境变量插值） |
| allowedEnvVars | 允许插值的环境变量名列表 |

## Matcher 规则

| 模式 | 行为 |
|------|------|
| 空/"*"/省略 | 匹配所有 |
| 纯字母数字 | 精确匹配（如 "Bash"） |
| 含 \| 或 , | 多值列表（如 "Edit\|Write" 或 "Edit, Write"） |
| 含特殊字符 | JavaScript 正则（如 "mcp__memory__.*"） |

## Hook 输入（stdin JSON）

PreToolUse 接收：
```json
{
  "session_id": "...",
  "transcript_path": "...",
  "cwd": "...",
  "hook_event_name": "PreToolUse",
  "permission_mode": "bypassPermissions",
  "tool_use_id": "...",
  "tool_name": "Bash",
  "tool_input": { "command": "rm -rf /tmp" }
}
```

PostToolUse 接收：
```json
{
  "session_id": "...",
  "hook_event_name": "PostToolUse",
  "tool_name": "Read",
  "tool_input": { "file_path": "..." },
  "tool_response": { "type": "text", "file": { "filePath": "...", "content": "..." } }
}
```

Stop 接收：
```json
{
  "session_id": "...",
  "hook_event_name": "Stop",
  "stop_hook_active": false,
  "last_assistant_message": "...",
  "parent_business_info": { "product": "cli", "version": "1.0.16", ... }
}
```

## 退出码含义（command handler）

| 退出码 | PreToolUse | PostToolUse | 其他事件 |
|--------|-----------|-------------|----------|
| 0 | 放行（无决策） | 继续 | 继续 |
| 1 | 需用户确认 | — | — |
| 2 | 阻止执行 | — | 唤醒 Claude（asyncRewake） |

## JSON 输出决策格式

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive command blocked"
  }
}
```

## CLI 命令

```bash
qodercli hooks migrate --from-claude  # 从 Claude Code 迁移 hooks 配置
```
