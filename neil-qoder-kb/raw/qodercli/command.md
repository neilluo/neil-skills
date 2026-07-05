# 命令

> 来源: https://docs.qoder.com/zh/cli/command

## 概述

命令是 Qoder CLI 中唤起特定任务的快捷方式，通过斜杠 `/` 前缀触发。

## 命令类型

| 类型 | 说明 | 适用模式 | 扩展性 |
|------|------|---------|--------|
| TUI 类型 | 提供交互式界面（弹出对话框、列表选择） | TUI | 内置，不支持自定义 |
| Prompt 类型 | 向对话中提交预设提示词 | TUI + Headless | 支持用户自定义 |

## 内置命令

| 命令 | 类型 | 用途 |
|------|------|------|
| /agents | TUI | 查看和管理 Subagent |
| /tasks | TUI | 查看后台任务 |
| /workflows | TUI | 动态工作流面板 |
| /clear | TUI | 清除对话 |
| /commands | TUI | 查看和管理自定义命令 |
| /compact | Prompt | 压缩对话历史 |
| /config | TUI | 配置管理 |
| /init | TUI | 生成 AGENTS.md |
| /memory | TUI | 记忆管理 |
| /model | TUI | 模型选择 |
| /effort | TUI | 思考深度 |
| /quest | Prompt | Spec 委派任务 |
| /review | Prompt | 代码审查 |
| /resume | TUI | 恢复会话 |
| /skills | TUI | 管理 Skill |
| /status | TUI | 系统状态 |

## 自定义命令

### 配置文件格式

```markdown
---
name: git-commit
description: 分析 git 变更生成规范提交信息
---

系统提示词内容...
```

### 存储位置

| 级别 | 路径 | 生效范围 |
|------|------|---------|
| 项目级 | `.qoder/commands/<name>.md` | 仅当前项目 |
| 用户级 | `~/.qoder/commands/<name>.md` | 所有项目 |

项目级优先于用户级。

### 命名规范

- 使用小写字母和连字符
- 子目录用 `:` 作为命名空间分隔符（如 `git/commit.md` → `/git:commit`）
- 存在 SKILL.md 的目录注册为单个命令

### 创建方式

1. AI 辅助：`/commands` → Create new command → 描述功能
2. 手动编写：直接创建 .md 配置文件

### Headless 使用

```bash
qodercli -p '/review 重点检查注释覆盖情况'
qodercli -p '/git-commit'
```
