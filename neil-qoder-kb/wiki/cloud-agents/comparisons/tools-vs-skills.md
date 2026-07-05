# 工具 vs 技能

> 理解 Tools 和 Skills 的定位差异，正确选型。

## 概述

Tools 和 Skills 都扩展 Agent 的能力，但定位不同。Tools 是原子操作（读文件、执行命令），Skills 是领域知识模块（编码规范、审查流程）。两者互补，不是替代关系。

## 核心差异

| 维度 | Tools | Skills |
|------|-------|--------|
| 本质 | 可执行的原子操作 | 领域知识和流程指令 |
| 粒度 | 单一动作 | 多步骤流程 |
| 激活方式 | Agent 自主决定调用 | 按需激活 |
| 配置位置 | Agent `tools[]` | Agent `skills[]` |
| 权限控制 | 支持 `permission_policy` | 不支持 |
| 运行时行为 | 平台执行并返回结果 | 注入为上下文指令 |
| 版本管理 | 随 toolset 版本 | 每次上传新版本 |
| 上传方式 | 内置 / JSON 定义 | ZIP 文件上传 |

## 类比

- **Tools** = 员工的工具箱（锤子、螺丝刀）
- **Skills** = 员工的培训手册（操作规范、最佳实践）

## 何时用 Tools

- 需要 Agent 执行文件操作、命令执行
- 需要访问外部 API（自定义工具 / MCP）
- 需要精细的权限控制（allow/ask/deny）

## 何时用 Skills

- 需要注入领域专业知识
- 需要定义复杂的工作流程
- 需要携带模板和示例文件
- 对比 `system` 提示词：system 对所有任务生效，Skill 按需激活

## 自定义工具 vs MCP 工具

| 类型 | 执行方 | 前缀 | 暂停行为 |
|------|--------|------|----------|
| 内置工具 | 平台 | 无 | 按 permission_policy |
| 自定义工具 | 客户端 | 无 | 总是暂停 (requires_action) |
| MCP 工具 | MCP 服务器 | `mcp__` | 平台代理 |

## 组合使用

```json
{
  "tools": [
    {"type": "agent_toolset_20260401", "enabled_tools": ["Read", "Write", "Bash"]},
    {"type": "custom", "name": "lookup_order", "description": "查订单", "input_schema": {...}}
  ],
  "skills": [{"type": "custom", "skill_id": "skill_xxx"}]
}
```

## 交叉引用

- [[agent]] — Tools 和 Skills 都配置在 Agent 上
- [[skill]] — Skill 详细说明
- [[permission-model]] — 工具权限策略
- [[event]] — 自定义工具的事件交互

## 来源

- raw/cloud-agents/tools.md [official-docs] 2026-06-21
- raw/cloud-agents/skills.md [official-docs] 2026-06-21
- raw/cloud-agents/permission-policies.md [official-docs] 2026-06-21
