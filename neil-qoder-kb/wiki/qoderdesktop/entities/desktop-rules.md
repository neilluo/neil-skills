# Rules（规则系统）

> 为项目配置专属规则，将编码标准和项目约定注入 AI 提示词，引导 Agent 输出更符合项目规范。

## 概述

Rules 存放于 `.qoder/rules` 目录中，仅对当前项目生效。通过版本控制与团队共享。所有活跃规则合计上限 100,000 字符。

## 四种规则类型

| 类型 | 触发方式 | 适用场景 |
|------|----------|----------|
| **手动引入** | @rule 手动应用 | 按需工作流、自定义提示词 |
| **模型决策** | Agent 评估描述自动判断 | 场景化任务（生成测试/注释） |
| **始终生效** | 所有会话自动注入 | 项目级编码风格/文档格式 |
| **指定文件生效** | 匹配 glob 模式的文件 | 语言/目录特定规则 |

## AGENTS.md 兼容性

Qoder 自动识别项目中的 AGENTS.md 文件并应用其中的规则。无需额外配置。

**优先级**：.qoder/rules 中的规则 > AGENTS.md（冲突时规则优先）。

## 最佳实践
- 保持简洁聚焦
- 使用 Markdown 结构化
- 包含"良好"代码示例
- 根据输出迭代优化

## 交叉引用
- [[desktop-editor]] — 规则在 Editor 的 Ask/Agent 模式中生效
- [[desktop-quest]] — Quest 中的 Agent 同样受规则约束
- [[desktop-knowledge-engine]] — 知识引擎是另一种注入项目上下文的机制
- [[cli-memory-system]] — CLI 的 AGENTS.md 采用相同格式

## 来源
- raw/qoderdesktop/rules.md [official-docs]
