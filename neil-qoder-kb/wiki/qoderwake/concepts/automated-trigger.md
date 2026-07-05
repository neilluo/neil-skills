# Automated Trigger（自动触发机制）

> 自动任务的三种触发方式——定时、事件驱动和 API 调用，支持混用最多 5 种触发器。

## 概述

QoderWake 自动任务支持三种触发方式，可以混合使用（最多 5 种）。触发后 Waker 自动开始执行预设任务，无需人工介入。通过 PAT（Personal Access Token）认证，还可从外部系统通过 API 触发任务。

## 详细内容

### 触发方式

| 类型 | 说明 | 示例 |
|------|------|------|
| **定时** | 一次性/周期性/复杂周期 | 每天 9 点、每周一、每月 1 号 |
| **事件驱动** | 监听 GitHub 仓库变化 | Issue 创建、PR 提交、评论变化 |
| **API 触发** | HTTP 调用外部触发 | CI/CD、Webhook、内部平台集成 |

### API 触发详解

**认证方式**：PAT（Personal Access Token）

获取步骤：
1. 登录 [Qoder 控制台](https://qoder.com)
2. 个人设置 → 服务集成
3. 新建令牌（设置名称与过期时间）
4. 复制令牌（格式：`pt-your-token-here`，仅显示一次）

**调用格式**：

```bash
curl -X POST 'https://api.qoder.com/v1/qoderwake/automation/invoke/<invoke_key>' \
  --header 'Authorization: Bearer pt-your-token-here' \
  --header 'Content-Type: application/json' \
  --data '{"prompt": "your appended prompt here"}'
```

- `invoke_key`：创建自动任务时系统生成，可在任务详情页获取
- `prompt`：本次追加的提示词，与任务描述合并后传递

### 限制配置

- **最大次数**（可选）：限制任务不要无限跑
- **截止日期**（可选）：到期后自动停止

### 管理操作

- 随时暂停/启用
- 立即运行测试（手动触发一次验证配置）
- 查看运行历史

## 交叉引用

- [[task-types]] — 自动任务是三种任务类型之一
- [[waker]] — 自动任务的执行主体
- [[connector]] — 事件触发依赖连接器监听外部平台
- [[waker-permission]] — 自动执行时的权限控制

## 来源

- raw/qoderwake/automated-tasks.md [official-docs] 2026-06-28
