# QoderWork Skill（技能）

> 一次定义、反复触发的工作指南，让 QoderWork 在面对特定任务时遵循固定步骤和格式。

## 概述

Skill 本质是一个包含 `SKILL.md` 文件的文件夹，存放于 `~/.qoderwork/skills/`。用自然语言描述触发条件和执行步骤，无需写代码。

## 核心价值
- 告别重复解释 → 一句话触发
- 保证输出一致性 → 符合既定标准
- 个人经验变可复用资产 → 可分享给团队
- AI 从通才变专才 → 按需加装专业模块

## 获取渠道

| 方式 | 说明 |
|------|------|
| 对话中搜索安装 | find-skill 自动检索推荐 |
| Skill 广场 | 扩展 → 技能，浏览内置市场 |
| 开源社区 | GitHub 仓库链接发给 QoderWork |
| 手动上传 | 上传 SKILL.md 及辅助文件 |

## 触发方式
- **自动触发**：描述需求时自动匹配
- **/ 快捷调用**：输入 / 弹出列表
- **对话中指名**："使用 xxx skill"

## 内置技能
docx / pdf / pptx / xlsx / find-skills / create-skill / plugin-creator / install-skill-dependency / vm-error-recovery

## Skill UI
部分 Skill 支持渲染交互式 HTML 组件嵌入对话流。

## 分享
生成 24 小时有效分享链接，对方一键安装。

## 交叉引用
- [[qw-task]] — 技能在任务中被调用
- [[qw-connector]] — 连接器提供外部能力，技能提供内部流程
- [[cli-skill]] — CLI 产品的技能系统采用相同的 SKILL.md 规范

## 来源
- raw/qoderwork/skills.md [official-docs]
