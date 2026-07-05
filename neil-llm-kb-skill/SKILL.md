---
name: neil-llm-kb-skill
description: "Compile git repos and document collections into three-layer knowledge bases (raw → wiki → schema) with cross-referenced wiki pages, health scoring, and regression testing. Supports Codebase, Document, and Hybrid modes. Use when user mentions '创建知识库', '初始化KB', '生成wiki', '知识库工厂', 'neil-llm-kb', '蒸馏知识', 'wiki factory', 'LLM wiki', 'ingest', 'lint 知识库', 'KB health score', or wants to systematically compile scattered knowledge into a navigable knowledge base for AI agents."
---

# LLM Wiki 知识库工厂

## Overview

**将任意 git 仓库或文档集编译为 AI Agent 可直接使用的三层知识库（raw → wiki → schema）。**
核心原理：编译知识（wiki）作为 feedforward 预加载层提高 Agent 首次正确率，检索（RAG/QMD）作为 feedback 回退层处理边缘案例。

基于 Karpathy LLM Wiki 理念 + ThoughtWorks Harness Engineering + Anthropic 分层加载架构。

## When to Use

**触发症状：**
- 散落的文档/代码知识无法被 Agent 有效利用
- 团队新人 onboarding 反复问相同问题
- Agent 幻觉频发，缺乏项目上下文约束
- 调研报告/技术文章积累多但无结构化综合
- 想对代码库生成架构文档供 AI 使用
- 知识库已存在但质量不明，需要健康检查

## Quick Start

```
1. 用户说"初始化知识库" → Skill 自动检测项目类型 → 生成 kb/ 目录骨架
2. 用户说"学习一下 xxx.md" → Skill 执行 Ingest → 生成 wiki 页面
3. 用户提问 → Skill 从 wiki 检索 → 综合回答（必要时回写）
```

| 场景 | 操作 | 产出 |
|------|------|------|
| 新仓库入门 | `init` → `ingest --full` | 完整代码知识库 |
| 投喂 ATA 文章 | `ingest` 文章链接/文件 | 主题 wiki 页面 |
| 团队知识沉淀 | 持续 `ingest` + 定期 `lint` | 可搜索的团队知识图谱 |
| 知识库质量审计 | `lint --score` | P0/P1/P2 报告 + Health Score |

## When NOT to Use

| 场景 | 原因 | 替代方案 |
|------|------|----------|
| 快速变化的数据（日级更新） | 编译跟不上变化速度 | 直接 RAG / 搜索引擎 |
| 一次性问答（不需持久化） | 编译成本高于收益 | 直接搜索回答 |
| 超大规模（10k+ 文件） | 超出单 Agent 管理能力 | 专业 RAG 系统 + 部分热区 wiki |
| 纯结构化数据（数据库/表格） | 不适合 Markdown wiki 形态 | 数据分析工具 |
| 高度敏感信息 | wiki 文件明文存储 | 加密存储 + 权限控制系统 |

## 核心架构（Feedforward + Feedback 模型）

```
┌──────────────────────────────────────────────────┐
│  SCHEMA LAYER（Thin Harness / 90天制品心态）       │
│  精简可演化的合约，≤200行，JSON/YAML 元数据       │
├──────────────────────────────────────────────────┤
│  COMPILED KNOWLEDGE（Feedforward / 预加载）        │
│  Tier 1: index.md（always-on，每次会话必读）      │
│  Tier 2: category pages（按分类条件加载）         │
│  Tier 3: detail pages（按需加载）                 │
├──────────────────────────────────────────────────┤
│  RAW SOURCES（Provenance / 不可变）               │
│  原始资料 + git history 审计轨迹                  │
├──────────────────────────────────────────────────┤
│  RETRIEVAL LAYER（Feedback Fallback）              │
│  <50页: 无需 | 50-200: QMD keyword 备用           │
│  200-500: QMD 混合必需 | 500+: 搜索为主入口       │
├──────────────────────────────────────────────────┤
│  FEEDBACK SENSORS                                 │
│  Lint（矛盾/孤立/过时） + Regression（覆盖率）     │
└──────────────────────────────────────────────────┘
```

## 规模阈值决策树

```
START: 预期 wiki 页面数？

├── < 50 页（Small）
│   └── index.md 导航足够。无需搜索层。
│
├── 50-200 页（Medium）
│   └── 分层 index.md + QMD keyword 搜索备用
│
├── 200-500 页（Large）
│   └── QMD 混合搜索（BM25+向量+重排序）为必需
│       配置 QMD MCP Server
│
└── 500+ 页（XLarge）
    └── 搜索为主要入口，index.md 只是其中一个导航点
        建议 QMD + 编译 wiki 做热路径 + RAG 做长尾
```

## 自动检测逻辑

本 Skill 自动检测项目类型并选择对应策略：

