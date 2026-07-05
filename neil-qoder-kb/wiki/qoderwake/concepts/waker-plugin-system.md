# 插件双层架构

> QoderWake 的插件系统分为 Daemon 级和 Agent 级两层：Daemon 级管理触发器/扩展等平台能力，Agent 级为每个数字员工自动生成个性化的 Hook/MCP/Skills 注入配置。

## 概述

QoderWake 的插件体系分为两层，对应「平台运维」和「员工个性化」两个不同关注点：

- **Daemon 级插件**：影响整个平台——触发器事件源、扩展热重载、HotDeploy 自动升级
- **Agent 级插件**：影响单个员工——AgentPluginManager 为每个 Waker 自动生成 `.qoder-plugin/`

## Daemon 级插件

### 管理命令

```bash
qoderwake plugin list                      # 列出已安装插件
qoderwake plugin info <name>               # 插件详情
qoderwake plugin install <dir|zip>         # 安装插件
qoderwake plugin enable <name>             # 启用
qoderwake plugin disable <name>            # 禁用
qoderwake ext list                         # 列出扩展
qoderwake ext reload                       # 热重载扩展
qoderwake ext enable/disable <name>        # 扩展开关
```

### 当前已安装（bundled）

| 插件 | 版本 | 说明 |
|------|------|------|
| aone | 1.0.3 | Aone 工单触发器 |
| dingtalk | 1.0.9 | 钉钉消息触发器 |

### HotDeploy 服务

- 每 60 分钟自动检查插件更新
- 从 bundled 源自动拉取新版本
- `forceUpgrade: true` 标记的插件会强制升级

### 注册表

`~/.qoderwake/plugins/registry.json`：

```json
{
  "schema": "qoderwake.plugin.registry.v1",
  "plugins": {
    "aone": {
      "versions": {
        "1.0.3": {
          "manifestHash": "sha256:...",
          "installedAt": "...",
          "enabled": true
        }
      }
    }
  }
}
```

## Agent 级插件

### AgentPluginManager

每次 Waker 创建或更新时，AgentPluginManager 自动在 `.qoder-plugin/` 下生成：

| 文件 | 说明 |
|------|------|
| plugin.json | 声明关联的 skills 列表 |
| .mcp.json | 注入 MCP 服务（如 qoderwake_memory） |
| hooks/hooks.json | 配置 8 个生命周期 Hook |
| output-styles/*.md | 行为注入规范 |
| skill-versions/ | 技能版本快照（Git-based） |

### 内置 MCP 注入

`.mcp.json` 自动注入 `qoderwake_memory` MCP 服务：

```json
{
  "mcpServers": {
    "qoderwake_memory": {
      "type": "sse",
      "url": "http://127.0.0.1:19820/api/internal/builtin-mcp/qoderwake_memory/sse",
      "headers": {
        "x-qoderwake-builtin-mcp-token": "..."
      }
    }
  }
}
```

提供工具：`memory_search` / `memory_add` / `memory_update` / `memory_remove`

### 内置技能包管理

BuiltinSkillManager 通过 manifest 管理技能安装：

`~/.qoderwake/resources/builtin-skills/manifest.json`：
```json
{
  "skills": [
    {
      "skillId": "qoderwake-assistant",
      "name": "QoderWake Assistant",
      "version": "2.1.6",
      "contentHash": "sha256:...",
      "enabled": true
    }
  ]
}
```

技能从 OSS 自动拉取 ZIP 包并安装到 Waker 的 plugin 目录。

## 两层协同关系

```
Daemon 级
├── 触发器插件（aone/dingtalk/github）→ 产生事件
├── 扩展管理（ext reload/enable/disable）
└── HotDeploy（每 60 分钟自动升级）
     ↓ 配置注入
Agent 级（每个 Waker 独立一份）
├── plugin.json → 声明技能
├── .mcp.json → 注入 memory MCP
├── hooks.json → 配置 Hook 链
└── output-styles → 行为规范
```

**关键缝合点**：Daemon 通过 Hook 命令调用自身二进制，将平台能力注入到底层 QoderCLI：

```bash
qoderwake __plugin_hook qoderwake_permission_guard pre-tool-use
qoderwake __plugin_hook qoderwake_memory session-start
```

## 交叉引用

- [[waker-trigger-plugins]] — Daemon 级的 3 个触发器插件详情
- [[waker-hook-lifecycle]] — Agent 级 Hook 链的 8 个阶段
- [[waker-identity-system]] — Agent 级的身份卡和 plugin 生成
- [[waker-daemon]] — Daemon 进程管理插件的生命周期
- [[cli-plugin]] — QoderCLI 底层的插件系统

## 来源

- ~/.qoderwake/plugins/registry.json [reverse-engineering] 2026-06-30
- ~/.qoderwake/data/workers/<id>/.qoder-plugin/ 结构分析 [reverse-engineering] 2026-06-30
- ~/.qoderwake/resources/builtin-skills/manifest.json [reverse-engineering] 2026-06-30
