# 生产环境清单

> 上线前必须检查的配置和安全项。

## 概述

将 Qoder Cloud Agents 部署到生产环境时，需确保安全性、可靠性和可观测性。本清单覆盖认证、版本控制、网络、监控等关键维度。

## 认证与密钥

- [ ] PAT 通过环境变量或密钥管理系统注入，不硬编码
- [ ] PAT 设置合理的过期时间
- [ ] 敏感凭证存储在 [[vault]] 中
- [ ] Token 不提交到代码仓库

## Agent 配置

- [ ] 生产 Agent 使用 `{"id": "agent_xxx", "version": N}` 锁定版本
- [ ] 系统提示词明确角色、输出格式、限制条件
- [ ] 只配置任务必需的工具（最小权限原则）
- [ ] 使用 `metadata` 标签分类管理

## 环境配置

- [ ] 网络策略使用白名单模式（`allowed_hosts`）或受限模式（`limited`）
- [ ] 只预装必需的依赖包
- [ ] 依赖包锁定版本（`pandas==2.1.0`）

## 工具权限

- [ ] 高风险工具（Bash、Write）设置 `always_ask` 或 `always_deny`
- [ ] 客户端实现 `user.tool_confirmation` 处理逻辑
- [ ] 只读场景工具集限制为 `["Read", "Glob", "Grep"]`

## 事件流与监控

- [ ] 客户端记录 last event id 用于断线重连
- [ ] 实现 30 秒超时重连逻辑
- [ ] 监控 `session.error` 事件
- [ ] 跟踪 `usage` 字段中的 token 消耗
- [ ] 监听 `terminated` 事件做清理

## 数据持久化

- [ ] 重要产出通过 Files API 上传（容器存储仅 24 小时）
- [ ] 跨 Session 知识存入 [[memory-store]]
- [ ] 定义 Outcome rubric 确保产出质量

## 容量规划

- [ ] 了解容器限制：4 vCPU / 8 GB 内存 / 25 GB 磁盘 / 30 分钟/Turn
- [ ] 批量场景评估并发 Session 数量
- [ ] 多 Agent 场景注意线程限制（25 并发/Session）

## 错误处理

- [ ] 实现 409 冲突重试逻辑（OCC）
- [ ] 处理 401 令牌过期自动刷新
- [ ] SSE 断线重连带 `after_id`

## 交叉引用

- [[deployment]] — 部署链路概览
- [[vault]] — 凭证安全管理
- [[permission-model]] — 工具权限策略
- [[container-sandbox]] — 容器资源限制
- [[occ-versioning]] — 并发控制
- [[troubleshooting]] — 问题排查
- [[outcome-rubric]] — 定义产出质量标准

## 来源

- raw/cloud-agents/overview.md [official-docs] 2026-06-21
- raw/cloud-agents/sessions.md [official-docs] 2026-06-21
- raw/cloud-agents/permission-policies.md [official-docs] 2026-06-21
- raw/cloud-agents/container-reference.md [official-docs] 2026-06-21
- raw/cloud-agents/vaults.md [official-docs] 2026-06-21
