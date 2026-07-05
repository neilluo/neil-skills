# 回归测试报告 — 2026-06-28 14:25

> 阈值: 85% | 用例数: 20 | 语料: 53,785 字符

## 总览

- **整体命中率**: 100.0%
- **PASS**: 20/20
- **FAIL**: 0/20

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
| T11 | entity | Waker 数字员工 | 6/6 | 100% | ✅ PASS |
| T12 | entity | 角色模板 | 6/6 | 100% | ✅ PASS |
| T13 | concept | 对话任务 | 6/6 | 100% | ✅ PASS |
| T14 | concept | 自动触发机制 | 6/6 | 100% | ✅ PASS |
| T15 | entity | 群组任务 | 6/6 | 100% | ✅ PASS |
| T16 | concept | Waker 权限模型 | 5/5 | 100% | ✅ PASS |
| T17 | concept | Waker 记忆系统 | 5/5 | 100% | ✅ PASS |
| T18 | entity | 连接器 | 4/4 | 100% | ✅ PASS |
| T19 | guide | QoderWake 安装部署 | 5/5 | 100% | ✅ PASS |
| T20 | comparison | Cloud Agents vs QoderWake 选型 | 6/6 | 100% | ✅ PASS |

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

### T11 — Waker 数字员工 [PASS]

| 关键词 | 命中 |
| --- | --- |
| `waker` | ✅ |
| `数字员工` | ✅ |
| `创建` | ✅ |
| `角色` | ✅ |
| `控制台` | ✅ |
| `19820` | ✅ |

### T12 — 角色模板 [PASS]

| 关键词 | 命中 |
| --- | --- |
| `role` | ✅ |
| `后端工程师` | ✅ |
| `前端工程师` | ✅ |
| `测试工程师` | ✅ |
| `产品经理` | ✅ |
| `自定义` | ✅ |

### T13 — 对话任务 [PASS]

| 关键词 | 命中 |
| --- | --- |
| `对话` | ✅ |
| `追问` | ✅ |
| `审批` | ✅ |
| `切换` | ✅ |
| `模型` | ✅ |
| `产物` | ✅ |

### T14 — 自动触发机制 [PASS]

| 关键词 | 命中 |
| --- | --- |
| `定时` | ✅ |
| `事件` | ✅ |
| `API` | ✅ |
| `PAT` | ✅ |
| `invoke` | ✅ |
| `触发` | ✅ |

### T15 — 群组任务 [PASS]

| 关键词 | 命中 |
| --- | --- |
| `群组` | ✅ |
| `Leader` | ✅ |
| `成员` | ✅ |
| `协作` | ✅ |
| `拆解` | ✅ |
| `汇总` | ✅ |

### T16 — Waker 权限模型 [PASS]

| 关键词 | 命中 |
| --- | --- |
| `工具防护` | ✅ |
| `文件防护` | ✅ |
| `命令注入` | ✅ |
| `权限提升` | ✅ |
| `审批` | ✅ |

### T17 — Waker 记忆系统 [PASS]

| 关键词 | 命中 |
| --- | --- |
| `记忆` | ✅ |
| `自动沉淀` | ✅ |
| `手动` | ✅ |
| `本地` | ✅ |
| `长期` | ✅ |

### T18 — 连接器 [PASS]

| 关键词 | 命中 |
| --- | --- |
| `连接器` | ✅ |
| `GitHub` | ✅ |
| `Jira` | ✅ |
| `外部` | ✅ |

### T19 — QoderWake 安装部署 [PASS]

| 关键词 | 命中 |
| --- | --- |
| `安装` | ✅ |
| `macOS` | ✅ |
| `Linux` | ✅ |
| `curl` | ✅ |
| `install.sh` | ✅ |

### T20 — Cloud Agents vs QoderWake 选型 [PASS]

| 关键词 | 命中 |
| --- | --- |
| `cloud` | ✅ |
| `本地` | ✅ |
| `waker` | ✅ |
| `session` | ✅ |
| `API` | ✅ |
| `GUI` | ✅ |
