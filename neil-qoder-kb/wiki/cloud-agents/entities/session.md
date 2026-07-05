# Session

> 将 Agent 与 Environment 组合在一起的有状态执行实例。

## 概述

Session 是实际执行任务的单元，将 Agent（配置）和 Environment（基础设施）绑定在一起。每个 Session 运行在隔离的容器沙箱中，支持多轮对话。同一 Agent 可同时关联多个活跃 Session。

## 生命周期状态机

| 状态 | 说明 | 可流转到 |
|------|------|------|
| `idle` | 空闲，等待用户消息 | `processing` |
| `processing` | Agent 执行中 | `canceling`, `idle` |
| `canceling` | 等待中断完成 | `idle` |
| `archived` | 已归档（终态） | — |

详见 [[session-lifecycle]]。

## 创建 Session

```bash
# 基本创建（绑定 Agent 最新版本）
curl -s -X POST https://api.qoder.com/api/v1/cloud/sessions \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{"agent": "agent_xxx", "environment_id": "env_xxx"}'

# 锁定 Agent 版本（生产推荐）
curl -s -X POST https://api.qoder.com/api/v1/cloud/sessions \
  -d '{"agent": {"id": "agent_xxx", "version": 2}, "environment_id": "env_xxx"}'
```

## 可附加资源

| 资源类型 | 请求字段 | 用途 |
|------|------|------|
| 文件 | `resources[]` (`type: "file"`) | 挂载已上传文件 |
| GitHub 仓库 | `resources[]` (`type: "github_repository"`) | 自动克隆仓库 |
| 记忆存储 | `resources[]` (`type: "memory_store"`) | 关联 [[memory-store]]（⚠️ 2026-06-23 起替代原 `memory_store_ids` 字段） |
| 密钥库 | `vault_ids` | 关联 [[vault]] 凭证 |

> **⚠️ Breaking Change (2026-06-23)**：Memory Store 不再支持顶层字段 `memory_store_ids`，必须通过 `resources` 数组传入：
> ```json
> "resources": [{"type": "memory_store", "memory_store_id": "memstore_xxx"}]
> ```
> 官网文档尚未更新，此结论来自 Qoder 研发团队确认 + curl 验证。

## 环境变量

通过 `environment_variables` 字段注入（分号分隔）：

```json
{"environment_variables": "NODE_ENV=production; FEATURE_FLAG=1"}
```

保留名称：`SERVER_ENDPOINT`、`USER_ID`、`WORK_DIR`，以及 `CAW_`、`QODER_` 前缀。

## 发送消息

```bash
curl -s -X POST "https://api.qoder.com/api/v1/cloud/sessions/sess_xxx/events" \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{"events": [{"type": "user.message", "content": [{"type": "text", "text": "分析代码。"}]}]}'
```

向 `processing` 状态发消息会返回 409 `conflict_error`。

## 取消执行

```bash
curl -s -X POST "https://api.qoder.com/api/v1/cloud/sessions/sess_xxx/cancel" \
  -H "Authorization: Bearer $QODER_PAT"
```

仅 `processing` 状态可取消，取消后回到 `idle` 可继续复用。

## Usage 统计

通过 `session.status_idle` 事件的 `usage` 字段获取：

| 字段 | 说明 |
|------|------|
| `usage.input_tokens` | 本轮输入 token |
| `usage.output_tokens` | 本轮输出 token |
| `usage.cache_read_input_tokens` | 缓存命中 token |
| `usage.cache_creation_input_tokens` | 写入缓存 token |

## 存储与生命周期

- 容器临时存储保留 24 小时
- Session 结束后容器及文件销毁
- 重要文件应通过 [[file]] API 持久化

## 交叉引用

- [[agent]] — Session 绑定的配置模板
- [[environment]] — Session 运行的容器环境
- [[event]] — Session 产生的实时事件流
- [[session-lifecycle]] — 状态机详细说明
- [[memory-store]] — 跨 Session 持久记忆
- [[vault]] — 注入到 Session 的凭证
- [[managed-agents-threading]] — 多 Agent 线程运行在 Session 内
- [[outcome-rubric]] — 定义 Session 执行的成功标准

## 来源

- raw/cloud-agents/sessions.md [official-docs] 2026-06-21
- raw/cloud-agents/overview.md [official-docs] 2026-06-21
