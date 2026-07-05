# 使用 CLI

> 来源: https://docs.qoder.com/zh/cli/using-cli

## TUI 模式

在任意项目根目录运行 `qodercli` 进入默认的 TUI 交互式模式。

### 输入模式

| 命令 | 描述 |
|------|------|
| `>` | 对话模式（默认） |
| `!` | Bash 模式，直接运行 shell 命令 |
| `/` | 斜杠模式，打开并运行内置命令 |
| `\` `⏎` | 多行输入 |

### 高级启动选项

| 参数 | 说明 | 示例 |
|------|------|------|
| `-w` | 指定工作区目录 | `qodercli -w /path/to/project` |
| `-c` | 继续上次会话 | `qodercli -c` |
| `-r` | 恢复指定会话 | `qodercli -r <session-id>` |
| `--allowed-tools` | 仅允许指定工具 | `qodercli --allowed-tools=Read,Write` |
| `--disallowed-tools` | 禁止指定工具 | `qodercli --disallowed-tools=Read,Write` |
| `--max-turns` | 最大对话轮数 | `qodercli --max-turns=10` |
| `--yolo` | 跳过权限检查 | `qodercli --yolo` |

## Print 模式

非交互式模式：`qodercli --print` 或 `qodercli -p "prompt"`

| 参数 | 说明 |
|------|------|
| `-p` | 以非交互方式运行 Agent |
| `--output-format` | 输出格式：text、json、stream-json |

## Worktree

`--worktree [name]` 在独立 Git worktree 中启动会话。适合同仓库并行处理多任务。

```shell
qodercli --worktree feature-a
qodercli --worktree feature-a "Implement the login fix"
qodercli --worktree  # 自动生成名称
```

## 记忆

通过 AGENTS.md 和自动记忆跨会话保留上下文：
- 用户级：`~/.qoder/AGENTS.md`
- 项目级：`${project}/AGENTS.md`
- 本地项目级：`${project}/AGENTS.local.md`

`/init` 自动生成项目 AGENTS.md；`/memory` 管理记忆。
