# 触发器插件架构

> QoderWake 触发器系统的插件化实现，通过标准化的 `qoderwake.plugin.v1` Schema 定义事件源，内置 Aone 工单、钉钉消息、GitHub Webhook 三种触发器插件。

## 概述

触发器插件是 QoderWake 让数字员工「主动接活」的核心机制。每个插件定义一种事件源（Event Source），通过 Polling 或 Webhook 方式拉取外部事件，转化为 Session 任务分派给 Waker 执行。

插件目录：`~/.qoderwake/resources/plugins/trigger-event-sources/`

## 插件总览

| 插件 | Kind | 类型 | 运行时 | 默认调度 |
|------|------|------|--------|----------|
| **Aone** | `a1-workitem` | Polling (Python) | `a1_workitem.py` | 10 分钟 |
| **DingTalk** | `dingtalk-chat` | Polling (Python) | `dws_chat_message.py` | 1 分钟 |
| **GitHub** | `github_hook` | Webhook (TypeScript) | `github-hook.ts` | 实时推送 |

## 插件 Schema：qoderwake.plugin.v1

每个插件包含 `qoderwake-plugin.json`，标准结构：

```json
{
  "schema": "qoderwake.plugin.v1",
  "name": "插件名",
  "version": "1.0.x",
  "description": "...",
  "forceUpgrade": true,
  "eventSources": [
    {
      "kind": "事件类型",
      "displayName": "展示名",
      "schedule": { "defaultInterval": "10m" },
      "backoff": { "strategy": "exponential", "multiplier": 2, "maxInterval": "120m" },
      "setup": { "requirements": [...], "actions": [...] },
      "formSchema": { ... },
      "uiSchema": { ... }
    }
  ]
}
```

## 插件详解

### 1. Aone 工单插件（a1-workitem）

**功能**：监控阿里 Aone 工单系统，检测新工单或工单状态变化，自动触发数字员工接单。

| 配置项 | 值 | 说明 |
|--------|---|------|
| 拉取脚本 | `triggers/a1_workitem.py` | Python 轮询 |
| 超时 | 120s | 单次拉取超时 |
| 默认间隔 | 10 分钟 | 轮询频率 |
| 退避策略 | exponential × 2 | 失败后指数退避 |
| 最大间隔 | 120 分钟 | 退避上限 |

**前置依赖链**（setup）：
1. `a1-cli` 是否已安装 → 未安装则执行 `npm install -g @ali/aone-kit`
2. `a1 login` 是否已登录 → 未登录则引导用户登录

**高级配置**（官方文档未提及）：
- 支持 `tags` 标签过滤（仅处理带特定标签的工单）
- 支持 `@assignee` 分配人过滤
- 支持 `watchComments` 评论监听
- 支持状态过滤（仅特定状态变化触发）

### 2. 钉钉消息插件（dingtalk-chat）

**功能**：监听钉钉群/单聊消息，当用户 @数字员工时自动触发任务。

| 配置项 | 值 | 说明 |
|--------|---|------|
| 拉取脚本 | `triggers/dws_chat_message.py` | Python 轮询 |
| 超时 | 120s | 单次拉取超时 |
| 默认间隔 | 1 分钟 | 高频轮询 |
| 退避策略 | exponential × 2 | 失败后退避 |
| 最大间隔 | 10 分钟 | 退避上限 |
| visibility | hidden | 内部自动创建，不在 UI 展示 |

**关键设计**：
- 依赖 `dws` CLI v1.0.39（由 Daemon 自动管理版本）
- 含 sha256 校验确保 CLI 完整性
- `@mention` 检测：仅处理 @ 到当前 Waker 的消息
- `visibility: "hidden"`：此触发器由系统自动创建，用户无需手动配置

### 3. GitHub Webhook 插件（github_hook）

**功能**：接收 GitHub Webhook 推送，响应 Issue/PR/评论等事件。

| 配置项 | 值 | 说明 |
|--------|---|------|
| 运行时 | TypeScript (`src/github-hook.ts`) | 非 Python |
| 模式 | Webhook（实时推送） | 非轮询 |
| 匹配规则 | `matchExpression` 构建器 | 按 event+action 组合 |

**matchExpression 机制**：
- 支持按 GitHub event 类型（issues / pull_request / issue_comment 等）匹配
- 支持按 action 细分（opened / closed / created 等）
- 构建器模式：组合多个条件生成匹配表达式

## 插件版本管理

插件注册表：`~/.qoderwake/plugins/registry.json`

```json
{
  "schema": "qoderwake.plugin.registry.v1",
  "plugins": {
    "aone": {
      "versions": {
        "1.0.3": {
          "manifestHash": "sha256:...",
          "installedAt": "2026-...",
          "enabled": true
        }
      }
    },
    "dingtalk": {
      "versions": { "1.0.9": { ... } }
    }
  }
}
```

**版本管理特性**：
- 多版本并存（每版本独立目录）
- `manifestHash`（sha256）完整性校验
- `source: "bundled"`：当前仅支持 bundled 来源
- `forceUpgrade: true`：强制升级标记

## 运维命令

```bash
qoderwake trigger list                    # 列出所有触发器
qoderwake trigger detail <id>             # 查看触发器详情
qoderwake trigger create                  # 创建触发器
qoderwake trigger test-pull <id>          # 测试拉取（调试）
qoderwake trigger run-now <id>            # 立即执行一次
qoderwake trigger inspect <id>            # 检查触发器状态
```

## 交叉引用

- [[automated-trigger]] — 触发器的上层概念设计
- [[waker-data-model]] — 触发器相关数据表（triggers / trigger_runs / tasks）
- [[waker-plugin-system]] — 插件双层架构中触发器插件的位置
- [[waker-hook-lifecycle]] — 触发器触发后的 Hook 执行链
- [[connector]] — 连接器与触发器的关系

## 来源

- ~/.qoderwake/resources/plugins/trigger-event-sources/*/qoderwake-plugin.json [reverse-engineering] 2026-06-30
- ~/.qoderwake/plugins/registry.json [reverse-engineering] 2026-06-30
- ~/.qoderwake/data/state/dws-auto-upgrade.json [reverse-engineering] 2026-06-30
