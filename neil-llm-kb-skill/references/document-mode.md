# Document Mode — 文档集知识化 SOP

## 适用条件

- 项目仅包含 `.md` / `.pdf` / `.docx` / `.html` / `.txt` 文件
- 不存在 manifest 文件（无 `package.json` / `pom.xml` / `go.mod` 等）
- Init 阶段 `PROJECT_TYPE` 判定为 `Document`
- 典型场景：个人技术笔记库、团队调研报告集、行业白皮书归档、课程材料编纂

---

## 文档分类策略（三级）

### Level 1: 文件元数据分类

从文件名、目录结构、文件格式推断初始分类：

| 信号 | 推断分类 | 示例 |
|------|---------|------|
| 文件名含日期前缀 `YYYYMMDD-` | 时间线文档（日志/周报/纪要） | `20240115-sprint-review.md` |
| 目录名暗示类型 `research/` `notes/` | 按目录归类 | `research/llm-agents.md` |
| 文件格式为 `.pdf` / `.docx` | 正式文档（白皮书/规范/合同） | `alibaba-java-guide.pdf` |
| 文件名含 `vs` / `compare` / `对比` | 对比分析类 | `redis-vs-memcached.md` |
| 文件名含 `guide` / `how-to` / `教程` | 操作指南类 | `k8s-deployment-guide.md` |

### Level 2: 内容主题聚类

当 Level 1 分类粒度不足时，通过内容分析进行主题聚类：

1. 读取每个文件的前 500 字 + 标题/小标题结构
2. 提取关键实体（人名/工具名/概念名）
3. 按**主题相似性**分组：
   - 同一技术栈 → 聚为一组
   - 同一业务领域 → 聚为一组
   - 同一作者/来源 → 可作为辅助分组依据

### Level 3: 知识图谱关系推断

分析文档间的隐含关系：

- **引用关系**：文档 A 提到了文档 B 中的概念
- **时序关系**：同一主题的多篇文档按时间演进
- **依赖关系**：理解文档 B 需要先读文档 A
- **对立关系**：两篇文档对同一问题持不同观点

输出为 `[[wikilink]]` 交叉引用建议。

---

## 5 类必生成文章

对每个识别出的**主题领域**，生成以下 5 类文章：

### 类型 1: 领域综述

**路径**：`wiki/concepts/<domain-name>.md`

**模板**：

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: domain-overview
domain: <domain-name>
evidence: derived
sources: [raw/file1.md, raw/file2.md, ...]
---

# <Domain Name> — 领域综述

## 定义
<!-- 这个领域是什么，用 2-3 句话概括 -->

## 核心论点
- 论点 1（来源：[[source-page-1]]）
- 论点 2（来源：[[source-page-2]]）
- 论点 3（综合多源得出）

## 关键实体
| 实体 | 类型 | 说明 |
|------|------|------|
| Entity1 | 工具/人物/概念 | 一句话说明 |

## 知识边界
### 已覆盖
- 覆盖的子主题 1
- 覆盖的子主题 2

### 未覆盖（已知空白）
- 尚未有资料涉及的子主题

## 交叉引用
- [[related-domain-1]] — 关联说明
- [[related-domain-2]] — 关联说明
```

### 类型 2: 核心实体页

**路径**：`wiki/entities/<entity-name>.md`

**模板**：

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity
entity-type: tool | person | organization | framework | standard
evidence: primary | derived
sources: [raw/YYYYMMDD-slug.md]
---

# <Entity Name>

## 概述
<!-- 一句话描述这个实体是什么 -->

## 核心能力/特征
- 能力 1 — 具体说明
- 能力 2 — 具体说明

## 适用场景
| 场景 | 适合度 | 原因 |
|------|--------|------|
| 场景 A | ✅ 适合 | 原因说明 |
| 场景 B | ❌ 不适合 | 原因说明 |

## 关键参数/限制
| 参数 | 值 | 说明 |
|------|-----|------|
| 参数 1 | 具体值 | 补充说明 |

## 与其他实体的关系
- [[entity-a]] — 互补/竞争/依赖
- [[entity-b]] — 继承/替代

## 来源
- [primary] raw/YYYYMMDD-source.md — 具体章节
```

