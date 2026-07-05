# 日志与可观测性

> QoderWake 的 6 层日志体系和可观测性架构，包含主日志、生命周期日志、对话链路 JSONL trace、崩溃日志，支持 traceId 级查询和遥测上报。

## 概述

QoderWake 在 `~/.qoderwake/logs/` 下维护 6 个独立日志文件，覆盖从应用运行到对话链路的全栈可观测性。配合 `qoderwake log` 命令和 traceId 机制，实现了从 UI 操作到 LLM 调用的端到端追踪。

## 日志文件体系

| 文件 | 用途 | 格式 |
|------|------|------|
| qoderwake.log | 主日志（全部事件） | 文本 |
| qoderwake_lifecycle.log | 生命周期事件（启停/版本/硬件） | 结构化文本 |
| conversation-trace.log | 对话链路追踪 | JSONL |
| qoderwake.crash.log | 崩溃日志 | 文本 |
| qoderwake.crash.err.log | 崩溃 stderr | 文本 |
| qoderwake-menubar.log | macOS 菜单栏进程日志 | 文本 |

## 日志详解

### 主日志（qoderwake.log）

全量事件日志，配置：
- `maxFileSize`: 100MB
- `maxTotalSize`: 2048MB（约 2GB）
- 自动轮转

### 生命周期日志（qoderwake_lifecycle.log）

记录系统级事件：
- Daemon 启停
- 版本升级
- 硬件信息
- Worker 创建/销毁

格式：`[时间戳] [LEVEL] [trace=xxx] [模块] 键: 值`

### 对话链路 JSONL（conversation-trace.log）

结构化 JSONL 格式，每行一个事件：

```json
{
  "event": "console.submit.received",
  "trace": "abc123",
  "request_set_id": "...",
  "sse_stream_id": "...",
  "timestamp": "..."
}
```

记录的事件类型：
- `console.submit.received` — 用户提交消息
- `worker.event.routed` — 事件路由到 Worker
- `session.created` / `session.completed`
- 工具调用、LLM 响应等

开关：`config.json` 中 `log.conversationTrace.enabled`

### 崩溃日志

- `qoderwake.crash.log`：崩溃时的 stdout 捕获
- `qoderwake.crash.err.log`：崩溃时的 stderr 捕获
- 用于 post-mortem 分析

## TraceId 机制

每条日志带 `trace=` 字段，支持 traceId 级查询：

```bash
qoderwake log <traceId>         # 按 traceId 查询
qoderwake log -f                # 跟随模式（实时）
```

traceId 贯穿整个调用链：
```
用户操作 → Daemon 接收 → Session 创建 → Worker spawn → QoderCLI 执行 → LLM 调用
    ↑ 同一个 traceId 贯穿全链路
```

## 遥测与上报

三类后台上报任务：

| 类型 | 间隔 | 说明 |
|------|------|------|
| reporter.telemetry | 30s | 遥测数据（运行指标） |
| reporter.taskSync | 10s | 任务状态同步到云端 |
| reporter.logCollector | 60s | 日志采集上报 |

上报可通过 `config.json` 中 `telemetry` 字段控制开关。

## 日志清理策略

配置在 `config.sample.json`：

```json
{
  "triggerRunRetention": {
    "sweepIntervalHours": 6,
    "defaultRetentionDays": 14,
    "failedRetentionDays": 30,
    "vacuumOnSweep": true
  }
}
```

- 成功记录：保留 14 天
- 失败记录：保留 30 天
- 每 6 小时清理一次
- 清理后执行 SQLite VACUUM

## Feature Config 开关

`feature-config.json` 中与可观测性相关的开关：

| Key | 说明 |
|-----|------|
| conversationTrace.enabled | 对话 trace 日志开关 |
| observability.workerError.enabled | Worker 错误埋点 |

## 交叉引用

- [[waker-daemon]] — Daemon 进程的配置和运行时
- [[waker-data-model]] — session_events 等可观测性相关表
- [[sse-event-stream]] — Cloud Agents 的 SSE 事件流（对比参考）
- [[waker-hook-lifecycle]] — Hook 执行的 trace 记录

## 来源

- ~/.qoderwake/logs/ 目录结构 [reverse-engineering] 2026-06-30
- ~/.qoderwake/config/config.sample.json [reverse-engineering] 2026-06-30
- ~/.qoderwake/config/feature-config.json [reverse-engineering] 2026-06-30
