# Managed Agents

> 通过 coordinator Agent 将子任务并行或串行委派给 child Agent。

## 核心概念

| 概念 | 说明 |
|------|------|
| Coordinator | 协调者线程，负责编排和分派任务 |
| Child thread | 子线程，独立执行任务并回报结果 |
| Session Thread | 线程实体，ID 前缀为 `sthr_` |

## 配置 Managed Agent

在 Agent 的 `multiagent` 字段中设置：

```bash
curl -X POST "https://api.qoder.com/api/v1/cloud/agents" \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "task-coordinator",
    "model": "ultimate",
    "system": "你是任务协调者。",
    "tools": [{"type": "agent_toolset_20260401", "enabled_tools": ["Bash", "Read", "Write"]}],
    "multiagent": {
      "type": "coordinator",
      "agents": [
        {"type": "agent", "id": "agent_xxx", "name": "Research Agent"},
        {"type": "self"}
      ]
    }
  }'
```

### agents 数组格式

| 格式 | 示例 | 说明 |
|------|------|------|
| 对象 `type: "agent"` | `{"type": "agent", "id": "agent_xxx"}` | 引用其他 Agent |
| 对象 `type: "self"` | `{"type": "self"}` | 引用自身 |
| 字符串简写 | `"agent_xxx"` | 等价于对象格式 |

## Coordinator 控制工具

系统自动注入：

- **`create_agent`** — 创建子线程并发送初始任务（异步）
- **`Agent`** — 委派任务并同步等待结果（阻塞式）
- **`send_to_agent`** — 向已有子线程发送后续消息
- **`list_agents`** — 列出所有子线程状态

## Child 控制工具

- **`send_to_parent`** — 向 coordinator 发送结果

## 线程事件

| 事件类型 | 说明 |
|--------|------|
| `session.thread_created` | 创建了新的子线程 |
| `session.thread_status_running` | 线程开始执行 |
| `session.thread_status_idle` | 线程完成或暂停 |
| `agent.thread_message_sent` | 线程间发送消息 |
| `agent.thread_message_received` | 线程间接收消息 |

## 限制

| 项目 | 限制 |
|------|------|
| 每个 Agent 最多子 Agent 数量 | 20 个 |
| 每个 Session 最多并发线程 | 25 个 |
