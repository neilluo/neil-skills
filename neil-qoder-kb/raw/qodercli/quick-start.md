# 快速上手

> 来源: https://docs.qoder.com/zh/cli

## 安装

支持的操作系统：macOS、Linux、Windows（Windows Terminal）
支持的 CPU 架构：arm64、amd64（Windows arm64 暂不支持）

```shell
# MacOS / Linux
curl -fsSL https://qoder.com/install | bash

# Windows PowerShell
irm https://qoder.com/install.ps1 | iex
```

验证安装：`qodercli --version`

## 登录

两种身份验证方式：
1. 交互式登录（推荐）：`/login` → 选择 browser 或 personal access token
2. 环境变量（自动化）：`export QODER_PERSONAL_ACCESS_TOKEN="your_token"`

Token 获取地址：https://qoder.com/account/integrations

优先级：/login 提供的令牌 > 环境变量令牌

## 升级

默认启用自动升级。手动升级方式：
- `qodercli update`（内置）
- `curl -fsSL https://qoder.com/install | bash -s -- --force`（重新安装）

禁用自动更新：`~/.qoder/settings.json` → `general.enableAutoUpdate: false`

## 退出登录

`/logout`（需先清除环境变量 QODER_PERSONAL_ACCESS_TOKEN）
