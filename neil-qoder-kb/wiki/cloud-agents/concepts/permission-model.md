# 权限模型

> 控制工具调用的运行时权限：允许、询问或拒绝。

## 概述

权限模型决定了 Agent 调用工具时平台的行为。通过 `permission_policy` 配置每个工具的权限策略，实现对 Agent 能力的精细控制。当策略为 `ask` 时，Session 会暂停等待客户端确认。

## 运行时行为

| evaluated_permission | 行为 |
|------|------|
| `allow` | 平台直接执行工具 |
| `ask` | Turn 暂停，等待 `user.tool_confirmation` |
| `deny` | 返回被拒绝的工具结果 |

## 配置方式

在 Agent 的 `tools[].configs` 中设置：

```json
{
  "tools": [{
    "type": "agent_toolset_20260401",
    "enabled_tools": ["Bash", "Read", "Write"],
    "configs": [
      {"name": "Read", "permission_policy": {"type": "always_allow"}},
      {"name": "Write", "permission_policy": {"type": "always_ask"}},
      {"name": "Bash", "permission_policy": {"type": "always_deny"}}
    ]
  }]
}
```

`permission_policy.type` 可选值：`always_allow`、`always_ask`、`always_deny`

## Pending Action 流程

1. Agent 决定调用工具 → 发出 `agent.tool_use` 事件
2. 平台检查权限策略 → 如果是 `ask`，发出 `session.status_idle`（`stop_reason.type` = `requires_action`）
3. 客户端收到暂停信号 → 回传 `user.tool_confirmation`

## 确认/拒绝工具调用

```bash
# 批准
curl -X POST https://api.qoder.com/api/v1/cloud/sessions/sess_xxx/events \
  -d '{"events": [{"type": "user.tool_confirmation", "tool_use_id": "evt_xxx", "result": "allow"}]}'

# 拒绝（可附带消息）
curl -X POST https://api.qoder.com/api/v1/cloud/sessions/sess_xxx/events \
  -d '{"events": [{"type": "user.tool_confirmation", "tool_use_id": "evt_xxx", "result": "deny", "deny_message": "不允许执行此操作。"}]}'
```

## 自定义工具回传

自定义工具不受 permission_policy 控制（由客户端负责执行）：

```bash
curl -X POST https://api.qoder.com/api/v1/cloud/sessions/sess_xxx/events \
  -d '{"events": [{"type": "user.custom_tool_result", "custom_tool_use_id": "evt_xxx", "content": [{"type": "text", "text": "结果数据"}]}]}'
```

## 关键注意点

- Pending action **不会超时**，保持直到被解决或 session/turn 被取消
- 自定义工具不能使用 permission_policy
- 权限配置在 Agent 级别，不支持 Session 级别覆盖

## 交叉引用

- [[agent]] — 权限在 Agent tools 中配置
- [[event]] — 确认事件类型定义
- [[session-lifecycle]] — requires_action 暂停状态
- [[tools-vs-skills]] — 工具权限与技能的关系

## 来源

- raw/cloud-agents/permission-policies.md [official-docs] 2026-06-21
- raw/cloud-agents/tools.md [official-docs] 2026-06-21
