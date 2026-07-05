# Outcome / Rubric

> 通过成功标准（Rubric）定义 Agent 的验收条件，驱动迭代直到达标。

## 概述

Outcome 是 Qoder Cloud Agents 的质量控制机制。通过 `user.define_outcome` 事件向 Session 发送 Rubric（成功标准），Agent 会自动按标准逐项检查并迭代工作，直到满足所有验收条件。这是实现"可预测产出质量"的关键手段。

## 核心概念

| 概念 | 说明 |
|------|------|
| Outcome | 对 Agent 产出结果的预期定义 |
| Rubric | 具体的验收标准文本（编号列表式） |
| 事件类型 | `user.define_outcome` |

## 发送 Rubric

通过 Session 事件 API 发送：

```bash
curl -X POST https://api.qoder.com/api/v1/cloud/sessions/sess_xxx/events \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "events": [{
      "type": "user.define_outcome",
      "rubric": "重构后的函数：1) 单元测试全部通过 2) 圈复杂度 ≤ 10 3) 无 lint 警告"
    }]
  }'
```

## Rubric 编写最佳实践

| 原则 | 说明 | 示例 |
|------|------|------|
| 编号列表 | 便于 Agent 逐项检查 | `1) ... 2) ... 3) ...` |
| 可测量 | 避免模糊描述 | ✅ "≤ 200 字" ❌ "简洁" |
| 前置发送 | 在任务指令前或同时发送 | 确保 Agent 开始时就知道标准 |
| 控制长度 | ≤ 500 字 | 过长 Rubric 分散 Agent 注意力 |
| 拆分复杂度 | 对大任务拆为多条验收项 | 每条单独可验证 |

## 典型 Rubric 示例

### 代码审查

```
1) 识别所有潜在安全漏洞
2) 每个问题附带修复建议和代码示例
3) 按严重程度排序（Critical > High > Medium > Low）
4) 输出为 Markdown 表格
```

### 报告生成

```
1) 执行摘要不超过 200 字
2) 至少 3 条可执行建议
3) 所有数据来源标注引用
4) 包含结论与下一步行动
```

## 触发时机

| 时机 | 说明 |
|------|------|
| 任务开始前 | 最佳——Agent 从第一步就知道目标 |
| 与消息同时 | 可以——一次 POST 包含 message + outcome |
| 执行中追加 | 可以——Agent 会调整后续行为 |

## 排障

| 症状 | 原因 | 解决 |
|------|------|------|
| Agent 未按标准执行 | Rubric 过于模糊 | 使用编号列表 + 可测量条件 |
| Agent 过度迭代 | Rubric 标准相互矛盾 | 检查条件间的一致性 |
| Agent 忽略部分条件 | Rubric 过长 | 控制在 500 字以内，优先级排序 |

## 交叉引用

- [[event]] — `user.define_outcome` 事件类型定义
- [[session]] — Outcome 发送到 Session
- [[production-checklist]] — 生产环境中定义 Outcome 确保质量

## 来源

- raw/cloud-agents/outcomes.md [official-docs] 2026-06-21
