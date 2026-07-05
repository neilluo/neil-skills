# Waker Permission（权限模型）

> 控制 Waker 能做什么、不能做什么——工具防护、文件防护和内置工具策略三层安全机制。

## 概述

QoderWake 的权限模型通过三层防护机制（工具防护 + 文件防护 + 内置工具策略）确保数字员工在安全边界内运行。高危操作触发审批卡片，需用户明确允许或拒绝。

## 详细内容

### 工具防护

基于内置安全规则对工具参数做校验，命中高危规则后请求用户授权。

| 规则分类 | 检测内容 |
|----------|----------|
| **命令注入** | `rm`、`mv` 等危险操作 |
| **资源滥用** | fork 炸弹、系统重启等 |
| **代码执行** | `curl \| bash` 等远程执行 |
| **网络滥用** | 反弹 shell、本地回环访问 |
| **敏感文件访问** | 访问系统关键文件 |
| **权限提升** | `sudo` 等提权操作 |

### 文件防护

控制员工对本地文件的读写权限，可设定允许/禁止访问的路径范围。

### 内置工具策略

对 Waker 可用的内置工具设置三种策略：
- **允许**：无需确认直接执行
- **询问**：执行前弹出审批卡片
- **禁用**：完全不可使用

### 审批交互

当员工执行操作触发安全规则时，会弹出审批卡片让用户决定是否允许。这确保了自动执行场景下的人类监督。

## 深层实现（逆向分析）

### 完整安全链路

```
Agent 调用工具
  ↓
PreToolUse Hook 触发
  ↓
① qoderwake_permission_guard（305s 超时）
  ├─ 加载 Tool Guard 规则库（29条 regex）
  ├─ 匹配工具调用参数
  ├─ 检查 excludePatterns 白名单
  └─ 决策：放行 / 阻断 / 询问用户
  ↓
② qoderwake_change_tracker（5s）
  └─ 记录「准备做什么」
  ↓
工具执行
  ↓
PostToolUse Hook
  └─ 记录「实际做了什么」
```

### 三层防护叠加

| 层次 | 机制 | 来源 | 规则数 |
|------|------|------|--------|
| 1 | Tool Guard 规则引擎 | QoderWake 专有 | 29条 |
| 2 | Security Hook 脚本 | QoderCLI/Desktop 共享 | 8个脚本 |
| 3 | QoderCLI 权限模式 | CLI 底层 | 5种模式 |

QoderWake 中三层**叠加生效**：即使 CLI 处于 `auto` 模式，Tool Guard 仍可阻断 CRITICAL 级别操作。

### 内部权限检查 API

```
POST /api/internal/permissions/check
```

Daemon 内部权限检查端点，被 `qoderwake_permission_guard` Hook 调用。

### feature-config 相关开关

> ⚠️ 以下 key 从二进制字符串分析推断，本地 `~/.qoderwake/config/feature-config.json` 中未实际出现（可能为服务端远程下发）。标注为 [inferred]。

| Key | 说明 | 验证状态 |
|-----|------|----------|
| client.mcp.security.check | MCP 调用安全检查 | [inferred] |
| client.agent.terminal.sandbox.enable | 终端沙箱模式 | [inferred] |

## 交叉引用

- [[waker]] — 权限模型的绑定对象
- [[waker-tool-guard]] — 29条 Tool Guard 安全规则引擎详情
- [[waker-hook-lifecycle]] — permission_guard Hook 在生命周期中的位置
- [[desktop-security-audit]] — Desktop/CLI 的 common.sh 安全审计（叠加层）
- [[permission-model]] — Cloud Agents 中的权限策略模型（allow/ask/deny）
- [[cli-permission-model]] — QoderCLI 的 5 种权限模式（底层引擎）
- [[waker-config-guide]] — 权限配置实践指南
- [[automated-trigger]] — 自动任务场景下的权限控制

## 来源

- raw/qoderwake/manage-wakers.md [official-docs] 2026-06-28
- ~/.qoderwake/resources/security/tool-guard-rules/dangerous_shell_commands.json [reverse-engineering] 2026-06-30
- ~/.qoderwake/data/workers/<id>/.qoder-plugin/hooks/hooks.json [reverse-engineering] 2026-06-30
- ~/.qoderwake/config/feature-config.json [reverse-engineering] 2026-06-30
