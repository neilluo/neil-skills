# Qoder 产品家族架构总览

> Qoder 五大产品的分层架构、组件关系和能力矩阵，从「引擎 → 整车 → 4S 店 → 工厂」的递进关系理解整个产品线。

## 概述

Qoder 产品线由 5 个产品组成，形成从个人工具到企业平台的完整谱系。核心关系：**QoderCLI 是共享引擎，所有其他产品在其上构建差异化价值**。

## 产品关系图

```
                    ┌─────────────────────────────┐
                    │     Cloud Agents (云端)       │
                    │  全托管 API-first 沙箱平台     │
                    └─────────────────────────────┘
                                  ↑ 远程派发
    ┌──────────────────────────────────────────────────┐
    │              QoderWake (本地服务)                  │
    │  Daemon + Web UI + Trigger + Channel + Memory     │
    │  「数字员工工厂」— 7×24 多 Agent 调度平台          │
    └───────────────────────┬──────────────────────────┘
                            │ spawn + Hook 注入
    ┌───────────────────────┼──────────────────────────┐
    │              QoderCLI (核心引擎)                   │
    │  LLM + Tools + Skills + MCP + Memory + Hooks      │
    │  「AI 编程发动机」— 单用户终端 Agent               │
    └───────────┬───────────────────────┬──────────────┘
                │ 共享引擎               │ 共享引擎
    ┌───────────┴──────────┐ ┌──────────┴──────────────┐
    │  Qoder Desktop (IDE) │ │  QoderWork (桌面助手)    │
    │  Editor + Quest      │ │  任务 + 电脑操控         │
    │  「Agentic IDE」     │ │  「智能工作助手」         │
    └──────────────────────┘ └─────────────────────────┘
```

## 能力矩阵

| 能力维度 | Cloud Agents | QoderWake | QoderCLI | Desktop | QoderWork |
|---------|:---:|:---:|:---:|:---:|:---:|
| **进程形态** | 云端容器 | 本地 Daemon | 终端前台 | GUI 应用 | GUI 应用 |
| **LLM 对话** | ✅ | ✅（通过 CLI） | ✅ | ✅ | ✅ |
| **代码编辑** | ✅ | ✅ | ✅ | ✅ | ❌ |
| **文件操作** | ✅（沙箱内） | ✅ | ✅ | ✅ | ✅ |
| **Shell 执行** | ✅（沙箱内） | ✅ | ✅ | ✅ | ❌ |
| **MCP 协议** | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Skill 市场** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **多 Agent** | ✅（Managed） | ✅（Waker Group） | ✅（Subagent） | ✅（Quest） | ❌ |
| **记忆系统** | ✅（Memory Store） | ✅（dream/snapshot） | ✅（AGENTS.md） | ✅（知识引擎） | ✅（意识系统） |
| **IM 集成** | ❌ | ✅（钉钉/飞书） | ❌ | ❌ | ✅（钉钉/飞书/微信） |
| **定时触发** | ❌（需外部） | ✅（Cron/事件/API） | ✅（CronCreate） | ❌ | ✅（定时任务） |
| **安全防护** | ✅（沙箱隔离） | ✅（Tool Guard 28条） | ✅（common.sh 681行） | ✅（共享 CLI） | ❌ |
| **Web UI** | ❌（API only） | ✅（:19820） | ❌ | ✅（IDE） | ✅（应用） |
| **电脑操控** | ❌ | ❌ | ❌ | ❌ | ✅（截屏+鼠标） |
| **7×24 在线** | ✅ | ✅ | ❌ | ❌ | ✅（定时） |
| **API 丰富度** | ✅✅（完整 REST） | ⚠️（invoke only） | ❌ | ❌ | ❌ |

## 安全防护体系对比

| 层次 | Cloud Agents | QoderWake | QoderCLI / Desktop |
|------|:---:|:---:|:---:|
| 容器沙箱 | ✅（Firecracker） | ❌ | ❌ |
| Tool Guard 规则 | ❌ | ✅（28条） | ❌ |
| Security Hook 脚本 | ❌ | ✅（叠加） | ✅（common.sh 681行） |
| 权限模式 | allow/ask/deny | 继承 CLI + Guard | 5 种模式 |
| Prompt 注入检测 | ❌ | ✅ | ✅ |

## 记忆系统对比

| 维度 | Cloud Agents | QoderWake | QoderCLI | Desktop | QoderWork |
|------|:---:|:---:|:---:|:---:|:---:|
| 存储 | 云端 KV | agent.sqlite | 本地文件 | 知识卡片 | 意识系统 |
| 持久性 | 永久 | 永久 + 版本化 | 永久 | 永久 | 永久 |
| 版本控制 | OCC（version） | dream/snapshot/rollback | ❌ | ❌ | ❌ |
| 导出/导入 | ❌ | ✅ | ❌ | ❌ | ❌ |
| 跨会话 | ✅（Memory Store） | ✅ | ✅（AGENTS.md） | ✅ | ✅ |
| 知识引擎 | ❌ | QMind（proposal+OCC） | ❌ | Repo Wiki | ❌ |

## 技术栈对比

| 维度 | Cloud Agents | QoderWake | QoderCLI | Desktop |
|------|:---:|:---:|:---:|:---:|
| 运行时 | 云容器 | Bun 1.3.14 | Bun | Electron |
| 数据库 | 云端 | SQLite/PostgreSQL | 本地文件 | SQLite |
| 二进制大小 | N/A | ~91 MB | ~94 MB | ~200+ MB |
| API 框架 | REST + SSE | HTTP + SSE | CLI | IPC |
| 向量搜索 | 云端 | sqlite-vec | ❌ | 内置 |

## 选型指南

| 场景 | 推荐产品 | 理由 |
|------|---------|------|
| 个人日常编程 | **Desktop** | GUI + 代码编辑 + 知识引擎一体 |
| 终端重度用户 | **QoderCLI** | 最轻量、最灵活、可脚本化 |
| 团队 AI 员工 | **QoderWake** | 多 Agent + IM + 定时 + 权限管理 |
| API 集成/嵌入 | **Cloud Agents** | 唯一的 API-first 产品 |
| 非编程场景 | **QoderWork** | 电脑操控 + 文档处理 + IM 集成 |
| 定时批处理 | **QoderWake** | 原生 Cron + 事件触发 |
| 云端无人值守 | **Cloud Agents** | 不依赖本机 |

## 交叉引用

- [[cli-vs-cloud-agents]] — CLI 与 Cloud Agents 详细对比
- [[cloud-agents-vs-qoderwake]] — Cloud Agents 与 QoderWake 对比
- [[qw-vs-qoderwake]] — QoderWork 与 QoderWake 对比
- [[waker-daemon]] — QoderWake Daemon 架构详情
- [[waker-tool-guard]] — QoderWake 安全规则引擎
- [[desktop-security-audit]] — Desktop/CLI 安全审计 Hook

## 来源

- 综合全部 5 个产品的 wiki 页面和逆向分析结果 [cross-reference] 2026-06-30
- ATA 文章《从 AI 编程助手到 AI 数字员工平台》架构分析 [user-reported] 2026-06-30