### 类型 3: 观点对比

**路径**：`wiki/comparisons/<topic>-comparison.md`

**模板**：

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: comparison
evidence: derived
sources: [raw/file1.md, raw/file2.md]
---

# <Topic> — 观点/方案对比

## 对比维度

| 维度 | 方案 A | 方案 B | 胜出 |
|------|--------|--------|------|
| 维度 1 | A 的表现 | B 的表现 | A/B/平 |
| 维度 2 | A 的表现 | B 的表现 | A/B/平 |

## 方案 A 详解
<!-- 来源：[[source-page]] -->
### 核心论点
### 优势
### 劣势

## 方案 B 详解
<!-- 来源：[[source-page]] -->
### 核心论点
### 优势
### 劣势

## 综合判断
<!-- 适用条件分析 -->
- 当 X 条件成立时 → 选 A
- 当 Y 条件成立时 → 选 B

## 来源
- [primary] raw/YYYYMMDD-a-perspective.md
- [primary] raw/YYYYMMDD-b-perspective.md
- [derived] 综合分析
```

### 类型 4: 实践指南

**路径**：`wiki/guides/<action-name>.md`

**模板**：

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: guide
difficulty: beginner | intermediate | advanced
evidence: primary | derived
sources: [raw/YYYYMMDD-slug.md]
---

# <Action Name> — 实践指南

## 前置条件
- 条件 1
- 条件 2

## 步骤

### Step 1: 标题
具体操作说明

```shell
# 如果有命令行示例
example-command --flag value
```

### Step 2: 标题
具体操作说明

## 验证方法
如何确认操作成功

## 常见问题
| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 问题 1 | 原因 | 方案 |

## 交叉引用
- [[related-guide]] — 下一步操作
- [[prerequisite-concept]] — 前置知识

## 来源
- [primary] raw/YYYYMMDD-source.md — 具体段落
```

### 类型 5: 时间线/演进

**路径**：`wiki/concepts/<topic>-evolution.md`

**模板**：

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: timeline
evidence: derived
sources: [raw/file1.md, raw/file2.md, ...]
---

# <Topic> — 演进时间线

## 时间线

| 时间 | 事件 | 影响 | 来源 |
|------|------|------|------|
| YYYY-MM | 事件描述 | 影响说明 | [[source-page]] |
| YYYY-MM | 事件描述 | 影响说明 | [[source-page]] |

## 阶段划分

### 阶段 1: 名称（时间范围）
- 特征
- 关键事件

### 阶段 2: 名称（时间范围）
- 特征
- 关键事件

## 趋势预判
<!-- 标注 [inferred]，基于时间线外推 -->

