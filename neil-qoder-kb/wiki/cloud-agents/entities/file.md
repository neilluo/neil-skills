# File

> 上传文件为 Agent 提供上下文，下载 Agent 产出的文件。

## 概述

File API 允许 upload（上传）文件给 Agent 作为输入上下文，也可 download（下载）Agent 执行过程中产出的文件。文件通过 `purpose` 字段区分用途，挂载到 Session 后 Agent 即可读取。

## 核心流程

1. `POST /files` — 上传文件
2. `POST /sessions/{id}/resources` — 挂载到 Session
3. Agent 读取文件完成任务
4. 下载产出文件（如适用）

## purpose 字段

| 值 | 含义 | 可下载 |
|---|------|------|
| `user_upload` | 用户上传的输入文件 | 否 |
| `tool_output` | 工具执行产出 | 是 |
| `skill_output` | Skill 执行产出 | 是 |
| `session_resource` | Session 级别资源 | 否 |
| `agent_output` | Agent 最终输出 | 否 |

`user_upload` 不可下载是出于安全考虑。Agent 需导出结果时以 `tool_output` 产出新文件。

## 上传文件

```bash
curl -X POST https://api.qoder.com/api/v1/cloud/files \
  -H "Authorization: Bearer $QODER_PAT" \
  -F "file=@./src/main.py" \
  -F "purpose=user_upload"
```

## 挂载到 Session

```bash
curl -X POST https://api.qoder.com/api/v1/cloud/sessions/sess_xxx/resources \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{"resources": [{"type": "file", "file_id": "file_xxx"}]}'
```

## 下载文件

仅 `tool_output` 和 `skill_output` 可下载：

```bash
curl https://api.qoder.com/api/v1/cloud/files/file_xxx/content \
  -H "Authorization: Bearer $QODER_PAT" -o output.txt
```

## 交叉引用

- [[session]] — 文件挂载到 Session
- [[memory-vs-files]] — 文件与记忆的选型对比
- [[container-sandbox]] — 容器内文件存储行为

## 来源

- raw/cloud-agents/files.md [official-docs] 2026-06-21
