---
name: neil-harness
description: Initialize or audit a project's AI agent harness system. Generates AGENTS.md, coding rules, feedback hooks, and quality gates following harness engineering best practices from OpenAI, Anthropic, Martin Fowler, and Karpathy. Also performs requirement analysis (Analyze Mode) and AGENTS.md self-evolution. Use when setting up a new project for AI-assisted development, auditing an existing project's harness, improving AGENTS.md, writing coding rules, configuring hooks, analyzing new requirements, or when the user mentions harness, agent setup, project initialization, harness audit, or requirement analysis.
---

# Harness Engineering

Agent = Model + Harness. This skill builds the **User Harness**: the project-specific layer you control.

## Three Control Surfaces

| Surface | Timing | Purpose | Artifacts |
|---------|--------|---------|-----------|
| **Feedforward** | Before agent acts | Guide behavior | AGENTS.md, rules, reference docs, skills |
| **Feedback** | After agent acts | Self-correction | Linters, tests, hooks, quality gates |
| **Context Engineering** | Runtime | Right info at right time | Progressive disclosure, storage offloading, lessons |

## Mode Detection

Determine mode by scanning the project root:

- **No AGENTS.md** at project root --> **Init mode**
- **AGENTS.md exists** + user提需求 --> **Analyze mode**
- **AGENTS.md exists** + user要审计/优化 --> **Audit mode**
- **Post-merge/Post-CR** --> **Evolve mode** (自进化)
- User explicitly requests one mode --> Follow user intent

---

## Init Mode: New Project

### Step 1: Discover Project DNA

Scan the project to extract:

```
Check for:
- Package managers: package.json, pom.xml, build.gradle, go.mod, requirements.txt
- Framework markers: src/main/java (Spring), src/app (Next.js), cmd/ (Go)
- Existing tooling: .eslintrc, checkstyle.xml, .editorconfig
- CI/CD: .github/workflows/, .gitlab-ci.yml
- Existing docs: README.md, SPEC.md, docs/
- Git conventions: last 20 commit messages for style inference
```

### Step 2: Generate Directory Structure

```
project-root/
├── AGENTS.md                  # Index document (60-150 lines MAX)
└── .harness/
    ├── rules/                 # Coding rules (frontmatter-triggered)
    ├── docs/                  # Reference docs (progressive disclosure)
    │   └── architecture.md    # Code map
    ├── hooks/                 # Feedback scripts
    ├── memory/                # Cross-session knowledge
    │   ├── learnings.md       # Append-only lesson log
    │   └── archive/           # Decayed entries
    └── skills/                # Project-specific skills
```

### Step 3: Write AGENTS.md

Key constraints:
- **60-150 lines maximum**. Every line must earn its place.
- **Index-style**: point to `.harness/docs/` for details, never inline them.
- **Five sections only**: Identity, Tech Stack, Commands, Doc Navigation, Critical Rules (top 5-10).

### Step 4: Write Rules

Create rules in `.harness/rules/`:
- Behavioral, not procedural
- Each rule has a self-check
- Include counter-examples
- 1 file per domain

### Step 5: Set Up Feedback

Three essential hooks:
1. Post-edit lint
2. Pre-completion checklist
3. Build gate

### Step 6: Bootstrap Context Engineering

Create `.harness/memory/learnings.md` + `.harness/docs/architecture.md`

---

## Analyze Mode: New Requirement (新增)

当用户提出新需求时，自动进行需求分析并输出可执行方案。

### Step 1: 读取项目上下文

```
读取:
1. AGENTS.md (项目架构概览)
2. .harness/docs/architecture.md (代码地图)
3. .harness/memory/learnings.md (历史经验)
4. 相关模块代码（通过 grep/目录扫描定位）
```

### Step 2: 需求分析

输出结构化分析：

