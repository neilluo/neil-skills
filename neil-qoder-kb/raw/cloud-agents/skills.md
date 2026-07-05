# Agent 技能 (Skills)

> 为 Agent 附加领域专业知识。

Skills 为 Agent 附加**领域专业知识**。一个 Skill 是一组结构化的指令和流程。

## Skill 文件结构

以 `.zip` 文件上传：

```
my-skill/
├── SKILL.md          # 必需：Skill 定义文件
├── templates/        # 可选：模板文件
└── examples/         # 可选：示例文件
```

`SKILL.md` 使用 YAML frontmatter + Markdown 格式。

## 创建 Skill

```bash
# 打包并上传
cd my-skill && zip -r ../my-skill.zip . && cd ..

curl -X POST https://api.qoder.com/api/v1/cloud/skills \
  -H "Authorization: Bearer $QODER_PAT" \
  -F "file=@my-skill.zip"
```

## 关联到 Agent

使用 PUT 全量替换 + 携带当前 `version`：

```bash
curl -X PUT https://api.qoder.com/api/v1/cloud/agents/agent_xxx \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "version": 1,
    "skills": [{"type": "custom", "skill_id": "skill_xxx"}]
  }'
```

## 版本管理

每次上传同名 Skill 会创建新版本。Agent 关联的 Skill 始终使用最新版本。

## Skill 编写建议

1. 在 description 中写清触发条件
2. Steps 中写精确操作
3. Pitfalls 帮助避免常见错误
4. 提供验证方法

## 常见问题

**Q：Skill 和 system 提示词的区别？**
A：`system` 对所有任务生效。Skill 是按需激活的专业模块。

**Q：一个 Agent 可关联多少个 Skills？**
A：无硬性限制，建议控制在 10 个以内。

**Q：zip 文件大小限制？**
A：单个 Skill zip 不超过 10MB。
