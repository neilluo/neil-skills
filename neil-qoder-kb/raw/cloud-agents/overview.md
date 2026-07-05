# 概览

> 在完全托管的云沙箱中运行 AI Agent。

Qoder Cloud Agents 是全托管的 AI Agent 运行平台。你无需自建 agent loop、管理工具执行沙箱或处理长连接——只需通过 API 定义 Agent、启动 Session，即可在云端运行复杂任务并实时接收结果。

## 核心概念

| 概念 | 说明 | 类比 |
|------|------|------|
| **Agent** | 可复用的配置模板，定义模型、系统提示词、工具集 | "员工的岗位说明书" |
| **Environment** | Session 运行的容器环境，包含网络、依赖包配置 | "办公桌和工具箱" |
| **Session** | 一次具体的对话/任务执行实例 | "一次具体的工作会话" |
| **Event** | Session 中产生的实时事件流 | "工作进度实时播报" |

## 工作流程

1. **定义 Agent** — 指定模型、system prompt、可用工具。
2. **配置 Environment** — 选择容器类型、网络策略、预装依赖。新账号需先 POST /environments 创建环境（无预置默认环境）。
3. **启动 Session** — 绑定 Agent + Environment，创建运行实例。
4. **发消息 + 收事件** — 向 Session 发送 `user.message`，然后通过 SSE 流（或轮询）实时接收 Agent 思考、消息、状态变更等事件。

## 快速验证连通性

```bash
# 验证 PAT 是否有效，列出所有 Agent
curl -s https://api.qoder.com/api/v1/cloud/agents \
  -H "Authorization: Bearer $QODER_PAT"
```

成功响应格式：

```json
{
  "data": [],
  "first_id": null,
  "last_id": null,
  "has_more": false
}
```

## 适用场景

* **长时间异步任务** — 代码审查、大规模重构、自动化测试生成
* **API 集成** — 在后端服务中嵌入 Agent 能力，无需维护运行时
* **批量处理** — 并行启动多个 Session 处理批量请求
* **定时任务** — 结合调度系统，周期性运行 Agent 完成巡检/报告

## 认证方式

所有 API 请求需要携带以下 Header：

| Header | 值 | 说明 |
|--------|---|------|
| `Authorization` | `Bearer <PAT>` | 个人访问令牌 |

PAT 在 Qoder 控制台「设置 → 个人访问令牌」中创建，请妥善保管，不要提交到代码仓库。

## 分页机制

列表接口统一使用游标分页，响应结构：

```json
{
  "data": [...],
  "first_id": "agent_019e451902fe7a2ca42c2dfc62d9320e",
  "last_id": "agent_019e45369b3379e18bfaf59b3aad2fc9",
  "has_more": true
}
```

使用 `after_id` / `before_id` 查询参数翻页。

## 常见问题

**Q: Cloud Agents 和 Qoder CLI 可以同时使用吗？**
A: 完全可以。CLI 适合本地交互开发，Cloud Agents 适合自动化和集成场景，两者互补。

**Q: 一个 Agent 可以同时运行多少个 Session？**
A: 没有硬性限制，同一个 Agent 配置可以同时关联多个活跃 Session。

**Q: 数据安全如何保障？**
A: 每个 Session 运行在隔离的容器沙箱中，Session 之间无法互相访问。环境销毁后数据清除。