| 信号 | 判定 | 策略 |
|------|------|------|
| 存在 package.json/pom.xml/go.mod/Cargo.toml | Codebase | 生成 5 类代码文章 |
| 存在 src/ + tests/ 结构 | Codebase | 按模块拆分 |
| 仅有 .md/.pdf/.docx 文件 | Document | 按主题编译 |
| 混合（代码+文档） | Hybrid | 代码→架构wiki + 文档→主题wiki |

**Codebase 模式生成 5 类文章**：
1. 模块概览（职责/边界/依赖）
2. 架构决策（ADR 风格）
3. 数据流图（请求如何流经系统）
4. 配置地图（环境变量/配置文件/Secret）
5. 依赖图谱（内部/外部依赖关系）

详见 [references/codebase-mode.md](references/codebase-mode.md)

**Document 模式生成 5 类文章**：
1. 领域综述（跨文档综合视图）
2. 核心实体页（工具/人物/框架实体）
3. 观点对比（方案 A vs B 分析）
4. 实践指南（How-to 步骤）
5. 时间线/演进（主题发展历史）

详见 [references/document-mode.md](references/document-mode.md)

**Hybrid 模式**：代码→Codebase Pipeline + 文档→Document Pipeline，统一交叉引用

详见 [references/hybrid-mode.md](references/hybrid-mode.md)

## 四大操作

### init — 初始化知识库

**触发**：用户说"初始化知识库""创建 KB""init"

详见 [references/init-workflow.md](references/init-workflow.md)

流程概要：
1. 检测项目类型（Codebase / Document / Hybrid）
2. 评估规模 → 确定 SCALE_TIER → 选择搜索策略
3. 扫描代表性文件（采样 10-20 个）
4. 从模板生成 SCHEMA.md（≤200 行，Thin Harness）
5. 从模板生成 AGENTS.md（对齐 Linux Foundation 开放标准）
6. 创建 kb/ 目录骨架
7. 生成 index.md + inbox.md + log.md
8. 若 SCALE_TIER >= medium：输出 QMD MCP 配置建议
9. 输出初始化报告

### ingest — 编译新源到 Wiki

**触发**：用户说"学习一下""蒸馏""ingest""投喂" + 文件/URL

详见 [references/ingest-workflow.md](references/ingest-workflow.md)

流程概要（2-Step CoT + 写入优先 + 增量预算）：
1. **写入优先**：inbox.md 登记 pending + log.md 追加 ⏳
2. SHA256 对比：跳过未变更文件
3. 预算检查：待更新页数 ≤ INGEST_BUDGET（默认 15）
4. Step 1 — 分析：LLM 读源 → 结构化分析
5. Step 2 — 生成：基于分析 → 生成/更新 wiki 页面
6. 维护 [[wikilink]] 交叉引用
7. 更新 index.md
8. inbox 改 done，log.md 标记完成
9. 输出摘要

### query — 基于 Wiki 回答问题

**触发**：用户提问且答案可能在知识库中

详见 [references/query-workflow.md](references/query-workflow.md)

流程概要（含回写门禁）：
1. 读 index.md 定位相关页面
2. 读 wiki 页面综合回答
3. 不足则回退 raw/
4. 仍不足则 WebSearch / QMD 搜索
5. 回写判定（跨页综合/纠错/新话题/深度解析）
6. **回写门禁**（防幻觉传播）：
   - 必须有明确来源（raw 文件/官方文档 URL）
   - 纯推理标注 [inferred]，不得标注 [primary]
   - 与现有 wiki 矛盾时标注 [disputed]，不直接覆盖
7. 执行回写（如通过门禁）

### lint — 健康检查

**触发**：用户说"lint""检查知识库""健康检查"；或每 5 次 ingest 后建议执行

详见 [references/lint-workflow.md](references/lint-workflow.md)

6 维检查：
1. 矛盾检测（同一事实跨页不一致）
2. 过时检测（>6 月未验证的标注时间信息）
3. 孤立页检测（无入站 [[引用]] 的页面）
4. 缺页检测（被提及但未创建的概念）
5. [[wikilink]] 完整性（断链检测）
6. 数据空白（可通过搜索补充的领域）

输出 P0/P1/P2 分级报告。

## 生成物结构

init 完成后生成的 kb/ 目录：

```
kb/
├── SCHEMA.md              # Wiki 维护规则（从 SCHEMA-TEMPLATE 生成）
├── AGENTS.md              # Agent 操作手册（从 AGENTS-TEMPLATE 生成）
├── raw/                   # Layer 1: 不可变源
│   └── {YYYYMMDD-slug}.md
├── wiki/                  # Layer 2: LLM 编译产物
│   ├── index.md           # 全局导航（always-on）
│   ├── inbox.md           # 来源状态机（pending/processing/done）
│   ├── log.md             # 操作时间线（append-only）
│   ├── entities/          # 实体页
│   ├── concepts/          # 概念页
│   ├── guides/            # 操作指南
│   └── comparisons/       # 对比分析
└── references/            # Layer 2 可选: 静态框架性内容
```

