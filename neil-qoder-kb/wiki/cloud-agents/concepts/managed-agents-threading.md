# 多 Agent 线程模型

> 通过 Coordinator 将子任务并行或串行委派给 Child Agent。

## 概述

Managed Agents 允许一个 Coordinator Agent 编排多个 Child Agent 协同完成任务。每个 Child 运行在独立的 Session Thread 中，可并行或串行执行。Coordinator 通过系统注入的控制工具管理子线程。

## 核心概念

| 概念 | 说明 |
|------|------|
| Coordinator | 协调者线程，负责编排和分派任务 |
| Child thread | 子线程，独立执行任务并回报结果 |
| Session Thread | 线程实体，ID 前缀 `sthr_` |

## 配置方式

在 Agent 的 `multiagent` 字段中设置：

```json
{
  "name": "task-coordinator",
  "model": "ultimate",
  "multiagent": {
    "type": "coordinator",
    "agents": [
      {"type": "agent", "id": "agent_xxx", "name": "Research Agent"},
      {"type": "self"}
    ]
  }
}
```

### agents 数组格式

| 格式 | 示例 | 说明 |
|------|------|------|
| 对象 `type: "agent"` | `{"type": "agent", "id": "agent_xxx"}` | 引用其他 Agent |
| 对象 `type: "self"` | `{"type": "self"}` | 引用自身 |
| 字符串简写 | `"agent_xxx"` | 等价于对象格式 |

## Coordinator 控制工具

系统自动注入以下工具：

| 工具 | 用途 | 模式 |
|------|------|------|
| `create_agent` | 创建子线程并发送初始任务 | 异步 |
| `Agent` | 委派任务并等待结果 | 同步阻塞 |
| `send_to_agent` | 向已有子线程发送后续消息 | 异步 |
| `list_agents` | 列出所有子线程状态 | 查询 |

## Child 控制工具

| 工具 | 用途 |
|------|------|
| `send_to_parent` | 向 coordinator 发送结果 |

## 线程事件

| 事件类型 | 说明 |
|--------|------|
| `session.thread_created` | 新子线程创建 |
| `session.thread_status_running` | 线程开始执行 |
| `session.thread_status_idle` | 线程完成或暂停 |
| `agent.thread_message_sent` | 线程间发送消息 |
| `agent.thread_message_received` | 线程间接收消息 |

## 资源限制

| 项目 | 限制 |
|------|------|
| 每个 Agent 最多子 Agent | 20 个 |
| 每个 Session 最多并发线程 | 25 个 |

## 交叉引用

- [[agent]] — Coordinator 和 Child 都是 Agent
- [[session]] — 线程运行在 Session 内
- [[event]] — 线程相关事件类型

## 来源

- raw/cloud-agents/managed-agents.md [official-docs] 2026-06-21
