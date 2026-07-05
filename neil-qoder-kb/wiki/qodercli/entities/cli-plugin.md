# CLI Plugin — 插件系统

> 将命令、Subagent、Skill、Hook、MCP 等扩展能力打包为一个可安装、可共享的目录单元。

## 概述

Plugin 是 Qoder CLI 的扩展分发机制。一个插件目录可以包含多种扩展资源（命令、子 Agent、Skill、Hook、MCP server、输出样式），安装后 CLI 自动发现并加载所有资源。

## 目录结构

```
my-plugin/
├── .qoder-plugin/
│   └── plugin.json        # manifest（推荐）
├── commands/              # 自定义斜杠命令
├── agents/                # 自定义 Subagent
├── skills/                # 自定义 Skill
├── hooks/
│   └── hooks.json         # Hook 配置
├── output-styles/         # 输出样式
├── bin/                   # 可执行文件
└── .mcp.json              # MCP server 声明
```

## manifest（plugin.json）

仅 `name` 必填：

| 字段 | 必填 | 说明 |
|------|------|------|
| name | 是 | 唯一标识（kebab-case） |
| version | 否 | 语义化版本号 |
| description | 否 | 简短描述 |
| author / homepage / repository / license / keywords | 否 | 元信息 |

## 安装方式

```shell
qodercli plugins install ~/my-plugin           # 本地目录
qodercli plugins install @org/plugin-name      # npm 包
qodercli plugins install github:user/repo      # GitHub 仓库
```

## 管理

| 命令 | 功能 |
|------|------|
| `qodercli plugins list` | 列出已安装 |
| `qodercli plugins enable <name>` | 启用 |
| `qodercli plugins disable <name>` | 禁用 |
| `qodercli plugins remove <name>` | 卸载 |
| `/plugins` (TUI) | 交互式管理 |
| `/plugins reload` (TUI) | 重新加载 |

## 安装位置

`~/.qoder/plugins/`（用户级）

## 优先级规则

同名资源按来源覆盖：**项目级 > 用户级 > Plugin > 内置**

## 交叉引用

- [[cli-skill]] — 插件可包含 Skills
- [[cli-subagent]] — 插件可包含 Subagent
- [[cli-command-system]] — 插件可注册自定义命令
- [[cli-hook-system]] — 插件可提供 Hook 配置
- [[cli-tool-mcp]] — 插件可声明 MCP server

## 来源

- raw/qodercli/plugins.md [official-docs]
