# Hooks（Qoder Desktop / JetBrains 插件）

> 来源: https://docs.qoder.com/zh/extensions/hooks
> 注意: 官方文档仅列出 5 种事件 + 1 种 Handler（command），但文档同时声明"IDE / JB 插件与 CLI 共享同一套配置文件"。
> 根据 CLI 实测（30 事件 + 5 Handler），Desktop 底层引擎极大概率支持完整能力集，文档滞后于实际实现。

## 概述

Hooks 让你可以在 Qoder IDE 和 JetBrains 插件执行的关键节点插入自定义逻辑，而无需修改任何代码。与 Prompt 指令不同，Hooks 是确定性的——只要事件触发，脚本就一定执行，不受模型理解偏差的影响。

**与 CLI 的关系**：IDE / JB 插件与 CLI 共享同一套配置文件（~/.qoder/settings.json）。

## 文档声称支持的事件（5 种）

| 事件名称 | 触发时机 | 可阻断 |
|---------|---------|-------|
| UserPromptSubmit | 用户提交 Prompt 后、Agent 处理前 | 是 |
| PreToolUse | 工具调用执行前 | 是 |
| PostToolUse | 工具调用成功后 | 否 |
| PostToolUseFailure | 工具调用失败后 | 否 |
| Stop | Agent 完成响应时 | 否（下版本支持） |

## Handler 类型

文档仅提及 `type: "command"`（Shell 脚本），未提及 http/mcp_tool/prompt/agent。

## 配置文件位置

| 位置 | 作用域 | 优先级 | 可共享 |
|------|-------|-------|-------|
| `~/.qoder/settings.json` | 用户级 | 1（最低） | 否 |
| `.qoder/settings.json` | 项目级 | 2 | 是（可 git 共享） |
| `.qoder/settings.local.json` | 项目级（本地） | 3 | 否（gitignore） |

注意：修改配置文件后需要**重启 IDE** 才能生效（暂不支持热加载）。

## 配置格式

```json
{
  "hooks": {
    "事件名": [
      {
        "matcher": "匹配条件",
        "hooks": [
          {
            "type": "command",
            "command": "要执行的命令"
          }
        ]
      }
    ]
  }
}
```

| 字段 | 必填 | 说明 |
|------|------|------|
| type | 是 | 固定为 "command" |
| command | 是 | shell 命令或脚本路径 |
| timeout | 否 | 默认 30 秒（当前版本不支持自定义） |
| matcher | 否 | 不填则匹配所有 |

## Matcher 规则

| 写法 | 含义 | 示例 |
|------|------|------|
| 不填或 "*" | 匹配所有 | — |
| 精确值 | 精确匹配 | "Bash" |
| `\|` 分隔 | 匹配多个值 | "Write \| Edit" |
| 正则表达式 | 正则匹配 | "mcp__.*" |

## 工具名双向映射表（Desktop 独有文档）

Qoder Desktop 支持两套工具名——原生名与 Claude Code 兼容名。matcher 中使用任意一套等价。

| Qoder 原生名 | 兼容名 | 说明 |
|-------------|-------|------|
| run_in_terminal | Bash | 执行 shell 命令 |
| read_file | Read | 读取文件内容 |
| create_file | Write | 创建/写入文件 |
| search_replace | Edit | 编辑文件 |
| delete_file | — | 删除文件 |
| grep_code | Grep | 搜索文件内容 |
| search_file | Glob | 文件名匹配 |
| list_dir | LS | 列出目录 |
| task | Task | 启动子任务/子代理 |
| Skill | — | 调用技能 |
| search_web | WebSearch | 网页搜索 |
| fetch_content | WebFetch | 获取网页内容 |
| todo_write | TodoWrite | 写入 TODO |
| ask_user_question | — | 向用户提问 |
| search_memory | — | 搜索记忆 |
| update_memory | — | 更新记忆 |
| switch_mode | — | 切换模式 |
| create_plan | — | 创建计划 |
| run_preview | — | 预览 Web 应用 |
| mcp__<server>__<tool> | 同左 | MCP 工具 |

## Hook 输入（stdin JSON）

通用字段：
```json
{
  "session_id": "...",
  "cwd": "/path/to/project",
  "hook_event_name": "事件名",
  "transcript_path": "会话上下文 JSON 文件路径"
}
```

### PreToolUse 额外字段
```json
{
  "tool_name": "Bash",
  "tool_input": { "command": "rm -rf /tmp/build" }
}
```

### PostToolUse 额外字段
```json
{
  "tool_name": "Write",
  "tool_input": { "file_path": "...", "content": "..." },
  "tool_response": "File written successfully"
}
```

### PostToolUseFailure 额外字段
```json
{
  "tool_name": "Bash",
  "tool_input": { "command": "npm test" },
  "error": "Command exited with non-zero status code 1"
}
```

### UserPromptSubmit 额外字段
```json
{
  "prompt": "帮我写一个排序函数"
}
```

### Stop 额外字段
```json
{
  "stop_hook_active": true,
  "last_assistant_message": "我已经完成了排序函数的编写。"
}
```

## 退出码含义

| Exit Code | 含义 | 行为 |
|-----------|------|------|
| 0 | 成功 | 继续执行，尝试解析 stdout JSON |
| 2 | 阻断 | 停止操作，stderr 注入对话（仅可阻断事件生效） |
| 其他 | 错误 | 非阻断错误，stderr 显示给用户，继续执行 |

## stdout JSON 输出（exit 0 时）

### PreToolUse 可输出字段

| 字段 | 说明 |
|------|------|
| permissionDecision | "allow" / "deny" / "ask" |
| permissionDecisionReason | 决策原因 |
| updatedInput | 修改后的工具输入参数 |
| additionalContext | 附加上下文 |

### UserPromptSubmit 可输出字段

| 字段 | 说明 |
|------|------|
| additionalContext | 注入到 Agent 对话中的附加上下文 |

### PostToolUse 可输出字段

| 字段 | 说明 |
|------|------|
| feedback | 反馈信息（如 lint 结果摘要） |

### Stop 可输出字段（下版本生效）

| 字段 | 说明 |
|------|------|
| decision | "block"（让 Agent 继续工作） |
| reason | 阻止原因 |

## 注意事项

- 超时默认 30 秒，超时后脚本被终止，按放行处理
- 多级配置中同一事件 Hook 按优先级从低到高依次执行，任一返回阻断则终止后续
- 脚本需要可执行权限（chmod +x）
- 示例脚本依赖 jq 解析 JSON
