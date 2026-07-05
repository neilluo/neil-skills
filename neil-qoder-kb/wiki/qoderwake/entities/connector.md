# Connector（连接器）

> Waker 对接外部工具和服务的桥梁——将 GitHub、Jira、GitLab 等平台能力注入数字员工。

## 概述

Connector 是 QoderWake 中将外部工具/服务能力桥接给 Waker 的机制。通过连接器，Waker 可以访问代码仓库、项目管理平台等外部系统，实现跨平台自动化协作。

## 详细内容

### 支持的连接器

当前支持的外部服务包括：
- **GitHub** — 代码仓库、Issue、PR 操作
- **Jira** — 项目管理、任务跟踪
- **GitLab** — 代码仓库、CI/CD 集成

### 配置方式

进入 **员工详情 → 连接器**，可手动添加连接器。每个连接器需要提供对应服务的认证凭据。

### 与技能的区别

| 维度 | 连接器 | 技能 |
|------|--------|------|
| 本质 | 外部服务认证桥梁 | 领域知识能力包 |
| 来源 | 手动配置认证 | 市场安装/上传 |
| 作用 | 让 Waker 能操作外部平台 | 让 Waker 具备特定领域专长 |

## 交叉引用

- [[waker]] — 连接器的宿主实体
- [[waker-config-guide]] — 连接器配置实践
- [[automated-trigger]] — 事件触发需要连接器来监听外部变化
- [[vault]] — Cloud Agents 中类似的凭据管理机制

## 来源

- raw/qoderwake/manage-wakers.md [official-docs] 2026-06-28
