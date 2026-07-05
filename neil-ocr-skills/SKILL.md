---
name: neil-ocr-skills
description: Set up OpenCodeReview (OCR) for any git repository with DashScope/Qwen integration, and provide OCR usage guidance by consulting the source code. Use when the user mentions OCR setup, code review configuration, open-code-review, or asks how to use ocr CLI commands.
---

# Neil OCR Skills

Two core capabilities:
1. **Setup**: Configure OCR for a git repository (local CLI + GitHub Actions CI/CD)
2. **Usage Guide**: Answer OCR usage questions by consulting the source code at `/Users/neil/Desktop/neilcodebase/open-code-review`

---

## Capability 1: OCR Setup for a Repository

### Prerequisites Check

```bash
# 1. Verify OCR CLI is installed
ocr version
# If not installed:
npm install -g @alibaba-group/open-code-review

# 2. Verify DashScope API key exists
echo $DASHSCOPE_API_KEY
# Expected: sk-... (non-empty)
```

### Local Configuration

```bash
# Set provider and model
ocr config set provider dashscope
ocr config set model qwen3.7-max

# Test connectivity
ocr llm test
```

Config file location: `~/.opencodereview/config.json`

### GitHub Actions Setup

Follow this checklist:

```
Task Progress:
- [ ] Step 1: Create .github/workflows/ocr-review.yml in the target repo
- [ ] Step 2: Push workflow to default branch (master/main)
- [ ] Step 3: Set DASHSCOPE_API_KEY as repo secret
- [ ] Step 4: Create test PR to verify
```

**Step 1: Create workflow file**

Use the template in [reference.md](reference.md) section "GitHub Actions Workflow Template".

Key design decisions in the workflow:
- `pull_request_target` (not `pull_request`) — allows fork PRs to access secrets
- `fetch-depth: 0` — OCR needs full git history for diff
- `|| true` after ocr review — prevents workflow failure from blocking PR
- `concurrency.cancel-in-progress: true` — avoids duplicate runs on rapid pushes

**Step 2: Push to default branch**

The workflow MUST exist on the default branch (master/main) for `pull_request_target` to trigger.

**Step 3: Configure secret**

```bash
# Using gh CLI (preferred)
echo "$DASHSCOPE_API_KEY" | gh secret set DASHSCOPE_API_KEY --repo <owner>/<repo>

# If gh not authenticated:
# 1. brew install gh
# 2. gh auth login (device flow via browser)
# 3. Then set secret
```

**Step 4: Verify**

```bash
# Create test branch with a file containing intentional issues
git checkout -b test/ocr-verify
# Add test file, commit, push
gh pr create --title "test: verify OCR integration" --base master
# Check: gh run list --repo <owner>/<repo>
# Check: gh pr view <number> --comments
```

### OCR JSON Output Field Mapping

When writing the "Post review comments" step, use these actual OCR field names:

| OCR JSON field | Content |
|----------------|---------|
| `path` | File path (e.g., `src/main.py`) |
| `content` | Issue description text |
| `start_line` | Start line number |
| `end_line` | End line number |
| `existing_code` | Original code snippet |
| `suggestion_code` | Suggested fix code |
| `summary.files_reviewed` | Number of files reviewed |
| `summary.comments` | Number of issues found |
| `summary.total_tokens` | Token consumption |
| `summary.elapsed` | Time elapsed |

---

## Capability 2: OCR Usage Guidance

### Source Code Location

OCR source code is at: `/Users/neil/Desktop/neilcodebase/open-code-review`

### How to Answer Usage Questions

When the user asks "how do I do X with OCR":

1. **First**, check the relevant source files based on the topic:

| Topic | Source files to read |
|-------|---------------------|
| CLI commands & flags | `cmd/opencodereview/main.go`, `cmd/opencodereview/flags.go` |
| Provider configuration | `cmd/opencodereview/provider_cmd.go`, `cmd/opencodereview/config_cmd.go` |
| Supported LLM providers | `internal/llm/providers.go` |
| Endpoint resolution logic | `internal/llm/resolver.go` |
| Review execution flow | `cmd/opencodereview/review_cmd.go` |
| Output formatting | `cmd/opencodereview/output.go` |
| File filtering & rules | `internal/config/rules/system_rules.go` |
| Tool definitions | `internal/config/toolsconfig/tools.json` |
| Diff parsing | `internal/diff/parser.go`, `internal/diff/hunk.go` |
| Agent logic | `internal/agent/agent.go` |

2. **Read the actual source code** to provide accurate answers — never guess.

3. **Common queries and quick answers:**

```bash
# List all supported providers
ocr llm providers

# Test current LLM connection
ocr llm test

# Review workspace changes (staged + unstaged + untracked)
ocr review

# Review branch diff
ocr review --from main --to feature-branch

# Review single commit
ocr review --commit abc123

# Override model for one review
ocr review --model qwen3.7-plus

# Preview which files will be reviewed (no LLM calls)
ocr review --preview

# JSON output for CI
ocr review --from main --to dev --format json

# Agent mode (summary only, no progress)
ocr review --audience agent

# Provide business context
ocr review --background "Adding rate limiting to login API"

# Interactive provider setup
ocr config provider
ocr config model

# Non-interactive config
ocr config set provider dashscope
ocr config set model qwen3.7-max
ocr config set providers.dashscope.api_key "your-key"

# Custom provider
ocr config set provider my-gateway
ocr config set custom_providers.my-gateway.url https://gateway.internal.com/v1
ocr config set custom_providers.my-gateway.protocol openai
ocr config set custom_providers.my-gateway.model my-model
ocr config set custom_providers.my-gateway.api_key "key"
```

### Built-in Providers (from source)

| Provider | Base URL | Protocol | Env Var |
|----------|----------|----------|---------|
| dashscope | dashscope.aliyuncs.com/compatible-mode/v1 | openai | DASHSCOPE_API_KEY |
| dashscope-tokenplan | token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1 | openai | DASHSCOPE_TOKENPLAN_KEY |
| anthropic | api.anthropic.com | anthropic | ANTHROPIC_API_KEY |
| openai | api.openai.com/v1 | openai | OPENAI_API_KEY |
| volcengine | ark.cn-beijing.volces.com/api/v3 | openai | ARK_API_KEY |
| deepseek | api.deepseek.com | openai | DEEPSEEK_API_KEY |
| kimi | api.moonshot.cn/v1 | openai | MOONSHOT_API_KEY |

### Endpoint Resolution Priority

OCR resolves LLM endpoint in this order (first valid wins):
1. `~/.opencodereview/config.json` (provider or llm block)
2. OCR env vars (`OCR_LLM_URL`, `OCR_LLM_TOKEN`, `OCR_LLM_MODEL`)
3. Claude Code env (`ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_MODEL`)
4. Shell rc files (`~/.zshrc`, `~/.bashrc`)

Each layer requires all three fields (URL + Token + Model) non-empty.

---

## Additional Resources

- Complete GitHub Actions workflow template: [reference.md](reference.md)
- OCR source: `/Users/neil/Desktop/neilcodebase/open-code-review`
- OCR GitHub: https://github.com/alibaba/open-code-review
