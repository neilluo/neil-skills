# 持久化记忆 (Memory Stores)

> 让 Agent 拥有跨 Session 的持久记忆。

## 核心概念

| 概念 | 说明 |
|------|------|
| Memory Store | 记忆仓库，按项目或领域划分 |
| Entry | 一条记忆，由 `path` 标识 |
| Version | 每次写入/更新自动生成的版本快照 |

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/memory_stores` | 创建 Store |
| GET | `/memory_stores` | 列出所有 Store |
| POST | `/memory_stores/{id}/memories` | 创建 Entry |
| GET | `/memory_stores/{id}/memories/{entry_id}` | 获取单条（含 content） |
| PUT | `/memory_stores/{id}/memories/{entry_id}` | 更新 Entry（OCC） |

## 路径规则

Entry 的 `path` 必须是相对路径（不能以 `/` 开头）。

## 创建 Memory Store

```bash
curl -X POST https://api.qoder.com/api/v1/cloud/memory_stores \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "project-alpha-memory",
    "description": "Alpha 项目的 Agent 知识库"
  }'
```

## 创建 Entry

```bash
curl -X POST https://api.qoder.com/api/v1/cloud/memory_stores/memstore_xxx/memories \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "decisions/arch-choice.md",
    "content": "# 架构决策\n\n选择微服务架构。"
  }'
```

## 更新 Entry（OCC）

```bash
curl -X PUT https://api.qoder.com/api/v1/cloud/memory_stores/memstore_xxx/memories/mem_xxx \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# 架构决策 v2\n\n改为 Modular Monolith。",
    "version": 1
  }'
```

## 在 Session 中使用

```bash
curl -X POST https://api.qoder.com/api/v1/cloud/sessions \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "agent_xxx",
    "memory_store_ids": ["memstore_xxx"]
  }'
```

## Sandbox 内路径

Entry 挂载到：`/data/.qoder/awareness/<entry.path>`

## 常见问题

**Q: 一个 Session 可关联多少个 Memory Store？**
A: 支持多个。

**Q: Entry path 可以包含子目录吗？**
A: 可以，如 `notes/2026/05/daily.md`。
