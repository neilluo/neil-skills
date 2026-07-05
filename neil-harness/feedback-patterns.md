# Feedback Patterns

How to build the feedback layer: hooks, quality gates, linter escalation, and loop detection.

---

## Principle: Computational > Inferential

| Type | Execution | Cost | Reliability | Examples |
|------|-----------|------|-------------|---------|
| **Computational** | CPU, deterministic | Free/cheap | 100% consistent | Linters, type checkers, tests, build |
| **Inferential** | GPU, non-deterministic | Expensive | Variable | LLM-as-judge, AI code review |

**Always prefer computational checks.** Only use inferential when computational cannot cover the case (e.g., "does this code match the design intent?").

---

## The Three Essential Hooks

### 1. Post-Edit Lint Hook

Runs the project's linter/formatter after code changes. The single highest-ROI feedback mechanism.

**Template (adapt commands to your stack):**

```bash
#!/bin/bash
# .harness/hooks/post-edit.sh
# Runs after agent modifies code files.
# Exit 0 = pass, non-zero = fail (output goes to agent context).

CHANGED_FILES="$@"
EXIT_CODE=0

# --- Adapt this section to your project ---

# JavaScript/TypeScript
if echo "$CHANGED_FILES" | grep -qE '\.(ts|tsx|js|jsx)$'; then
    npx eslint $CHANGED_FILES --fix 2>&1
    EXIT_CODE=$((EXIT_CODE + $?))
    npx tsc --noEmit 2>&1
    EXIT_CODE=$((EXIT_CODE + $?))
fi

# Java
if echo "$CHANGED_FILES" | grep -qE '\.java$'; then
    mvn compile -q 2>&1
    EXIT_CODE=$((EXIT_CODE + $?))
fi

# Python
if echo "$CHANGED_FILES" | grep -qE '\.py$'; then
    ruff check $CHANGED_FILES 2>&1
    EXIT_CODE=$((EXIT_CODE + $?))
    mypy $CHANGED_FILES 2>&1
    EXIT_CODE=$((EXIT_CODE + $?))
fi

# Go
if echo "$CHANGED_FILES" | grep -qE '\.go$'; then
    go vet ./... 2>&1
    EXIT_CODE=$((EXIT_CODE + $?))
    golangci-lint run 2>&1
    EXIT_CODE=$((EXIT_CODE + $?))
fi

# --- End stack-specific section ---

exit $EXIT_CODE
```

### 2. Build Gate Hook

Ensures the project still compiles/builds after changes. Catches structural errors that lint alone misses.

**Template:**

```bash
#!/bin/bash
# .harness/hooks/build-gate.sh
# Runs after significant code changes.
# Exit 0 = pass, non-zero = fail.

# --- Adapt to your build system ---

# Maven (Java)
# mvn compile -q 2>&1

# npm/yarn (JavaScript/TypeScript)
# npm run build 2>&1

# Go
# go build ./... 2>&1

# Cargo (Rust)
# cargo build 2>&1

# Python (syntax check)
# python -m py_compile *.py 2>&1

exit $?
```

### 3. Pre-Completion Checklist

A markdown checklist the agent must verify before declaring a task "done". This is the **pre-completion validation** pattern from OpenAI and Anthropic.

**Template:**

```markdown
# Pre-Completion Checklist

Before declaring any task complete, verify every item:

## Code Quality
- [ ] Code compiles/builds without errors
- [ ] No linter warnings in changed files
- [ ] No type errors in changed files

## Tests
- [ ] All existing tests still pass
- [ ] New code has corresponding tests (if applicable)
- [ ] Edge cases are covered

## Cleanup
- [ ] No dead code left behind (unused imports, functions, variables)
- [ ] No commented-out code
- [ ] No TODO/FIXME added without a tracking issue

## Consistency
- [ ] Naming follows project conventions
- [ ] Code structure matches existing patterns in the codebase
- [ ] API responses use project's standard wrapper (if applicable)

## Documentation
- [ ] AGENTS.md updated if architecture changed
- [ ] Reference docs updated if contracts changed
- [ ] Learnings.md updated if non-obvious issue was encountered
```

