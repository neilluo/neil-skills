# QoderCLI 内置任务追踪器

> QoderCLI 内置的项目任务管理系统，通过 6 个 Agent 工具实现 epic/task/bug 追踪、依赖关系管理和 ASCII 可视化。

## 概述

QoderCLI 1.0.16 内置了完整的任务追踪系统（Task Tracker），Agent 可在对话中创建、更新、查询任务，建立依赖关系，并生成 ASCII 可视化图。适合在 Goal 模式下自动拆解和追踪子任务。

## 工具集（6 个）

| 工具 | 功能 |
|------|------|
| TrackerCreateTask | 创建任务（支持 epic/task/bug 类型） |
| TrackerUpdateTask | 更新任务状态/描述 |
| TrackerGetTask | 查询单个任务详情 |
| TrackerListTasks | 列出所有任务（支持过滤） |
| TrackerAddDependency | 添加任务间依赖关系 |
| TrackerVisualize | 生成 ASCII 任务图 |

## 任务类型

| 类型 | 用途 | 典型场景 |
|------|------|----------|
| epic | 史诗级大任务 | "重构支付模块" |
| task | 具体子任务 | "实现 PaymentService" |
| bug | 缺陷修复 | "修复超时问题 #123" |

## 依赖关系

`TrackerAddDependency` 支持建立任务间的依赖链：
- Task B 依赖 Task A → A 完成前 B 不应开始
- 支持多对多依赖
- `TrackerVisualize` 可视化依赖图

## ASCII 可视化

`TrackerVisualize` 生成任务关系的文本图：

```
[epic] 重构支付模块 ─┬─ [task] 接口设计 ✅
                     ├─ [task] 实现 Service ⏳ ← depends on 接口设计
                     ├─ [task] 单元测试 ⬜ ← depends on 实现 Service
                     └─ [bug] 修复超时 ✅
```

## 与 Goal 系统协同

典型配合模式：

```
用户: /goal set "重构支付模块"
  ↓
Agent 调用 TrackerCreateTask(type=epic, "重构支付模块")
  ↓
Agent 拆解为子任务:
  TrackerCreateTask(type=task, "接口设计")
  TrackerCreateTask(type=task, "实现 Service")
  TrackerAddDependency("实现 Service" → "接口设计")
  ↓
Agent 逐个执行，完成后 TrackerUpdateTask(status=done)
  ↓
TrackerVisualize() 输出进度
```

## 交叉引用

- [[cli-goal-system]] — Goal 系统与 TaskTracker 的协同
- [[cli-cron-system]] — 可定时执行任务追踪报告
- [[cli-session]] — 任务在 session 内管理

## 来源

- QoderCLI 1.0.16 二进制逆向分析（TrackerCreateTask/UpdateTask/GetTask/ListTasks/AddDependency/Visualize） [reverse-engineering] 2026-06-30
