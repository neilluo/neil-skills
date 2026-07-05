# CLI Workflow Engine — 动态工作流引擎

> JavaScript 脚本编排的多 Agent 后台流程，支持分阶段、并发、流水线执行。

## 概述

动态工作流让 Qoder CLI 在后台运行结构化的多 Agent 流程。编排计划放在 JavaScript 脚本中，脚本决定启动哪些子 Agent、如何划分阶段、如何合并结果。适合仓库审计、深度研究、迁移规划、跨文件扫描等复杂任务。

## 与 Subagent/Skill 的定位区分

| 机制 | 适合场景 |
|------|---------|
| Subagent | 单个聚焦子任务 |
| Skill | 可复用说明、领域知识 |
| 动态工作流 | 多 Agent、多阶段、并行分支、验证轮次 |

## 能力矩阵

| 能力 | 说明 |
|------|------|
| 脚本化编排 | 循环、分支、阶段、中间状态 |
| 多 Agent 分发 | 为独立工作切片启动多个子 Agent |
| 分阶段执行 | 扫描→分析→验证→总结 |
| 并行/流水线 | 并发独立分支 或 依次经过多处理阶段 |
| 后台运行 | 启动后可继续使用 CLI |
| 流程复用 | 保存后按名称调用 |

## 脚本格式

```javascript
export const meta = {
  name: "repo-audit",
  description: "审计仓库风险",
  whenToUse: "用户要求结构化审计时",
  phases: [
    { title: "Scan", detail: "找到相关文件" },
    { title: "Analyze", detail: "执行分析" },
    { title: "Summarize", detail: "合并为报告" }
  ]
};
```

## 辅助函数

`agent()` / `parallel()` / `pipeline()` / `phase()` / `log()` / `workflow()` / `args` / `budget`

## 保存位置与优先级

| 范围 | 位置 | 优先级 |
|------|------|--------|
| 项目级 | `.qoder/workflows/` | 最高 |
| 用户级 | `~/.qoder/workflows/` | ↓ |
| Plugin | 插件提供 | ↓ |
| 内置 | CLI 内置 | 最低 |

## 安全模型

- 脚本**不能**直接访问 shell、文件系统、网络、Node.js API、MCP
- 所有副作用通过子 Agent 发生
- 子 Agent 经过完整的工具 + 权限 + Hooks + 沙箱

## 管理

- `/workflows` — 动态工作流任务面板
- `/tasks` — 后台任务视图

## 交叉引用

- [[cli-subagent]] — 工作流的执行单元是 Subagent
- [[cli-permission-model]] — 工作流子 Agent 继承权限体系
- [[cli-plugin]] — 插件可包含工作流
- [[cli-session]] — 工作流作为后台任务在会话中管理

## 来源

- raw/qodercli/workflows.md [official-docs]
