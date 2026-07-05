# Session 状态机

> Session 从创建到归档的完整生命周期和状态流转规则。

## 概述

Session 有 4 个状态，形成一个有限状态机。理解状态流转是正确使用 API 的基础——向错误状态发送操作会返回 409 冲突。

## 状态定义

| 状态 | 说明 | 可执行操作 |
|------|------|------|
| `idle` | 空闲，等待输入 | 发消息、归档 |
| `processing` | Agent 执行中 | 取消 |
| `canceling` | 等待中断完成 | 等待 |
| `archived` | 终态，不可恢复 | 无 |

## 状态流转图

```
           user.message
  idle ──────────────────→ processing
   ↑                          │
   │    cancel完成             │ cancel请求
   │←──── canceling ←─────────│
   │                          │
   │    一轮完成（status_idle） │
   │←─────────────────────────│
   │
   └──→ archived（终态）
```

## 关键规则

1. **只有 idle 可接收消息**：向 `processing` 状态发消息返回 409
2. **只有 processing 可取消**：其他状态调用 cancel 无效
3. **cancel 后回到 idle**：Session 可继续复用
4. **archived 是终态**：不可恢复
5. **长时间不活跃**：系统可能自动归档

## 对应 SSE 事件

| 事件 | 状态流转 |
|------|----------|
| `session.status_running` | idle → processing |
| `session.status_idle` | processing → idle |
| `terminated` | → archived |

## 容器生命周期

- 容器在 Session 生命周期内保持
- 临时存储保留 24 小时
- 超时后磁盘可能回收，但 Session 对话仍可继续

## 交叉引用

- [[session]] — Session 实体定义
- [[event]] — 状态变更对应的事件
- [[sse-event-stream]] — 通过事件流感知状态变化

## 来源

- raw/cloud-agents/sessions.md [official-docs] 2026-06-21
- raw/cloud-agents/events-stream.md [official-docs] 2026-06-21
