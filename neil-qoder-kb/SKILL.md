---
name: qoder-cloud-agent-kb
description: "Qoder Cloud Agents 官方知识库（Karpathy LLM Wiki 架构）。基于三层架构（raw 原始镜像 → wiki LLM编译知识 → SCHEMA 维护规则）提供 Cloud Agents 平台的结构化知识，涵盖 Agent/Environment/Session/Tools/Events/Skills/Memory Stores/Managed Agents/Vaults/Deployments 等全部核心能力。知识库每日 22:00 自动从官网同步 raw 并触发 LLM Ingest 更新 wiki。查询 Qoder Cloud Agent 的 API、配置、概念或排障信息时使用。"
---

# Qoder Cloud Agents 知识库

基于 Karpathy LLM Wiki 理念构建的结构化知识库。

## 三层架构

```
raw/      → 不可变的原始文档镜像（从官网同步）
wiki/     → LLM 编译维护的结构化知识（交叉引用、综合分析）
SCHEMA.md → Wiki 维护规则（给 LLM 的操作手册）
```

## 使用方式（Query 操作）

1. 先读 `wiki/index.md` 定位相关页面
2. 读取 wiki/ 中的编译知识回答问题
3. 如果 wiki 不足，回退 raw/ 文件补充细节
4. 如果 raw/ 也没有，WebFetch 官网：https://docs.qoder.com/zh/cloud-agents/
5. 绝不猜测，找不到就说"不知道"
6. 有价值的新回答可回写到 wiki/（遵循 SCHEMA.md）

## Wiki 页面分类

| 目录 | 用途 | 示例 |
|------|------|------|
| `wiki/entities/` | 实体页（一个实体一个文件） | agent.md, session.md |
| `wiki/concepts/` | 概念页（跨实体通用机制） | occ-versioning.md |
| `wiki/guides/` | 操作指南（面向任务的 how-to） | quickstart.md |
| `wiki/comparisons/` | 对比分析 | tools-vs-skills.md |

## 维护操作

| 操作 | 触发方式 | 说明 |
|------|------|------|
| **Sync** | `scripts/sync-docs.sh`（crontab 22:00） | 拉取官网最新内容到 raw/ |
| **Ingest** | `scripts/ingest.sh [--full]` | qodercli 读 raw 更新 wiki |
| **Lint** | `scripts/ingest.sh --lint` | 健康检查（矛盾/孤立/缺页） |

## API 快速参考

- **Base URL**: `https://api.qoder.com/api/v1/cloud`
- **认证**: `Authorization: Bearer <PAT>`
- **分页**: 游标分页，`after_id` / `before_id`
- **并发控制**: 乐观锁 OCC，更新必须携带 `version`
