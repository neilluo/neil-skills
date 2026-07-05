# CLI Memory System — 记忆系统

> AGENTS.md 文件 + 自动记忆双轨机制，实现跨会话知识持久化。

## 概述

Qoder CLI 每次会话重新构造上下文。跨会话保留的知识来自两类记忆：AGENTS.md（用户/团队维护的持久指令）和自动记忆（CLI 自动保存的 Markdown 文件）。记忆提供上下文但不是强制策略。

## 双轨机制

| 机制 | 写入者 | 适合内容 | 强制性 |
|------|--------|---------|--------|
| AGENTS.md | 用户/团队 | 规范、结构、命令、约定 | 建议遵循 |
| 自动记忆 | CLI | 偏好、反馈、背景、参考资料 | 上下文参考 |

## AGENTS.md

### 三级位置

| 位置 | 用途 | 提交 git |
|------|------|---------|
| `~/.qoder/AGENTS.md` | 跨项目通用偏好 | 否 |
| `<project>/AGENTS.md` | 团队共享规则 | 是 |
| `<project>/AGENTS.local.md` | 本机私有说明 | 否 |

### 加载逻辑

- **向上查找**：从工作区到 .git 所在目录
- **不扫描子目录**：子目录记忆按需加载（访问文件后补充）
- **可信工作区**：未信任目录不加载

### @导入

`@path/to/file` 引入其他文件。支持相对/绝对/~/ 路径。递归展开有深度限制。项目外导入需批准。

## 自动记忆

### 启用

```bash
QODER_MEMORY=1 qodercli                    # 项目级
QODER_MEMORY=1 QODER_MEMORY_USER=1 qodercli  # +用户级
```

### 四类内容

| 类型 | 用途 |
|------|------|
| user | 角色、长期偏好 |
| feedback | 用户纠正/确认 |
| project | 背景、约束、决策原因 |
| reference | 外部系统、文档位置 |

### 存储结构

```
~/.qoder/projects/<project>/memory/MEMORY.md  # 项目级索引
~/.qoder/memory/MEMORY.md                      # 用户级索引
```

索引 + 主题文件。MEMORY.md 不超 200 行/25KB。

## 管理入口

| 入口 | 功能 |
|------|------|
| `/memory` | 打开记忆概览 |
| `/memory manage` | 管理自动记忆主题文件 |
| `/init` | 生成项目 AGENTS.md |
| 自然语言 | "记住...""忘记..." |

## 交叉引用

- [[cli-session]] — 会话启动时的记忆加载
- [[cli-hook-system]] — Hooks 适合强制策略（记忆不适合）
- [[cli-permission-model]] — 权限是强制的，记忆是建议的
- [[waker-memory]] — QoderWake 的记忆系统对比

## 来源

- raw/qodercli/memory.md [official-docs]
