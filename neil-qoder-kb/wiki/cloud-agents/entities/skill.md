# Skill

> 为 Agent 附加的领域专业知识模块，按需激活的结构化指令。

## 概述

Skill 是一组结构化的指令和流程，为 Agent 附加领域专业知识。与 `system` 提示词不同，Skill 是按需激活的专业模块（system 对所有任务生效）。一个 Agent 可关联多个 Skill，建议控制在 10 个以内。

## Skill 文件结构

以 `.zip` 文件上传（≤ 10MB）：

```
my-skill/
├── SKILL.md          # 必需：Skill 定义文件（YAML frontmatter + Markdown）
├── templates/        # 可选：模板文件
└── examples/         # 可选：示例文件
```

## API 操作

| 操作 | 方法 | 路径 |
|------|------|------|
| 创建/上传 | POST | `/api/v1/cloud/skills` (multipart) |

## 创建 Skill

```bash
cd my-skill && zip -r ../my-skill.zip . && cd ..
curl -X POST https://api.qoder.com/api/v1/cloud/skills \
  -H "Authorization: Bearer $QODER_PAT" \
  -F "file=@my-skill.zip"
```

## 关联到 Agent

使用 PUT 全量替换 + 携带当前 `version`（[[occ-versioning]]）：

```bash
curl -X PUT https://api.qoder.com/api/v1/cloud/agents/agent_xxx \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{"version": 1, "skills": [{"type": "custom", "skill_id": "skill_xxx"}]}'
```

## 版本管理

每次上传同名 Skill 会创建新版本。Agent 关联的 Skill 始终使用最新版本。

## 编写建议

1. 在 description 中写清触发条件
2. Steps 中写精确操作步骤
3. Pitfalls 帮助避免常见错误
4. 提供验证方法

## 交叉引用

- [[agent]] — Skill 挂载在 Agent 上
- [[tools-vs-skills]] — 工具与技能的区别和选型
- [[occ-versioning]] — 关联 Skill 时的版本控制

## 来源

- raw/cloud-agents/skills.md [official-docs] 2026-06-21
