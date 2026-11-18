"""Explicitly refresh the checked-in package integrity record after intentional edits."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build():
    files = {}
    for p in sorted((ROOT / "skills").rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc":
            if p.is_symlink():
                raise ValueError(f"Symlink cannot be packaged: {p}")
            files[p.relative_to(ROOT).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    manifest = {
        "version": 1,
        "skills": sorted(p.name for p in (ROOT / "skills").iterdir() if p.is_dir()),
        "files": files,
    }
    (ROOT / "bundle.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    m = build()
    print(f"Recorded {len(m['skills'])} skills, {len(m['files'])} files")

