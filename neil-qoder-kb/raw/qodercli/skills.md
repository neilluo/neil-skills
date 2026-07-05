# Skills

> 来源: https://docs.qoder.com/extensions/skills

## 概述

Skills 是将领域专业知识打包为可复用能力的机制。每个 Skill 含 SKILL.md 文件定义描述、指令和可选辅助文件。在 IDE 和 CLI 中工作方式相同。

## 关键特性

- 智能调用：模型根据用户请求和描述自主决定何时使用 Skill
- 模块化设计：每个 Skill 聚焦一类任务
- 灵活扩展：支持用户级和项目级自定义

## 内置 Skills

| 名称 | 用途 |
|------|------|
| /create-skill | 引导创建新 Skill |
| /create-skill-ui | 生成 Skill 的 HTML Widget 界面 |
| /vercel-deploy | 一键 Vercel 部署 |
| /create-subagent | 创建自定义 Subagent |
| /canvas | 创建/编辑 .canvas.tsx 可视化制品 |

## 触发方式

1. 自动触发：描述需求，模型自动判断是否使用相应 Skill
2. 手动触发：`/skill-name` 直接调用

## 创建 Skills

### 方式一：AI 辅助（推荐）
```bash
/create-skill <描述>
```

### 方式二：skills CLI 安装
```bash
npx skills add vercel-labs/agent-browser -a qoder
npx skills add https://github.com/anthropics/skills --skill skill-creator -a qoder
```

### 方式三：手动创建

存储位置：
| 位置 | 路径 | 作用域 |
|------|------|--------|
| 用户级 | `~/.qoder/skills/{skill-name}/SKILL.md` | 所有项目 |
| 项目级 | `.qoder/skills/{skill-name}/SKILL.md` | 当前项目 |

同名 Skill：项目级优先于用户级。

## Skill UI

可渲染交互式 HTML 组件（表单、图表、配置面板），嵌入对话流中。

## Canvas

将文本/数据/分析转为 .canvas.tsx 面板（stat cards、表格、图表），Agent 实时渲染。
