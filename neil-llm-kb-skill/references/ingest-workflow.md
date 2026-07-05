# Ingest — 源编译 SOP（2-Step CoT + 写入优先 + 增量预算）

## 触发条件

- 用户投喂文件（`.md` / `.pdf` / `.docx` / `.html` / 代码文件）
- 用户提供 URL（文章/文档/API 参考）
- 用户指定文件夹（批量导入）

---

## 步骤

### Step 1: 写入优先（红线规则 🔴）

**不可违反的红线**：任何 ingest 操作必须先登记，后执行。

1. 在 `wiki/inbox.md` 的 `Pending` 区追加条目：
   ```
   - [ ] YYYY-MM-DD source-slug | 来源描述（文件名/URL）
   ```
2. 在 `wiki/log.md` 追加记录：
   ```
   | YYYY-MM-DD | ⏳ Ingest 进行中 | source-slug — 开始处理 |
   ```

**为什么是红线**：防止处理中断导致状态丢失，确保任何时刻都能追溯"正在做什么"。

### Step 2: SHA256 对比

1. 计算源文件的 SHA256 哈希值
2. 对比 `raw/` 目录下已有文件的哈希（存储在文件头部 YAML frontmatter 中）
3. 判定：
   - **哈希匹配** → 跳过，inbox 标记 `[skip-unchanged]`，流程结束
   - **哈希不匹配** → 继续后续步骤
   - **新文件** → 继续后续步骤

### Step 3: 预算检查

1. 估算本次源文件将影响的 wiki 页面数（基于内容量和主题广度）
2. 对比 `INGEST_BUDGET`（默认值：15 页）
3. 判定：
   - **≤ INGEST_BUDGET** → 继续
   - **> INGEST_BUDGET** → 拆分为多批次，每批 ≤ 15 页，在 inbox 登记所有批次

预算估算公式参考：
```
预估页面数 ≈ ceil(源文件字数 / 2000) + 新实体数 + 新概念数
```

### Step 4: 归档 Raw

将原始全文存入 `raw/` 目录：

文件命名：`YYYYMMDD-slug.md`

文件格式：
```markdown
---
sha256: <hash>
source: <原始路径或URL>
ingested: YYYY-MM-DD
type: article | doc | code | url
---

# 原始标题

（原文全文，不做任何编辑）
```

**不可变原则**：raw 文件一旦写入，永不修改。如源文件更新，创建新的 raw 文件。

### Step 5: Step 1 分析（CoT 第一步）

LLM 阅读源文件，输出结构化分析（内部思考，不直接写入 wiki）：

```markdown
## 分析报告

### 关键实体
- Entity1 — 简述（新增/已有）
- Entity2 — 简述（新增/已有）

### 核心概念
- Concept1 — 定义 + 重要性
- Concept2 — 定义 + 重要性

### 与现有 Wiki 的连接点
- [[existing-page-1]] — 可补充/可更新的内容
- [[existing-page-2]] — 相关但无需修改

### 矛盾/张力
- 现有页面 X 说"A"，新源说"B" → 需要处理

### 结构建议
- 建议新增页面：page-name-1（entities/）, page-name-2（concepts/）
- 建议更新页面：existing-page-1
- 建议目录：guides/ 或 comparisons/
```

### Step 6: Step 2 生成（CoT 第二步）

基于 Step 5 的分析结果，创建/更新 wiki 页面。

**每页标准结构（四段落）**：

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [raw/YYYYMMDD-slug.md]
evidence: primary | derived | inferred
---

# 页面标题

## 概述
（2-3 句话概括核心要点）

## 详细
（完整展开，包含关键参数/步骤/细节）

## 交叉引用
- [[related-page-1]] — 关联说明
- [[related-page-2]] — 关联说明

## 来源
- [primary] raw/YYYYMMDD-slug.md — 章节X
- [derived] 基于实战验证的结论
```

### Step 7: 维护 [[wikilink]]

1. 扫描新增/更新页面中的所有 `[[page-name]]` 引用
2. 确认被引用页面是否存在：
   - **存在** → 在被引用页面的"交叉引用"区添加反向链接
   - **不存在** → 记录为"缺页"（lint 时处理），但保留引用
3. 使用 `[[page-name]]` 格式（不含路径前缀，不含 `.md` 后缀）

### Step 8: 更新索引和状态

1. **index.md**：在对应分区添加新条目
   ```
   - [[page-name]] — 一句话描述
   ```
2. **inbox.md**：将当前条目从 `Pending` 移到 `Done`
   ```
   - [x] YYYY-MM-DD source-slug | 完成，生成 N 页（page1, page2, ...）
   ```
3. **log.md**：追加完成记录
   ```
   | YYYY-MM-DD | ✅ Ingest 完成 | source-slug → 新增 X 页，更新 Y 页 |
   ```

### Step 9: 输出摘要

向用户报告本次 ingest 结果：

```
📥 Ingest 完成：source-slug

学到什么：
- [新概念] concept-name — 简述
- [新实体] entity-name — 简述

刷新什么：
- [更新] existing-page — 补充了 XX 内容

落地到哪：
- wiki/entities/entity-name.md（新增）
- wiki/concepts/concept-name.md（新增）
- wiki/guides/existing-page.md（更新）
```

---

## 蒸馏原则

### 保留（高价值信息）

| 类型 | 示例 |
|------|------|
| 能力边界 | "支持最大 10MB 文件"、"不支持嵌套超过 5 层" |
| 适用场景 | "适用于实时流处理，不适用于批处理" |
| 关键参数 | "timeout 默认 30s，建议生产环境设为 60s" |
| 实战案例 | "在 1000 QPS 下表现稳定" |
| 避坑指南 | "不要在循环中调用，会导致 N+1 问题" |

### 丢弃（低价值信息）

| 类型 | 示例 |
|------|------|
| 冗余背景 | 已在其他页面覆盖的历史介绍 |
| 过时参数 | 已废弃版本的配置方式 |
| 纯营销内容 | "业界领先"、"颠覆性创新" |
| 重复示例 | 同一概念的多个类似 demo |

---

## 证据等级标注规则

每条知识必须标注证据等级：

| 标注 | 含义 | 来源要求 | 可信度 |
|------|------|---------|--------|
| `[primary]` | 官方文档 / 一手来源 | 需提供 raw 文件路径或官方 URL | ⭐⭐⭐ |
| `[derived]` | 实战验证 / 二手分析 | 需说明验证场景和条件 | ⭐⭐ |
| `[inferred]` | LLM 推理 / 未验证 | 需标注推理依据 | ⭐ |

**规则**：
- 优先使用 `[primary]`，有官方来源必须引用
- `[derived]` 需说明"谁在什么场景下验证的"
- `[inferred]` 不得超过页面内容的 30%
- 混合等级时，按段落逐一标注
