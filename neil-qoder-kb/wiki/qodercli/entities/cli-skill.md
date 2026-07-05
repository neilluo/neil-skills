# CLI Skill — 技能系统

> 将领域专业知识打包为可复用能力模块，模型自主判断何时调用。

## 概述

Skills 是 Qoder 中把领域专长封装为 SKILL.md 文件的机制。每个 Skill 聚焦一类任务（如代码审查、PDF 处理、部署流程），支持自动触发和手动调用，在 IDE 和 CLI 中行为一致。

## 关键特性

- **智能调用**：模型根据用户请求描述自主决定是否使用 Skill
- **模块化设计**：每个 Skill 聚焦一类任务
- **灵活扩展**：支持用户级、项目级和社区 Skill

## 触发方式

| 方式 | 说明 | 示例 |
|------|------|------|
| 自动触发 | 模型根据描述判断 | "分析这个日志文件" → 自动用 log-analyzer |
| 手动触发 | `/skill-name` 直接调用 | `/create-skill`、`/review` |

## 内置 Skills

| 名称 | 用途 |
|------|------|
| `/create-skill` | 引导创建新 Skill |
| `/create-skill-ui` | 生成交互式 HTML Widget 界面 |
| `/vercel-deploy` | 一键 Vercel 部署 |
| `/create-subagent` | 创建自定义 Subagent |
| `/canvas` | 创建/编辑 .canvas.tsx 可视化制品 |

## 创建方式

| 方式 | 适用场景 |
|------|---------|
| `/create-skill <描述>` | AI 辅助快速生成（推荐） |
| `npx skills add ...` | 从 skills.sh 社区安装 |
| 手动创建 SKILL.md | 完全定制 |

## 存储位置与优先级

| 位置 | 路径 | 作用域 |
|------|------|--------|
| 项目级（最高） | `.qoder/skills/{name}/SKILL.md` | 仅当前项目 |
| 用户级 | `~/.qoder/skills/{name}/SKILL.md` | 所有项目 |
| Plugin | 插件 `skills/` 目录 | 随插件启用 |

同名 Skill：项目级 > 用户级 > Plugin > 内置。

## Skill UI

Skill UI 可在对话流中渲染交互式 HTML 组件（表单、图表、配置面板）。通过 `/create-skill-ui` 创建。

## 管理

- `/skills` — 管理当前工作区 Skills
- `qodercli skills list` — Headless 列出

## 交叉引用

- [[cli-subagent]] — Subagent 与 Skill 的区别（Skill 是说明，Subagent 是执行者）
- [[cli-plugin]] — 插件可包含 Skills
- [[cli-command-system]] — Skill 可注册为斜杠命令
- [[skill]] — Cloud Agents 的 Skill 概念对比

## 来源

- raw/qodercli/skills.md [official-docs]
