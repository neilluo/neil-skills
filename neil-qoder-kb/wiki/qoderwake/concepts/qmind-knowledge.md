# QMind 知识引擎

> QoderWake 的内部知识管理系统，通过提案-审计-变更三阶段流程和 OCC（乐观并发控制）实现数字员工知识的协作编辑与版本化治理。

## 概述

QMind 是 QoderWake 内置的知识引擎，管理数字员工的 Notebook（知识库）。与简单的 Memory 记忆系统不同，QMind 提供了完整的知识生命周期管理：绑定、提案、审计、编辑锁、幂等变更。

其设计理念借鉴了 Git 的 proposal → commit 模型：**任何知识变更都先经过提案和审计，再正式生效**。

## 数据模型（5 张核心表）

### 1. qmind_knowledge_bindings

Waker 与 Notebook 的绑定关系：

| 字段 | 说明 |
|------|------|
| agent_id | 数字员工 ID |
| notebook_id | 绑定的知识库 ID |
| binding_type | 绑定类型（读/写/管理） |

### 2. qmind_knowledge_action_proposals

知识变更提案（核心表）：

| 字段 | 说明 |
|------|------|
| type | 变更类型 |
| operation | 操作（create/update/delete） |
| evidence_json | 支撑证据（JSON 格式） |
| reason | 变更理由 |
| status | 状态（pending/approved/rejected/committed） |
| committed_at | 提交时间 |

### 3. qmind_knowledge_action_audits

知识操作审计日志：

| 字段 | 说明 |
|------|------|
| action | 操作动作 |
| status | 执行结果 |
| error_code | 失败原因码 |
| created_at | 记录时间 |

### 4. qmind_source_edit_sessions

OCC 编辑会话（乐观并发控制）：

| 字段 | 说明 |
|------|------|
| base_content_hash | 基准内容哈希（版本锁） |
| expires_at | 编辑锁过期时间 |
| editor_id | 编辑者 ID |

工作原理：
1. 开启编辑会话时记录当前内容 hash
2. 提交时对比 hash —— 若不一致说明有并发修改，拒绝提交
3. 编辑锁有超时机制防止死锁

### 5. qmind_knowledge_mutations

幂等变更记录：

| 字段 | 说明 |
|------|------|
| scope | 变更作用域 |
| idempotency_key | 幂等键（防重复执行） |
| input_hash | 输入内容哈希 |
| expires_at | 变更记录过期时间 |

## 知识变更流程

```
Agent 产出新知识
  ↓
创建 Proposal（附 evidence_json + reason）
  ↓
Audit 记录操作日志
  ↓
检查 OCC（base_content_hash 匹配？）
  ├─ 匹配 → 提交变更（status=committed）
  └─ 不匹配 → 拒绝（需基于最新版本重试）
  ↓
Mutation 记录（幂等键防重复）
  ↓
Knowledge 正式生效
```

## 设计亮点

1. **Evidence-driven**：每个知识变更必须携带证据（evidence_json），防止 LLM 幻觉污染知识库
2. **OCC 版本控制**：借鉴 [[occ-versioning]]，多 Agent 并发编辑知识时不丢数据
3. **审计链完整**：每次操作都有 audit 记录，可追溯任何知识的变更历史
4. **幂等保护**：idempotency_key 确保网络重试不会产生重复变更
5. **过期机制**：编辑锁和变更记录都有 TTL，防止资源泄漏

## 与其他记忆系统对比

| 维度 | QMind 知识引擎 | Waker Memory | Cloud Agents Memory Store |
|------|---------------|--------------|--------------------------|
| 定位 | 结构化知识管理 | 经验记忆沉淀 | 跨 Session KV 存储 |
| 变更控制 | Proposal + OCC | 直接写入 | 版本号控制 |
| 审计 | 完整审计链 | 无 | 无 |
| 并发 | OCC 编辑锁 | 无（单 Agent） | OCC（version 字段） |
| 持久性 | SQLite + Notebook | agent.sqlite | 云端持久化 |

## 交叉引用

- [[waker-memory]] — Waker 的经验记忆系统（与 QMind 互补）
- [[occ-versioning]] — Cloud Agents 中的 OCC 机制（QMind 借鉴此设计）
- [[memory-store]] — Cloud Agents 的 Memory Store API
- [[cli-memory-system]] — QoderCLI 的记忆系统（自动记忆 + AGENTS.md）
- [[desktop-knowledge-engine]] — Desktop 的知识引擎（Repo Wiki + 知识卡片）

## 来源

- ~/.qoderwake/data/store/qoderwake.sqlite（qmind_* 5 张表 schema） [reverse-engineering] 2026-06-30
- Output Style 文件中的记忆防幻觉规则 [reverse-engineering] 2026-06-30
