# AGENTS.md — neil-aliyun-sa 知识库操作指南

> 本文件是给 AI coding agent 的操作手册。基于 [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 三层架构。
> Agent 在开始任何工作前必须读取本文件。

## 项目概述

这是一个**阿里云解决方案架构师知识库**，采用 Karpathy LLM Wiki 三层架构：

```
Schema 层 (SKILL.md)        — 你的行为协议，定义 8 种工作模式
Wiki 层   (knowledge/ + references/) — 你维护的预编译知识
Raw 层    (raw/)             — 不可变原始资料，只读不改
```

你的角色：**wiki maintainer**——读取 raw，维护 wiki，遵守 schema。

## 启动检查清单

每次新 session 启动时，按顺序执行：

1. 读 `index.md` — 了解 wiki 全貌和交叉引用
2. 读 `changelog.md` 最近 5 条 — 了解最近变更
3. 读 `knowledge/inbox.md` — 检查是否有 pending 待处理资料
4. 如有 pending 项 → 提醒用户是否要执行 Ingest

## 三大操作

> **强制要求**：执行 Ingest/Query/Lint 前，**必须先读取 SKILL.md 对应模式的完整定义**，因为 SKILL.md 含有本文件未展开的细节约束（如“知识蒸馏原则”“分步确认”等）。

### Ingest（模式 A：资料消化）

**触发词**：`学习一下`、`蒸馏`、`投喂`

**流程**（严格按顺序，不可跳步）：
```
1. inbox.md 登记 pending     ← 第一个动作，不可违反
2. changelog.md 追加 ⏳       ← 第二个动作
3. raw/ 归档原始内容          ← 不可变副本
4. 阅读 + 提炼洞察
5. 写入 knowledge/ 对应文件   ← 增量更新，不删旧信息
6. 更新 index.md             ← 若有新章节/实体
7. inbox 改 done, changelog 改 ✅
8. 输出反馈摘要
```

**写入优先红线**：宁可多写一次 "pending"，也不允许 "读了但没落盘"。

### Query（模式 B-F：查询回答）

**流程**：
```
1. 读 index.md 定位相关页面
2. 读取相关 knowledge/ 或 references/ 文件
3. 综合回答（含文档链接、量级数字、避坑点）
4. 用回写 checklist 判断是否触发模式 H
```

**Query→Wiki 回写 checklist**（满足任一则必须回写）：
- [ ] 输出含 ≥3 行新产品对比/分析（未在 knowledge 中存在）
- [ ] 发现了新的架构模式或最佳实践
- [ ] 完成了客户方案且含 BOM/架构图（可复用）
- [ ] 问答中发现并填补了知识空白

### Lint（模式 G：健康检查）

**触发词**：`lint`、`检查知识库`、`健康检查`

**检查维度**：矛盾 / 过时 / 孤立条目 / 缺页 / 交叉引用完整性 / 数据空白

## 文件操作规则

### 可以修改的文件

| 路径 | 修改场景 |
|------|----------|
| `knowledge/*.md` | Ingest 蒸馏、Query 回写、Lint 修复 |
| `index.md` | 每次 Ingest 后更新目录和交叉引用 |
| `changelog.md` | 每次 Ingest/Lint/Query回写后追加记录 |
| `knowledge/inbox.md` | 登记来源、更新状态 |

### 只读文件（不可修改）

| 路径 | 原因 |
|------|------|
| `raw/**` | 不可变源层，source of truth。实体归档策略：ATA 文章必须存全文；官方文档（help.aliyun.com）可仅存 URL+摘要+SHA256，因官网长期可访问；客户案例尽力存全文 |
| `references/*.md` | 默认只读；仅在用户明确指令下可更新 |
| `SKILL.md` | Schema 层，仅在架构升级时修改 |
| `AGENTS.md` | 本文件，仅在协议升级时修改 |

### 写入约定

- **增量优先**：追加新信息，不删除仍有效的旧信息
- **标注来源**：所有事实标注 `[官方]` / `[实战]` / `[推断]` + URL + 日期
- **交叉引用**：提及其他文件中已有的实体时，用相对链接 `[实体](文件名.md)`
- **命名规范**：raw/ 文件命名为 `{来源类型}-{日期}-{简称}.md`
- **文件拆分阈值**：单个 knowledge 文件超过 **2500 行**时，必须拆分为多个子文件（如 `aliyun-products-compute.md` / `aliyun-products-database.md`），并更新 index.md
- **过期标记机制**：知识条目标注的日期超过 12 个月未验证时，Lint 应标记为 `[待验证-YYYY]` 并建议用户确认或刷新
- **[[wikilink]] 支持**：提及其他 knowledge 文件中的实体时，使用 `[[entity-name]]` 格式标注（如 `[[PolarDB]]`、`[[百炼]]`），便于未来 Lint 自动检测断链
- **SHA256 增量检测**：ingest 时先对源文件计算 SHA256，若 raw/ 下已有相同 hash 文件则跳过蒸馏（节省 token）

## 验证命令

```bash
# 回归测试 — 验证知识库关键词覆盖率（阈值 85%）
python3 scripts/run-regression.py

# 快速检查文件行数
wc -l knowledge/*.md references/*.md
```

测试不通过时，先修复知识缺口再继续。

## 质量红线

详见 [SKILL.md](SKILL.md) 末尾“质量红线”章节（9 条）。Agent 必须严格遵守，此处不重复列举。

核心红线摘要：
- **写入优先** — 收到资料后第一个动作必须是写 inbox + changelog
- **增量更新** — 不删除仍有效的旧信息
- **标注来源** — `[官方]` / `[实战]` / `[推断]` + URL + 日期

## 搜索优先级

详见 [SKILL.md](SKILL.md) “搜索策略”章节。简要顺序：本地 knowledge/ → help.aliyun.com → ATA → WebSearch → 行业报告。

## 输出格式约定

详见 [SKILL.md](SKILL.md) “输出模板”章节。简要：
- **方案设计**：一句话方案 → 架构图 → BOM → 风险 → 路线图
- **产品选型**：对比表 + 推荐组合 + 边界提醒
- **资料消化**：来源 → 关键收获 → 刷新认知 → 落地位置
- **Lint 报告**：P0/P1/P2 分级 + 修复建议

## 协作模式

- 用户是 curator（策展人），决定什么值得蒸馏
- Agent 是 maintainer（维护者），负责所有写入和交叉引用
- 用户 "学习一下" = 触发 Ingest
- 用户问问题 = 触发 Query
- 高质量 Query 输出 = 自动触发 Query→Wiki 回写

## 错误恢复协议

当 Ingest 中途失败（session 断开、工具报错、上下文溢出）时：

```
1. 重新进入 session 后，立即检查 inbox.md 中状态为 pending/processing 的条目
2. 检查 changelog.md 是否有对应的 ⏳ 未关闭记录
3. 判断中断点：
   - 如果只写了 inbox 未蒸馏 → 从步骤 3 继续（归档 raw → 蒸馏）
   - 如果已蒸馏但未更新 index → 从步骤 6 继续
   - 如果完全无法确定进度 → 标记为 `[failed]` 并通知用户
4. 恢复完成后正常关闭（inbox done + changelog ✅）
```

## 并发写入保护

本项目设计为**单 agent 单 session 操作**。并发保护规则：

1. 启动时检查 `changelog.md` 最近一条记录的时间戳
2. 如果发现非本 session 产生的最近变更（如存在不认识的条目）：
   - **暂停写入**
   - 报告用户："检测到知识库有其他 session 的修改，建议先 diff 再合并"
   - 用户确认后再继续
3. 不允许多个 agent 同时写入同一个 knowledge 文件
