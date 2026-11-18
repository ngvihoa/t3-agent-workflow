#!/usr/bin/env python3
"""Local bookkeeping helpers. Never executes project commands or external writes."""
import argparse
import copy
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

CONFIG = ".t3-workflow/project.json"
TASKS = ".t3-workflow/local/tasks"


def utcnow():
    return datetime.now(timezone.utc).isoformat()


def default_config():
    return {
        "version": 1,
        "tracker": "local",
        "docs": {"tasks": "docs/workflow", "wiki": "docs/wiki"},
        "execution": {"provider": "inherit", "model": "inherit", "delegation": "ask", "concurrency": 1, "review_attempts": 2, "repair_attempts": 2},
        "review": {"independent": False},
        "qa": [],
        "capabilities": {},
        "permissions": {"issue_updates": False, "pr_comments": False, "notifications": []},
        "ship": {"action": "unconfigured", "target": "", "command": ""},
        "maintenance": {"enabled": False, "timezone": "Asia/Ho_Chi_Minh", "weekdays": [0, 1, 2, 3, 4, 5], "start": "07:30", "end": "19:00", "interval_minutes": 60, "repairs": [], "outside_hours": False},
    }


def checked_path(repo, relative):
    root = Path(repo).resolve()
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError("Path must remain inside the project")
    p = root / rel
    for item in (p, *p.parents):
        if item.is_symlink():
            raise ValueError(f"Symlink state path: {item}")
        if item == root:
            break
    return p


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, tmp = tempfile.mkstemp(prefix=".workflow-", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(data, stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def time_value(value):
    if not isinstance(value, str) or not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", value):
        raise ValueError("Time must be HH:MM in 24-hour format")
    hour, minute = map(int, value.split(":"))
    return hour * 60 + minute


def tz(name):
    # Vietnam has no DST; fixed offset also works without a system tz database.
    if name == "Asia/Ho_Chi_Minh":
        return timezone(timedelta(hours=7), name)
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"Timezone data unavailable for {name}; configure a supported zone") from exc


def validate_config(c):
    if not isinstance(c, dict) or set(c) != set(default_config()) or c.get("version") != 1:
        raise ValueError("Unsupported config schema/version; preserve unknown fields for manual migration")
    if c["tracker"] not in {"local", "github"}:
        raise ValueError("V1 tracker must be local or github")
    for loc in c["docs"].values():
        if not isinstance(loc, str) or not loc or Path(loc).is_absolute() or ".." in Path(loc).parts:
            raise ValueError("Documentation locations must be project-relative")
    e = c["execution"]
    if e["delegation"] not in {"ask", "allowed", "disabled"}:
        raise ValueError("Invalid delegation policy")
    if any(type(e[k]) is not int or not 1 <= e[k] <= 16 for k in ["concurrency", "review_attempts", "repair_attempts"]):
        raise ValueError("Execution limits must be integers in 1..16")
    if any(not isinstance(e[k], str) or not e[k] for k in ["provider", "model"]):
        raise ValueError("Provider/model must be explicit strings or inherit")
    if type(c["review"]["independent"]) is not bool:
        raise ValueError("Independent review must be boolean")
    ids = set()
    for q in c["qa"]:
        if set(q) != {"id", "command", "required", "kind"} or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", q["id"]) or q["id"] in ids:
            raise ValueError("QA check IDs must be unique safe names with command/required/kind fields")
        ids.add(q["id"])
        if type(q["required"]) is not bool or q["kind"] not in {"command", "human", "device", "browser"} or not isinstance(q["command"], str):
            raise ValueError("Invalid QA check")
        if q["kind"] == "command" and not q["command"].strip():
            raise ValueError("Command QA needs an actual command")
    for key, cap in c["capabilities"].items():
        if not isinstance(key, str) or set(cap) != {"status", "evidence"} or cap["status"] not in {"configured", "authenticated", "verified", "unavailable"} or not isinstance(cap["evidence"], str):
            raise ValueError("Invalid capability status/evidence")
        if cap["status"] == "verified" and not cap["evidence"].strip():
            raise ValueError("Verified capability requires observed evidence")
    p = c["permissions"]
    if set(p) != {"issue_updates", "pr_comments", "notifications"} or any(type(p[k]) is not bool for k in ["issue_updates", "pr_comments"]):
        raise ValueError("Invalid external-write permissions")
    if not isinstance(p["notifications"], list) or any(not isinstance(x, str) or not x for x in p["notifications"]):
        raise ValueError("Notification destinations must be explicit strings")
    s = c["ship"]
    if set(s) != {"action", "target", "command"} or s["action"] not in {"unconfigured", "ready", "push", "merge", "command", "prompt"}:
        raise ValueError("Invalid ship policy")
    if not all(isinstance(s[k], str) for k in ["target", "command"]) or (s["action"] != "unconfigured" and not s["target"].strip()):
        raise ValueError("Configured ship needs an exact target")
    if s["action"] in {"command", "prompt"} and not s["command"].strip():
        raise ValueError("Ship command/prompt must be specified")
    m = c["maintenance"]
    if set(m) != set(default_config()["maintenance"]) or type(m["enabled"]) is not bool or type(m["outside_hours"]) is not bool:
        raise ValueError("Invalid maintenance schema")
    tz(m["timezone"])
    if not isinstance(m["weekdays"], list) or not m["weekdays"] or any(type(d) is not int or not 0 <= d <= 6 for d in m["weekdays"]) or len(set(m["weekdays"])) != len(m["weekdays"]):
        raise ValueError("Weekdays use Python numbering: Monday=0 to Sunday=6")
    if time_value(m["start"]) >= time_value(m["end"]):
        raise ValueError("Work window must start before end; overnight windows unsupported")
    if type(m["interval_minutes"]) is not int or not 1 <= m["interval_minutes"] <= 1440:
        raise ValueError("Maintenance interval must be 1..1440 minutes")
    if not isinstance(m["repairs"], list) or any(r not in {"ci", "conflicts"} for r in m["repairs"]):
        raise ValueError("Repairs may include ci and conflicts only")
    return c


def load_config(repo):
    try:
        return validate_config(read_json(checked_path(repo, CONFIG)))
    except (KeyError, TypeError, AttributeError) as exc:
        raise ValueError(f"Invalid configuration structure: {exc}") from exc


def init_config(repo):
    p = checked_path(repo, CONFIG)
    if p.exists():
        return load_config(repo), False
    c = default_config()
    write_json(p, c)
    return c, True


def scan(repo):
    root = Path(repo).resolve()
    result = {"indexed": (root / ".codegraph").is_dir(), "instructions": [n for n in ["AGENTS.md", "CLAUDE.md"] if (root / n).is_file()], "configuration": (root / CONFIG).is_file()}
    if result["indexed"]:
        result["next"] = "Use CodeGraph before reading or locating project code; this helper did not read manifests."
        return result
    result["manifests"] = [n for n in ["package.json", "pnpm-workspace.yaml", "pyproject.toml", "Cargo.toml", "go.mod", "app.json"] if (root / n).is_file()]
    package = root / "package.json"
    if package.is_file():
        data = read_json(package)
        result["scripts"] = data.get("scripts", {})
        result["package_manager"] = data.get("packageManager", "unknown")
    result["capability_note"] = "Manifest presence is discovery only, not authentication or runtime verification."
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, default=Path.cwd())
    sub = p.add_subparsers(dest="op", required=True)
    sub.add_parser("scan")
    init = sub.add_parser("config-init")
    init.add_argument("--write", action="store_true")
    sub.add_parser("config-check")
    a = p.parse_args()
    if a.op == "scan":
        result = scan(a.repo)
    elif a.op == "config-init":
        result = init_config(a.repo)[0] if a.write else default_config()
    else:
        result = load_config(a.repo)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as exc:
        raise SystemExit(str(exc))