## 交叉引用
- [[related-concept]] — 平行发展的领域
- [[key-entity]] — 推动演进的关键实体
```

---

## 蒸馏优先级

从文档集提取知识时，按以下优先级分配精力：

```
跨文档综合 > 独特观点/洞察 > 实操步骤 > 数据/参数 >> 背景铺垫
```

| 优先级 | 类型 | 说明 | 投入比例 |
|--------|------|------|---------|
| P0 | 跨文档综合 | 多篇文档观点的交叉验证和综合 | 35% |
| P1 | 独特观点/洞察 | 非共识的原创见解、反直觉结论 | 25% |
| P2 | 实操步骤 | 可复用的具体操作方法 | 20% |
| P3 | 数据/参数 | 关键数值、基准线、阈值 | 15% |
| P4 | 背景铺垫 | 领域介绍、已知常识 | 5% |

**原则**：越不容易从单篇文档直接获得的综合性知识，蒸馏优先级越高。

---

## 文档预处理规则

### 格式转换

| 原始格式 | 处理方式 | 工具建议 |
|---------|---------|---------|
| `.md` | 直接归档 | — |
| `.pdf` | 转 Markdown 后归档 | MarkItDown / MinerU |
| `.docx` | 转 Markdown 后归档 | MarkItDown / pandoc |
| `.html` | 提取正文转 Markdown | trafilatura |
| URL | 抓取正文转 Markdown | trafilatura / Web Clipper |

### 归档命名规则

```
raw/YYYYMMDD-{slug}.md
```

slug 生成规则：
1. 取文档标题关键词（英文小写，连字符分隔）
2. 若无标题，取文件名（去后缀）
3. 若有重名，追加序号 `-2`、`-3`

示例：
- `raw/20240115-karpathy-llm-wiki.md`
- `raw/20240320-harness-engineering.md`
- `raw/20240320-harness-engineering-2.md`（同日同主题第二篇）

### 大文件拆分规则

当单个源文件超过 **8000 字**时：

1. 按文档自然章节拆分
2. 每个拆分片段独立归档：`raw/YYYYMMDD-slug-part1.md`、`raw/YYYYMMDD-slug-part2.md`
3. inbox.md 中登记所有片段，标注父文档关系
4. 蒸馏时维护片段间的连贯性

---

## 增量更新策略

### 触发机制

文档模式的增量更新触发条件：

1. **新文件加入** → 新增 raw + 全流程 ingest
2. **已有主题新资料** → 更新对应 wiki 页面（追加/修正）
3. **观点修正** → 使用 `[disputed]` 或 `[superseded]` 标注旧结论

### 影响范围确定

```
新源涉及的实体/概念
    ↓
查找 index.md 中已有的对应页面
    ↓
判定：新增页面 OR 更新已有页面
    ↓
追踪 [[wikilink]] 确定间接影响页面（最多 2 层）
```

### 更新规则

- **只更新受影响页面**（不全量刷新）
- **每次最多更新 15 页**（超出则分批）
- **优先更新**：领域综述 > 观点对比 > 实践指南 > 实体页 > 时间线
- **更新粒度**：段落级追加（不重写整页，保留已有内容，追加新信息）

---

## 忽略规则

以下文件在 Document Mode 中**始终忽略**：

```
.git/
.DS_Store
Thumbs.db
*.bak
*.tmp
*~
node_modules/
__pycache__/
.obsidian/    # Obsidian 配置目录（不是内容）
.trash/       # 回收站
```

**忽略原则**：
- 系统文件 → 忽略
- 编辑器临时文件 → 忽略
- 备份文件 → 忽略
- 配置目录（非内容） → 忽略

---

## 与 Codebase Mode 的差异对比

| 维度 | Document Mode | Codebase Mode |
|------|--------------|---------------|
| 输入特征 | 松散文档集（主题多样） | 结构化代码库（有 manifest） |
| 模块识别 | 主题聚类（语义驱动） | 目录/manifest（结构驱动） |
| 5 类文章 | 领域综述/实体/对比/指南/时间线 | 模块概览/ADR/数据流/配置/依赖 |
| 蒸馏重点 | 跨文档综合 > 独特观点 | 架构决策 > API 表面 |
| 更新触发 | 新文档加入 | 代码变更 (git diff) |
| 交叉引用密度 | 高（文档间关联是核心价值） | 中（模块间依赖较固定） |
| frontmatter 重点 | sources + evidence + domain | module + type + evidence |

---

## 示例：ATA 文章集 Ingest 场景

假设用户投喂 5 篇 ATA 关于"AI Agent 在研发流程中的应用"的文章：

**Step 1 分析输出**：
```markdown
### 关键实体
- Qoder（AI Coding Agent）— 新增
- Codex（OpenAI）— 新增
- Harness Engineering — 与已有 [[harness-concept]] 关联

### 核心概念
- Agent 幻觉防控 — 高优先级新概念
- 知识库分层加载 — 与已有 [[tiered-loading]] 关联

### 建议生成
- wiki/concepts/ai-agent-in-rnd.md（领域综述）
- wiki/entities/qoder.md（实体页）
- wiki/comparisons/agent-vs-copilot.md（对比页）
- wiki/guides/agent-harness-setup.md（指南页）
- wiki/concepts/ai-agent-evolution.md（时间线）
```

**Step 2 生成**：按上述建议创建 5 个页面，维护交叉引用。
