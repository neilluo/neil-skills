# 动态工作流

> 来源: https://docs.qoder.com/zh/cli/workflows

## 概述

动态工作流在后台运行结构化的多 Agent 流程。适合多阶段执行、大规模并发、交叉验证或复用固定流程的任务。编排计划放在 JavaScript 脚本中。

## 适用场景对比

| 使用方式 | 适合场景 |
|---------|---------|
| Subagent | 单个聚焦子任务 |
| Skill | 可复用说明、领域知识 |
| 动态工作流 | 多个子 Agent、多阶段、并行分支、验证轮次 |

## 能力

- 脚本化编排（循环、分支、阶段）
- 多 Agent 分发
- 分阶段执行（扫描→分析→验证→总结）
- 并行或流水线处理
- 后台运行
- 流程复用

## 运行方式

```text
使用动态工作流审查这个仓库的安全风险
使用 deep-research 动态工作流调研这个架构决策
```

## 保存位置

| 范围 | 位置 |
|------|------|
| 项目级 | `.qoder/workflows` |
| 用户级 | `~/.qoder/workflows` |
| Plugin | 插件提供 |
| 内置 | Qoder CLI 内置 |

## 脚本格式

```js
export const meta = {
  name: "repo-audit",
  description: "Audit a repository area and summarize risks",
  whenToUse: "Use when the user asks for a structured repository audit",
  phases: [
    { title: "Scan", detail: "Find relevant files" },
    { title: "Analyze", detail: "Run focused analysis agents" },
    { title: "Summarize", detail: "Merge findings into a report" }
  ]
};
```

## 辅助函数

`agent()`, `parallel()`, `pipeline()`, `phase()`, `log()`, `workflow()`, `args`, `budget`

## 权限与安全

- 脚本不能直接访问 shell/文件系统/网络/Node.js API/MCP
- 所有副作用通过子 Agent 发生
- 子 Agent 经过工具、权限、Hooks、沙箱设置

## 管理

- `/workflows` — 动态工作流任务面板
- `/tasks` — 包含工作流的后台任务视图
