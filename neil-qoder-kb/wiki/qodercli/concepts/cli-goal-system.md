# QoderCLI Goal 自主执行系统

> QoderCLI 内置的目标驱动自主执行模式，设置 Goal 后 Agent 自动切入零弹窗模式持续工作直到目标完成，支持预算控制和完成审计。

## 概述

Goal 系统是 QoderCLI 的自主执行框架。用户通过 `/goal set <目标描述>` 设置目标后，Agent 自动切入 `auto` 权限模式（零弹窗），持续执行直到目标完成或预算耗尽。

核心理念：**从「对话式助手」升级为「目标驱动的自主 Agent」**。

## 工具集

| 工具 | 功能 |
|------|------|
| CreateGoal | 创建目标（含预算设置） |
| GetGoal | 查询当前目标状态 |
| UpdateGoal | 更新目标状态（complete/blocked/paused/active） |

## 持久化

目标状态存储在 `~/.qoder/goals/current-goal.json`，包含：

| 字段 | 说明 |
|------|------|
| objective | 目标描述 |
| status | 状态（active/complete/blocked/paused） |
| turnsUsed | 已使用的对话轮次 |
| maxTurns | 最大轮次预算 |
| timeUsedSeconds | 已用时间（秒） |

## 执行机制

```
用户: /goal set "重构支付模块，通过所有测试"
  ↓
CreateGoal → 自动切入 auto 权限模式
  ↓
Agent 自主规划 → 拆解子任务
  ↓
循环执行（读代码 → 修改 → 编译 → 测试）
  ↓
每轮检查预算（turnsUsed < maxTurns?）
  ↓
达成条件后 → Completion Audit（防虚假完成）
  ↓
UpdateGoal(status=complete)
```

## 关键设计

### 1. 自动权限升级

设置 Goal 后自动切入 `auto` 模式：
- 文件读写：自动放行
- Shell 命令：AI 分类器判断风险（workspace 内通常放行）
- 危险操作：仍受 Tool Guard 规则约束

### 2. 预算控制

| 预算类型 | 说明 |
|---------|------|
| maxTurns | 最大工具调用轮次（防无限循环） |
| timeUsedSeconds | 累计执行时间 |

超出预算时自动暂停，等待用户决策。

### 3. Completion Audit

Goal 完成前的验证机制：
- Agent 声称完成时，系统执行独立审计
- 检查目标是否真正达成（如：测试是否通过、代码是否编译）
- 防止 LLM 过早声称完成（虚假完成问题）

### 4. 状态机

```
active → complete（目标达成）
active → blocked（遇到阻塞，需人工介入）
active → paused（预算耗尽或用户暂停）
paused → active（恢复执行）
```

## 使用场景

| 场景 | Goal 描述 | 预期行为 |
|------|-----------|----------|
| 大型重构 | "重构 UserService，拆分为 3 个微服务" | 自动读代码、创建文件、迁移逻辑、更新依赖 |
| Bug 修复 | "修复 #123 支付超时问题，通过所有测试" | 分析日志、定位问题、修复、运行测试验证 |
| 知识库维护 | "同步官方文档并更新所有过时 wiki 页面" | 执行 sync、diff 检测、逐页更新 |

## 与其他系统的协同

- **+ CronCreate**：定时触发 Goal（如每天 9:00 自动执行知识库维护 Goal）
- **+ TaskTracker**：Goal 内自动创建和追踪子任务
- **+ Remote Control**：远程触发 Goal 执行（手机端发起）

## 交叉引用

- [[cli-permission-model]] — Goal 模式下的权限行为变化
- [[cli-cron-system]] — 定时触发 Goal 的配合使用
- [[cli-session]] — Goal 在 session 内执行
- [[automated-trigger]] — QoderWake 的自动触发（对比参考）

## 来源

- QoderCLI 1.0.16 二进制逆向分析（CreateGoal/GetGoal/UpdateGoal + GoalManager） [reverse-engineering] 2026-06-30
- ~/.qoder/goals/current-goal.json 结构分析 [reverse-engineering] 2026-06-30
