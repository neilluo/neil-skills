# ACP

> 来源: https://docs.qoder.com/zh/cli/acp

## 概述

ACP（Agent Client Protocol）是客户端与 Agent 之间的协议。Qoder CLI 实现该协议标准，可被集成到任何实现了 ACP 协议的客户端中（如 Zed IDE）。

协议详见：https://agentclientprotocol.com/overview/introduction

## 运行模式

- 默认模式：按默认权限设置运行
- Bypass Permissions 模式：等同于 `--yolo`，跳过权限检查

## 支持的特性

| 特性 | 说明 |
|------|------|
| 内置工具 | 与 CLI 相同 |
| Subagent | 与 CLI 相同 |
| MCP Server | Stdio/SSE/HTTP 类型 |
| 权限配置 | 与 CLI 相同 |
| 上下文压缩 | 与 CLI 相同 |
| 多模态 | 支持图像 |
| 文件操作/Terminal | 通过 ACP 使用 IDE 侧能力 |

## 启动方式

```shell
qodercli --acp    # 以 ACP 服务器启动
```

## Zed IDE 集成

```json
{
  "agent_servers": {
    "Qoder CLI": {
      "type": "custom",
      "command": "qodercli",
      "args": ["--acp"]
    }
  }
}
```

## 登录

使用与 Qoder CLI 相同的登录状态。也支持环境变量：

```json
{
  "agent_servers": {
    "Qoder CLI": {
      "env": { "QODER_PERSONAL_ACCESS_TOKEN": "your_token" },
      "command": "qodercli",
      "args": ["--acp"]
    }
  }
}
```
