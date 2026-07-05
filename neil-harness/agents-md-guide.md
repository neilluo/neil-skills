# AGENTS.md Writing Guide

The most critical file in your harness. Gets it right and agent productivity multiplies; get it wrong and every session starts confused.

---

## Core Principle: Index, Not Manual

AGENTS.md is a **table of contents**, not an encyclopedia. It tells the agent:
1. What this project IS (2 sentences)
2. What tech it uses (1 table)
3. How to run it (3-5 commands)
4. Where to find details (navigation table)
5. What rules are non-negotiable (5-10 bullet points)

Everything else lives in `.harness/docs/` and is loaded on demand.

---

## ETH Zurich Research Data

- Auto-generated AGENTS.md **decreases** success rate by ~3% and increases cost >20%.
- Human-written AGENTS.md improves success rate by only ~4%.
- Tools/commands mentioned in AGENTS.md get used **160x more often**.
- Frontier models reliably execute ~150-200 instructions. Harness overhead takes ~50. You get 100-150 for your AGENTS.md.
- **Target: <150 lines total. Ideal: ~60 lines.**

---

## Template

```markdown
# [Project Name]

> [One-line description of what this project does]

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | [Language] + [Framework] + [ORM/DB layer] |
| Frontend | [Framework] + [Language] + [UI library] + [Build tool] |
| Database | [DB name + extensions] |
| External | [APIs, cloud services] |

## Commands

```bash
# Build
[build command]

# Run
[run command]

# Test
[test command]

# Lint
[lint command]
```

## Documentation

| Doc | Purpose | Link |
|-----|---------|------|
| Architecture | Code map, file-by-file guide | [-> view](.harness/docs/architecture.md) |
| Database | Schema, connection details | [-> view](.harness/docs/database.md) |
| [Domain doc] | [What it covers] | [-> view](.harness/docs/[file].md) |
| Rules | Coding standards | [-> view](.harness/rules/) |
| Lessons | Past learnings | [-> view](.harness/lessons/learnings.md) |

## Critical Rules

1. [Most important rule -- the one that causes the most bugs when violated]
2. [Second most important rule]
3. [Third ...]
4. ...
5. [No more than 10 rules here. Full rules in .harness/rules/]

## Warnings

- **[Critical warning]**: [What NOT to do and why]
```

---

## Section-by-Section Guidance

### Project Identity (2 lines max)

Good:
```markdown
# Lock
> Door surveillance video AI analysis: upload -> OSS -> Qwen-VL understanding -> vectorize -> semantic search
```

Bad:
```markdown
# Lock Project - AI Video Analysis Platform
This project is a comprehensive platform designed to help users upload their door surveillance videos,
which are then stored in Alibaba Cloud OSS and analyzed using the Qwen-VL multimodal model...
[3 more paragraphs]
```

### Tech Stack (1 table)

List every major technology. This is how the agent knows what tools and patterns to use. Be specific about versions when they affect APIs.

### Commands (3-5 lines)

**This is the highest-ROI section.** Tools mentioned here get used 160x more. Include:
- Build/compile command
- Run/start command
- Test command (with variants if applicable)
- Lint/format command
- Any project-specific scripts (start.sh, deploy.sh)

### Documentation Table

The navigation table implements **progressive disclosure**. Agent reads AGENTS.md first (~100 tokens), then follows links only when needed.

Rules for the table:
- Every row must link to an actual file that exists.
- Use relative paths from project root.
- "Purpose" column should be 3-8 words.
- Order by frequency of use (most-accessed docs first).

### Critical Rules (5-10 max)

These are the rules that, when violated, cause the most damage. Not coding style rules -- structural integrity rules.

Good critical rules:
- "All API responses must use `ApiResponse<T>` wrapper."
- "Database changes only through migration scripts, never direct DDL."
- "Domain layer must be pure -- no framework dependencies."
- "Don't use SQLite tools; this project uses PostgreSQL."

Bad critical rules (too vague):
- "Write clean code."
- "Follow best practices."
- "Test your code."

### Warnings

For things that are **actively dangerous** or frequently cause agent confusion. Use sparingly (1-3 items max).

---

## Anti-Patterns

### 1. The Encyclopedia
AGENTS.md is 400+ lines with full coding standards, API docs, architecture details, troubleshooting guides. Fix: Extract everything except the 5 sections above into `.harness/docs/`.

### 2. The Ghost Reference
Links to files that don't exist or have been moved. Fix: Validate all links after changes.

### 3. The Tutorial
Step-by-step instructions like "First, create a new file..." The agent already knows how to create files. Fix: State the WHAT and WHY, not the HOW.

### 4. The Wishlist
Rules that describe aspirational practices not actually enforced. Fix: Only include rules that are real constraints, not goals.

### 5. No Commands
Agent doesn't know how to build, test, or lint. Fix: Add the Commands section -- highest ROI improvement.

---

## Adaptation by Project Type

### Monorepo
Add a "Project Structure" section above Tech Stack:
```markdown
## Structure
| Package | Purpose |
|---------|---------|
| apps/web | React frontend |
| apps/api | Node.js backend |
| packages/shared | Shared types and utils |
```

### Backend-Only
Drop frontend from Tech Stack table. Emphasize API contracts and database sections in the doc navigation.

### Frontend-Only
Drop backend from Tech Stack table. Emphasize component library and design system sections.

### Multi-Language
List each language's commands separately:
```bash
# Backend (Java)
mvn clean compile && mvn test

# Frontend (TypeScript)
npm run lint && npm run build
```
