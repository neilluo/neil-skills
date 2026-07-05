# 回归测试报告 — 2026-06-28 10:47

> 阈值: 85% | 用例数: 10 | 语料: 34,296 字符

## 总览

- **整体命中率**: 100.0%
- **PASS**: 10/10
- **FAIL**: 0/10

## 用例矩阵

| ID | 模式 | 标题 | 命中/总数 | 命中率 | 状态 |
| --- | --- | --- | --- | --- | --- |
| T01 | entity | Agent 配置与版本控制 | 7/7 | 100% | ✅ PASS |
| T02 | entity | Session 生命周期 | 6/6 | 100% | ✅ PASS |
| T03 | concept | SSE 事件流 | 6/6 | 100% | ✅ PASS |
| T04 | entity | Memory Store 持久记忆 | 5/5 | 100% | ✅ PASS |
| T05 | concept | 权限模型 | 5/5 | 100% | ✅ PASS |
| T06 | concept | 多 Agent 协作 | 5/5 | 100% | ✅ PASS |
| T07 | concept | 容器沙箱 | 4/4 | 100% | ✅ PASS |
| T08 | entity | Vault 密钥管理 | 3/3 | 100% | ✅ PASS |
| T09 | entity | 文件操作 | 3/3 | 100% | ✅ PASS |
| T10 | guide | 快速入门与排障 | 4/4 | 100% | ✅ PASS |

## 详细明细

### T01 — Agent 配置与版本控制 [PASS]

| 关键词 | 命中 |
| --- | --- |
| `agent` | ✅ |
| `model` | ✅ |
| `system` | ✅ |
| `tools` | ✅ |
| `version` | ✅ |
| `occ` | ✅ |
| `409` | ✅ |

### T02 — Session 生命周期 [PASS]

| 关键词 | 命中 |
| --- | --- |
| `session` | ✅ |
| `idle` | ✅ |
| `processing` | ✅ |
| `canceling` | ✅ |
| `archived` | ✅ |
| `environment` | ✅ |

### T03 — SSE 事件流 [PASS]

| 关键词 | 命中 |
| --- | --- |
| `event` | ✅ |
| `sse` | ✅ |
| `user.message` | ✅ |
| `agent.message` | ✅ |
| `tool_use` | ✅ |
| `tool_result` | ✅ |

### T04 — Memory Store 持久记忆 [PASS]

| 关键词 | 命中 |
| --- | --- |
| `memory` | ✅ |
| `store` | ✅ |
| `entry` | ✅ |
| `version` | ✅ |
| `persist` | ✅ |

### T05 — 权限模型 [PASS]

| 关键词 | 命中 |
| --- | --- |
| `permission` | ✅ |
| `allow` | ✅ |
| `ask` | ✅ |
| `deny` | ✅ |
| `tool` | ✅ |

### T06 — 多 Agent 协作 [PASS]

| 关键词 | 命中 |
| --- | --- |
| `managed` | ✅ |
| `coordinator` | ✅ |
| `child` | ✅ |
| `thread` | ✅ |
| `multiagent` | ✅ |

### T07 — 容器沙箱 [PASS]

| 关键词 | 命中 |
| --- | --- |
| `container` | ✅ |
| `sandbox` | ✅ |
| `environment` | ✅ |
| `resource` | ✅ |

### T08 — Vault 密钥管理 [PASS]

| 关键词 | 命中 |
| --- | --- |
| `vault` | ✅ |
| `secret` | ✅ |
| `credential` | ✅ |

### T09 — 文件操作 [PASS]

| 关键词 | 命中 |
| --- | --- |
| `file` | ✅ |
| `upload` | ✅ |
| `download` | ✅ |

### T10 — 快速入门与排障 [PASS]

| 关键词 | 命中 |
| --- | --- |
| `quickstart` | ✅ |
| `troubleshoot` | ✅ |
| `production` | ✅ |
| `checklist` | ✅ |
