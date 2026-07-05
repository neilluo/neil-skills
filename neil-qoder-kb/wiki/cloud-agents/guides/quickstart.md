# 快速开始

> 5 步跑通你的第一个 Qoder Cloud Agent，全程只需 curl。

## 概述

本指南帮助你从零开始，在 5 分钟内创建并运行第一个 Cloud Agent。无需安装 SDK，只需终端和 curl。

## 前置条件

- 一个 Qoder 账号
- 终端环境（macOS / Linux / WSL）
- `curl` 和 `jq`（可选）

## 步骤 1：获取 PAT

1. 登录 Qoder 控制台
2. 设置 → 个人访问令牌 → 创建令牌
3. 导出环境变量：

```bash
export QODER_PAT="your-personal-access-token"
```

> 令牌只在创建时显示一次。建议写入 `~/.bashrc` 或 `~/.zshrc`。

## 步骤 2：创建环境

新账号没有预置环境，需先创建：

```bash
curl -s -X POST https://api.qoder.com/api/v1/cloud/environments \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{"name":"default","config":{"type":"cloud","networking":{"type":"unrestricted"}}}'
```

记录返回的 `env_xxx` ID。

## 步骤 3：创建 Agent

```bash
curl -s -X POST https://api.qoder.com/api/v1/cloud/agents \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-first-agent",
    "model": "ultimate",
    "system": "你是一个高效的编程助手。",
    "tools": [{"type": "agent_toolset_20260401", "enabled_tools": ["Bash", "Read", "Write", "Edit", "Glob", "Grep"]}]
  }'
```

记录返回的 `agent_xxx` ID。

## 步骤 4：创建 Session

```bash
curl -s -X POST https://api.qoder.com/api/v1/cloud/sessions \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{"agent": "agent_xxx", "environment_id": "env_xxx"}'
```

Session 创建后处于 `idle` 状态。

## 步骤 5：发消息 + 接收事件流

```bash
# 发送消息
curl -s -X POST "https://api.qoder.com/api/v1/cloud/sessions/sess_xxx/events" \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{"events": [{"type": "user.message", "content": [{"type": "text", "text": "用 Python 写一个斐波那契函数并运行测试。"}]}]}'

# 接收 SSE 事件流
curl -s -N "https://api.qoder.com/api/v1/cloud/sessions/sess_xxx/events/stream" \
  -H "Authorization: Bearer $QODER_PAT"
```

## 执行流程

发送消息后平台会：
1. Session idle → processing（`session.status_running`）
2. 启动模型请求（`span.model_request_start`）
3. 流式输出思考和回复（`agent.thinking`、`agent.message`）
4. 工具调用（`agent.tool_use` + `agent.tool_result`）
5. 完成（`session.status_idle`）

## 验证连通性

```bash
curl -s https://api.qoder.com/api/v1/cloud/agents \
  -H "Authorization: Bearer $QODER_PAT"
# 成功返回 {"data": [], ...}
```

## 交叉引用

- [[agent]] — Agent 配置详情
- [[environment]] — 环境配置选项
- [[session]] — Session 完整 API
- [[sse-event-stream]] — 事件流详细说明
- [[troubleshooting]] — 常见问题排查
- [[production-checklist]] — 下一步：生产环境上线检查
- [[deployment]] — 部署链路概览

## 来源

- raw/cloud-agents/quickstart.md [official-docs] 2026-06-21
- raw/cloud-agents/overview.md [official-docs] 2026-06-21
