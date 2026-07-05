# {{PROJECT_NAME}} Wiki 维护规则 (Schema)

> 本文件定义 wiki/ 的结构规范、维护操作和质量标准。≤200行，可演化。
> 生成时间：{{GENERATED_DATE}} | 规模等级：{{SCALE_TIER}}

## 目标
{{PURPOSE}}

## 三层架构
raw/ → 不可变源（LLM只读）
wiki/ → LLM编译维护的结构化知识
SCHEMA.md → 本规则文件

## Wiki 目录结构
wiki/
├── index.md（全量索引，每次ingest后更新）
├── inbox.md（来源状态机：pending→processing→done）
├── log.md（操作时间线，append-only）
├── entities/（实体页）
├── concepts/（概念页）
├── guides/（操作指南）
├── comparisons/（对比分析）
└── references/（静态框架内容，可选）

## 页面格式规范
每个 wiki 页面必须包含四段落：
1. 概述（> 一句话描述）
2. 详细内容（表格/代码块/列表）
3. 交叉引用（[[wikilink]] 列表）
4. 来源（标注 raw 文件 + 证据等级）

## 证据等级
- [primary] — 官方文档/一手来源
- [derived] — 实战验证/二手分析
- [inferred] — LLM 推理/未验证

## 交叉引用规则
- 使用 [[page-name]] 格式（不含 .md 和目录前缀）
- 每页 ≥3 个出站引用
- 每次更新检查新增引用需求

## Ingest 操作
触发：新源加入
预算：单次最多更新 {{INGEST_BUDGET}} 页（默认15）
流程：写入优先 → SHA256检测 → 2-Step CoT → 更新wiki → 更新index/inbox/log

### 写入优先红线
ingest 的第一个动作必须是 inbox.md 登记 + log.md 追加。不可违反。

## Query 操作
触发：用户提问
流程：index.md → wiki页面 → raw/ → 外部搜索
回写门禁：必须有来源，纯推理标 [inferred]，矛盾标 [disputed]

## Lint 操作
触发：手动 / 每5次ingest建议
检查：矛盾(P0) / 过时(P1) / 孤立(P2) / 缺页(P1) / 断链(P1) / 空白(P2)

## 搜索策略
规模等级：{{SCALE_TIER}}
{{SEARCH_STRATEGY}}

## 质量标准
1. 不重复 raw — wiki 是综合提炼，不是复制
2. 可独立阅读 — 每页自成一体
3. 交叉引用丰富 — 平均 ≥3 出站引用
4. 面向回答 — 组织方式便于 Agent 快速定位
5. 标注来源 — 每页标注 raw 文件 + 证据等级
