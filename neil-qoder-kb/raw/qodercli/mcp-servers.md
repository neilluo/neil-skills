# MCP 服务

> 来源: https://docs.qoder.com/zh/cli/mcp-servers

## 快速开始

```shell
qodercli mcp add playwright -- npx -y @playwright/mcp@latest
```

Stdio 服务随 CLI 自动启动。已运行的 CLI 使用 `/mcp reload` 重新发现。

## 服务类型

| 类型 | 适用场景 |
|------|---------|
| stdio | MCP 服务作为本地命令运行 |
| sse | 通过 Server-Sent Events 端点暴露 |
| http | 通过 HTTP 端点暴露 |
| ws | 通过 WebSocket 端点暴露 |

## 作用域

| 作用域 | 配置文件 | 适用场景 |
|--------|---------|---------|
| user | `~/.qoder/settings.json` | 所有项目可用 |
| local | `${project}/.qoder/settings.local.json` | 仅本机当前项目（默认） |
| project | `${project}/.mcp.json` | 随项目共享 |

## 管理

```shell
qodercli mcp list       # 列出已配置服务
qodercli mcp remove xxx # 移除服务
```

## 权限

MCP 工具经过 CLI 权限系统。工具名格式：`mcp__<server>__<tool>`

```json
{
  "permissions": {
    "allow": ["mcp__context7__*"]
  }
}
```

## 推荐服务

```shell
qodercli mcp add context7 -- npx -y @upstash/context7-mcp@latest
qodercli mcp add deepwiki -- npx -y mcp-deepwiki@latest
qodercli mcp add chrome-devtools -- npx chrome-devtools-mcp@latest
```
