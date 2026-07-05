# Reference: State Files

This skill keeps two JSON files under `~/.skill-installer/`. They're plain text, safe to read, safe to edit if you know what you're doing.

## tools.json

Maps a tool name to its skills directories.

```json
{
  "qoder": {
    "user": "~/.qoder/skills",
    "project": ".qoder/skills"
  },
  "qoderwork": {
    "user": "~/.qoderwork/skills",
    "project": ".qoderwork/skills"
  }
}
```

- `user` paths use `~` expansion.
- `project` paths are relative to the project root (resolved at install time).
- Built-in entries (`qoder`, `qoderwork`) are auto-restored if missing, but custom edits are preserved.

## installations.json

A flat array of records, one per install.

```json
[
  {
    "skill": "neil-bootstrap-skill",
    "source": "/Users/neil/Desktop/neilskills/neil-bootstrap-skill",
    "tool": "qoder",
    "scope": "user",
    "target": "/Users/neil/.qoder/skills/neil-bootstrap-skill",
    "mode": "symlink",
    "installed_at": "2026-05-16T10:00:00+00:00"
  }
]
```

- A record is uniquely keyed by `(skill, tool, scope, target)`.
- Re-installing the same combo replaces the old record (no duplicates).
- `installer.py doctor` walks this list to verify every symlink is still healthy.

## Manual Recovery

If you nuke `~/.skill-installer/`:

- `tools.json` regenerates with built-ins on next run.
- `installations.json` is rebuilt empty — your existing symlinks still work, but `list` / `doctor` will show nothing until you re-install.

## Migrating Sources

If you move your local skills folder (e.g. `~/Desktop/neilskills` → `~/skills`):

1. Update the source paths inside `installations.json` (or just re-run `install` with `--force`).
2. Symlinks point to absolute paths, so a move always breaks them — `doctor` will flag the broken ones.
