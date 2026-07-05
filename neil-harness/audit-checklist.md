# Audit Checklist

Detailed scoring criteria for each harness dimension. Score 0-5 per dimension.

---

## Dimension 1: AGENTS.md Quality (0-5)

| Score | Criteria |
|-------|----------|
| 0 | No AGENTS.md or equivalent exists |
| 1 | Exists but is a generic README or >400 lines with no structure |
| 2 | Has project identity and tech stack, but inlines too much detail (>200 lines) |
| 3 | Reasonably structured, 100-200 lines, has doc navigation but still contains inline guides |
| 4 | Index-style, <150 lines, progressive disclosure via doc links, lists key commands |
| 5 | 60-150 lines, pure index, all details in linked docs, mentions key tools/commands, has critical rules section |

### What to check

- [ ] Line count (target: 60-150)
- [ ] Is it an index or a manual? (Count inline code blocks -- more than 3 is a red flag)
- [ ] Does it have a doc navigation table pointing to deeper docs?
- [ ] Does it list key commands (build, test, lint, run)?
- [ ] Does it declare project identity in 1-2 sentences?
- [ ] Does it list tech stack concisely?
- [ ] Does it have a "critical rules" section (top 5-10 rules)?
- [ ] Does it avoid tutorials/explanations that belong in reference docs?
- [ ] Are tools/commands mentioned? (Mentioned tools get used 160x more)

### Common problems

- **Bloated AGENTS.md**: Contains full coding standards, API docs, architecture details. Fix: Extract to `.harness/docs/`.
- **Missing commands**: Agent doesn't know how to build/test/lint. Fix: Add Commands section.
- **No progressive disclosure**: Everything in one file. Fix: Create doc navigation table.
- **Stale content**: Refers to files/tools that no longer exist. Fix: Verify all links.

---

## Dimension 2: Feedforward — Rules (0-5)

| Score | Criteria |
|-------|----------|
| 0 | No coding rules documented anywhere |
| 1 | Rules exist only inside AGENTS.md as bullet points |
| 2 | Separate rule files exist but without trigger metadata or structure |
| 3 | Rule files with triggers, organized by domain, but missing counter-examples |
| 4 | Well-structured rules with Do/Don't/Self-check pattern, glob or always_on triggers |
| 5 | Behavioral rules, <67 lines each, with self-checks, counter-examples, and stated tradeoffs |

### What to check

- [ ] Are rules in separate files (not inlined in AGENTS.md)?
- [ ] Do rule files have YAML frontmatter with `trigger`?
- [ ] Are rules organized by domain (backend, frontend, database, etc.)?
- [ ] Does each rule have counter-examples (wrong vs right)?
- [ ] Does each rule have a self-check criterion?
- [ ] Are rules behavioral (change decisions) rather than procedural (list steps)?
- [ ] Is each rule file under 100 lines (ideal: under 67)?
- [ ] Do rules state when they DON'T apply?

### Common problems

- **Rules as step-by-step procedures**: "Step 1: Open file. Step 2: Add import." Fix: Rewrite as behavioral constraints.
- **No enforcement mechanism**: Rules exist but nothing checks compliance. Fix: Add corresponding lint rules or hooks.
- **Too many rules**: Agent can reliably follow ~100-150 instructions. Fix: Prioritize, move lower-priority rules to reference docs.

---

## Dimension 3: Feedforward — Docs (0-5)

| Score | Criteria |
|-------|----------|
| 0 | No reference documentation beyond README |
| 1 | Some docs exist but not linked from AGENTS.md, agent unlikely to find them |
| 2 | Docs linked from AGENTS.md but not structured for agent consumption |
| 3 | Architecture doc exists, some reference docs, linked from AGENTS.md |
| 4 | Architecture code map + domain reference docs + linked from AGENTS.md with navigation table |
| 5 | Full progressive disclosure: index -> chapter -> appendix. Architecture map, database reference, API contracts, decision records. All agent-consumable. |

### What to check

- [ ] Does an architecture/code-map document exist? (Most valuable single doc)
- [ ] Is there a database schema reference?
- [ ] Are API contracts documented?
- [ ] Are docs organized in a discoverable directory (`.harness/docs/` or `docs/`)?
- [ ] Are docs linked from AGENTS.md's navigation table?
- [ ] Are docs written for agent consumption? (Structured, concise, no narrative fluff)
- [ ] Is progressive disclosure implemented? (Index -> detail -> appendix)
- [ ] Are there decision records (ADRs) for non-obvious choices?

### Common problems

- **Docs exist but agent can't find them**: Not linked from AGENTS.md. Fix: Add doc navigation table.
- **Docs too long**: Agent's context gets flooded. Fix: Split into focused chapters.
- **No architecture map**: Agent doesn't know what files do. Fix: Create file-by-file code map.
- **Human-oriented docs**: Written for onboarding humans, too narrative for agents. Fix: Restructure as reference material.

