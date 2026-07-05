# CLI Cloud & Remote — 云端与远程执行

> 三种方式突破本地限制：Cloud Mode（云端VM）、Remote Control（手机控制）、ACP（IDE集成）。

## 概述

Qoder CLI 不仅限于本地终端使用。通过三种机制可以突破本地限制：Cloud Mode 在云端 VM 执行任务、Remote Control 通过手机远程操控、ACP 协议集成到第三方 IDE。

## Cloud Mode（`--remote`）

在 Qoder 管理的云端 VM 中执行任务，本地无需保持开机。

```bash
qodercli --remote "review the auth middleware and suggest improvements"
```

### 执行流程

1. 创建 Cloud Session
2. 发送任务到云端 Agent
3. 实时流式输出到本地终端
4. 完成后打印 Web 端会话 URL

### 关键特性

| 特性 | 说明 |
|------|------|
| 断线续跑 | Ctrl+C 仅断开订阅，云端继续 |
| 多任务并行 | 每次 --remote 创建独立 Session |
| 环境选择 | `/remote-env` 选择默认环境 |
| GitHub 集成 | 需授权 Qoder 访问仓库 |

### 适用场景

长时任务、离线发起、统一环境、资源隔离

## Remote Control（远程控制）

手机/Web 实时掌控本地 CLI Agent。

### 模式一：远程控制模式

已有 TUI 会话中开启：
```bash
/remote-control        # 开启（显示二维码）
/remote-control stop   # 停止
```

### 模式二：守护进程模式（Daemon）

后台待命，手机随时发任务：
```bash
qodercli remote-control    # 启动
# Ctrl+C 退出
```

### 两种模式区别

| 模式 | 前提 | 场景 |
|------|------|------|
| 远程控制 | 已有 TUI 会话 | 临时离开，继续监控 |
| 守护进程 | 无需先启动会话 | 电脑待命，手机派活 |

## ACP 协议（Agent Client Protocol）

Qoder CLI 实现 ACP 标准，可集成到任何 ACP 客户端。

```bash
qodercli --acp    # 以 ACP 服务器启动
```

### Zed IDE 配置

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

### ACP 支持的能力

内置工具、Subagent、MCP Server（Stdio/SSE/HTTP）、权限配置、上下文压缩、多模态（图像）。

## 三种方式对比

| 方式 | 任务执行位置 | 控制入口 | 典型场景 |
|------|------------|---------|---------|
| Cloud Mode | 云端 VM | 终端/Web | 长时任务、离线 |
| Remote Control | 本地电脑 | 手机/Web | 移动办公 |
| ACP | 本地电脑 | 第三方 IDE | IDE 集成 |

## 交叉引用

- [[cli-session]] — 基础会话模式（TUI/Print/ACP）
- [[session]] — Cloud Agents 的 Session 概念
- [[cli-permission-model]] — 云端任务的权限控制

## 来源

- raw/qodercli/cloud-mode.md [official-docs]
- raw/qodercli/remote-control.md [official-docs]
- raw/qodercli/acp.md [official-docs]
