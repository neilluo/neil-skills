# 插件

> 来源: https://docs.qoder.com/zh/cli/plugins

## 概述

插件（Plugin）将命令、子 Agent、Skill、Hook、MCP server 等扩展能力打包为一个目录，便于安装、启用与共享。

## 目录结构

```
my-plugin/
├── .qoder-plugin/
│   └── plugin.json        # manifest
├── commands/              # 自定义命令
├── agents/                # 自定义子 Agent
├── skills/                # 自定义 Skill
├── hooks/
│   └── hooks.json         # Hook 配置
├── output-styles/         # 输出样式
├── bin/                   # 可执行文件
└── .mcp.json              # MCP server 声明
```

## manifest (plugin.json)

| 字段 | 必填 | 说明 |
|------|------|------|
| name | 是 | 唯一标识，kebab-case |
| version | 否 | 语义化版本号 |
| description | 否 | 简短描述 |
| author | 否 | 作者信息 |
| homepage | 否 | 文档 URL |
| repository | 否 | 源码仓库 URL |
| license | 否 | SPDX license |
| keywords | 否 | 标签数组 |

## 安装方式

```shell
# 本地目录
qodercli plugins install ~/my-plugin

# npm 包
qodercli plugins install @org/plugin-name

# GitHub 仓库
qodercli plugins install github:user/repo
```

## 管理

```shell
qodercli plugins list                  # 列出已安装
qodercli plugins enable <name>         # 启用
qodercli plugins disable <name>        # 禁用
qodercli plugins remove <name>         # 卸载
```

TUI 中：`/plugins` 查看和管理；`/plugins reload` 重新加载。

## 安装位置

```
~/.qoder/plugins/    # 用户级（默认）
```

## 优先级

同名资源：项目级 > 用户级 > Plugin > 内置
