# CLI Tool & MCP — 工具与 MCP 集成

> CLI 通过内置工具处理本地工作区，通过 MCP 协议接入外部服务，统一经过权限系统。

## 概述

Qoder CLI 的工具体系分两层：内置工具（搜索、读取、编辑、执行、管理上下文）和 MCP 工具（通过 Model Context Protocol 接入外部服务）。两者共享相同的权限和 Hooks 机制。

## 内置工具分类

| 类别 | 能力 |
|------|------|
| 搜索与探索 | 文件搜索、代码搜索、目录浏览、Web 搜索、网页内容获取 |
| 读取上下文 | 查看文件、读取大文件片段、PDF 等文档 |
| 编辑文件 | 修改/创建文件、编辑 Notebook |
| 执行命令 | Shell 命令、长任务跟踪 |
| 管理上下文 | 任务列表、提问、记忆、Skills、Plan Mode |
| 分派自动化 | Subagents、Workflows、Goals、Worktrees、定时任务 |

## MCP 集成

### 传输类型

| 类型 | 适用场景 |
|------|---------|
| stdio | 本地命令进程（默认） |
| sse | Server-Sent Events 端点 |
| http | HTTP 端点 |
| ws | WebSocket 端点 |

### 作用域与配置位置

| 作用域 | 配置文件 | 场景 |
|--------|---------|------|
| user | `~/.qoder/settings.json` | 所有项目可用 |
| local | `${project}/.qoder/settings.local.json` | 本机本项目（默认） |
| project | `${project}/.mcp.json` | 随项目共享 |

### 管理命令

```shell
qodercli mcp add <name> -- <command>    # 添加
qodercli mcp add <name> -t sse <url>    # 添加 SSE
qodercli mcp list                        # 列出
qodercli mcp remove <name>              # 移除
/mcp reload                              # TUI 中重新发现
```

### 权限控制

MCP 工具名格式：`mcp__<server>__<tool>`

```json
{ "permissions": { "allow": ["mcp__context7__*"] } }
```

## 工具控制参数

| 参数 | 说明 |
|------|------|
| `--tools` | 限制可见工具 |
| `--allowed-tools` | 预先允许 |
| `--disallowed-tools` | 禁止 |
| `tools.exclude` | settings 中排除 |

## 交叉引用

- [[cli-permission-model]] — 工具调用的权限判定
- [[cli-hook-system]] — PreToolUse/PostToolUse 拦截
- [[cli-plugin]] — 插件可通过 .mcp.json 声明 MCP server
- [[cli-session]] — 会话中可用工具集合
- [[cli-workflow-engine]] — 工作流子 Agent 继承工具配置

## 来源

- raw/qodercli/tools.md [official-docs]
- raw/qodercli/mcp-servers.md [official-docs]
