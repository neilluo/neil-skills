# Deployment

> Agent 部署到云端运行的完整链路和生产注意事项。

## 概述

Qoder Cloud Agents 是全托管平台，用户无需管理部署基础设施。核心部署流程是：定义 Agent → 配置 Environment → 启动 Session。生产环境需关注版本锁定、认证安全和资源规划。

## 部署链路

```
定义 Agent → 配置 Environment → 创建 Session → 发消息执行
```

## 认证方式

所有 API 请求需携带：

| Header | 值 | 说明 |
|--------|---|------|
| `Authorization` | `Bearer <PAT>` | 个人访问令牌 |

PAT 在 Qoder 控制台「设置 → 个人访问令牌」中创建。

## 分页机制

列表接口统一使用游标分页：

```json
{"data": [...], "first_id": "...", "last_id": "...", "has_more": true}
```

使用 `after_id` / `before_id` 查询参数翻页。

## 生产环境建议

1. **锁定 Agent 版本**：`{"agent": {"id": "agent_xxx", "version": N}}`
2. **最小工具集**：生产 Agent 只配必要工具
3. **白名单网络**：限制容器可访问的外部地址
4. **Vault 管理凭证**：不要硬编码 Token
5. **监控 Usage**：通过 `session.status_idle` 事件跟踪 token 消耗

## 适用场景

| 场景 | 说明 |
|------|------|
| 长时间异步任务 | 代码审查、大规模重构、测试生成 |
| API 集成 | 后端嵌入 Agent 能力 |
| 批量处理 | 并行多 Session 处理批量请求 |
| 定时任务 | 周期性巡检/报告 |

## 交叉引用

- [[agent]] — 部署的配置模板
- [[environment]] — 运行容器配置
- [[session]] — 执行实例
- [[container-sandbox]] — 容器资源与限制
- [[production-checklist]] — 生产上线检查清单

## 来源

- raw/cloud-agents/overview.md [official-docs] 2026-06-21
- raw/cloud-agents/quickstart.md [official-docs] 2026-06-21
