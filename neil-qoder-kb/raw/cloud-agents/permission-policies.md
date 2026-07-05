# 权限策略

> 控制工具调用是允许、询问还是拒绝。

## 运行时行为

| evaluated_permission | 行为 |
|------|------|
| `allow` | 平台直接执行工具 |
| `ask` | Turn 暂停，等待 `user.tool_confirmation` |
| `deny` | 返回被拒绝的工具结果 |

## 配置权限

```json
{
  "tools": [
    {
      "type": "agent_toolset_20260401",
      "enabled_tools": ["Bash", "Read", "Write"],
      "configs": [
        {"name": "Read", "permission_policy": {"type": "always_allow"}},
        {"name": "Write", "permission_policy": {"type": "always_ask"}},
        {"name": "Bash", "permission_policy": {"type": "always_deny"}}
      ]
    }
  ]
}
```

`permission_policy.type` 可选值：`always_allow`、`always_ask`、`always_deny`

## Pending Action 流程

1. 事件流发送 `agent.tool_use`
2. 发送 `session.status_idle`，`stop_reason.type` 为 `requires_action`
3. 客户端回传 `user.tool_confirmation`

## 确认工具调用

```bash
# 批准
curl -X POST https://api.qoder.com/api/v1/cloud/sessions/sess_xxx/events \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "events": [{
      "type": "user.tool_confirmation",
      "tool_use_id": "evt_xxx",
      "result": "allow"
    }]
  }'

# 拒绝
curl -X POST https://api.qoder.com/api/v1/cloud/sessions/sess_xxx/events \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "events": [{
      "type": "user.tool_confirmation",
      "tool_use_id": "evt_xxx",
      "result": "deny",
      "deny_message": "不允许执行此操作。"
    }]
  }'
```

## 自定义工具回传

```bash
curl -X POST https://api.qoder.com/api/v1/cloud/sessions/sess_xxx/events \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "events": [{
      "type": "user.custom_tool_result",
      "custom_tool_use_id": "evt_xxx",
      "content": [{"type": "text", "text": "订单状态：已发货"}]
    }]
  }'
```

## 常见问题

**Q：pending action 会超时吗？**
A：不会。保持 pending 直到被解决或 session/turn 被取消。

**Q：自定义工具能用 permission_policy 吗？**
A：不能。自定义工具由客户端负责执行。
