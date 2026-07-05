# Knowledge Engine（知识引擎）

> Qoder 的核心能力模块，自动沉淀开发中的业务知识，让 Agent 每次对话都比上次更了解你的项目。

## 概述

知识引擎负责自动沉淀和管理日常开发产生的业务知识。减少重复踩坑，提升回答精度，降低 Credit 消耗。三类知识汇入同一引擎，无需人工整理，Agent 按需自动调用。

## 三类知识来源

| 来源 | 说明 | 沉淀路径 |
|------|------|----------|
| **Repo Wiki** | 基于代码库自动生成的结构化文档 | 代码侧：自动从代码库生成 |
| **知识卡片（Knowledge Card）** | 高密度知识单元：架构文档、代码规约、技术栈 | 代码侧：生成 Repo Wiki 时自动提炼 |
| **对话记忆（Memory）** | 踩坑记录、决策依据和项目经验 | 对话侧：交互过程中自动提炼 |

## 自动沉淀双路径

1. **代码侧**：生成 Repo Wiki 时 → 系统自动将代码意图、设计方案提炼为知识卡片
2. **对话侧**：与 Agent 交互 → 踩坑记录、决策依据自动提炼为 Memory

## 与 Quest 协同

在 Quest 中使用时，知识引擎让 Agent 持续了解项目，减少重复解释和 Credit 消耗。

## 交叉引用
- [[desktop-editor]] — Editor 中 Agent 自动调用知识引擎
- [[desktop-quest]] — Quest 拓展功能中的知识中心
- [[desktop-rules]] — 规则是另一种注入项目上下文的方式
- [[cli-memory-system]] — CLI 的记忆系统采用类似的 AGENTS.md + 自动记忆双轨设计

## 来源
- raw/qoderdesktop/knowledge-engine.md [official-docs]
