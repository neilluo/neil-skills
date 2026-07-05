# Directory Blueprint

The `.harness/` directory structure and what goes in each location.

---

## Full Structure

```
project-root/
├── AGENTS.md                          # THE entry point (60-150 lines)
├── .harness/
│   ├── rules/                         # Feedforward: coding rules
│   │   ├── backend-rules.md           # Backend-specific rules
│   │   ├── frontend-rules.md          # Frontend-specific rules
│   │   └── database-rules.md          # Database/migration rules
│   │
│   ├── docs/                          # Progressive disclosure: reference docs
│   │   ├── architecture.md            # Code map (most valuable doc)
│   │   ├── database.md                # Schema, connection, migration details
│   │   ├── api-contracts.md           # API endpoint specifications
│   │   ├── decisions/                 # Architecture Decision Records
│   │   │   └── 001-chose-x-over-y.md
│   │   └── guides/                    # Task-specific guides
│   │       ├── async-processing.md
│   │       └── error-handling.md
│   │
│   ├── hooks/                         # Feedback: automated checks
│   │   ├── post-edit.sh               # Runs after code changes
│   │   ├── pre-completion.md          # Checklist before declaring "done"
│   │   └── build-gate.sh              # Compile/build verification
│   │
│   ├── lessons/                       # Context engineering: memory
│   │   └── learnings.md               # Append-only cross-session log
│   │
│   └── skills/                        # Project-specific agent skills
│       └── [skill-name]/
│           └── SKILL.md
```

---

## File Purposes

### AGENTS.md (project root)

The only file the agent reads automatically at session start. Must be an **index** pointing to everything else. See [agents-md-guide.md](agents-md-guide.md).

### .harness/rules/

Coding rules that the agent should follow. Each file has YAML frontmatter controlling when it's loaded:

```yaml
---
trigger: always_on              # Loaded every session
---
```

```yaml
---
trigger: "**/*.java"            # Loaded only when editing Java files
---
```

```yaml
---
trigger: "**/migrations/**"     # Loaded only when working with migrations
---
```

**Naming convention**: `{domain}-rules.md` (e.g., `backend-rules.md`, `frontend-rules.md`, `testing-rules.md`)

**Content pattern**: Each rule should follow Do/Don't/Self-check:

```markdown
## [Rule Name]
**Do**: [Correct behavior] + code example
**Don't**: [Incorrect behavior] + code example
**Self-check**: [How agent verifies compliance]
```

### .harness/docs/

Reference documentation loaded on demand via progressive disclosure. The agent follows links from AGENTS.md's navigation table to read these files only when relevant.

#### architecture.md (most valuable)

A file-by-file code map. Format:

```markdown
# Architecture

## Project Structure
[Directory tree overview]

## [Layer/Module Name]
| File | Purpose |
|------|---------|
| path/to/file.ext | One-line description of what it does |
| ... | ... |

## Data Flow
[Key data flow diagrams in ASCII or mermaid]
```

#### database.md

Connection details, schema overview, migration conventions. Keep sensitive credentials in `.env` and reference them here.

#### api-contracts.md

Endpoint specifications. Format:

```markdown
## [Endpoint Group]
| Method | Path | Request | Response | Notes |
|--------|------|---------|----------|-------|
| POST | /api/v1/resource | { field: type } | ApiResponse<ResourceDto> | ... |
```

#### decisions/

Architecture Decision Records (ADR). One file per decision.

Format: `NNN-title.md` with sections: Context, Decision, Consequences.

#### guides/

Task-specific guides for non-obvious workflows. Only create when a pattern has caused repeated confusion. These are loaded by the agent on demand when working on related tasks.

### .harness/hooks/

Automated feedback scripts. Two forms:

**Shell scripts** (executable checks):
```bash
#!/bin/bash
# post-edit.sh - Run after code changes
# Exit 0 = pass, non-zero = fail with message

[lint/build/test commands]
```

**Markdown checklists** (agent self-checks):
```markdown
# Pre-Completion Checklist
Before declaring a task "done", verify:
- [ ] Code compiles without errors
- [ ] All existing tests still pass
- [ ] New code has corresponding tests
- [ ] No dead code left behind
- [ ] AGENTS.md updated if architecture changed
```

### .harness/lessons/learnings.md

Append-only log of non-obvious discoveries. The agent reads this at session start to avoid repeating past mistakes.

**Entry format:**

```markdown
## YYYY-MM-DD - [Topic]

**Problem**: [What went wrong]
**Solution**: [What fixed it]
**Lesson**: [One-line takeaway for future sessions]
```

**Rules:**
- Never edit or delete existing entries.
- New entries appended at the bottom.
- Keep each entry under 10 lines.
- Only record non-obvious findings (not "I forgot a semicolon").

### .harness/skills/

Project-specific agent skills. Each skill is a directory containing a `SKILL.md`. Skills are reusable capability packages -- for example, a "trace-debugger" skill that knows how to search project logs by traceId.

---

## Migration from Other Conventions

### From .qoder/

```
.qoder/rules/    -->  .harness/rules/     (direct move)
.qoder/hooks/    -->  .harness/hooks/     (direct move)
.qoder/lessons/  -->  .harness/lessons/   (direct move)
.qoder/skills/   -->  .harness/skills/    (direct move)
```

### From .ai/

```
.ai/tasks/       -->  .harness/tasks/     (optional: task tracking)
.ai/progress.md  -->  .harness/lessons/progress.md
.ai/learnings.md -->  .harness/lessons/learnings.md
```

### From .cursor/ or .cursorrules

```
.cursorrules     -->  Content merges into AGENTS.md + .harness/rules/
.cursor/         -->  .harness/ (restructure contents)
```

---

## Gitignore Recommendations

Add to `.gitignore`:

```
# Harness artifacts that should NOT be committed
.harness/lessons/learnings.md    # Optional: some teams commit this for shared learning
```

Add to `.gitignore` if using task tracking:

```
.harness/tasks/progress.md       # Session-specific, may contain noise
```

**DO commit:**
- AGENTS.md
- .harness/rules/
- .harness/docs/
- .harness/hooks/
- .harness/skills/

These are team-shared assets that define project conventions.
