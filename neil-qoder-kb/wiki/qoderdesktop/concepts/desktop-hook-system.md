# Desktop Hook System — 桌面端钩子系统

> IDE / JetBrains 插件的 Agent 执行拦截机制。文档声称 5 事件 + 1 Handler，但与 CLI 共用引擎，实际能力极大概率完整。

## 概述

Hooks 在 Qoder Desktop（IDE 和 JetBrains 插件）的 Agent 生命周期关键节点注入自定义逻辑。确定性执行，不受模型理解偏差影响。

**关键事实**：IDE / JB 插件与 CLI **共享同一套配置文件**（`~/.qoder/settings.json`），底层引擎一致。

## 文档声称 vs 实际能力

| 维度 | 文档声称 | CLI 实测（共用引擎） |
|------|---------|------------------|
| 事件数 | **5 种** | 30 种 |
| Handler 类型 | **仅 command** | 5 种（command/http/mcp_tool/prompt/agent） |
| 超时自定义 | 不支持（默认 30s） | 支持（默认 600s） |
| 高级字段 | 无 | if/async/asyncRewake/once/args |
| 热加载 | 不支持（需重启 IDE） | 待验证 |

## 文档列出的 5 种事件

| 事件 | 触发时机 | 可阻断 | matcher 匹配 |
|------|---------|-------|------------|
| UserPromptSubmit | 用户提交 Prompt 后 | 是（exit 2） | 无（统一触发） |
| PreToolUse | 工具调用执行前 | 是（exit 2） | 工具名 |
| PostToolUse | 工具调用成功后 | 否 | 工具名 |
| PostToolUseFailure | 工具调用失败后 | 否 | 工具名 |
| Stop | Agent 完成响应时 | 否（下版本） | 无（统一触发） |

## 工具名双向映射（Desktop 独有知识）

Desktop 支持两套工具名——原生名与 Claude Code 兼容名，matcher 中等价使用：

| Qoder 原生名 | 兼容名 | 说明 |
|-------------|-------|------|
| `run_in_terminal` | `Bash` | 执行 shell 命令 |
| `read_file` | `Read` | 读取文件 |
| `create_file` | `Write` | 创建/写入文件 |
| `search_replace` | `Edit` | 编辑文件 |
| `grep_code` | `Grep` | 搜索文件内容 |
| `search_file` | `Glob` | 文件名匹配 |
| `list_dir` | `LS` | 列出目录 |
| `task` | `Task` | 启动子代理 |
| `search_web` | `WebSearch` | 网页搜索 |
| `fetch_content` | `WebFetch` | 获取网页内容 |
| `todo_write` | `TodoWrite` | 写入 TODO |
| `mcp__<server>__<tool>` | 同左 | MCP 工具 |

## 退出码协议

| Exit Code | 含义 | 行为 |
|-----------|------|------|
| 0 | 成功 | 继续，解析 stdout JSON |
| 2 | 阻断 | 停止操作，stderr 注入对话 |
| 其他 | 错误 | stderr 显示给用户，继续执行 |

## stdout JSON 输出能力

### PreToolUse（exit 0 时）

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "...",
    "updatedInput": { "command": "..." },
    "additionalContext": "..."
  }
}
```

### UserPromptSubmit（exit 0 时）

```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "注入到对话的附加上下文"
  }
}
```

### PostToolUse（exit 0 时）

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "feedback": "lint 结果摘要"
  }
}
```

## Desktop 特有注意事项

- **不支持热加载**：修改 settings.json 后必须重启 IDE
- **超时固定 30 秒**：文档声称不支持自定义（"下个版本开放"）
- **jq 依赖**：示例脚本需要 jq（`brew install jq`）

## 交叉引用

- [[cli-hook-system]] — CLI 版钩子系统（30 事件 + 5 Handler，已实测验证）
- [[desktop-rules]] — 规则系统（与 Hooks 互补：规则影响 prompt，Hooks 拦截执行）
- [[desktop-agent-mode]] — Agent 模式（Hooks 在 Agent 模式下触发）

## 来源

- raw/qoderdesktop/hooks.md [official-docs]
- https://docs.qoder.com/zh/extensions/hooks [official-docs] (2026-06-28)
- CLI 实测交叉引用 [verified-by-api] (2026-06-28)
