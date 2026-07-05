# Cloud Agents vs QoderWake

> Qoder 两大产品的选型指南——云端 API 驱动 vs 本地 GUI 驱动，根据场景选择合适的方案。

## 概述

Cloud Agents 和 QoderWake 是 Qoder 平台的两种 Agent 部署形态。前者面向 API 集成和云端无服务器场景，后者面向本地桌面的交互式数字员工团队。两者共享 Skill 和权限等概念，但运行模型和交互方式完全不同。

## 详细内容

### 核心对比

| 维度 | Cloud Agents | QoderWake |
|------|-------------|-----------|
| **部署位置** | Qoder 云端托管沙箱 | 本机（macOS/Linux） |
| **交互方式** | API 调用（RESTful + SSE） | 本地 GUI 控制台 |
| **执行单元** | Session（绑定 Agent + Environment） | Waker（绑定 Role） |
| **配置方式** | API 创建 Agent JSON 配置 | GUI 选角色模板或自定义 |
| **网络隔离** | 容器沙箱（可选 full/none/egress-only） | 本地环境（无沙箱） |
| **持久记忆** | Memory Store API（云端） | 本地记忆（不上传云端） |
| **协作模式** | Managed Agents（Coordinator + Child Threads） | Waker Group（Leader + 成员 Group Chat） |
| **触发方式** | API 创建 Session / Deployment cron | 对话/定时/事件/API 触发 |
| **权限模型** | Permission Policy（allow/ask/deny per tool） | 工具防护 + 文件防护 + 内置工具策略 |
| **凭据管理** | Vault（云端密钥注入） | 连接器（本地配置认证） |
| **适合用户** | 开发者/平台方（API 集成） | 终端用户/团队（GUI 操作） |

### 选型决策树

```
你的 Agent 需要...
├── 被其他系统 API 调用？ → Cloud Agents
├── 在云端隔离沙箱中运行？ → Cloud Agents
├── 通过 GUI 交互式派活？ → QoderWake
├── 本地 7×24 持续运行？ → QoderWake
├── 多角色实时协作？ → QoderWake（Group Chat）
└── 编程集成到产品中？ → Cloud Agents（API）
```

### 共享概念映射

| 概念 | Cloud Agents | QoderWake |
|------|-------------|-----------|
| 执行配置 | Agent | Role + Waker |
| 技能 | Skill（zip 上传） | Skill（市场/上传/内置） |
| 记忆 | Memory Store | Waker Memory |
| 权限 | Permission Policy | 工具防护+文件防护 |
| 凭据 | Vault | Connector |
| 协作 | Managed Agents | Waker Group |

## 交叉引用

- [[agent]] — Cloud Agents 的执行配置
- [[waker]] — QoderWake 的数字员工
- [[session]] — Cloud Agents 的执行实例
- [[permission-model]] — Cloud Agents 的权限策略
- [[waker-permission]] — QoderWake 的权限模型
- [[managed-agents-threading]] — Cloud Agents 的多 Agent 线程模型
- [[waker-group]] — QoderWake 的群组协作

## 来源

- raw/cloud-agents/overview.md [official-docs] 2026-06-21
- raw/qoderwake/overview.md [official-docs] 2026-06-28
- 跨产品综合分析 [inferred] 2026-06-28
