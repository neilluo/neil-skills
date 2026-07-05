# Daemon 守护进程

> QoderWake 的核心常驻服务进程，提供 Web 控制台（端口 19820）、进程生命周期管理、云端 Gateway 桥接，将 QoderCLI 从命令行工具升级为 7×24 在线的平台服务。

## 概述

Daemon 是 QoderWake 的主进程，启动后以守护进程模式常驻运行。它承载了 Web Server、Session Manager、Trigger Scheduler、Channel 等所有平台级服务，并通过 spawn 子进程调用 QoderCLI 执行实际任务。

**一句话定位**：如果 QoderCLI 是发动机，Daemon 就是把它装进车里的底盘。

## 进程管理

### 生命周期命令

```bash
qoderwake start    # 启动 Daemon
qoderwake stop     # 停止 Daemon
qoderwake restart  # 重启 Daemon
qoderwake status   # 查看运行状态
```

### 运行时文件

位于 `~/.qoderwake/run/`：

| 文件 | 说明 |
|------|------|
| daemon.pid | 进程 PID |
| daemon.port | 监听端口（默认 19820） |
| daemon.lock | 进程锁（防多实例） |
| daemon.info.json | 完整运行信息（PID/port/version/uid） |
| daemon.workers.json | 活跃 Worker 注册表 |

### daemon.info.json 示例

```json
{
  "pid": 61599,
  "port": 19820,
  "version": "0.1.14",
  "uid": "unique-instance-id"
}
```

### daemon.workers.json 结构

```json
{
  "schemaVersion": 2,
  "workers": {
    "<session-id>": {
      "sessionId": "...",
      "pid": 12345,
      "pgid": 12345,
      "agentId": "...",
      "buildRegion": "...",
      "status": "active"
    }
  }
}
```

**关键发现**：存在特殊 Worker `__workflow_customizer__`（工作流定制器专用 Agent），说明 Daemon 为特定系统任务保留了专用 Worker 槽位。

## Web 控制台

### 地址

`http://127.0.0.1:19820`（默认，仅本地访问）

### API 端点

| 路径 | 方法 | 说明 |
|------|------|------|
| /api/agents | GET | 数字员工列表 |
| /api/sessions/<id>/events | GET | 会话事件列表 |
| /api/sessions/<id>/events/stream | GET | SSE 实时事件流 |
| /api/sessions/<id>/artifacts | GET | 会话产物 |
| /api/employee-templates | GET | 员工模板列表 |
| /api/skill-market | GET | 技能市场 |
| /api/settings/language | GET | 语言设置 |
| /api/feedback/meta | GET | 反馈元数据 |
| /api/internal/permissions/check | POST | 内部权限检查 |

### 云端桥接

Daemon 通过 MachineBridge 与远端 Gateway 建立双向连接：

```
Daemon → https://openapi.qoder.sh/api/v1/remote/machines/bridge（注册本机设备）
Cloud  → /api/v1/remote/employees（远端员工管理）
Cloud  → /api/v1/remote/sessions/query（远端会话查询）
```

## 配置

### 核心配置（config.json）

| 参数 | 默认值 | 说明 |
|------|--------|------|
| webPort | 19820 | Web 服务端口 |
| webHost | 127.0.0.1 | 监听地址 |
| heartbeatInterval | 30000ms | 心跳间隔 |
| sseReconnectInterval | 5000ms | SSE 重连间隔 |
| sseMaxReconnectAttempts | 10 | SSE 最大重连次数 |
| sessionCheckInterval | 60000ms | 会话状态检查间隔 |

### 系统设置（settings.json）

| 参数 | 说明 |
|------|------|
| system.launchAtLogin | 开机自启 |
| system.preventSleep | 运行时阻止休眠 |
| triggerQueue.maxGlobalActiveSessions | 全局最大并发（默认 20） |
| triggerQueue.maxActiveSessionsPerWorker | 单 Worker 最大并发（默认 5） |
| backup.preUpgrade.retentionCount | 升级前备份保留数（默认 5） |

### 上报配置

| 类型 | 间隔 | 说明 |
|------|------|------|
| reporter.telemetry | 30s | 遥测数据上报 |
| reporter.taskSync | 10s | 任务状态同步 |
| reporter.logCollector | 60s | 日志收集上报 |

## 内置定时任务

Daemon 自带 5 个系统级 Cron 任务：

| 任务 | 调度 | 说明 |
|------|------|------|
| session-timeout-check | `* * * * *` | 每分钟检查会话超时 |
| system-health-check | `*/5 * * * *` | 每 5 分钟健康检查 |
| session-cleanup | `0 0 * * *` | 每天清理过期会话 |
| qoderwake-memory-daily-maintenance | `0 3 * * *` | 每天 03:00 记忆维护 |
| qoderwake-agent-profile-summary | `0 2 * * *` | 每天 02:00 Agent 画像总结 |

## 技术栈

- **运行时**：Bun 1.3.14（非 Node.js）
- **前端**：Vite 构建的 Web UI
- **数据库**：SQLite（默认）/ PostgreSQL
- **二进制大小**：约 91 MB（Bun 单文件打包）
- **macOS 集成**：LaunchAgent `com.qoder.QoderWake`

## 交叉引用

- [[waker]] — Daemon 管理的数字员工实体
- [[waker-data-model]] — Daemon 使用的 70 张数据库表
- [[waker-hook-lifecycle]] — Daemon 注入 QoderCLI 的 Hook 链
- [[waker-trigger-plugins]] — Daemon 加载的触发器插件
- [[waker-plugin-system]] — Daemon 级与 Agent 级的双层插件
- [[session-lifecycle]] — Cloud Agents 的 Session 状态机（对比参考）

## 来源

- ~/.qoderwake/run/ 目录结构分析 [reverse-engineering] 2026-06-30
- ~/.qoderwake/config/ 配置文件分析 [reverse-engineering] 2026-06-30
- qoderwake status 命令输出 [verified-by-api] 2026-06-30
