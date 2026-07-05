# AGENTS.md — Qoder Cloud Agents 知识库操作指南

> 本文件是给 AI coding agent 的操作手册。基于 Karpathy LLM Wiki 三层架构。

## 项目概述

Qoder Cloud Agents 官方知识库，采用三层架构：
- Schema 层 (SCHEMA.md) — wiki 维护规则
- Wiki 层 (wiki/) — LLM 编译维护的结构化知识
- Raw 层 (raw/) — 从官网同步的不可变文档镜像

你的角色：wiki maintainer — 读 raw，维护 wiki，遵守 schema。

## 启动检查清单

每次新 session 启动时按顺序执行：
1. 读 `wiki/index.md` — 了解 wiki 全貌
2. 读 `wiki/log.md` 最近 5 条 — 了解最近变更
3. 读 `wiki/inbox.md` — 检查 pending 待处理
4. 如有 pending → 提醒用户是否执行 Ingest

## 三大操作

> 执行前必须先读 SCHEMA.md 对应段落的完整定义。

### Ingest（源编译）
触发条件：sync-docs.sh 检测到 raw/ 变化 或 手动触发
流程：
1. 写入优先：inbox.md 登记 pending + log.md 追加 ⏳（不可违反）
2. SHA256 对比：跳过未变更文件
3. 2-Step CoT：先分析变化内容，再更新 wiki 页面
4. 维护 [[wikilink]] 交叉引用
5. 更新 index.md + inbox done + log 完成

### Query（知识检索）
流程：
1. 读 wiki/index.md 定位
2. 读 wiki 页面回答
3. 不足则回退 raw/
4. 仍不足则 WebFetch 官网
5. 回写判定（含门禁：必须有来源，纯推理标 [inferred]）

### Lint（健康检查）
触发词：lint / 检查 / 健康检查
6维：矛盾(P0) / 过时(P1) / 孤立(P2) / 缺页(P1) / 断链(P1) / 空白(P2)

## 文件操作权限

### 可修改
| 路径 | 场景 |
|------|------|
| wiki/**/*.md | Ingest/Query回写/Lint修复 |
| wiki/index.md | 每次Ingest后 |
| wiki/inbox.md | 登记来源/更新状态 |
| wiki/log.md | 每次操作后追加 |

### 只读（不可修改）
| 路径 | 原因 |
|------|------|
| raw/** | 不可变源层（sync-docs.sh 维护） |
| SCHEMA.md | 仅架构升级时修改 |
| AGENTS.md | 仅协议升级时修改 |
| SKILL.md | Skill 定义，不常改 |

## 写入约定
- 增量优先：追加新信息，不删旧
- 标注来源：[official-docs] / [verified-by-api] / [user-reported] + 日期
- 交叉引用：[[page-name]] 格式
- [[wikilink]] 规则：page-name 为文件名（不含 .md 和目录前缀）

## 错误恢复协议

当 Ingest 中途失败：
1. 检查 inbox.md 中 pending/processing 状态条目
2. 检查 log.md 未关闭的 ⏳ 记录
3. 判断中断点：
   - 只写了 inbox → 从 SHA256 检测继续
   - 已蒸馏未更新 index → 从步骤 4 继续
   - 无法确定 → 标记 [failed] 通知用户
4. 恢复后正常关闭

## 并发写入保护

设计为单 agent 单 session 操作：
1. 启动时检查 log.md 最近条目时间戳
2. 如发现非本 session 的最近变更 → 暂停写入，报告用户
3. 不允许多 agent 同时写入同一 wiki 文件
