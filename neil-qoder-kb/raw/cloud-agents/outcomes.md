# 定义 Outcomes

> 告诉 Agent 什么样的结果算成功。

通过 `user.define_outcome` 事件将 Rubric（成功标准）发送给 Session，Agent 会按标准迭代工作。

## 事件格式

```json
{
  "events": [
    {
      "type": "user.define_outcome",
      "rubric": "生成的报告必须包含：1) 执行摘要不超过 200 字 2) 至少 3 条可执行建议 3) 数据来源标注"
    }
  ]
}
```

## curl 示例

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

## 最佳实践

* 在发送任务指令前或同时发送 Outcome
* Rubric 使用编号列表，便于 Agent 逐项检查
* 对复杂任务拆分为多个可测量的验收条件
* Rubric 长度建议控制在 500 字以内
