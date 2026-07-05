# QoderCLI 内置 Cron 调度系统

> QoderCLI 内置的定时任务引擎，通过 CronCreate/CronDelete/CronList 三个 Agent 工具实现会话内定时调度，支持一次性和循环执行，最多 50 个并发任务。

## 概述

QoderCLI 1.0.16 内置了完整的 Cron 调度引擎（基于 Bun.cron 运行时），是 Agent 侧工具而非 CLI 子命令。Agent 可在对话中自主创建定时任务，实现定期执行特定操作。

**关键限制**：这不是 CLI 子命令（无法 `qodercli cron create`），而是 Agent 在对话中通过工具调用创建。

## 工具集

### CronCreate

创建定时任务：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| cron | string | ✅ | 标准 5 字段 cron 表达式（分 时 日 月 周），本地时间 |
| prompt | string | ✅ | 每次触发时入队的 prompt |
| recurring | boolean | ✅ | true=循环触发，false=一次性 |
| durable | boolean | ❌ | true=持久化到磁盘，false=仅会话内有效（默认） |

### CronDelete

删除指定定时任务（by task ID）。

### CronList

列出当前所有活跃的定时任务。

## 运行机制

```
用户/Agent 调用 CronCreate
  ↓
CronSchedulerManager 注册任务
  ↓
Bun.cron 运行时按表达式调度
  ↓
触发时通过 task-notification commandMode 入队
  ↓
Agent 以 "later" 优先级执行 prompt
```

## 约束与限制

| 约束 | 值 | 说明 |
|------|---|------|
| 最大并发任务 | 50 | 超过拒绝创建 |
| 循环任务有效期 | 7 天 | 自动过期，需重新创建 |
| durable=false | 进程退出即丢失 | 默认行为 |
| durable=true | 持久化到磁盘 | 跨会话保留 |
| 时间基准 | 本地时间 | 非 UTC |

## Cron 表达式格式

标准 5 字段格式：`分 时 日 月 周`

```
┌───────────── 分 (0-59)
│ ┌─────────── 时 (0-23)
│ │ ┌───────── 日 (1-31)
│ │ │ ┌─────── 月 (1-12)
│ │ │ │ ┌───── 周 (0-7, 0和7都是周日)
│ │ │ │ │
* * * * *
```

常用示例：
- `0 9 * * *` — 每天 09:00
- `30 12 * * *` — 每天 12:30
- `0 */4 * * *` — 每 4 小时
- `0 9 * * 1-5` — 工作日 09:00
- `0 9 * * 1` — 每周一 09:00

## 使用场景

| 场景 | cron 表达式 | prompt 示例 |
|------|-------------|-------------|
| 每日知识库维护 | `0 9 * * *` | "执行 sync-docs.sh 同步文档并 ingest 更新 wiki" |
| 每周回归测试 | `0 10 * * 1` | "运行 regression.py 生成本周回归报告" |
| 每 4 小时检查文档更新 | `0 */4 * * *` | "检查官网文档是否有更新，有则同步到 raw/" |
| 每日代码审计 | `0 18 * * 1-5` | "对今天的 git commits 执行代码审查" |

## 与外部调度器对比

| 维度 | CronCreate（内置） | macOS launchd | QoderWake Trigger |
|------|-------------------|---------------|-------------------|
| 持久性 | 7天自动过期 | 永久 | 永久 |
| 关机行为 | 丢失（durable=false）| 开机补执行 | 错过不补 |
| 配置方式 | Agent 对话 | plist XML | GUI 界面 |
| 执行上下文 | 当前 session | headless 新进程 | 完整 Agent 运行时 |
| 适合场景 | 临时性定时 | 系统级自动化 | 数字员工定时派活 |

## 交叉引用

- [[cli-session]] — Cron 触发的任务在 session 内执行
- [[cli-permission-model]] — 定时任务通常需 bypass_permissions 模式
- [[automated-trigger]] — QoderWake 的定时触发（更持久的方案）
- [[cli-goal-system]] — Goal 系统可与 Cron 配合实现自主目标追踪

## 来源

- QoderCLI 1.0.16 二进制逆向分析（CronSchedulerManager / CronCreate / CronDelete / CronList） [reverse-engineering] 2026-06-30
- Bun.cron 运行时文档 [cross-reference]
