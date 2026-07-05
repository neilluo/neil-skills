# 工具

> 来源: https://docs.qoder.com/zh/cli/tools

## 工具分类

### 搜索与探索
文件搜索、代码搜索、目录浏览、Web 搜索、网页内容获取

### 读取项目上下文
查看文件、读取大文件片段、读取 PDF 等文档

### 编辑文件
修改已有文件、创建新文件、编辑 Notebook

### 执行命令
运行 shell 命令、跟踪长任务

### 管理上下文
跟踪任务、澄清问题、管理记忆、使用 Skills、规划工作

### 分派与自动化
Subagents（分派子任务）、Workflows（可重复工作流）、Goals（长周期目标）、Worktrees（并行会话）、定时任务

### MCP 工具
连接外部 MCP 服务，工具经过相同权限系统。适合接入 Issue 系统、代码托管、数据库、浏览器自动化等。

## 控制工具使用

| 控制项 | 说明 |
|--------|------|
| `--tools` | 限制当前会话中可见的工具 |
| `--allowed-tools` | 预先允许指定工具 |
| `--disallowed-tools` | 阻止指定工具 |
| `permissions.allow/ask/deny` | settings 文件中的持久化权限规则 |
| `tools.exclude` | 启动时移除工具 |

示例：
```shell
# 只读探索
qodercli --tools Read Grep Glob --allowed-tools 'Read,Grep,Glob'
# 禁止文件编辑
qodercli -p "review this repository" --disallowed-tools 'Write,Edit'
```
