# Event

> Session 中产生的实时事件流，通过 SSE 协议传输 Agent 的思考、消息和工具调用。

## 概述

Event 是 Session 执行过程中产生的结构化数据单元。客户端通过 SSE（Server-Sent Events）连接实时接收事件流，获取 Agent 的思考过程、回复内容、工具调用和状态变更。

## 完整事件类型

| 事件类型 | 含义 | 触发时机 |
|--------|------|------|
| `user.message` | 用户消息 | 客户端 POST 事件后 |
| `session.status_running` | 开始执行 | 收到消息后 |
| `span.model_request_start` | 模型请求开始 | Agent 发起 LLM 调用 |
| `agent.thinking` | Agent 思考中 | 模型推理过程中 |
| `agent.message` | Agent 回复 | 模型产出文本 |
| `agent.tool_use` | 内置工具调用 | 模型决定调用工具 |
| `agent.tool_result` | 工具执行回执 | 工具执行完成 |
| `agent.custom_tool_use` | 自定义工具请求 | 模型调用 client-side 工具 |
| `session.status_idle` | Session 空闲 | 一轮完成 |
| `span.model_request_end` | 模型请求结束 | LLM 调用完成 |
| `session.error` | 出错 | 运行时异常 |
| `terminated` | Session 终止 | 被关闭或超时 |

## 用户可发送的事件

| 事件类型 | 用途 |
|--------|------|
| `user.message` | 发送消息给 Agent |
| `user.tool_confirmation` | 批准/拒绝工具调用 |
| `user.custom_tool_result` | 回传自定义工具结果 |
| `user.define_outcome` | 定义成功标准（Rubric） |

## status_idle 完整结构

```json
{
  "type": "session.status_idle",
  "status": "idle",
  "stop_reason": {"type": "end_turn"},
  "usage": {
    "input_tokens": 23487,
    "output_tokens": 1024,
    "cache_read_input_tokens": 11223,
    "cache_creation_input_tokens": 0
  }
}
```

`stop_reason.type` 可能值：`end_turn`、`requires_action`、`cancel`、`max_turns`、`error`

## 典型事件生命周期

```
user.message → session.status_running → span.model_request_start
→ agent.thinking → agent.message → session.status_idle → span.model_request_end
```

## 交叉引用

- [[session]] — 事件所属的执行实例
- [[sse-event-stream]] — SSE 连接与断线重连机制
- [[permission-model]] — 工具确认事件流程
- [[outcome-rubric]] — user.define_outcome 事件的用法

## 来源

- raw/cloud-agents/events-stream.md [official-docs] 2026-06-21
- raw/cloud-agents/outcomes.md [official-docs] 2026-06-21
- raw/cloud-agents/permission-policies.md [official-docs] 2026-06-21