```markdown
## 需求分析：{requirement}

### 影响范围
- 模块：[受影响的代码模块列表]
- 文件：[预计需要修改/新增的文件]
- 数据库：[是否需要Schema变更]

### 技术方案
- 方案选择：[技术方案及理由]
- 依赖：[新增依赖/库]
- 接口变更：[API增删改]

### 风险评估
- [风险1]：概率/影响/缓解
- [风险2]：...

### 与现有架构的关系
- 复用：[可复用的现有组件]
- 冲突：[潜在冲突点]
```

### Step 3: 生成/补充 Spec

- 如果是新功能 → 生成独立 spec 文件 `spec-{feature}.md`
- 如果是现有功能增强 → 补充到现有 SPEC.md
- 多轮自检（至少2轮：架构合理性 + 边界情况）

### Step 4: 拆解 Tasks

基于 spec 按原子性拆解，输出 `tasks-{feature}.md`：

```markdown
# Tasks: {feature}

## Task 1: {描述}
- 分支: task/01-{name}
- 内容: [详细实现指引]
- 验证: [验证命令]
- 依赖: [前置Task]

## Task 2: ...
```

---

## Audit Mode: Existing Project

### Step 1: Scan Artifacts

Search for all harness-related files (AGENTS.md, rules, hooks, lessons, docs, CI).

### Step 2: Score Each Dimension (0-5)

| Dimension | Score | Key Gap |
|-----------|-------|---------|
| AGENTS.md Quality | X/5 | ... |
| Feedforward: Rules | X/5 | ... |
| Feedback: Hooks/Tests | X/5 | ... |
| Context Engineering | X/5 | ... |
| Self-Evolution | X/5 | ... |

### Step 3: Generate & Execute Improvements

Order by ROI (quick wins first). Respect existing conventions.

---

## Evolve Mode: Self-Evolution (新增)

AGENTS.md 不需要人维护，由系统自动进化。

### 触发时机

- 每次 PR merge 后（post-merge reflection）
- CR 发现规律性问题时
- 定期审计发现膨胀时

### 进化规则

**添加条件**（全部满足才加）：
- 失败驱动：是因为踩坑才发现的
- 普遍适用：不是一次性问题
- 不可推断：Agent 不能从代码库自己发现

**删除/归档条件**：
- 可工具化：能用 linter/hook 强制的 → 移到 hook，从 AGENTS.md 删除
- 已过时：workaround 的根因已修复
- 权重衰减：30天未被引用 → 移入 `.harness/memory/archive/`

**硬性约束**：
- AGENTS.md 绝不超过 200 行
- 超过时自动触发 compaction（合并相似条目、归档低权重条目）

### 进化流程

```
1. 收集信号（CR评论 / 编译错误 / 重复踩坑）
2. 分类决策：
   - 能hook/linter强制 → 加规则（不改AGENTS.md）
   - 架构知识 → 更新 .harness/docs/architecture.md
   - 通用经验 → 评估是否加入AGENTS.md（检查200行上限）
   - 详细经验 → 追加 .harness/memory/learnings.md
3. 如果加入AGENTS.md：
   - 检查是否有语义重复条目 → 合并
   - 检查总行数 → 超200则compaction
4. 记录变更日志
```

### Compaction 策略

当 AGENTS.md 接近上限时：
1. 语义相似条目 → 合并为一条
2. 过于细节的描述 → 移到 rules/ 用 frontmatter 触发
3. 长期未引用的条目 → 移入 archive
4. 结果：保持根文件精简，知识不丢失（只是换位置）

---

## Universal Design Principles

### AGENTS.md
- It is an **INDEX**, not a manual. Point to docs, don't contain them.
- **Progressive disclosure**: root (~100 tokens) -> rules (<5k) -> docs (on demand).
- **Requests, not laws**: If a rule can't be broken, enforce it with a hook, not markdown.

### Rules
- Under 67 lines per rule file, every line has weight.
- Description is the routing mechanism.
- State the tradeoff.

### Feedback
- Computational over inferential (prefer linters over LLM-as-judge).
- Success silent, failure loud.
- Escalation path: Documentation -> Rule -> Linter -> Hard block.

### Context Engineering
- Storage offloading → persist to files for cross-session memory.
- Build to delete → design modules to be replaceable.
