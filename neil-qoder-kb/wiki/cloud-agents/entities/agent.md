# Agent

> 可复用的 AI 代理配置模板，定义模型、系统提示词、工具集和技能。

## 概述

Agent 是 Qoder Cloud Agents 的核心配置单元，描述了 AI 代理的能力边界。一个 Agent 可被多个 Session 复用；修改 Agent 不影响已运行的 Session（Session 在创建时绑定 Agent 的特定版本）。

## 配置字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | — | 系统生成，`agent_` 前缀 + 32 字符十六进制 |
| `type` | string | — | 固定 `"agent"` |
| `name` | string | 是 | 名称（≤ 64 字符） |
| `description` | string | 否 | 描述，默认 `""` |
| `model` | string | 是 | 模型标识（如 `"ultimate"`） |
| `system` | string | 否 | 系统提示词 |
| `tools` | array | 否 | 工具列表，见 [[tools-vs-skills]] |
| `skills` | array | 否 | 关联的 Skill ID 列表 |
| `mcp_servers` | array | 否 | MCP 服务器配置 |
| `multiagent` | object | 否 | 多 Agent 协作配置，见 [[managed-agents-threading]] |
| `metadata` | object | 否 | 自定义键值对 |
| `version` | integer | — | 版本号，从 1 递增 |
| `archived` | boolean | — | 是否已归档 |
| `created_at` | string | — | 创建时间 |
| `updated_at` | string | — | 最后更新时间 |

## API 操作

| 操作 | 方法 | 路径 |
|------|------|------|
| 创建 | POST | `/api/v1/cloud/agents` |
| 获取 | GET | `/api/v1/cloud/agents/{id}` |
| 列表 | GET | `/api/v1/cloud/agents?limit=N` |
| 更新 | PUT | `/api/v1/cloud/agents/{id}` |

更新时必须携带当前 `version`，采用 [[occ-versioning]] 机制。

## 创建示例

```bash
curl -s -X POST https://api.qoder.com/api/v1/cloud/agents \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "code-reviewer",
    "model": "ultimate",
    "system": "你是代码审查专家。",
    "tools": [{"type": "agent_toolset_20260401", "enabled_tools": ["Bash", "Read", "Write"]}],
    "metadata": {"team": "backend"}
  }'
```

## 更新与版本控制

- 创建时 `version` 从 1 开始，每次成功更新自动 +1
- 缺少 `version` → 400 `invalid_request_error`
- `version` 不一致 → 409 `conflict_error`（需 GET 最新版本后重试）

## 最佳实践

1. **命名**：`团队-用途` 格式（如 `backend-code-review`）
2. **提示词**：写清角色、输出格式、限制条件
3. **最小工具集**：只配置任务所需的工具
4. **生产锁版本**：创建 Session 时用 `{"id": ..., "version": ...}` 形式

## 交叉引用

- [[session]] — Agent 绑定到 Session 执行
- [[environment]] — Session 运行的容器环境
- [[skill]] — Agent 可关联的领域技能
- [[occ-versioning]] — Agent 更新使用的并发控制
- [[managed-agents-threading]] — 多 Agent 协作模式

## 来源

- raw/cloud-agents/define-agent.md [official-docs] 2026-06-21
- raw/cloud-agents/overview.md [official-docs] 2026-06-21
- raw/cloud-agents/managed-agents.md [official-docs] 2026-06-21
