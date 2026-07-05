# LLM Knowledge Base Architecture: Authority Perspectives & Engineering Practice Report

## Executive Summary

This report synthesizes perspectives from top engineering voices and companies on LLM knowledge base architecture, the emerging "agent harness" pattern, and how compiled knowledge relates to modern AI-assisted development. The key finding: **the industry is converging on a layered model where compiled knowledge (wiki/CLAUDE.md/AGENTS.md) serves as the "feedforward" layer, while search/RAG serves as the "feedback" fallback** — validating the Karpathy pattern while adding important nuance about when each approach wins.

---

## Part 1: Authority Source Perspectives

### 1.1 Martin Fowler / ThoughtWorks

#### Birgitta Böckeler — "Harness Engineering for Coding Agent Users" (April 2026)

**URL**: https://martinfowler.com/articles/harness-engineering.html

The single most relevant framework for understanding how knowledge files fit into the agent architecture. Böckeler introduces a precise taxonomy:

> "Agent = Model + Harness. In coding agents, part of the harness is already built in (via the system prompt, or the chosen code retrieval mechanism). But coding agents also provide us with many features to build an **outer harness** specifically for our use case."

**Key Concepts:**

| Term | Definition |
|------|-----------|
| **Guides** (feedforward) | Anticipate agent behavior and steer it *before* it acts. AGENTS.md, Skills, architecture docs. |
| **Sensors** (feedback) | Observe *after* the agent acts and help it self-correct. Linters, tests, review agents. |
| **Computational** | Deterministic, CPU-run. Tests, type checkers, structural analysis. |
| **Inferential** | Semantic, GPU-run. AI code review, "LLM as judge." Non-deterministic but rich. |

**Critical Insight for Wiki/Knowledge Layer:**
The compiled wiki is a **feedforward guide** — it increases the probability of correct first-pass output. This is exactly what CLAUDE.md, AGENTS.md, and compiled knowledge do: they are anticipatory context that prevents the "frustration loop."

**Inner vs Outer Harness:**
- **Inner harness**: What the coding agent builder ships (Anthropic's system prompt, Cursor's retrieval)
- **Outer harness**: What the *user* assembles — AGENTS.md, MCP servers, custom skills, organization rules

> "Harnesses are an attempt to externalise and make explicit what human developer experience brings to the table."

#### Rahul Garg — "Patterns for Reducing Friction in AI-Assisted Development" (Feb-April 2026)

**URL**: https://martinfowler.com/articles/reduce-friction-ai/

Five patterns that directly validate the compiled wiki approach:

1. **Knowledge Priming** — "Before asking AI to generate code, share curated context about the project... This practice is essentially **manual RAG** — filling the context window with high-value, project-specific information that overrides generic training data."

2. **Context Anchoring** — "Maintain a **living document** that captures decisions, constraints, and current state as a feature evolves. This document serves as **external memory**, anchoring context that would otherwise be lost."

3. **Encoding Team Standards** — "Make tacit knowledge explicit. Just as I would walk a new hire through our conventions, I make those defaults explicit and shareable."

4. **Feedback Flywheel** — "Systematically harvest learnings from AI interactions to improve the other four patterns."

**Key Quote:**
> "AI assistants are like junior developers with infinite energy but zero context. They can work faster than any human, they never tire, and they never complain. But they know nothing about a specific project's conventions, constraints, or history."

**Implication**: The compiled wiki is the "onboarding documentation" for AI teammates.

---

### 1.2 OpenAI

#### AGENTS.md — The Open Standard (2026)

**URL**: https://agents.md/

AGENTS.md emerged as an open format stewarded by the **Agentic AI Foundation under the Linux Foundation**, with support from OpenAI Codex, Google Jules, Cursor, Factory, Amp, and others.

**Philosophy:**
> "README.md files are for humans: quick starts, project descriptions, and contribution guidelines. AGENTS.md complements this by containing the extra, sometimes detailed context coding agents need: build steps, tests, and conventions that might clutter a README."

