# 记忆 vs 文件

> Memory Store 和 Files API 的选型指南。

## 概述

Memory Store 和 Files API 都能为 Agent 提供持久化数据，但设计目的不同。Memory Store 面向跨 Session 的知识积累，Files API 面向单次任务的输入/输出。

## 核心差异

| 维度 | Memory Store | Files API |
|------|-------------|-----------|
| 设计目的 | 跨 Session 知识积累 | 单次任务输入/输出 |
| 生命周期 | 持久（直到删除） | 随平台存储策略 |
| 组织方式 | path 层级结构 | 扁平 file_id |
| 版本控制 | 有（OCC） | 无 |
| 关联方式 | `resources[]` (type: memory_store) | `resources[]` (type: file) |
| 沙箱路径 | `/data/.qoder/awareness/<path>` | 挂载到容器 |
| Agent 可写 | 是（通过 API） | 是（tool_output） |
| 下载 | 通过 API | 仅 tool_output/skill_output |

## 何时用 Memory Store

- Agent 需要记住跨 Session 的决策和知识
- 需要结构化组织（按项目、领域分目录）
- 需要版本追踪（谁改了什么）
- 多个 Session 共享同一份知识

**典型场景**：架构决策记录、项目规范、学到的教训、持续积累的知识库

## 何时用 Files API

- 为单次任务提供输入文件（代码、文档、数据）
- 获取 Agent 产出的文件（报告、生成的代码）
- 文件是一次性的，不需要跨 Session 复用

**典型场景**：上传待审查的代码文件、下载生成的报告、提供参考文档

## 组合使用

```bash
# Session 同时关联 Memory Store 和文件（⚠️ 2026-06-23 起统一使用 resources 数组）
curl -X POST https://api.qoder.com/api/v1/cloud/sessions \
  -d '{
    "agent": "agent_xxx",
    "environment_id": "env_xxx",
    "resources": [
      {"type": "memory_store", "memory_store_id": "memstore_xxx"},
      {"type": "file", "file_id": "file_xxx"}
    ]
  }'
```

## 决策流程

```
需要跨 Session 复用？ → Yes → Memory Store
                      → No → 需要下载产出？ → Yes → Files (tool_output)
                                            → No → Files (user_upload)
```

## 交叉引用

- [[memory-store]] — Memory Store 详细说明
- [[file]] — Files API 详细说明
- [[session]] — 两者在 Session 中的关联方式
- [[container-sandbox]] — 容器内的文件存储行为

## 来源

- raw/cloud-agents/memory-stores.md [official-docs] 2026-06-21
- raw/cloud-agents/files.md [official-docs] 2026-06-21
- raw/cloud-agents/sessions.md [official-docs] 2026-06-21
