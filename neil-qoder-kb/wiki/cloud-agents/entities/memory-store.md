# Memory Store

> 跨 Session 的持久化记忆仓库，让 Agent 积累和复用知识。

## 概述

Memory Store 提供跨 Session 的持久化（persist）记忆能力。每个 Store 包含多条 Entry（记忆条目），按 `path` 组织。Session 关联 Memory Store 后，Entry 会挂载到沙箱内供 Agent 读取。数据在 Session 结束后依然 persist（持久保存），实现知识的长期积累。

## 核心概念

| 概念 | 说明 |
|------|------|
| Memory Store | 记忆仓库，按项目或领域划分 |
| Entry | 一条记忆，由 `path` 标识 |
| Version | 每次写入/更新自动生成的版本快照 |

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/cloud/memory_stores` | 创建 Store |
| GET | `/api/v1/cloud/memory_stores` | 列出所有 Store |
| POST | `/api/v1/cloud/memory_stores/{id}/memories` | 创建 Entry |
| GET | `/api/v1/cloud/memory_stores/{id}/memories/{entry_id}` | 获取单条（含 content） |
| PUT | `/api/v1/cloud/memory_stores/{id}/memories/{entry_id}` | 更新 Entry（OCC） |

## Entry 路径规则

- 必须是相对路径（不能以 `/` 开头）
- 支持子目录，如 `notes/2026/05/daily.md`
- 沙箱内挂载路径：`/data/.qoder/awareness/<entry.path>`

## 创建示例

```bash
# 创建 Store
curl -X POST https://api.qoder.com/api/v1/cloud/memory_stores \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{"name": "project-alpha-memory", "description": "Alpha 项目知识库"}'

# 创建 Entry
curl -X POST https://api.qoder.com/api/v1/cloud/memory_stores/memstore_xxx/memories \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{"path": "decisions/arch-choice.md", "content": "# 架构决策\n选择微服务架构。"}'
```

## 更新 Entry

使用 [[occ-versioning]]：

```bash
curl -X PUT https://api.qoder.com/api/v1/cloud/memory_stores/memstore_xxx/memories/mem_xxx \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{"content": "# 架构决策 v2\n改为 Modular Monolith。", "version": 1}'
```

## 在 Session 中使用

> ⚠️ 2026-06-23 起，`memory_store_ids` 顶层字段已废弃，改用 `resources` 数组。

```bash
curl -X POST https://api.qoder.com/api/v1/cloud/sessions \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "agent_xxx",
    "environment_id": "env_xxx",
    "resources": [{"type": "memory_store", "memory_store_id": "memstore_xxx"}]
  }'
```

## 交叉引用

- [[session]] — Memory Store 关联到 Session
- [[occ-versioning]] — Entry 更新的并发控制
- [[memory-vs-files]] — 记忆与文件的选型对比

## 来源

- raw/cloud-agents/memory-stores.md [official-docs] 2026-06-21
