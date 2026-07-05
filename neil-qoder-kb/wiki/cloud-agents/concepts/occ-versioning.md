# 乐观并发控制 (OCC)

> 通过版本号防止并发更新冲突，保证数据一致性。

## 概述

Qoder Cloud Agents 对 Agent、Memory Store Entry 等资源采用乐观并发控制（Optimistic Concurrency Control）。每次更新必须携带当前 `version`，服务端校验通过后 version 自动 +1。不匹配则返回 409 冲突。

## 工作原理

```
客户端 GET → 拿到 version=N → 修改数据 → PUT (version=N) → 成功 → version=N+1
                                                          → 409 → 重新 GET → 合并 → 重试
```

## 适用资源

| 资源 | 字段名 | 初始值 |
|------|--------|--------|
| Agent | `version` | 1 |
| Memory Store Entry | `version` | 1 |

## 错误码

| 场景 | HTTP 状态码 | error_type |
|------|------------|------------|
| 缺少 version | 400 | `invalid_request_error` |
| version 不一致 | 409 | `conflict_error` |

## 409 冲突处理流程

1. `GET` 最新资源，获取当前 `version`
2. 合并自己的变更（注意可能需要 3-way merge）
3. 用新 `version` 重新 `PUT`

## 示例：更新 Agent

```bash
# version 不一致会返回 409
curl -s -X PUT https://api.qoder.com/api/v1/cloud/agents/agent_xxx \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{"name": "code-reviewer", "model": "ultimate", "version": 1}'
```

## 交叉引用

- [[agent]] — Agent 更新使用 OCC
- [[memory-store]] — Entry 更新使用 OCC
- [[skill]] — Skill 关联到 Agent 时需要 version

## 来源

- raw/cloud-agents/define-agent.md [official-docs] 2026-06-21
- raw/cloud-agents/memory-stores.md [official-docs] 2026-06-21
