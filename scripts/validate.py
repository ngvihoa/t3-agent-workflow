"""Offline integrity/reference validation. Does not prove agent behavior."""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from install import load_bundle


def validate():
    m = load_bundle(ROOT)
    errors = []
    for name in m["skills"]:
        path = ROOT / "skills" / name
        content = (path / "SKILL.md").read_text(encoding="utf-8")
        header = re.match(r"^---\n(.*?)\n---\n", content, re.S)
        if not header or f"name: {name}\n" not in header[0] or not re.search(r"^description: .+", header[1], re.M):
            errors.append(f"Invalid entrypoint: {name}")
        if not (path / "agents/openai.yaml").is_file():
            errors.append(f"Missing UI metadata: {name}")
        for p in path.rglob("*.md"):
            text = re.sub(r"(?ms)^```.*?^```[^\n]*$", "", p.read_text(encoding="utf-8"))
            for link in re.findall(r"\]\(([^)]+)\)", text):
                if link.startswith(("https://", "http://", "#", "mailto:")) or "<" in link:
                    continue
                target = (p.parent / link.split("#")[0]).resolve()
                if not target.is_relative_to(ROOT / "skills") or not target.exists():
                    errors.append(f"Broken/escaping link: {p.relative_to(ROOT)} -> {link}")
    provenance = json.loads((ROOT / "upstream.json").read_text(encoding="utf-8"))
    for entry in provenance["records"]:
        if entry["artifact"] not in m["files"]:
            errors.append(f"Missing upstream artifact: {entry['artifact']}")
        elif entry.get("adapted_sha256") != m["files"][entry["artifact"]]:
            errors.append(f"Adaptation hash mismatch: {entry['artifact']}")
    for name in {Path(e["artifact"]).parts[1] for e in provenance["records"]}:
        if not (ROOT / "skills" / name / "UPSTREAM_LICENSE").is_file():
            errors.append(f"Missing upstream license: {name}")
    for p in (ROOT / "skills").rglob("*.py"):
        compile(p.read_text(encoding="utf-8"), str(p), "exec")
    if errors:
        raise ValueError("\n".join(errors))
    print(f"Validated {len(m['skills'])} skills / {len(m['files'])} artifacts and local references")


if __name__ == "__main__":
    try:
        validate()
    except (ValueError, OSError, KeyError) as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)

