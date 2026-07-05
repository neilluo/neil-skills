# Session 事件流

> 通过 SSE 实时获取 Agent 的思考、消息、工具调用与状态。

## 连接 URL

```
GET https://api.qoder.com/api/v1/cloud/sessions/{session_id}/events/stream
Authorization: Bearer $QODER_PAT
Accept: text/event-stream
```

## 完整事件类型

| 事件类型 | 含义 | 触发时机 |
|--------|------|------|
| `user.message` | 用户发送消息 | 客户端 POST 事件后 |
| `session.status_running` | 开始执行 | 收到消息后 |
| `span.model_request_start` | 模型请求开始 | Agent 发起 LLM 调用 |
| `agent.thinking` | Agent 思考中 | 模型推理过程中 |
| `agent.message` | Agent 回复 | 模型产出文本 |
| `agent.tool_use` | 内置工具调用 | 模型决定调用工具 |
| `agent.tool_result` | 工具执行回执 | 工具执行完成 |
| `agent.custom_tool_use` | 自定义工具请求 | 模型决定调用自定义工具 |
| `session.status_idle` | Session 空闲 | 一轮完成 |
| `span.model_request_end` | 模型请求结束 | LLM 调用完成 |
| `session.error` | 出错 | 运行时异常 |
| `terminated` | Session 终止 | 被关闭或超时 |

## 典型事件生命周期

```
user.message              ← 用户输入
session.status_running    ← 开始执行
span.model_request_start  ← 模型请求
agent.thinking            ← 推理中（可选）
agent.message             ← 回复内容
session.status_idle       ← 完成
span.model_request_end    ← 模型请求收尾
```

## status_idle 完整 schema

```json
{
  "type": "session.status_idle",
  "status": "idle",
  "stop_reason": { "type": "end_turn" },
  "usage": {
    "input_tokens": 23487,
    "output_tokens": 1024,
    "cache_read_input_tokens": 11223,
    "cache_creation_input_tokens": 0
  }
}
```

`stop_reason.type` 可能值：`end_turn`、`requires_action`、`cancel`、`max_turns`、`error`

## 断线重连

```
GET /sessions/{session_id}/events/stream?after_id=evt_01abc123
```

默认从头重放所有历史事件。使用 `after_id` 参数获取增量事件。

## delta_flush_interval_ms

控制 `agent.message` delta 事件刷新间隔，默认 50ms：

```
GET /sessions/{session_id}/events/stream?delta_flush_interval_ms=100
```

## 客户端实现建议

1. 记录 last event id，用于重连恢复
2. 处理 delta 拼接
3. 监听 terminated，收到后关闭连接
4. 30 秒无事件时主动断开重连
5. 仅监听业务关心的事件类型
