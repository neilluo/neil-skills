# SSE 事件流

> Server-Sent Events 协议用于实时接收 Agent 执行过程中的所有事件。

## 概述

客户端通过 SSE（Server-Sent Events）连接到 Session 的事件流端点，实时接收 Agent 的思考、回复、工具调用和状态变更。支持断线重连和增量获取。

## 连接方式

```
GET https://api.qoder.com/api/v1/cloud/sessions/{session_id}/events/stream
Authorization: Bearer $QODER_PAT
Accept: text/event-stream
```

## 查询参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `after_id` | 从指定事件 ID 后开始（断线重连） | 无（从头重放） |
| `delta_flush_interval_ms` | message delta 刷新间隔 | 50ms |

## 断线重连

```bash
# 记录最后收到的事件 ID，重连时带上
curl -s -N "https://api.qoder.com/api/v1/cloud/sessions/sess_xxx/events/stream?after_id=evt_01abc123" \
  -H "Authorization: Bearer $QODER_PAT"
```

默认不带 `after_id` 会从头重放所有历史事件。

## Heartbeat

平台约 15 秒发送一次 heartbeat 事件保持连接。客户端应在 30 秒无事件时主动断开重连。

## 客户端实现建议

1. **记录 last event id**：用于重连恢复
2. **处理 delta 拼接**：`agent.message` 可能分多个 delta 发送
3. **监听 terminated**：收到后关闭连接
4. **超时重连**：30 秒无事件主动断开
5. **事件过滤**：仅监听业务关心的事件类型

## 与轮询对比

| 方式 | 延迟 | 复杂度 | 适用场景 |
|------|------|--------|----------|
| SSE 流 | 实时 | 需维护长连接 | 交互式客户端 |
| 轮询 GET events | 秒级 | 简单 | 后端集成 |

## 交叉引用

- [[event]] — 事件类型完整列表
- [[session]] — 事件所属的执行实例
- [[session-lifecycle]] — 状态事件与生命周期

## 来源

- raw/cloud-agents/events-stream.md [official-docs] 2026-06-21
- raw/cloud-agents/quickstart.md [official-docs] 2026-06-21
