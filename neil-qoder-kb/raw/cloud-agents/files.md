# 文件上传与挂载

> 上传文件为 Agent 提供上下文，并下载 Agent 产出的文件。

## 核心流程

1. `POST /files` — 上传文件
2. `POST /sessions/{id}/resources` — 挂载到 Session
3. Agent 读取文件完成任务

## 上传文件

```bash
curl -X POST https://api.qoder.com/api/v1/cloud/files \
  -H "Authorization: Bearer $QODER_PAT" \
  -F "file=@./src/main.py" \
  -F "purpose=user_upload"
```

### purpose 字段

| 值 | 含义 | 可下载 |
|---|------|------|
| `user_upload` | 用户上传的输入文件 | 否 |
| `tool_output` | 工具执行产出 | 是 |
| `skill_output` | Skill 执行产出 | 是 |
| `session_resource` | Session 级别资源 | 否 |
| `agent_output` | Agent 最终输出 | 否 |

## 挂载到 Session

```bash
curl -X POST https://api.qoder.com/api/v1/cloud/sessions/sess_xxx/resources \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "resources": [
      {"type": "file", "file_id": "file_xxx"}
    ]
  }'
```

## 下载文件

仅 `tool_output` 和 `skill_output` 可下载：

```bash
curl https://api.qoder.com/api/v1/cloud/files/file_xxx/content \
  -H "Authorization: Bearer $QODER_PAT" \
  -o output.txt
```

## 常见问题

**Q：支持哪些文件格式？**
A：无限制，任意二进制文件均可上传。Agent 对文本类文件理解效果最佳。

**Q：为什么 user_upload 不可下载？**
A：安全考虑。需导出结果时，Agent 以 `tool_output` 产出新文件。
