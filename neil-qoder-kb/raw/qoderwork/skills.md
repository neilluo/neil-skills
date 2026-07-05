# 技能（Skills）

Skills 是提前写好的工作指南，告诉 QoderWork 在面对某类任务时遵循什么步骤、输出什么格式、注意哪些细节。每个 Skill 本质是一个包含 SKILL.md 文件的文件夹，存放于 ~/.qoderwork/skills/ 目录下。

## 价值
- 告别重复解释：固化需求和偏好，一句话触发
- 保证输出一致性：确保每次输出符合既定标准
- 个人经验变成可复用资产：可分享给团队
- 让 AI 从通才变专才：按需加装专业模块

## 获取方式
- **对话中搜索安装**：描述需求，find-skill 自动检索推荐
- **Skill 广场浏览安装**：扩展 → 技能，内置技能市场
- **从开源社区获取**：GitHub 仓库链接发给 QoderWork
- **手动上传本地文件**：上传 SKILL.md 及辅助文件

## 使用方式
- **自动触发**：描述需求时自动匹配已安装 Skill
- **/ 快捷调用**：输入 / 弹出已安装列表
- **@ 添加上下文**：补充文件等上下文
- **对话中指名调用**：直接说"使用 xxx skill"

## 内置技能

| 技能名 | 功能 |
|--------|------|
| docx | 创建/阅读/编辑 Word 文档 |
| pdf | 阅读/合并/拆分 PDF |
| pptx | 创建/编辑 PowerPoint |
| xlsx | 处理 Excel 表格 |
| find-skills | 搜索并安装新技能 |
| create-skill | 互动式引导创建技能 |
| plugin-creator | 创建/修改专家套件 |

## 管理与分享
- 文件系统操作：~/.qoderwork/skills/ 目录
- 分享链接：生成 24 小时有效的分享链接，对方一键安装

## Skill UI
部分 Skill 支持渲染交互式 HTML 组件（表单、图表、配置面板），直接嵌入对话流。

来源：https://docs.qoder.com/zh/qoderwork/skills