---

## Dimension 4: Feedback — Hooks (0-5)

| Score | Criteria |
|-------|----------|
| 0 | No hooks, no automated checks on agent output |
| 1 | Manual reminder to run tests in AGENTS.md but no automation |
| 2 | One hook exists (e.g., auto-lint) but no quality gates |
| 3 | Post-edit lint + build gate configured |
| 4 | Post-edit lint + build gate + pre-completion checklist |
| 5 | Full hook system: post-edit lint, build gate, pre-completion checklist, loop detection, stop-on-failure |

### What to check

- [ ] Is there a post-edit lint/format hook?
- [ ] Is there a build/compile verification hook?
- [ ] Is there a pre-completion checklist (verify against spec before "done")?
- [ ] Is there loop detection (repeated edits to same file)?
- [ ] Is there a stop-on-failure mechanism (force agent to continue until tests pass)?
- [ ] Do hooks follow "success silent, failure loud" principle?
- [ ] Are hook error messages agent-friendly? (Include what went wrong + how to fix)

### Common problems

- **No feedback at all**: Agent can't self-correct. Fix: Add minimum viable hooks (lint + build).
- **Tests mentioned but not enforced**: AGENTS.md says "run tests" but no hook ensures it. Fix: Add test gate hook.
- **Error messages not actionable**: Linter output is cryptic. Fix: Custom linter rules with prompt-ready messages.
- **No escalation path**: Same mistake keeps happening. Fix: Docs -> Rule -> Linter -> Hard block.

---

## Dimension 5: Feedback — Tests & Lint (0-5)

| Score | Criteria |
|-------|----------|
| 0 | No test suite, no linter configured |
| 1 | Linter configured but not integrated into agent workflow |
| 2 | Linter + some tests, mentioned in AGENTS.md |
| 3 | Linter + test suite + clear test commands in AGENTS.md |
| 4 | Linter + comprehensive tests + test commands + CI integration |
| 5 | Linter with custom rules + comprehensive tests + type checking + CI + agent-friendly error messages |

### What to check

- [ ] Is a linter configured and runnable?
- [ ] Are lint commands listed in AGENTS.md?
- [ ] Does a test suite exist with meaningful coverage?
- [ ] Are test commands listed in AGENTS.md?
- [ ] Is type checking configured (TypeScript strict, Java compiler warnings)?
- [ ] Are there custom lint rules for project-specific patterns?
- [ ] Do linter errors include fix suggestions? (Agent-friendly messages)
- [ ] Is there CI that runs these checks?

### Common problems

- **Linter exists but agent doesn't know about it**: Not in AGENTS.md commands. Fix: Add to Commands section.
- **Tests exist but not categorized**: Agent doesn't know which tests to run for which changes. Fix: Add test matrix to AGENTS.md.
- **No custom lint rules**: Generic rules miss project-specific patterns. Fix: Add custom rules that encode project conventions.

---

## Dimension 6: Context Engineering (0-5)

| Score | Criteria |
|-------|----------|
| 0 | No context management strategy |
| 1 | All information in AGENTS.md, no progressive disclosure |
| 2 | Some docs separated but no loading strategy |
| 3 | Progressive disclosure + architecture doc, but no cross-session memory |
| 4 | Progressive disclosure + cross-session memory (learnings.md) + task tracking |
| 5 | Full context engineering: progressive disclosure, storage offloading, learnings log, task tracking, conditional loading (globs/triggers) |

### What to check

- [ ] Is progressive disclosure implemented? (Not everything in AGENTS.md)
- [ ] Is there cross-session memory? (learnings.md, progress.md)
- [ ] Is the learnings file append-only?
- [ ] Is there task tracking? (progress.md, task files)
- [ ] Are docs conditionally loaded? (Glob triggers, "read X only when working on Y")
- [ ] Is the context loading strategy documented? (What to load when)
- [ ] Is "repo as single source of truth" practiced? (No external dependencies for agent knowledge)

### Common problems

- **Context overload**: AGENTS.md + all rules + all docs loaded at once. Fix: Implement conditional loading.
- **No cross-session memory**: Agent rediscovers same issues. Fix: Add learnings.md.
- **Stale memory**: learnings.md has outdated entries. Fix: Periodic review and cleanup.

---

## Scoring Interpretation

| Total (X/30) | Grade | Meaning |
|--------------|-------|---------|
| 0-5 | F | No harness. Agent is flying blind. |
| 6-10 | D | Minimal harness. AGENTS.md exists but harness is incomplete. |
| 11-15 | C | Basic harness. Feedforward exists, feedback is weak. |
| 16-20 | B | Solid harness. Both feedforward and feedback functional. |
| 21-25 | A | Strong harness. Progressive disclosure, hooks, cross-session memory. |
| 26-30 | S | Elite harness. Full system with context engineering and escalation paths. |
