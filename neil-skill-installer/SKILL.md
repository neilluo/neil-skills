---
name: neil-skill-installer
description: Install local Skill folders into target tools (qoder, qoderwork, or any user-registered tool) via symlink, so local edits propagate instantly with zero copy. Use when the user says "把这个 skill 装到 qoder/qoderwork", "导入 skill", "安装 skill 到工具", "skill 同步", or asks to register a new tool's skills directory.
---

# neil-skill-installer

Install a local Skill directory into a target tool's skills folder by creating a **symlink**, so updating the local source is instantly reflected in the tool — no copy, no manual sync.

Built-in tools: `qoder`, `qoderwork`. Any other tool must be registered once (path is then remembered forever).

## Core Idea

- **Mode**: symlink only. `<tool-skills-dir>/<skill-name>` → `<local-source>`
- **State**: persisted in `~/.skill-installer/` (decoupled from this skill)
  - `tools.json` — tool path registry
  - `installations.json` — installation records
- **Unknown tool** → must call `register-tool` first; once registered it works like the built-ins.

## STOP — Pre-Flight Checklist (MUST pass before any install)

Before running ANY `install` command, the agent MUST satisfy every row below. **No inference. No defaults. No shortcuts.** If anything is missing, STOP and ask.

| # | Field | Source rule |
|---|-------|-------------|
| 1 | **Source path** | User-provided, or unambiguously the current workspace folder. Confirm if doubtful. |
| 2 | **Tool** | User said it explicitly (e.g. "qoder", "qoderwork", or a previously registered tool name). |
| 3 | **Scope** | ⚠️ **HARD RULE — not inferable**. Must come from the user's own words: `user` / `project` / 用户级 / 项目级 / global / 全局 etc. The agent is **forbidden** to default, guess, or pick "the obvious one". |

### Why scope is non-inferable (anti-shortcut clauses)

These statements **do NOT** authorize a scope choice:

- ❌ "Install it for myself" → says nothing about user vs project.
- ❌ "Install into qoder" → tool only, scope unknown.
- ❌ "Install it so I can use it everywhere" → still ask; the user might mean both, or just user-scope.
- ❌ Anything the agent thinks is "the reasonable default".

Only explicit user wording counts. When in doubt → **ask**.

## Unknown Tool Handling

If the user mentions a tool not in the registry, ask:
- "I don't know where `<tool>` stores skills. What's the user-scope path? What's the project-scope path?"
- Then call `register-tool` to remember it permanently.

## Commands

All commands run via the bundled script. Use python3.

```bash
python3 scripts/installer.py <command> [args...]
```

### 1. Install a skill

```bash
python3 scripts/installer.py install <source-path> \
    --tool <tool> --scope <user|project> --scope-confirmed \
    [--name <override>] [--project-root <path>] [--force]
```

- Creates symlink `<tool-dir>/<skill-name>` → `<source-path>`.
- Default `<skill-name>` = source folder name. Override with `--name`.
- For `--scope project`, the target is resolved against `--project-root` (default: current working dir).
- If target already exists → **errors out**. Pass `--force` only if the user explicitly approves overwriting.
- **`--scope-confirmed` is REQUIRED for agent invocations.** It is the agent's signed promise that scope was explicitly stated by the user. Skipping it makes the script refuse.
- Human users running interactively can either pass `--scope-confirmed` themselves or `export SKILL_INSTALLER_TRUST_ME=1` once to silence the check.

### 2. Register a new tool

```bash
python3 scripts/installer.py register-tool <tool-name> --user-path <path> --project-path <path> [--force]
```

Example for a hypothetical `cursor` tool:
```bash
python3 scripts/installer.py register-tool cursor \
  --user-path "~/.cursor/skills" \
  --project-path ".cursor/skills"
```

After this, `--tool cursor` works just like the built-ins.

### 3. List installed skills

```bash
python3 scripts/installer.py list
```

### 4. Show registered tools

```bash
python3 scripts/installer.py tools
```

### 5. Uninstall

```bash
python3 scripts/installer.py uninstall <skill-name> --tool <tool> --scope <user|project> [--project-root <path>]
```

### 6. Doctor (health check)

```bash
python3 scripts/installer.py doctor
```

Verifies every recorded symlink still points to an existing source.

## Workflow

When the user asks to install a skill:

1. **Run the Pre-Flight Checklist above.** Verify every row is satisfied with explicit user input. If the user did not say which scope, STOP and ask before doing anything else.
2. **Tool known?**
   - Yes → proceed.
   - No → ask user for the user/project paths, run `register-tool`, then proceed.
3. **Run install** — the command MUST include `--scope-confirmed` (the script enforces this; without the flag it will refuse to run). Adding the flag is a promise that step 1 was actually performed.
4. **Report** — print the target path and remind that the symlink means future edits to the source propagate automatically.

### Self-verification before sending the command

Before you actually run `install`, silently answer:

- Did the user say `user` or `project` (or Chinese / equivalent) in their own words? **If no → STOP, ask.**
- Am I about to add `--scope-confirmed` because step 1 truly passed, or because the script demands it? **If the latter → STOP, ask.**

## Examples

**Example 1: Install a personal skill into qoder (user scope)** — user said "装到用户级"
```bash
python3 scripts/installer.py install \
  /Users/neil/Desktop/neilskills/neil-bootstrap-skill \
  --tool qoder --scope user --scope-confirmed
```

**Example 2: Install into qoderwork (project scope)** — user said "只在这个项目里用"
```bash
python3 scripts/installer.py install ./my-skill \
  --tool qoderwork --scope project --scope-confirmed
```

**Example 3: First-time use of an unregistered tool**
```bash
# 1) register the tool's paths once (no scope-confirmed needed for register-tool)
python3 scripts/installer.py register-tool cursor \
  --user-path "~/.cursor/skills" --project-path ".cursor/skills"

# 2) install as usual (after asking user for scope)
python3 scripts/installer.py install ./my-skill \
  --tool cursor --scope user --scope-confirmed
```

## Why symlink (not copy)

Local source edits → instantly reflected in every tool that has it linked.
No `sync` step, no version drift, no manual re-install.

## Notes

- macOS / Linux only (symlink semantics).
- Source must contain `SKILL.md`, otherwise the script refuses.
- State files (`tools.json`, `installations.json`) live in `~/.skill-installer/` — safe to back up, safe to edit by hand.

## Additional Resources

- For state file schema and advanced editing, see [reference.md](reference.md).
