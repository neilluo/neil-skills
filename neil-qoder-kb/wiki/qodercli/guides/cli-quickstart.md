# CLI Quickstart — 快速上手

> 从安装到第一次对话的三步引导：安装 → 登录 → 使用。

## 概述

Qoder CLI 是终端中的 AI Coding Agent。支持 macOS、Linux、Windows，arm64 和 amd64 架构。安装后即可进入交互式 TUI 或非交互式 Print 模式开始工作。

## Step 1：安装

```shell
# macOS / Linux
curl -fsSL https://qoder.com/install | bash

# Windows PowerShell
irm https://qoder.com/install.ps1 | iex
```

验证：`qodercli --version`

## Step 2：登录

首次执行命令时 CLI 自动提示登录。两种方式：

| 方式 | 适用场景 | 操作 |
|------|---------|------|
| 交互式 | 日常使用 | TUI 中 `/login` → 浏览器 或 Token |
| 环境变量 | CI/CD 自动化 | `export QODER_PERSONAL_ACCESS_TOKEN="..."` |

Token 获取：https://qoder.com/account/integrations

## Step 3：使用

```shell
# 进入交互式 TUI
qodercli

# 非交互式执行
qodercli -p "解释这个项目的架构"

# 指定工作区
qodercli -w /path/to/project
```

## 下一步

| 想做什么 | 参考 |
|---------|------|
| 选择合适模型 | [[cli-model]] |
| 配置记忆和规范 | [[cli-memory-system]] |
| 接入外部工具 | [[cli-tool-mcp]] |
| 创建自定义 Skill | [[cli-skill]] |
| 配置权限 | [[cli-permission-model]] |
| 远程/云端执行 | [[cli-cloud-remote]] |

## 升级

```shell
qodercli update                  # 内置升级
# 或重新安装
curl -fsSL https://qoder.com/install | bash -s -- --force
```

禁用自动更新：`~/.qoder/settings.json` → `"general": { "enableAutoUpdate": false }`

## 交叉引用

- [[cli-session]] — 会话的三种运行模式详解
- [[cli-command-system]] — 所有内置斜杠命令列表
- [[cli-model]] — 模型选择与切换

## 来源

- raw/qodercli/quick-start.md [official-docs]
- raw/qodercli/using-cli.md [official-docs]
