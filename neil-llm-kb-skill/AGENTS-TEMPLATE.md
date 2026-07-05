# AGENTS.md — {{PROJECT_NAME}} 知识库操作指南

> 本文件是给 AI coding agent 的操作手册。对齐 agents.md 开放标准。

## 项目概述
{{PROJECT_DESCRIPTION}}

采用 Karpathy LLM Wiki 三层架构：
- Schema 层 (SCHEMA.md) — 行为合约
- Wiki 层 (wiki/) — 预编译知识
- Raw 层 (raw/) — 不可变源

你的角色：wiki maintainer — 读 raw，维护 wiki，遵守 schema。

## 启动检查清单
每次新 session 启动时按顺序执行：
1. 读 wiki/index.md — 了解全貌
2. 读 wiki/log.md 最近 5 条 — 了解最近变更
3. 读 wiki/inbox.md — 检查 pending 待处理
4. 如有 pending → 提醒用户是否执行 Ingest

## 三大操作
> 执行前必须先读 SCHEMA.md 对应段落的完整定义。

### Ingest（源编译）
触发词：学习/蒸馏/投喂/ingest
流程：写入优先(inbox+log) → SHA256检测 → 2-Step CoT → 更新wiki → 确认落盘
写入优先红线：宁可多写一次"pending"，也不允许"读了但没落盘"。

### Query（知识检索）
流程：index定位 → 读wiki → 回退raw → 外部搜索 → 回写判定(含门禁)

### Lint（健康检查）
触发词：lint/检查/健康检查
6维：矛盾/过时/孤立/缺页/断链/空白

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
| raw/** | 不可变源层 |
| SCHEMA.md | 仅架构升级时修改 |
| AGENTS.md | 仅协议升级时修改 |
| references/** | 默认只读 |

## 写入约定
- 增量优先：追加新信息，不删旧
- 标注来源：[primary]/[derived]/[inferred] + URL + 日期
- 交叉引用：[[page-name]] 格式
- 命名：raw/ 文件 YYYYMMDD-slug.md
- 拆分阈值：单文件 >2500 行时拆分

## 错误恢复协议
当 Ingest 中途失败（session 断开/工具报错）：
1. 检查 inbox.md 中 pending/processing 状态条目
2. 检查 log.md 未关闭的 ⏳ 记录
3. 判断中断点：
   - 只写了 inbox → 从 SHA256 检测继续
   - 已蒸馏未更新 index → 从步骤 7 继续
   - 无法确定 → 标记 [failed] 通知用户
4. 恢复后正常关闭（inbox done + log 完成）

## 并发写入保护
设计为单 agent 单 session 操作：
1. 启动时检查 log.md 最近条目时间戳
2. 如发现非本 session 的最近变更 → 暂停写入，报告用户
3. 不允许多 agent 同时写入同一 wiki 文件
