#!/usr/bin/env python3
"""
neil-skill-installer

Install/manage local Skill folders into target tools (qoder, qoderwork, ...) via symlink.

State files (single source of truth, decoupled from this skill folder):
  ~/.skill-installer/tools.json          - tool path registry
  ~/.skill-installer/installations.json  - installation records

Conventions:
  - A "skill source" is a local directory containing a SKILL.md file.
  - The directory name is used as <skill-name> by default.
  - Installation = create a symlink at <tool-path>/<skill-name> -> <source-abs-path>.
  - Updates to the local source are reflected instantly through the symlink (zero-copy).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STATE_DIR = Path.home() / ".skill-installer"
TOOLS_FILE = STATE_DIR / "tools.json"
INSTALLS_FILE = STATE_DIR / "installations.json"

# Built-in tools shipped with this skill. Users can add more via `register-tool`.
DEFAULT_TOOLS: dict[str, dict[str, str]] = {
    "qoder": {
        "user": "~/.qoder/skills",
        "project": ".qoder/skills",
    },
    "qoderwork": {
        "user": "~/.qoderwork/skills",
        "project": ".qoderwork/skills",
    },
}


# ---------- state helpers ----------
def _ensure_state() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if not TOOLS_FILE.exists():
        _write_json(TOOLS_FILE, DEFAULT_TOOLS)
    else:
        # Merge: ensure built-ins are always present (non-destructive for user edits).
        tools = _read_json(TOOLS_FILE, {})
        changed = False
        for name, paths in DEFAULT_TOOLS.items():
            if name not in tools:
                tools[name] = paths
                changed = True
        if changed:
            _write_json(TOOLS_FILE, tools)
    if not INSTALLS_FILE.exists():
        _write_json(INSTALLS_FILE, [])


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ---------- path resolution ----------
def _resolve_target_dir(tool: str, scope: str, project_root: Path | None) -> Path:
    """Return the absolute directory where <skill-name> will be installed."""
    tools = _read_json(TOOLS_FILE, {})
    if tool not in tools:
        raise SystemExit(
            f"[error] unknown tool '{tool}'. "
            f"Use `register-tool {tool} --user-path ... --project-path ...` first."
        )
    if scope not in ("user", "project"):
        raise SystemExit(f"[error] scope must be 'user' or 'project', got '{scope}'.")
    template = tools[tool].get(scope)
    if not template:
        raise SystemExit(f"[error] tool '{tool}' has no '{scope}' path registered.")

    if scope == "user":
        return Path(os.path.expanduser(template)).resolve()

    # project scope
    base = project_root if project_root else Path.cwd()
    return (base / template).resolve()


def _validate_source(source: Path) -> Path:
    src = source.expanduser().resolve()
    if not src.is_dir():
        raise SystemExit(f"[error] source '{src}' is not a directory.")
    if not (src / "SKILL.md").is_file():
        raise SystemExit(
            f"[error] source '{src}' does not contain SKILL.md (not a valid skill)."
        )
    return src


# ---------- commands ----------
def _enforce_scope_confirmation(args: argparse.Namespace) -> None:
    """Block install unless the caller has explicitly confirmed the scope with the user.

    Rationale: agents tend to silently default `--scope` to `user` based on weak
    heuristics ("skill installer should be global"). That assumption has caused
    real surprise installs. We force the caller to add `--scope-confirmed`,
    which doubles as the agent's promise that it actually asked the user.

    Escape hatch for human users running interactively:
        export SKILL_INSTALLER_TRUST_ME=1
    """
    if getattr(args, "scope_confirmed", False):
        return
    if os.environ.get("SKILL_INSTALLER_TRUST_ME") == "1":
        return
    raise SystemExit(
        "[error] scope was not confirmed.\n"
        "        --scope is a HARD CHECKPOINT and cannot be inferred.\n"
        "\n"
        "        Agent: you MUST ask the user whether to install at\n"
        "               'user' (global) or 'project' (current repo) scope,\n"
        "               then re-run with --scope-confirmed once they answer.\n"
        "\n"
        "        Human user (interactive shell): either add --scope-confirmed\n"
        "               or run `export SKILL_INSTALLER_TRUST_ME=1` once.\n"
    )


def cmd_install(args: argparse.Namespace) -> None:
    _enforce_scope_confirmation(args)
    _ensure_state()
    source = _validate_source(Path(args.source))
    skill_name = args.name or source.name
    target_dir = _resolve_target_dir(args.tool, args.scope, _project_root(args))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / skill_name

    if target.exists() or target.is_symlink():
        if not args.force:
            raise SystemExit(
                f"[error] target already exists: {target}\n"
                f"        use --force to overwrite (existing path will be removed)."
            )
        if target.is_symlink() or target.is_file():
            target.unlink()
        else:
            import shutil
            shutil.rmtree(target)

    os.symlink(source, target, target_is_directory=True)

    record = {
        "skill": skill_name,
        "source": str(source),
        "tool": args.tool,
        "scope": args.scope,
        "target": str(target),
        "mode": "symlink",
        "installed_at": _now(),
    }
    installs = _read_json(INSTALLS_FILE, [])
    # Replace any prior record with same (skill, tool, scope, target).
    installs = [
        r for r in installs
        if not (
            r.get("skill") == skill_name
            and r.get("tool") == args.tool
            and r.get("scope") == args.scope
            and r.get("target") == str(target)
        )
    ]
    installs.append(record)
    _write_json(INSTALLS_FILE, installs)

    print(f"[ok] installed '{skill_name}' -> {target}")
    print(f"     source: {source}")
    print(f"     mode:   symlink (local edits propagate instantly)")


def cmd_uninstall(args: argparse.Namespace) -> None:
    _ensure_state()
    skill_name = args.name
    target_dir = _resolve_target_dir(args.tool, args.scope, _project_root(args))
    target = target_dir / skill_name

    removed_fs = False
    if target.is_symlink() or target.exists():
        if target.is_symlink() or target.is_file():
            target.unlink()
        else:
            import shutil
            shutil.rmtree(target)
        removed_fs = True

    installs = _read_json(INSTALLS_FILE, [])
    before = len(installs)
    installs = [
        r for r in installs
        if not (
            r.get("skill") == skill_name
            and r.get("tool") == args.tool
            and r.get("scope") == args.scope
        )
    ]
    _write_json(INSTALLS_FILE, installs)

    if removed_fs or before != len(installs):
        print(f"[ok] uninstalled '{skill_name}' from {args.tool}/{args.scope}")
    else:
        print(f"[warn] no matching installation for '{skill_name}' in {args.tool}/{args.scope}")


def cmd_list(args: argparse.Namespace) -> None:
    _ensure_state()
    installs = _read_json(INSTALLS_FILE, [])
    if not installs:
        print("(no skills installed)")
        return
    # Group by tool/scope for readability.
    installs.sort(key=lambda r: (r.get("tool", ""), r.get("scope", ""), r.get("skill", "")))
    current = None
    for r in installs:
        key = (r.get("tool"), r.get("scope"))
        if key != current:
            print(f"\n[{r.get('tool')}/{r.get('scope')}]")
            current = key
        link_ok = "ok" if Path(r.get("target", "")).is_symlink() else "MISSING"
        print(f"  - {r.get('skill'):<30} <- {r.get('source')}  ({link_ok})")


def cmd_register_tool(args: argparse.Namespace) -> None:
    _ensure_state()
    tools = _read_json(TOOLS_FILE, {})
    if args.name in tools and not args.force:
        raise SystemExit(
            f"[error] tool '{args.name}' already registered. Use --force to overwrite."
        )
    tools[args.name] = {
        "user": args.user_path,
        "project": args.project_path,
    }
    _write_json(TOOLS_FILE, tools)
    print(f"[ok] registered tool '{args.name}'")
    print(f"     user:    {args.user_path}")
    print(f"     project: {args.project_path}")


def cmd_tools(args: argparse.Namespace) -> None:
    _ensure_state()
    tools = _read_json(TOOLS_FILE, {})
    if not tools:
        print("(no tools registered)")
        return
    for name, paths in tools.items():
        print(f"- {name}")
        print(f"    user:    {paths.get('user')}")
        print(f"    project: {paths.get('project')}")


def cmd_doctor(args: argparse.Namespace) -> None:
    """Verify all recorded installations still resolve to a live symlink."""
    _ensure_state()
    installs = _read_json(INSTALLS_FILE, [])
    if not installs:
        print("(nothing to check)")
        return
    bad = 0
    for r in installs:
        target = Path(r.get("target", ""))
        source = Path(r.get("source", ""))
        ok = target.is_symlink() and source.exists()
        flag = "ok" if ok else "BROKEN"
        if not ok:
            bad += 1
        print(f"[{flag}] {r.get('skill')} ({r.get('tool')}/{r.get('scope')}) -> {target}")
    print(f"\n{len(installs) - bad}/{len(installs)} healthy.")


# ---------- argparse plumbing ----------
def _project_root(args: argparse.Namespace) -> Path | None:
    if getattr(args, "project_root", None):
        return Path(args.project_root).resolve()
    return None


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="installer", description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)

    # install
    pi = sub.add_parser("install", help="symlink a local skill into a tool")
    pi.add_argument("source", help="path to the local skill directory")
    pi.add_argument("--tool", required=True, help="target tool name (e.g. qoder, qoderwork)")
    pi.add_argument("--scope", required=True, choices=["user", "project"])
    pi.add_argument(
        "--scope-confirmed",
        action="store_true",
        help="REQUIRED for agent invocations: signed promise that --scope was "
             "explicitly chosen by the user, not inferred. Humans can also set "
             "SKILL_INSTALLER_TRUST_ME=1 to skip this check.",
    )
    pi.add_argument("--name", help="override skill name (default: source folder name)")
    pi.add_argument("--project-root", help="project root for project-scope installs (default: cwd)")
    pi.add_argument("--force", action="store_true", help="overwrite if target already exists")
    pi.set_defaults(func=cmd_install)

    # uninstall
    pu = sub.add_parser("uninstall", help="remove an installed skill")
    pu.add_argument("name", help="skill name to remove")
    pu.add_argument("--tool", required=True)
    pu.add_argument("--scope", required=True, choices=["user", "project"])
    pu.add_argument("--project-root")
    pu.set_defaults(func=cmd_uninstall)

    # list
    pl = sub.add_parser("list", help="list all installed skills")
    pl.set_defaults(func=cmd_list)

    # register-tool
    pr = sub.add_parser("register-tool", help="register a new tool's install paths")
    pr.add_argument("name", help="tool name (e.g. cursor, my-ide)")
    pr.add_argument("--user-path", required=True, help="user-scope skills dir, e.g. ~/.foo/skills")
    pr.add_argument("--project-path", required=True, help="project-scope skills dir, e.g. .foo/skills")
    pr.add_argument("--force", action="store_true")
    pr.set_defaults(func=cmd_register_tool)

    # tools
    pt = sub.add_parser("tools", help="show registered tools")
    pt.set_defaults(func=cmd_tools)

    # doctor
    pd = sub.add_parser("doctor", help="verify symlinks of recorded installations")
    pd.set_defaults(func=cmd_doctor)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
