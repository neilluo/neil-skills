# Waker Group（员工群组）

> 多个 Waker 组成协作团队，由 Leader Waker 拆解任务、协调成员并汇总结果。

## 概述

Waker Group 是 QoderWake 面向多 Waker 协作的能力单元。一个群组包含一位 Leader Waker（负责人）和若干成员 Waker，通过 Group Chat 交互完成复杂任务。Leader 负责理解目标、拆解步骤、协调成员和汇总结果。

## 详细内容

### 创建群组

1. 进入聊天页面，点击"新建群组"
2. 填写群组名称（建议与任务相关，如"竞品功能分析"）
3. 选择 Leader Waker（任务负责人）
4. 选择成员 Waker（按需搭配：产品/研发/测试等）
5. 完成后进入群组开始协作

### 协作模式

| 阶段 | 说明 |
|------|------|
| **发起任务** | 在 Group Chat 中输入目标/问题 |
| **Leader 响应** | 理解意图 → 轻量直答 or 拆解阶段+成员分工 |
| **成员协作** | 各 Waker 按职责分工执行 |
| **随时介入** | 用户可打断/追问/调整方向 |
| **汇总交付** | Leader 整理最终结论 |

### 适用场景

- **方案产出**：跨角色的产品方案讨论与落地
- **问题诊断**：从 Issue 排查到 PR 提交的全流程协作
- **软件研发**：产品+研发+测试多方配合的复杂任务

### 交互技巧

- 指定成员补充细节："请研发 Waker 说明技术风险"
- 让 Leader 汇总："请 Leader 汇总当前结论"
- 调整方向："请先暂停 X，优先做 Y"

## 交叉引用

- [[waker]] — 群组中的执行单元
- [[role]] — 不同角色的 Waker 在群组中发挥不同作用
- [[task-types]] — 群组任务是三种任务类型之一
- [[managed-agents-threading]] — Cloud Agents 中类似的 Coordinator + Child 模型

## 来源

- raw/qoderwake/group-tasks.md [official-docs] 2026-06-28