---

## Advanced Patterns

### Escalation Path

When a pattern keeps being violated despite documentation:

```
Level 1: Documentation (AGENTS.md / .harness/docs/)
   ↓  (still violated)
Level 2: Rule (.harness/rules/ with trigger)
   ↓  (still violated)
Level 3: Linter (custom lint rule with agent-friendly error message)
   ↓  (still violated)
Level 4: Hard block (CI gate, pre-commit hook that rejects)
```

**Key insight from OpenAI**: Custom linter error messages should be written as prompts. Instead of "Error: method too long", write "This method exceeds 50 lines. Split it into smaller methods, each doing one thing. Consider extracting [specific logic] into a helper method."

### Agent-Friendly Error Messages

Transform cryptic linter output into actionable guidance:

```
# Bad error message (default linter)
error TS2322: Type 'string' is not assignable to type 'number'.

# Good error message (custom rule)
ERROR: Type mismatch at VideoService.ts:42.
Expected: number (videoId should be numeric)
Got: string
Fix: Use parseInt(videoId, 10) or update the type definition in src/types/video.ts
```

When writing custom lint rules, format the error message as if you're giving instructions to the agent.

### Loop Detection

Detect when the agent is stuck editing the same file repeatedly:

**Detection rule:**
If the same file has been edited more than 3 times in the same task without the issue being resolved, inject this message:

```
You've edited [filename] 3 times without resolving the issue.
Stop and reconsider your approach:
1. Re-read the error message carefully.
2. Check if you're solving the right problem.
3. Consider a completely different approach.
4. If stuck, ask the user for guidance.
```

### Stop Hook (Quality Gate)

Forces the agent to continue working until validation passes. Used for critical quality thresholds.

**Pattern:**

```
After agent signals "task complete":
1. Run post-edit lint hook
2. Run build gate hook
3. Run relevant test suite
4. If ANY check fails:
   - Inject failure details into agent context
   - Set `continue: true` to force agent to keep working
   - Agent must fix issues before completion is accepted
5. If ALL checks pass:
   - Accept completion
```

### Success Silent, Failure Loud

Only inject feedback into agent context when something goes **wrong**. Passing checks produce no output.

**Why**: Context window is limited. Every token of "Test passed! Build succeeded! Lint clean!" is wasted space that could be used for actual work.

**Implementation:**

```bash
# Good: only output on failure
mvn test -q 2>&1 || echo "TESTS FAILED: $(mvn test 2>&1 | tail -20)"

# Bad: verbose output always
mvn test 2>&1  # dumps hundreds of lines of "TEST PASSED" output
```

---

## Stack-Specific Feedback Configurations

### Java + Spring Boot
```
Post-edit: mvn compile -q
Build gate: mvn package -DskipTests -q
Tests: mvn test
Lint: checkstyle/spotless (if configured)
```

### TypeScript + React
```
Post-edit: npx tsc --noEmit && npx eslint [files]
Build gate: npm run build
Tests: npm test / npx vitest
Lint: eslint + prettier
```

### Python
```
Post-edit: ruff check [files] && mypy [files]
Build gate: python -m py_compile [files]
Tests: pytest
Lint: ruff + mypy
```

### Go
```
Post-edit: go vet ./... && golangci-lint run
Build gate: go build ./...
Tests: go test ./...
Lint: golangci-lint
```

### Rust
```
Post-edit: cargo check
Build gate: cargo build
Tests: cargo test
Lint: cargo clippy
```

---

## Feedback Integration Checklist

When setting up feedback for a project, verify:

- [ ] At least one computational check runs after code changes
- [ ] Build/compile verification exists
- [ ] Test commands are documented in AGENTS.md
- [ ] Pre-completion checklist is accessible
- [ ] Error messages are agent-friendly (include what to fix)
- [ ] Success is silent, failure is loud
- [ ] There's a path from "rule violated" to "automated enforcement"