## MCP 集成指引

当 SCALE_TIER >= medium，推荐配置 QMD MCP：

```json
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

QMD 提供的 MCP 工具：
- `query` — 混合搜索（BM25 + 向量 + 重排序）
- `get` — 精确文档检索
- `multi_get` — 批量检索
- `status` — 索引健康状态

## 设计哲学

| 原则 | 说明 | 来源 |
|------|------|------|
| Thin harness, fat skills | Schema 精简可演化，知识放 wiki 页面 | Han Chang Lee / Anthropic |
| 写入优先 | 第一个动作必须是 inbox 登记，防上下文丢失 | neil-aliyun-sa 实战 |
| 回写门禁 | Query→Wiki 回写必须有事实来源，防幻觉传播 | Survivor Forge 教训 |
| 增量预算 | 单次 ingest ≤15 页更新，防雪崩 | 社区最佳实践 |
| 90天制品心态 | Schema 设计为可演化，不过度规范化 | Bitter Lesson |
| 混合策略 | Wiki 做稳定综合 + RAG/搜索做动态精确 | arxiv 学术验证 |
| Git = 审计 | 每次变更 commit，history = provenance | GitLab handbook-first |
| 多对一映射 | 多篇源文档编译为同一主题页，不做 1:1 | KBase 实践 (ATA) |
| 两阶段编译 | Stage 1 分类 → Stage 2 生成，减少中间态信息损失 | Compass 天基 (ATA) |
| AI 审核门禁 | 生成后审核再发布，不通过则带反馈重新生成 | Compass 天基 (ATA) |

## 最佳实践（阿里内部验证）

详见 [references/best-practices.md](references/best-practices.md)

核心要点：
- **多对一映射**：多篇散落文档 → 1 篇主题 Wiki（从情景记忆到语义记忆）
- **两阶段编译**：先分类（轻量）→ 再生成（保留完整上下文），减少信息损失
- **AI 审核闭环**：生成 → 审核 → 通过发布/不通过重新生成 → 反哺 Prompt
- **Schema 约束行为不约束分类**：不预设 Topic，让分类在 Ingest 中自然涌现
- **首次不求完美**：分批编译 → 检查遗漏 → 引导补充 → 增量迭代
- **领域适配清单**：7 个问题回答清楚即可复用到任何新领域

## KB Health Score（质量评分）

详见 [references/quality-score.md](references/quality-score.md)

总分 100 分 = 结构完整性(25) + 内容质量(30) + 连通性(20) + 新鲜度(15) + 覆盖率(10)

| 等级 | 分数 | 说明 |
|------|------|------|
| A+ | 95-100 | 生产就绪 |
| A | 85-94 | 优秀 |
| B | 70-84 | 良好 |
| C | 50-69 | 及格 |
| D | < 50 | 需重建 |

## 脚本工具箱

| 脚本 | 用途 | 命令 |
|------|------|------|
| `scripts/init.sh` | 初始化 kb/ 目录 | `./scripts/init.sh` |
| `scripts/ingest.sh` | 全量/增量 ingest | `./scripts/ingest.sh [--full]` |
| `scripts/query.sh` | 知识库问答 | `./scripts/query.sh "问题"` |
| `scripts/lint.sh` | 健康检查 | `./scripts/lint.sh [--score]` |
| `scripts/regression-template.py` | 回归测试 | `python3 scripts/regression-template.py` |
| `scripts/regression-cases-template.yaml` | 回归用例模板 | 复制到 `tests/` 后定制 |

## Common Mistakes

| 错误 | 后果 | 正确做法 |
|------|------|----------|
| 跳过写入优先，直接蒸馏 | 中断时丢失进度状态 | **先 inbox 登记，后执行** |
| 将 LLM 推理标为 [primary] | 幻觉传播到 wiki 污染知识库 | 标注 [inferred]，且不超 30% |
| 一次 ingest 超 15 页更新 | 质量崩溃，交叉引用缺失 | 遵守 INGEST_BUDGET 预算 |
| Query 回写无来源 | 幻觉入库，无法追溯 | **回写门禁：无源不写** |
| index.md 与实际页面不同步 | Agent 找不到已有知识 | 每次 ingest 后必须更新 index |
| 矛盾信息直接覆盖 | 丢失原始观点，无法回溯 | 用 [disputed] 并存，不覆盖 |
| 长期不执行 lint | 知识库静默腐烂 | 每 5 次 ingest 后 lint 一次 |

## 与其他 Skill 的协作

- 对已有 KB 执行 lint → 可作为 code review 的知识库维度
- 对新仓库执行 init + ingest → 快速生成项目知识库供其他 Agent 使用
- 配合 neil-coding-autopilot plugin 的 autopilot-loop skill → 知识库构建本身也可以 loop 迭代
- 配合 neil-harness → 知识库作为 harness 的知识层组件
