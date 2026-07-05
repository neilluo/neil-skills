# CLI Hook System — 钩子系统

> Agent 执行生命周期 30 个事件点的可编程拦截机制，支持 5 种 Handler 类型。与 Claude Code 完全同构。

## 概述

Hooks 通过 JSON 配置在 Qoder CLI 生命周期的 30 个事件点注入自定义逻辑。支持 Shell 命令、HTTP 回调、MCP 工具、LLM Prompt 判断、Agent 子代理验证 5 种 Handler。实测确认与 Claude Code 完全同构（qodercli 1.0.16）。

## 核心概念

```
事件(Event) × 匹配器(Matcher) × 处理器(Handler) = Hook
```

## 事件类型（30 种，按触发频率分层）

### 会话级（1次/session）

| 事件 | 触发时机 |
|------|----------|
| SessionStart | 会话开始或恢复 |
| Setup | --init-only 或 --maintenance 启动 |
| SessionEnd | 会话终止 |

### 轮次级（1次/turn）

| 事件 | 触发时机 |
|------|----------|
| UserPromptSubmit | 用户提交 prompt 后 |
| UserPromptExpansion | 命令展开为 prompt 时 |
| Stop | Agent 完成响应 |
| StopFailure | 轮次因 API 错误终止 |
| TeammateIdle | Agent Team 成员即将空闲 |

### 工具级（每次工具调用）

| 事件 | 触发时机 | 决策控制 |
|------|----------|----------|
| PreToolUse | 工具调用前 | 可阻止 |
| PostToolUse | 工具调用成功后 | — |
| PostToolUseFailure | 工具调用失败后 | — |
| PostToolBatch | 并行工具调用全部完成后 | — |
| PermissionRequest | 权限对话框出现 | 可处理 |
| PermissionDenied | auto 模式拒绝工具调用 | 可 retry |

### 子代理/任务级

| 事件 | 触发时机 |
|------|----------|
| SubagentStart | 子代理启动 |
| SubagentStop | 子代理完成 |
| TaskCreated | 任务创建 |
| TaskCompleted | 任务完成 |

### 上下文/配置级

| 事件 | 触发时机 |
|------|----------|
| PreCompact | 上下文压缩前 |
| PostCompact | 上下文压缩后 |
| InstructionsLoaded | AGENTS.md/rules 加载时 |
| ConfigChange | 配置文件变化 |

### 文件/环境/工作树

| 事件 | 触发时机 |
|------|----------|
| FileChanged | 被监听文件磁盘变化 |
| CwdChanged | 工作目录变化 |
| WorktreeCreate | 工作树创建 |
| WorktreeRemove | 工作树移除 |

### MCP/展示/通知

| 事件 | 触发时机 |
|------|----------|
| Elicitation | MCP 服务器请求用户输入 |
| ElicitationResult | 用户响应 MCP elicitation |
| Notification | 通知发送时 |
| MessageDisplay | 助手消息流式显示时 |

## Handler 类型（5 种）

| 类型 | 说明 | 通信方式 |
|------|------|----------|
| `command` | Shell 命令 | stdin JSON → stdout JSON + 退出码 |
| `http` | HTTP POST | 请求体 JSON → 响应体 JSON |
| `mcp_tool` | MCP 服务器工具 | 工具文本输出等同 stdout |
| `prompt` | LLM 单轮判断 | 返回 yes/no 决策 |
| `agent` | 子代理验证 | 可用 Read/Grep/Glob 后返回决策 |

## 配置

### 三级来源（合并执行，不互相覆盖）

```
~/.qoder/settings.json                    # 用户级
${project}/.qoder/settings.json           # 项目级（可 git 共享）
${project}/.qoder/settings.local.json     # 本地
```

### 配置示例（多 Handler 类型）

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "~/.qoder/hooks/block-rm.sh", "if": "Bash(rm *)", "timeout": 600 },
          { "type": "prompt", "prompt": "Is this Bash command safe?", "timeout": 30 },
          { "type": "http", "url": "http://localhost:8080/validate", "timeout": 10 }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "eslint --fix", "async": true }
        ]
      }
    ]
  }
}
```

## Matcher 规则

| 模式 | 行为 | 示例 |
|------|------|------|
| 空/"*"/省略 | 匹配所有 | — |
| 纯字母数字 | 精确匹配 | "Bash" |
| 含 `\|` 或 `,` | 多值列表 | "Edit\|Write" 或 "Edit, Write" |
| 含特殊字符 | JavaScript 正则 | "mcp__memory__.*" |

## Handler 高级字段

| 字段 | 说明 |
|------|------|
| `if` | 权限规则语法过滤，如 `"Bash(rm *)"` / `"Edit(*.ts)"` |
| `async` | true 时后台执行不阻塞 |
| `asyncRewake` | true 时后台执行，完成后唤醒 Claude |
| `once` | true 时仅执行一次后移除（skill frontmatter 专用） |
| `statusMessage` | 自定义 spinner 消息 |
| `args` | Exec form 参数列表（跳过 shell 解析） |

## Hook 输入（stdin JSON 实测示例）

PreToolUse:
```json
{
  "session_id": "...", "transcript_path": "...", "cwd": "...",
  "hook_event_name": "PreToolUse", "permission_mode": "bypassPermissions",
  "tool_use_id": "...", "tool_name": "Bash",
  "tool_input": { "command": "rm -rf /tmp" }
}
```

Stop:
```json
{
  "session_id": "...", "hook_event_name": "Stop",
  "stop_hook_active": false, "last_assistant_message": "...",
  "parent_business_info": { "product": "cli", "version": "1.0.16", ... }
}
```

## 退出码含义（command handler）

| 退出码 | PreToolUse | 其他事件 |
|--------|-----------|----------|
| 0 | 放行（无决策） | 继续 |
| 1 | 需用户确认 | — |
| 2 | 阻止执行 | 唤醒 Claude（asyncRewake） |

## 典型用例

| 场景 | 事件 | Handler | 实现 |
|------|------|---------|------|
| 拦截 rm -rf | PreToolUse | command | if: "Bash(rm *)" → 退出码 2 |
| 写文件后 lint | PostToolUse | command+async | eslint --fix 后台执行 |
| 安全审计 | PreToolUse | http | POST 到安全服务判断 |
| AI 安全判断 | PreToolUse | prompt | LLM 单轮评估是否安全 |
| 复杂验证 | PreToolUse | agent | 子代理用工具检查后返回决策 |
| 任务完成通知 | Stop | command | 发送桌面通知 |
| 子代理监控 | SubagentStart | command | 记录子代理启动日志 |
| 文件监听 | FileChanged | command | .env 变化时重载环境 |

## CLI 命令

```bash
qodercli hooks migrate --from-claude  # 从 Claude Code 迁移 hooks 配置
```

## 交叉引用

- [[cli-permission-model]] — Hooks 在权限之外提供额外拦截层
- [[cli-plugin]] — 插件可通过 hooks/hooks.json 提供 Hook
- [[cli-subagent]] — 每个 Subagent 可配置独立 Hooks
- [[cli-tool-mcp]] — MCP 工具调用同样触发 Hooks
- [[cli-skill]] — Skill frontmatter 可内联定义 Hooks

## 来源

- raw/qodercli/hooks.md [official-docs]
- qodercli 1.0.16 本地实测 [verified-by-api] (2026-06-28)
- Claude Code docs: https://code.claude.com/docs/en/hooks [cross-reference]
