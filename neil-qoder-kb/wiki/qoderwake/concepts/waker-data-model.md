# QoderWake 数据模型参考

> QoderWake SQLite 数据库的 70 张表完整索引，揭示了数字员工平台的内部数据架构，涵盖核心领域、知识管理、工作流、团队协作、验证评审等 8 大模块。

## 概述

QoderWake 使用 SQLite（默认）或 PostgreSQL 作为统一数据存储，位于 `~/.qoderwake/data/store/qoderwake.sqlite`。70 张表按功能分为 8 大模块，反映了平台的完整内部架构。

## 核心领域（Core）

| 表名 | 职责 | 关键字段 |
|------|------|----------|
| agents | 数字员工注册 | employee_id, staff_id, workspace, last_conversation_at |
| sessions | 会话管理 | trigger_id, run_id, channel_id, conversation_id, current_trace_id |
| connectors | MCP 连接器 | 类型、配置、状态 |
| skills | 技能注册 | 名称、版本、来源 |
| projects | 项目绑定 | 路径、配置 |
| project_usages | 项目使用记录 | agent_id, project_id, last_used |
| mcps | MCP 服务器 | URL、认证、工具列表 |

## 调度引擎（Triggers）

| 表名 | 职责 | 关键字段 |
|------|------|----------|
| triggers | 触发器定义 | trigger_kind, source_kind, pull_mode, workflow_kind, execution_target, credits_this_month, max_runs, end_date |
| trigger_runs | 触发执行记录 | 状态、时间、结果 |
| tasks | 任务队列 | dispatch_mode(direct/queued), dedupe_key(UNIQUE), ingestion_run_id |
| trigger_work_item_states | 工作项扫描状态 | 外部系统对接 |

**设计亮点**：
- `credits_this_month` / `credits_month`：月度配额机制
- `dedupe_key`：UNIQUE 约束实现幂等去重
- `dispatch_mode`：direct（立即）/ queued（排队）

## 任务编排（Missions）

| 表名 | 职责 | 关键字段 |
|------|------|----------|
| missions | 高层任务 | 目标、状态、优先级 |
| plan_tasks | 计划任务 | 依赖关系、执行顺序 |
| role_runs | 角色执行 | 角色类型、执行结果 |

## 工作流引擎（Workflow）

| 表名 | 职责 | 关键字段 |
|------|------|----------|
| workflow_definitions | 工作流定义 | script_content, script_digest, meta_json, generation_session_id |
| workflow_runs | 工作流执行 | current_phase, retry_source_run_id, parent_run_id, trigger_source |
| workflow_events | 工作流事件 | 事件类型、时间戳 |
| workflow_pending_confirmations | 待确认节点 | 人工审批点 |
| workflow_run_locks | 执行锁 | 并发控制 |
| workflow_definition_versions | 版本管理 | 脚本版本历史 |
| workflow_worker_cache | Worker 缓存 | 执行上下文缓存 |

**设计亮点**：
- `parent_run_id`：支持嵌套工作流运行
- `retry_source_run_id`：重试关联源运行
- `generation_session_id`：记录哪个 session 生成了此工作流

## QMind 知识管理

| 表名 | 职责 | 关键字段 |
|------|------|----------|
| qmind_knowledge_bindings | Waker↔Notebook 绑定 | agent_id, notebook_id |
| qmind_knowledge_action_proposals | 知识变更提案 | type, operation, evidence_json, status |
| qmind_knowledge_action_audits | 操作审计 | action, status, error_code |
| qmind_source_edit_sessions | OCC 编辑会话 | base_content_hash, expires_at |
| qmind_knowledge_mutations | 幂等变更 | idempotency_key, input_hash |

详见 [[qmind-knowledge]]。

## 团队协作（Team Groups V3）

| 表名 | 职责 |
|------|------|
| team_groups_v3 | 团队小组 |
| team_group_members_v3 | 小组成员 |
| team_group_conversations_v3 | 小组对话 |
| team_group_messages_v3 | 小组消息 |
| team_group_activities_v3 | 活动记录 |
| team_group_append_routings_v3 | 追加路由 |
| team_group_mission_links_v3 | 任务链接 |
| team_mailbox_items | 团队邮箱 |

## 人机交互与验证

| 表名 | 职责 |
|------|------|
| user_confirmations | 用户确认请求 |
| human_action_projection | 人工操作投影 |
| board_task_projection | 看板投影 |
| verification_findings | 验证发现 |
| evidence | 证据链 |
| leader_review_requests | Leader 评审请求 |
| leader_model_invocations | Leader 模型调用 |
| leader_sdk_messages | Leader SDK 消息 |

## 基础设施

| 表名 | 职责 |
|------|------|
| work_items | 外部工作项 |
| work_item_comments | 工作项评论 |
| work_item_events | 工作项事件 |
| storage_records | KV 存储 |
| storage_logs | 存储日志 |
| channel_pairings | IM 渠道绑定 |
| channel_pending_pairings | 待绑定 |
| context_artifacts | 会话产物 |
| session_events | 会话事件 |
| event_delivery_outbox | 事件投递外发 |
| data_migration_state | 数据迁移状态 |

## 存储后端切换

```json
// settings.json
{
  "storage": "sqlite",           // 默认
  "externalDb": {
    "type": "postgresql",
    "connectionPoolSize": 10
  }
}
```

切换命令：`qoderwake storage migrate`

## 交叉引用

- [[waker]] — 数字员工实体（对应 agents 表）
- [[qmind-knowledge]] — QMind 知识引擎详解
- [[automated-trigger]] — 触发器系统（对应 triggers/tasks 表）
- [[waker-memory]] — 记忆系统（独立 agent.sqlite）
- [[occ-versioning]] — OCC 机制在多处表中的应用

## 来源

- ~/.qoderwake/data/store/qoderwake.sqlite (sqlite3 .schema) [reverse-engineering] 2026-06-30
- ~/.qoderwake/config/settings.sample.json [reverse-engineering] 2026-06-30
