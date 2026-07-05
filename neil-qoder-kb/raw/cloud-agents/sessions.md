# 启动 Session

> 让 Agent 在环境中以有状态对话的方式运行。

Session 是实际执行任务的单元。它将 Agent（配置）和 Environment（基础设施）组合在一起。

## Session 生命周期

| 状态 | 说明 | 可流转到 |
|------|------|------|
| `idle` | 空闲，等待用户消息 | `processing` |
| `processing` | Agent 执行中 | `canceling`, `idle` |
| `canceling` | 等待中断完成 | `idle` |
| `archived` | 已归档（终态） | — |

## 创建 Session

```bash
# 使用 Agent ID（绑定最新版本）
curl -s -X POST https://api.qoder.com/api/v1/cloud/sessions \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "agent_xxx",
    "environment_id": "env_xxx"
  }'

# 指定 Agent 版本（生产环境推荐）
curl -s -X POST https://api.qoder.com/api/v1/cloud/sessions \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "agent": {"id": "agent_xxx", "version": 2},
    "environment_id": "env_xxx"
  }'
```

## 环境变量

```bash
curl -s -X POST https://api.qoder.com/api/v1/cloud/sessions \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "agent_xxx",
    "environment_id": "env_xxx",
    "environment_variables": "NODE_ENV=production; FEATURE_FLAG=1"
  }'
```

变量名必须匹配 `[A-Za-z_][A-Za-z0-9_]*`。保留名称：`SERVER_ENDPOINT`、`USER_ID`、`WORK_DIR`，以及 `CAW_`、`QODER_` 前缀。

## 创建时附带资源

| 资源类型 | 请求字段 | 用途 |
|------|------|------|
| 文件 | `resources[]` (`type: "file"`) | 挂载已上传的文件 |
| GitHub 仓库 | `resources[]` (`type: "github_repository"`) | 自动克隆仓库 |
| 记忆存储 | `memory_store_ids` | 关联 Memory Store |
| 密钥库 | `vault_ids` | 关联 Vault 凭证 |

## 发送消息

```bash
curl -s -X POST "https://api.qoder.com/api/v1/cloud/sessions/sess_xxx/events" \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "events": [{
      "type": "user.message",
      "content": [{"type": "text", "text": "分析代码复杂度。"}]
    }]
  }'
```

## 取消 Session

```bash
curl -s -X POST "https://api.qoder.com/api/v1/cloud/sessions/sess_xxx/cancel" \
  -H "Authorization: Bearer $QODER_PAT"
```

> 仅在 `processing` 状态下有效。取消后回到 `idle`，Session 可继续复用。

## Usage 统计

Token 用量通过 SSE `session.status_idle` 事件的 `usage` 字段获取：

| 字段 | 说明 |
|------|------|
| `usage.input_tokens` | 本轮消耗的输入 token |
| `usage.output_tokens` | 本轮产生的输出 token |
| `usage.cache_read_input_tokens` | 命中缓存的 token |
| `usage.cache_creation_input_tokens` | 写入缓存的 token |

## 常见问题

**Q: 向 processing 状态发消息？**
A: 返回 409 `conflict_error`。需先 cancel 或等待 idle。

**Q: Session 有超时机制吗？**
A: 长时间不活跃的 Session 可能被系统自动归档。

**Q: 取消后还能继续用吗？**
A: 可以。cancel 后回到 `idle`，直接发新消息即可。

**Q: 容器磁盘文件保留多久？**
A: 容器临时存储保留 24 小时。超时后磁盘可能被回收，但 Session 仍可继续对话。
