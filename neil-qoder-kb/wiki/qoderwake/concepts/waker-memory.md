# Waker Memory（记忆系统）

> Waker 的长期记忆机制——通过自动沉淀、手动写入和系统整理积累对用户和项目的认知。

## 概述

每个 Waker 拥有独立的长期记忆系统，用于积累对用户偏好和项目知识的认知。记忆存储在本地（不上传云端），支持浏览、搜索和编辑。记忆分为员工个人记忆和项目记忆两个层次。

## 详细内容

### 记忆来源

| 来源 | 说明 |
|------|------|
| **自动沉淀** | 对话过程中员工认为值得记住的信息自动写入 |
| **手动写入** | 用户进入记忆页直接编辑 |
| **系统整理** | 定期由系统帮员工梳理和去重 |

### 记忆层次

- **员工个人记忆**：跟随 Waker，跨项目通用
- **项目记忆**：绑定在项目上，独立于员工个人记忆

### 管理操作

进入 **员工详情 → 记忆**：
- 浏览所有记忆条目
- 搜索特定记忆
- 编辑/删除记忆内容

### 存储特性

- **本地存储**：记忆数据保存在本机，不上传云端
- **持久化**：跨会话保持，Waker 重启后仍在
- **越用越懂**：记忆不断沉淀，员工越来越了解用户习惯和项目上下文

## 深层实现（逆向分析）

### 存储架构

记忆数据通过多层存储：
- **Markdown 文件**：`~/.qoderwake/data/workers/<agent-id>/.qoder/memory/` — Agent 运行时读写的记忆文本
- **时间线事件**：`~/.qoderwake/data/store/qoderwake.sqlite` 中的 `memory_timeline_events` 表 — 记录记忆变更的审计日志
- **RAG 索引**（非记忆本身）：`~/.qoderwake/data/workers/<agent-id>/.qoder/indexes/agent.sqlite` — 代码/文件的向量索引库（chunks + embeddings）

### 内置 MCP 服务

记忆系统通过内置 MCP `qoderwake_memory` 暴露给 Agent：

| MCP 工具 | 功能 |
|----------|------|
| memory_search | 搜索记忆 |
| memory_add | 添加记忆 |
| memory_update | 更新记忆 |
| memory_remove | 删除记忆 |

MCP 端点：`http://127.0.0.1:19820/api/internal/builtin-mcp/qoderwake_memory/sse`
认证：`x-qoderwake-builtin-mcp-token` header

### 记忆分层

| scope | target | 说明 |
|-------|--------|------|
| agent | long_term | 员工全局长期记忆 |
| agent | daily | 每日工作总结 |
| agent | topic | 主题级记忆 |
| project | long_term | 项目级长期记忆 |
| project | daily | 项目每日总结 |

优先级：project > agent（项目记忆优先于个人记忆）

### 运维命令

```bash
qoderwake memory show <waker-id>                  # 查看记忆
qoderwake memory dream <waker-id>                 # 梦境复盘（知识整理）
qoderwake memory snapshot <waker-id>              # 创建快照
qoderwake memory versions <waker-id>              # 版本历史
qoderwake memory diff <v1> <v2>                   # 版本对比
qoderwake memory rollback <waker-id> <version>    # 回滚到指定版本
qoderwake memory export <waker-id>                # 导出
qoderwake memory import <waker-id> <file>         # 导入
```

### 自动化维护

Daemon 内置两个记忆相关 Cron 任务：
- **每天 02:00**：`qoderwake-agent-profile-summary-<agent-id>` — 按 Agent 注册，自动总结该 Agent 画像（`AgentProfileSummarizer` 组件）
- **每天 03:00**：`qoderwake-memory-daily-maintenance` (cron: `0 3 * * *`) — 全局记忆整理、去重、过期清理

### feature-config 相关开关

> ⚠️ 以下 key 从二进制字符串分析推断，本地 `~/.qoderwake/config/feature-config.json` 中未实际出现（可能为服务端远程下发）。标注为 [inferred]。

| Key | 说明 | 验证状态 |
|-----|------|----------|
| client.memory.network.enable | 网络记忆同步 | [inferred] |
| client.memory.skill.save.enable | Skill 执行记忆保存 | [inferred] |
| client.memory.task.summary.experience.extract.enable | 任务经验提取 | [inferred] |

### Hook 集成

记忆系统通过两个 Hook 节点集成到工作流：
- **SessionStart**：加载相关记忆到 context
- **PostCompact**（async）：压缩后将重要信息沉淀为长期记忆

## 交叉引用

- [[waker]] — 记忆系统的宿主实体
- [[memory-store]] — Cloud Agents 中的持久记忆仓库（云端方案）
- [[waker-config-guide]] — 记忆配置实践
- [[cloud-agents-vs-qoderwake]] — 本地记忆 vs 云端 Memory Store 对比
- [[qmind-knowledge]] — QMind 知识引擎（与记忆系统互补）
- [[waker-hook-lifecycle]] — 记忆 Hook 在生命周期中的位置
- [[waker-data-model]] — 底层数据库结构
- [[cli-memory-system]] — QoderCLI 的记忆系统（对比参考）

## 来源

- raw/qoderwake/manage-wakers.md [official-docs] 2026-06-28
- ~/.qoderwake/data/workers/<id>/.qoder-plugin/.mcp.json [reverse-engineering] 2026-06-30
- ~/.qoderwake/data/workers/<id>/.qoder-plugin/hooks/hooks.json [reverse-engineering] 2026-06-30
- ~/.qoderwake/config/feature-config.json [reverse-engineering] 2026-06-30
