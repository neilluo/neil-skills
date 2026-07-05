# CLI vs Cloud Agents — 跨产品对比

> QoderCLI 与 Cloud Agents 的能力矩阵对比，帮助选择最适合的产品。

## 概述

QoderCLI 是本地终端 AI Coding Agent，Cloud Agents 是云端托管 API 服务。两者互补而非替代：CLI 适合交互式开发，Cloud Agents 适合后端集成和自动化流水线。

## 定位对比

| 维度 | QoderCLI | Cloud Agents |
|------|----------|--------------|
| 部署位置 | 用户本机终端 | Qoder 管理的云端沙箱 |
| 交互方式 | TUI 交互 / Print 脚本 | REST API + SSE |
| 主要用户 | 开发者（日常编码） | 平台方（构建产品） |
| 状态管理 | 本地会话 + AGENTS.md | 云端 Session + Memory Store |
| 工具执行 | 本地 shell + MCP | 容器内工具 + MCP |

## 能力矩阵

| 能力 | CLI | Cloud Agents |
|------|-----|--------------|
| 代码编辑 | 直接操作本地文件 | 容器内文件（需上传/挂载） |
| Git 操作 | 完整本地 Git | GitHub 挂载 + PR |
| 模型选择 | 分级/前沿/自定义 | API 指定模型 |
| 记忆持久化 | AGENTS.md + 自动记忆 | Memory Store API |
| 权限控制 | 5 种模式 + 规则 | Permission Policies |
| 扩展机制 | Skills / Plugins / Subagents / Hooks | Tools / Skills / Managed Agents |
| 多 Agent | Subagent 并发 + 工作流 | Managed Agents (Coordinator) |
| 远程执行 | --remote (Cloud Mode) | 原生云端执行 |
| 成本计费 | Credits（按模型档位） | API 调用计费 |

## 互通机制

| 机制 | 说明 |
|------|------|
| `--remote` | CLI 一键启动 Cloud Session |
| `/remote-env` | CLI 选择云端环境 |
| Cloud Agents SDK | 编程方式创建和管理 Session |
| ACP 协议 | CLI 被集成为 Agent 后端 |

## 选型建议

| 场景 | 推荐 |
|------|------|
| 个人日常编码、代码审查 | QoderCLI |
| 团队 CI/CD 集成 | QoderCLI (Print Mode) |
| 构建 AI 产品（SaaS） | Cloud Agents |
| 长时后台任务 | Cloud Mode 或 Cloud Agents |
| 移动端控制 | QoderCLI + Remote Control |
| 定时自动执行 | Cloud Agents Deployments |

## 交叉引用

- [[cli-session]] — CLI 的会话模式
- [[session]] — Cloud Agents 的 Session
- [[cli-skill]] — CLI 的 Skill 系统
- [[skill]] — Cloud Agents 的 Skill
- [[cli-permission-model]] — CLI 的权限模型
- [[permission-model]] — Cloud Agents 的权限策略
- [[cloud-agents-vs-qoderwake]] — Cloud Agents vs QoderWake 对比

## 来源

- raw/qodercli/cloud-mode.md [official-docs]
- raw/cloud-agents/overview.md [official-docs]
