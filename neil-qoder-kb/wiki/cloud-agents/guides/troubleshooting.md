# 排障指南

> 常见错误的快速诊断和解决方案。

## 概述

本页汇总 Qoder Cloud Agents 使用中的常见问题和解决方案，按错误类型组织，方便快速定位。

## 认证问题

| 症状 | 原因 | 解决 |
|------|------|------|
| 401 Unauthorized | PAT 未设置或已过期 | 检查 `$QODER_PAT`，重新创建令牌 |
| 403 Forbidden | PAT 无权限 | 确认令牌权限范围 |

## 请求格式问题

| 症状 | 原因 | 解决 |
|------|------|------|
| 400 Bad Request（创建 Agent） | JSON 格式错误或字段缺失 | 检查 `model` 是否有效，`tools` 是否为数组 |
| 400 `invalid_request_error`（更新） | 缺少 `version` 字段 | PUT 请求必须携带当前 version |

## 并发冲突

| 症状 | 原因 | 解决 |
|------|------|------|
| 409 `conflict_error`（更新 Agent） | version 不一致 | GET 最新版本 → 合并变更 → 重试 |
| 409 `conflict_error`（发消息） | Session 处于 processing | 等待 idle 或先 cancel |

## Session 问题

| 症状 | 原因 | 解决 |
|------|------|------|
| Session 一直 idle | 未发送 `user.message` | 向 Session POST 事件 |
| SSE 流中断 | 网络断开 | 重连时带 `?after_id=<last_event_id>` |
| 容器文件丢失 | 超过 24 小时 | 重要文件用 Files API 持久化 |

## 环境问题

| 症状 | 原因 | 解决 |
|------|------|------|
| GET /environments 返回空 | 新账号无预置环境 | 手动 POST 创建 |
| 包安装失败 | 网络策略限制 | 改用 `unrestricted` 或添加白名单 |

## 工具权限问题

| 症状 | 原因 | 解决 |
|------|------|------|
| Session 暂停在 requires_action | 工具设置了 `always_ask` | 回传 `user.tool_confirmation` |
| pending action 一直等待 | 未响应确认 | 不会超时，需手动 allow/deny 或 cancel |

## Outcome 定义问题

| 症状 | 原因 | 解决 |
|------|------|------|
| Agent 未按标准执行 | Rubric 过于模糊 | 使用编号列表写明可测量条件 |

## 调试技巧

1. **验证 PAT**：`curl -s https://api.qoder.com/api/v1/cloud/agents -H "Authorization: Bearer $QODER_PAT"`
2. **查看 Session 状态**：GET session 确认当前 status
3. **事件流调试**：不带 after_id 获取完整事件历史
4. **检查 stop_reason**：`session.status_idle` 的 `stop_reason.type` 说明结束原因

## 交叉引用

- [[quickstart]] — 正确的初始化流程
- [[session-lifecycle]] — 状态机理解
- [[permission-model]] — requires_action 处理
- [[occ-versioning]] — 409 冲突处理

## 来源

- raw/cloud-agents/quickstart.md [official-docs] 2026-06-21
- raw/cloud-agents/sessions.md [official-docs] 2026-06-21
- raw/cloud-agents/define-agent.md [official-docs] 2026-06-21
- raw/cloud-agents/permission-policies.md [official-docs] 2026-06-21
- raw/cloud-agents/events-stream.md [official-docs] 2026-06-21
