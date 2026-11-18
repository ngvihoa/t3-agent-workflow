#!/usr/bin/env python3
"""Preview-first, offline bundle installer. Python 3.11+, standard library only."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
RECEIPT = "bundle-receipt.json"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def no_symlinks(path):
    path = Path(os.path.abspath(path))
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError(f"Symlink destination component: {part}")
    return path


def load_bundle(root=ROOT):
    root = Path(root)
    m = json.loads((root / "bundle.json").read_text(encoding="utf-8"))
    if m.get("version") != 1 or not m.get("skills") or not m.get("files"):
        raise ValueError("Unsupported or empty bundle manifest")
    skills = m["skills"]
    if len(skills) != len(set(skills)) or any(not re.fullmatch(r"t3-[a-z0-9]+(?:-[a-z0-9]+)*", n) or len(n) > 64 for n in skills):
        raise ValueError("Invalid skill names")
    actual = {p.relative_to(root).as_posix() for p in (root / "skills").rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"}
    if actual != set(m["files"]):
        raise ValueError("Bundle contains missing or unlisted files; refresh only after reviewing edits")
    for name in skills:
        if f"skills/{name}/SKILL.md" not in m["files"]:
            raise ValueError(f"Missing entrypoint: {name}")
    for rel, sha in m["files"].items():
        p = PurePosixPath(rel)
        if p.is_absolute() or ".." in p.parts or len(p.parts) < 3 or p.parts[0] != "skills" or p.parts[1] not in skills:
            raise ValueError(f"Unsafe bundle path: {rel}")
        target = root / rel
        if any(x.is_symlink() for x in (target, *target.parents)) or digest(target.read_bytes()) != sha:
            raise ValueError(f"Bundle integrity failure: {rel}")
    return m


def plan_install(dest, prefix="", replace=False, root=ROOT):
    dest = no_symlinks(dest)
    if prefix and (not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*-", prefix)):
        raise ValueError("Prefix must be a lowercase name ending with '-', e.g. 'team-'")
    if dest.exists() and not dest.is_dir():
        raise ValueError("Destination is not a directory")
    if dest.exists() and any(dest.glob(".t3-install-*")):
        raise ValueError("Interrupted install found; run --recover before installing")
    manifest = load_bundle(root)
    if any(len(prefix + n) > 64 for n in manifest["skills"]):
        raise ValueError("Prefixed skill name exceeds 64 characters")
    entries = {}
    for rel in manifest["files"]:
        parts = PurePosixPath(rel).parts
        new_rel = str(PurePosixPath(prefix + parts[1], *parts[2:]))
        data = (Path(root) / rel).read_bytes()
        if prefix:
            # All package assets are UTF-8 text. Rewrite every internal namespace together.
            data = data.decode("utf-8").replace("t3-", prefix + "t3-").encode("utf-8")
        entries[new_rel] = data
    names = [prefix + n for n in manifest["skills"]]
    receipt = {"version": 1, "source_manifest_sha256": digest((Path(root) / "bundle.json").read_bytes()), "files": {k: digest(v) for k, v in entries.items()}}
    receipt_rel = prefix + "t3-agent-workflow/" + RECEIPT
    entries[receipt_rel] = (json.dumps(receipt, indent=2) + "\n").encode()
    changes = []
    for name in names:
        target = dest / name
        no_symlinks(target)
        if target.exists():
            if not target.is_dir() or any(p.is_symlink() for p in target.rglob("*")):
                raise ValueError(f"Unsafe existing skill: {name}")
            existing = {p.relative_to(dest).as_posix(): p.read_bytes() for p in target.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"}
            expected = {k: v for k, v in entries.items() if k.startswith(name + "/")}
            action = "unchanged" if existing == expected else "replace" if replace else "conflict"
        else:
            action = "add"
        changes.append({"skill": name, "action": action})
    return {"destination": str(dest), "changes": changes, "entries": entries}


def recover(dest):
    dest = no_symlinks(dest)
    for stage in sorted(dest.glob(".t3-install-*")):
        no_symlinks(stage)
        journal = stage / "journal.json"
        if not journal.is_file():
            raise ValueError(f"Recovery requires manual inspection: {stage}")
        data = json.loads(journal.read_text(encoding="utf-8"))
        if data.get("destination") != str(dest) or not isinstance(data.get("items"), list):
            raise ValueError(f"Invalid recovery journal: {stage}")
        # Validate the entire journal before touching any destination.
        for item in data["items"]:
            name = item.get("name", "")
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
                raise ValueError("Invalid recovery skill name")
            for p in (dest / name, stage / "backup" / name, stage / "new" / name):
                no_symlinks(p)
                if p.exists() and any(c.is_symlink() for c in p.rglob("*")):
                    raise ValueError("Recovery tree contains symlinks")
        for item in reversed(data["items"]):
            name = item["name"]
            target, backup, new = dest / name, stage / "backup" / name, stage / "new" / name
            if backup.exists():
                if target.exists():
                    shutil.rmtree(target)
                os.replace(backup, target)
            elif not item["existed"] and not new.exists() and target.exists():
                shutil.rmtree(target)
        shutil.rmtree(stage)


def apply_install(plan):
    if any(c["action"] == "conflict" for c in plan["changes"]):
        raise ValueError("Existing local content differs; select --replace or a --prefix after reviewing the preview")
    changes = [c for c in plan["changes"] if c["action"] != "unchanged"]
    if not changes:
        return
    dest = no_symlinks(plan["destination"])
    dest.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".t3-install-", dir=dest))
    try:
        for rel, data in plan["entries"].items():
            p = stage / "new" / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        (stage / "backup").mkdir()
        journal = {"destination": str(dest), "items": [{"name": c["skill"], "existed": (dest / c["skill"]).exists()} for c in changes]}
        (stage / "journal.json").write_text(json.dumps(journal), encoding="utf-8")
        for item in journal["items"]:
            name = item["name"]
            if item["existed"]:
                os.replace(dest / name, stage / "backup" / name)
            os.replace(stage / "new" / name, dest / name)
    except BaseException:
        if (stage / "journal.json").is_file():
            recover(dest)
        else:
            shutil.rmtree(stage)
        raise
    else:
        shutil.rmtree(stage)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", type=Path, help="Explicit provider skills directory")
    parser.add_argument("--provider", choices=["codex", "claude"], help="Default global directory convention; use --dest for other providers")
    parser.add_argument("--prefix", default="", help="Isolated side-by-side namespace, e.g. team-")
    parser.add_argument("--replace", action="store_true", help="Explicitly replace conflicting bundle skill directories")
    parser.add_argument("--apply", action="store_true", help="Write the displayed plan; default is preview only")
    parser.add_argument("--recover", action="store_true", help="Restore a prior interrupted transaction")
    args = parser.parse_args()
    if args.dest is None and args.provider is None:
        parser.error("Select --dest or --provider; no directory is guessed")
    dest = args.dest or Path.home() / (".codex/skills" if args.provider == "codex" else ".claude/skills")
    if args.recover:
        recover(dest)
        print("Interrupted transactions recovered; review a new preview before retrying.")
        return
    plan = plan_install(dest, args.prefix, args.replace)
    print(json.dumps({k: v for k, v in plan.items() if k != "entries"}, indent=2))
    if args.apply:
        apply_install(plan)
        print("Installed. Start a fresh agent turn/session if needed, then invoke $" + args.prefix + "t3-workflow-setup in your target repo.")
    else:
        print("Preview only. Add --apply to install the same selection. No tools or accounts are installed/connected by this command.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        print(f"Install failed: {exc}", file=sys.stderr)
        sys.exit(1)

