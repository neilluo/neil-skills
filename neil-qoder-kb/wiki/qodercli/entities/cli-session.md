# CLI Session — 会话与运行模式

> Qoder CLI 的核心运行单元，支持 TUI 交互式、Print 非交互式和 ACP 协议三种模式。

## 概述

CLI Session 是用户与 Qoder Agent 的一次对话生命周期。每次启动 `qodercli` 即创建一个会话，会话内维护完整的对话上下文、工具状态、权限模式和记忆加载结果。

## 三种运行模式

| 模式 | 启动方式 | 特点 | 典型场景 |
|------|---------|------|---------|
| TUI | `qodercli` | 交互式终端界面，支持斜杠命令、多模态输入 | 日常开发、探索、调试 |
| Print | `qodercli -p "prompt"` | 非交互式，按格式输出结果后退出 | CI/CD、脚本自动化 |
| ACP | `qodercli --acp` | Agent Client Protocol 服务端 | IDE 集成（如 Zed） |

## TUI 输入模式

| 前缀 | 模式 | 说明 |
|------|------|------|
| `>` | 对话 | 默认模式，自然语言对话 |
| `!` | Bash | 直接执行 shell 命令 |
| `/` | 斜杠 | 触发内置或自定义命令 |
| `\⏎` | 多行 | 长文本输入 |

## 会话管理

| 操作 | 方式 |
|------|------|
| 继续上次 | `qodercli -c` |
| 恢复指定 | `qodercli -r <session-id>` |
| 查看历史 | `/resume`（TUI 中按 Tab 分页） |
| 导出会话 | `/export [filename]` |
| 清除上下文 | `/clear` |
| 压缩上下文 | `/compact` |

## Worktree 隔离

`--worktree [name]` 在独立 Git worktree 中启动会话，实现同仓库并行处理多任务，避免工作目录冲突。

## 启动参数

| 参数 | 说明 |
|------|------|
| `-w <path>` | 指定工作区目录 |
| `--max-turns` | 限制最大对话轮数 |
| `--allowed-tools` | 仅允许指定工具 |
| `--disallowed-tools` | 禁止指定工具 |
| `--permission-mode` | 指定权限模式 |
| `--model` | 指定模型 |
| `--output-format` | Print 模式输出格式（text/json/stream-json） |

## 交叉引用

- [[cli-model]] — 会话中的模型选择与切换
- [[cli-permission-model]] — 会话的权限模式控制
- [[cli-memory-system]] — 会话启动时的记忆加载
- [[cli-command-system]] — TUI 模式的斜杠命令体系
- [[cli-tool-mcp]] — 会话中可用的工具集合

## 来源

- raw/qodercli/using-cli.md [official-docs]
- raw/qodercli/quick-start.md [official-docs]
- raw/qodercli/acp.md [official-docs]
