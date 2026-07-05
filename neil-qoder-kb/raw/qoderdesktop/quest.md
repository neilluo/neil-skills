# Quest 工作台

Quest 是面向 Agent-first 工作范式的独立视窗，聚合 Agent 与 Experts 两种子模式。

核心理念：Define the goal. Review the result.

## 核心能力

- **多任务并行调度**：多项目、多任务并行推进，统一界面统筹指挥
- **多智能体专家协同**：多 Agent 分工协作，从 Coding 到交付端到端执行
- **知识与记忆沉淀**：持续沉淀项目知识、任务经验与上下文记忆
- **自定义专家团队**：灵活定义专家角色、流程与能力边界

## 两种模式

| 模式 | 定位 | 适用场景 |
|------|------|----------|
| Agent 模式 | 智能体自主执行 | 端到端交付单一任务 |
| Experts 模式 | 多智能体协同并行 | 全栈开发、技术调研、疑难修复 |

任务创建时确定模式，后续不可切换。

## 界面布局（三栏）

### 左侧：任务管理区
- 以工作区为组织单位，支持 Pin/Fork/重命名/删除
- 任务状态：Running / Action Required / Ready / Error
- My Quests 全局看板：按 Running / Waiting / Completed 三列分类

### 中间：会话区
- 完整对话记录与执行步骤实时展示
- 输入框支持 @ 引用文件/符号、模型选择、语音输入、上下文压缩
- 变更概览入口与侧边定位能力

### 右侧：功能区
- **概要**：Progress + 概要文件 + 引用（Repo Wiki/Memory/Skills/MCP）
- **审查与提交**：Diff 视图、文件拒绝、Git Commit/Push/PR
- **终端与文件树**、**浏览器**、**Spec 面板**、**Supabase 面板**

## 平铺布局

拖拽 Quest 任务拆分为多窗格，并行处理任务。设置跨会话保留。

## 拓展功能

- 知识中心：Repo Wiki + 知识卡片 + Memory
- 插件市场：安装官方插件扩展能力
- 设置：系统设置与偏好

## 注意事项
- 任务开始后不能切换模式
- 编辑消息会触发工作区文件回滚
- 模式在任务创建时确定

来源：https://docs.qoder.com/zh/user-guide/quest/overview