**Key Design Decisions:**
- No required fields — just standard Markdown
- Hierarchical: nearest AGENTS.md to the edited file wins
- Monorepo-friendly: nested AGENTS.md files per subproject (OpenAI's own repo has 88 AGENTS.md files)
- "Treat AGENTS.md as living documentation"

**Ecosystem Adoption** (60k+ repos on GitHub):
Supported by: OpenAI Codex, Google Jules, Cursor, Windsurf, Aider, VS Code, JetBrains Junie, GitHub Copilot, Devin, Zed, Warp, RooCode, Augment Code, and many more.

#### Harness Engineering Blog Post (Feb 2026)

**URL**: https://openai.com/index/harness-engineering/

OpenAI's internal team documented their approach:
> "Our most difficult challenges now center on **designing environments, feedback loops, and control systems**" rather than writing application code.

They started with "an empty git repository" and let Codex agents generate a million-line production system. The engineer's role shifted to:
- Defining constraints and architectural boundaries
- Writing structural tests and custom linters
- Running "garbage collection" that scans for drift

#### OpenAI's Practical Guide to Building Agents (2025)

**URL**: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/

Recommends the composable primitives approach: **models + tools + state/memory + orchestration**. Knowledge management isn't treated as a monolithic system but as composable layers.

---

### 1.3 Anthropic

#### CLAUDE.md — Project Memory System

**URL**: https://code.claude.com/docs/en/claude-directory

Anthropic's `.claude/` directory structure implements a complete knowledge architecture:

```
your-project/
├── CLAUDE.md              # Project instructions loaded every session
├── .mcp.json              # MCP server configurations
├── .claude/
│   ├── settings.json      # Permissions and model config
│   ├── rules/             # Path-scoped instructions (load conditionally)
│   ├── skills/            # Reusable task workflows (invoked by /name)
│   ├── subagents/         # Specialized agent definitions
│   └── memory/            # Auto-managed observations
└── ~/.claude/
    └── CLAUDE.md          # Global user-level instructions
```

**Key Design Principles:**
- "Target under 200 lines. Longer files still load in full but may reduce adherence"
- Conditional loading: rules load by path, skills load on invocation
- Memory is auto-managed observations, not manual wiki pages
- CLAUDE.md loads into every session — it's the "compiled knowledge" baseline

**Architectural Insight:**
This is a **tiered knowledge loading system**: always-on (CLAUDE.md) → path-triggered (rules/) → on-demand (skills/) → retrieval-based (codebase search). This mirrors the wiki architecture: index.md always loaded, category pages loaded by navigation, deep content loaded by search.

#### Effective Harnesses for Long-Running Agents (Nov 2025)

**URL**: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

Anthropic's most direct statement on knowledge architecture for agents:

> "The core challenge of long-running agents is that they must work in discrete sessions, and **each new session begins with no memory of what came before**."

**Their Solution — A Two-Part Harness:**

1. **Initializer Agent**: Sets up `init.sh`, `claude-progress.txt`, feature list (JSON), initial git commit
2. **Coding Agent**: Makes incremental progress, reads progress file + git log, updates state

**Critical Design Choice — JSON over Markdown:**
> "We use strongly-worded instructions like 'It is unacceptable to remove or edit tests.' After experimentation, we landed on using **JSON** for this, as the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files."

**State Management:**
- `claude-progress.txt` — what has been done (human-readable log)
- `feature_list.json` — what needs to be done (structured, immutable schema)
- Git history — what changed and when

**This validates the Karpathy pattern**: The wiki is a "progress file" that bridges context windows. The schema layer is the JSON feature list. The raw sources are the git history.

#### Prompt Caching and Compiled Knowledge

Anthropic's prompt caching reduces cost by 90% and latency by 85% for repeated prefixes. This has a direct implication for compiled knowledge: **a stable, compiled knowledge document placed at the beginning of the prompt benefits maximally from caching**. This makes the "always load CLAUDE.md first" pattern not just architecturally clean but economically optimal.

---

### 1.4 Simon Willison (datasette/llm author)

#### LLM Fragments — Personal Knowledge Compilation (April 2025)

**URL**: https://simonwillison.net/2025/Apr/7/long-context-llm/

Willison's approach is the **pragmatic anti-pattern** to heavy wiki compilation:

> "I've been using long context models via my **files-to-prompt** tool to summarize large codebases, explain how they work and even to debug gnarly bugs. It's surprisingly inexpensive to drop tens of thousands of tokens into models like GPT-4o mini."

**Key Tool: LLM Fragments**
- `-f filename` or `-f url` adds reusable text fragments to prompts
- Fragments are stored once (SHA256 deduplication) and can be attached to multiple prompts
- Plugins extend this: `github:` prefix loads entire repos, `docs:` prefix loads documentation

**Philosophy**: Instead of compiling knowledge upfront, use **long context + cheap inference** to process raw sources on the fly. This is the "RAG without the R" approach — just dump everything in.

**Contrarian Position to Karpathy:**
Willison never explicitly critiques the wiki pattern, but his tooling embodies a different philosophy: raw sources + long context windows may make compilation unnecessary for personal use. His `docs-for-llms` project (publishing pre-packaged documentation files) is actually a form of light compilation, however — just without the wiki's cross-referencing layer.

**Where this connects to llms.txt:**
> "llms-txt is a project led by Jeremy Howard that encourages projects to publish similar files to help LLMs ingest a succinct copy of their documentation."

This is compilation at the project level — a signal that even the "just use long context" camp recognizes the value of pre-compiled, LLM-optimized knowledge artifacts.

---

### 1.5 Cursor / IDE AI Tool Patterns

#### How Cursor Indexes Your Codebase (Jan 2026)

**URL**: https://towardsdatascience.com/how-cursor-actually-indexes-your-codebase/

Cursor's RAG pipeline:

```
Code → AST-based Semantic Chunking (tree-sitter)
  → Custom Embedding Model → Turbopuffer (vector DB)
  → Merkle Tree for Change Detection (5-min sync)
  → Hybrid Retrieval (semantic + regex/ripgrep)
  → LLM with retrieved context
```

**Key Architecture Decisions:**
- **Code chunking respects semantics**: splits between functions, not mid-line
- **Metadata enrichment**: file paths, line ranges stored alongside embeddings
- **Privacy**: only embeddings stored remotely; source code stays local
- **Incremental updates**: Merkle trees efficiently detect which files changed
- **Hybrid search**: semantic (vector) + exact (ripgrep) together

**The .cursorrules / Rules Pattern:**
`.cursorrules` (now deprecated in favor of `.cursor/rules/`) is Cursor's equivalent to CLAUDE.md — project-level instructions that load into every AI interaction. Combined with codebase indexing, this creates:
- **Layer 1**: Static knowledge (rules file) = compiled knowledge
- **Layer 2**: Dynamic retrieval (codebase RAG) = search/retrieval layer

**This is exactly the hybrid architecture**: compiled knowledge for the common cases + retrieval for edge cases.

---

## Part 2: Engineering Practice Cases

### 2.1 Stripe — Documentation as Product

**URL**: https://stripe.dev/blog/markdoc

Stripe's approach to documentation is the gold standard for "docs as code":

**Markdoc** — Custom authoring format balancing interactivity and maintainability:
- Extended Markdown with composable tags (conditionals, variables, content reuse)
- **Deliberately constrained**: No loops, no variable assignment — prevents content from becoming code
- CI validation ensures correctness at build time
- Interactive docs feel like an application, not a manual

**Key Design Philosophy:**
> "Mixing code and content provided a natural way to programmatically tailor the docs... but it posed serious challenges to quality and maintainability when the body of content grew to hundreds of pages."

**Relevance to Wiki Architecture:**
Stripe's Markdoc validates the idea that documentation systems need **constrained expressiveness** — enough structure to be machine-readable and maintainable, but not so much that they become programming environments. This is the same tension in CLAUDE.md (keep under 200 lines) vs wiki (comprehensive but structured).

Stripe also uses **"blueprints"** for integrating feedback sensors into agent workflows, and pre-push hooks that run relevant linters — validating the harness engineering model.

### 2.2 HashiCorp — Docs as Code

HashiCorp treats documentation as a first-class engineering artifact:
- **Unified Docs API** (github.com/hashicorp/web-unified-docs) hosts all product documentation
- Documentation lives in the same repository as code, goes through the same review process
- Changes to docs require the same CI/CD pipeline as code changes

**UK Government Digital Service** articulated the philosophy clearly:
> "Docs as code means applying software development processes and tools to technical documentation. We write content in a plain text format, manage it with version control, and automate builds."

### 2.3 Shopify — AI-Native Tooling Culture

**URL**: https://www.firstround.com/ai/shopify

Shopify's approach under Farhan Thawar (VP Engineering) goes beyond QMD to full organizational AI adoption:

**Key Principles:**
1. **"MCP everything"** — "We make every single piece of data inside the company available via MCP servers... ready for people to interrogate and figure out their own workflows."
2. **Unlimited AI spend** — No quotas; leaderboard of token usage as proxy for value
3. **One AI interface** — Internal LLM proxy for model access, MCP collection, pre-built agents
4. **Infrastructure-first** — "Instead of just building the feature, we'd rather spend longer building the infra."

**Real Workflow Examples:**
- Sales engineer built a "What should I do today?" dashboard pulling from Slack, Salesforce, GSuite via MCPs — "He literally doesn't work in any of those other tools anymore. He works in Cursor as his homepage."
- RFP agent answers hundreds of questions by leveraging an internal content repository (public docs, help docs, case studies) with certainty scores and learning from past wins.

**Tobi Lütke's AI Memo (April 2025):**
> "AI usage is now a baseline expectation at Shopify."

**Relevance**: Shopify validates the "compiled knowledge + retrieval" hybrid. Their internal content repository for the RFP agent is essentially a compiled knowledge base, while QMD provides search over personal/team notes. The key insight is making all knowledge MCP-accessible.

### 2.4 GitLab — Handbook-First Approach

**URL**: https://handbook.gitlab.com/handbook/company/culture/all-remote/handbook-first/

GitLab operates the world's largest publicly-accessible company handbook (~2000+ pages). Their philosophy is the closest enterprise analog to the Karpathy wiki pattern:

**Core Principles:**
1. **Write things down first, communicate second** — "We write things down first, and communicate that. This way there is no need for documentation after the communication."
2. **Single source of truth** — One canonical location for every piece of knowledge
3. **Handbook as forcing function** — Only 90 days of Slack retention, forcing durable documentation
4. **Everyone contributes** — Merge requests, not wiki edits; code owners approve

**Key Quotes:**
> "A handbook-first organization is home to team members who benefit from having a single source of truth. This type of organization is able to operate with almost **supernatural efficiency**."

> "An organization that does not put concerted effort into structured documentation has no choice but to watch its team members ask and re-ask for the same bits of data in perpetuity."

> "Documentation is never finished. They are evolving, living entities."

**Anti-wiki stance (on traditional wikis):**
> "A common belief is that a company wiki can serve as a handbook, but the reality is that **wikis do not scale**. They are designed to be updated by a select few... content frequently falls out of date."

**GitLab's solution**: Use version control (git) instead of wiki software. This enables distributed contribution, proper review, change history, and accountability.

**Relevance**: GitLab validates that the "compile everything into a single navigable knowledge structure" approach works at massive scale — but ONLY with proper tooling (git, CI, merge requests, code owners). The Karpathy wiki pattern using LLMs as the "maintenance workforce" solves the same problem GitLab solved with cultural norms + version control.

### 2.5 Notion — Knowledge Management + AI Agents

Notion's approach is "eating their own dog food" through **Custom Agents** (2025-2026):
- Every team at Notion (Environment, Engineering, Leadership) builds their own agents
- Agents operate on Notion's structured knowledge (databases, pages, relations)
- The knowledge management layer IS the agent's context

Their philosophy on knowledge management:
> "Organize information based on how people actually work, not idealized processes: Build your knowledge system to fit how teams naturally share and find information."

---

## Part 3: The "Agent Harness" Pattern

### 3.1 Academic Formalization

#### "Natural-Language Agent Harnesses" (Tsinghua, 2026)

**URL**: https://arxiv.org/html/2603.25723v1

This paper formalizes what AGENTS.md, CLAUDE.md, and wiki schemas are doing:

**Natural-Language Agent Harness (NLAH)** = a structured natural-language representation of:
- **Contracts**: required inputs/outputs, validation gates, stop rules
- **Roles**: solver, verifier, researcher, orchestrator
- **Stage structure**: plan → execute → verify → repair
- **Adapters/scripts**: deterministic hooks (tests, linters, verifiers)
- **State semantics**: what persists across steps, how it's reopened
- **Failure taxonomy**: named failure modes driving recovery

**Key Finding**: The paper demonstrates that harness logic expressed in natural language can achieve comparable performance to code-based harnesses when executed by a capable model — NLAH scored 74.4% on SWE-bench Verified.

**Implication for Wiki Schema**: The wiki's `schema.md` file IS a natural-language harness. It defines contracts (page structure), stage structure (ingest → compile → lint), state semantics (file paths, frontmatter), and failure modes (contradictions, orphans).

### 3.2 The "Thin Harness, Fat Skills" Ethos

**Source**: Han Chang Lee's "Hidden Technical Debt of AI Systems: Agent Harness" (May 2026)

**URL**: https://leehanchung.github.io/blogs/2026/05/08/hidden-technical-debt-agent-harness/

The most comprehensive synthesis of the harness engineering landscape:

**Three Optimization Surfaces:**

| Surface | Cost to Change | Iteration Cadence | Owned By |
|---------|---------------|-------------------|----------|
| Skills / prompts | Cheap — text edits | Hourly to daily | Product builders |
| Harness | Medium — code, ships with binary | Daily to weekly | Research/Applied AI |
| Model | Expensive — post-training compute | Quarterly | Research engineers |

**The Bitter Lesson for Agent Harness:**

> "Add structure for the level of compute you have, then remove it, because the structure becomes the bottleneck for the next level of compute." — Hyung Won Chung, Meta

What this means for compiled knowledge:
- 2023: RAG pipelines because models had small context windows
- 2024: Orchestrator-worker workflows because models couldn't tool-use reliably  
- 2025-2026: Single long-horizon agents with simple text files (progress.md, git log)
- **Memory layers are dissolving**: "Anthropic's long-running agent harness uses a JSON feature list, a progress file, and git log. Plain text in the working directory is something the model already knows how to read."

**Design Rule:**
> "Thin harness, fat skills. Build the durable substrate like you mean to keep it. Build each production harness like you mean to replace it. Treat application-facing scaffolding as a **90-day artifact**."

### 3.3 The Relationship: Agent Harness Files ↔ Wiki Schema Layer

| Agent Harness File | Wiki Equivalent | Function |
|-------------------|-----------------|----------|
| `AGENTS.md` | `schema.md` + `index.md` | Top-level instructions, conventions, navigation |
| `CLAUDE.md` | Wiki frontmatter conventions | Project-specific behavioral rules |
| `.cursorrules` | Style guide pages | Coding conventions and patterns |
| `.claude/rules/` | Category-specific wiki pages | Path-scoped / domain-specific knowledge |
| `.claude/skills/` | Wiki operation scripts (ingest, lint) | Reusable workflows |
| `claude-progress.txt` | `log.md` | State bridging across sessions |
| `feature_list.json` | Wiki schema constraints | Immutable structural contract |
| Git history | Raw sources folder | Audit trail and change provenance |

**The Wiki Schema IS a Harness Specification:**
- It defines the **feedforward controls** (what structure pages should have)
- It specifies **state semantics** (how information persists and is updated)
- It provides **contracts** (what makes a valid wiki page)
- The `lint` operation is a **feedback sensor** (detecting contradictions, orphans)

### 3.4 Birgitta Böckeler's Inner/Outer Harness Model Applied to Knowledge

```
┌─────────────────────────────────────────────┐
│  OUTER HARNESS (User-assembled)             │
│  ┌─────────────────────────────────────┐    │
│  │ AGENTS.md / CLAUDE.md / Wiki Schema │    │
│  │ (feedforward guides)                │    │
│  ├─────────────────────────────────────┤    │
│  │ MCP Servers / Skills / Tools        │    │
│  │ (operational interface)             │    │
│  ├─────────────────────────────────────┤    │
│  │ Linters / Tests / Review Agents     │    │
│  │ (feedback sensors)                  │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │  INNER HARNESS (Agent builder)      │    │
│  │  System prompt, RAG retrieval,      │    │
│  │  tool orchestration                 │    │
│  │  ┌─────────────────────────┐       │    │
│  │  │        MODEL            │       │    │
│  │  └─────────────────────────┘       │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

---

## Part 4: Contrarian Views & Criticisms

### 4.1 The "Bitter Lesson" Critique

**Source**: Han Chang Lee, citing Hyung Won Chung (Meta)

> "The progress of the last three years is the amount of hand-designed hard-coded orchestration logic in the harness retreating slowly into the model."

**Applied to Wiki Compilation:**
- Compiled wikis are structure added to compensate for model limitations (limited context, weak cross-reference)
- As models get 10M token contexts (Llama 4 Scout) and better reasoning, the compilation step may become unnecessary
- "Memory layers are dissolving... plain text in the working directory is something the model already knows how to read"

**Counter-argument**: Compilation isn't just about context window limitations — it's about **cognitive compression**. A well-compiled wiki provides synthesis and cross-referencing that raw sources don't, even if the model *could* process them all.

### 4.2 Token Cost Inversion

**Source**: Academic study (arxiv.org/html/2605.18490v1) from existing research

The RAG vs Wiki comparison found that **wiki uses 21× more tokens per query** due to tool-loop browsing. This contradicts the expected token savings narrative.

**Nuance**: The cost advantage of compilation is in *repeated* queries. First compilation is expensive; subsequent reads are cheap. For one-off queries, RAG wins on cost.

### 4.3 Maintenance Burden

**GitLab's observation**: "Documentation is never finished. They are evolving, living entities."

The criticism of compiled wikis is the **maintenance tax**:
- Every new source requires updating multiple wiki pages
- Cross-references can become stale
- The compilation step itself requires LLM calls (cost)
- Schema drift: as the domain evolves, the schema must evolve too

**Karpathy's counter**: "LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass." The maintenance is automated.

### 4.4 Simon Willison's Pragmatic Alternative

Rather than pre-compiling, Willison's approach says:
- Long context is cheap and getting cheaper
- `files-to-prompt` + `llm fragments` = "just load everything"
- De-duplication at the tool level (SHA256 hashing) prevents storage bloat
- No compilation step = no maintenance tax

**When this works**: Personal, ad-hoc queries where synthesis isn't needed
**When this fails**: Team knowledge sharing, persistent cross-session context, structured domains

### 4.5 The "90-Day Artifact" Warning

From the harness engineering community:
> "The teams that internalize this design their harness so the structure can come out as easily as it went in. The teams that do not are building load-bearing scaffolding around a model that is about to outgrow it."

**Applied to Wiki Schema**: The schema should be designed for easy evolution. Over-specification (too many constraints, too rigid structure) becomes technical debt when models improve.

---

## Part 5: Synthesis & Recommendations for SOP Skill

### 5.1 What the Evidence Validates

1. **Compiled knowledge as feedforward guide is correct** — Every authority source (Fowler/ThoughtWorks, OpenAI, Anthropic) validates that pre-loaded context dramatically improves first-pass quality.

2. **The layered loading model works** — Always-on (CLAUDE.md/index.md) → conditional (rules/categories) → on-demand (skills/search). Anthropic's architecture proves this.

3. **Schema as contract is correct** — Anthropic chose JSON for immutable structure; the wiki schema serves the same role. Define what's allowed, prevent drift.

4. **Living documentation beats static** — GitLab, Anthropic, and the harness community all emphasize "treat as living entity, never finished."

5. **Hybrid compilation + retrieval is the dominant pattern** — No one recommends pure compilation OR pure RAG in isolation at any scale beyond trivial.

### 5.2 What to Adopt in the SOP Skill

| Principle | Implementation |
|-----------|---------------|
| **Thin harness, fat skills** | Keep the schema layer minimal and evolvable. Put domain knowledge in wiki pages (skills), not in the orchestration logic (harness). |
| **Feedforward + Feedback** | Wiki = feedforward (pre-loaded context). Lint operation = feedback sensor. Both are needed. |
| **Tiered loading** | index.md always loaded → category navigation → full page retrieval → search fallback |
| **90-day mentality** | Design schema for easy evolution. Version it. Expect to refactor when models improve. |
| **JSON for contracts, Markdown for content** | Use JSON/YAML frontmatter for structural metadata (tags, dates, status). Use Markdown for the actual knowledge content. |
| **Git as audit trail** | Every wiki change committed. History = provenance. This is what Anthropic, GitLab, and the Karpathy pattern all use. |
| **MCP as access layer** | Expose wiki via MCP (like QMD, llm-wiki-mcp). This is what Shopify does: "MCP everything." |
| **Incremental progress pattern** | Adopt Anthropic's "progress file + incremental updates" model for wiki maintenance. |

### 5.3 Architecture Recommendation

```
┌─────────────────────────────────────────────────┐
│  SOP Skill Architecture                         │
├─────────────────────────────────────────────────┤
│                                                 │
│  SCHEMA LAYER (Agent Harness / Contract)        │
│  ├── schema.md (wiki structure rules)           │
│  ├── conventions.yaml (frontmatter contract)    │
│  └── operations.md (ingest/lint/query rules)    │
│                                                 │
│  COMPILED KNOWLEDGE LAYER (Feedforward)         │
│  ├── index.md (always-loaded navigation)        │
│  ├── categories/ (conditional loading)          │
│  └── pages/ (on-demand loading)                 │
│                                                 │
│  RAW SOURCES LAYER (Provenance)                 │
│  ├── sources/ (immutable inputs)                │
│  └── git history (change audit trail)           │
│                                                 │
│  RETRIEVAL LAYER (Feedback Fallback)            │
│  ├── QMD / search index (for 200+ pages)        │
│  └── MCP interface (agent access)              │
│                                                 │
│  FEEDBACK SENSORS                               │
│  ├── lint (contradictions, orphans, staleness)  │
│  └── coverage (are all sources represented?)    │
│                                                 │
└─────────────────────────────────────────────────┘
```

### 5.4 Key Quotes Summary

| Source | Quote |
|--------|-------|
| Birgitta Böckeler (ThoughtWorks) | "Agent = Model + Harness. A well-built outer harness serves two goals: increases probability agent gets it right, and provides a feedback loop that self-corrects." |
| Rahul Garg (ThoughtWorks) | "Knowledge Priming is essentially manual RAG — filling the context window with high-value, project-specific information." |
| Anthropic | "The key insight was finding a way for agents to quickly understand the state of work when starting with a fresh context window." |
| OpenAI (Harness Engineering) | "Our most difficult challenges now center on designing environments, feedback loops, and control systems." |
| Han Chang Lee | "Thin harness, fat skills. Build the durable substrate like you mean to keep it. Build each production harness like you mean to replace it." |
| GitLab | "A handbook-first organization operates with almost supernatural efficiency." |
| Shopify (Thawar) | "MCP everything. We make every single piece of data inside the company available." |
| Hyung Won Chung (Meta) | "Add structure for the level of compute you have, then remove it, because the structure becomes the bottleneck for the next level of compute." |
| Simon Willison | "It's surprisingly inexpensive to drop tens of thousands of tokens into models like GPT-4o mini, and the results are often very impressive." |
| NLAH Paper (Tsinghua) | "Harness logic expressed in natural language can be executed directly by a capable LLM runtime." |

---

## Source URLs Index

| Source | URL |
|--------|-----|
| Böckeler — Harness Engineering | https://martinfowler.com/articles/harness-engineering.html |
| Garg — Reducing Friction in AI | https://martinfowler.com/articles/reduce-friction-ai/ |
| Böckeler — Context Engineering | https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html |
| AGENTS.md Specification | https://agents.md/ |
| OpenAI — Harness Engineering | https://openai.com/index/harness-engineering/ |
| OpenAI — Practical Guide to Agents | https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/ |
| Anthropic — Effective Harnesses | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents |
| Anthropic — .claude Directory | https://code.claude.com/docs/en/claude-directory |
| Simon Willison — LLM Fragments | https://simonwillison.net/2025/Apr/7/long-context-llm/ |
| Cursor Indexing (TDS) | https://towardsdatascience.com/how-cursor-actually-indexes-your-codebase/ |
| Stripe — Markdoc | https://stripe.dev/blog/markdoc |
| GitLab — Handbook-First | https://handbook.gitlab.com/handbook/company/culture/all-remote/handbook-first/ |
| Shopify — First Round Interview | https://www.firstround.com/ai/shopify |
| NLAH Paper (Tsinghua) | https://arxiv.org/html/2603.25723v1 |
| Hidden Tech Debt: Agent Harness | https://leehanchung.github.io/blogs/2026/05/08/hidden-technical-debt-agent-harness/ |
| RAG vs Wiki Academic Study | https://arxiv.org/html/2605.18490v1 |
| AGENTS.md on GitHub (60k+) | https://github.com/search?q=path%3AAGENTS.md |
