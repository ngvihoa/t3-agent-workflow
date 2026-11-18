"""Run installed helpers as a user would, in a real temporary Git fixture."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InstalledCliTest(unittest.TestCase):
    def test_install_setup_and_small_task_candidate(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            dest, repo = root / "provider-skills", root / "project"
            repo.mkdir()

            def run(*args, cwd=repo):
                return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=True).stdout

            run(sys.executable, str(ROOT / "install.py"), "--dest", str(dest), "--apply")
            helper = dest / "t3-agent-workflow/scripts"
            result = json.loads(run(sys.executable, str(helper / "workflow.py"), "config-init"))
            self.assertFalse((repo / ".t3-workflow").exists())
            self.assertEqual(result["ship"]["action"], "unconfigured")
            run(sys.executable, str(helper / "workflow.py"), "config-init", "--write")
            config_path = repo / ".t3-workflow/project.json"
            saved = json.loads(config_path.read_text())
            saved["execution"]["delegation"] = "disabled"
            config_path.write_text(json.dumps(saved), encoding="utf-8")
            preview = json.loads(run(sys.executable, str(helper / "workflow.py"), "config-init"))
            self.assertEqual(preview["execution"]["delegation"], "disabled")
            run("git", "init")
            run("git", "config", "user.name", "Workflow fixture")
            run("git", "config", "user.email", "fixture@example.test")
            (repo / "greeting.py").write_text('print("Welcome")\n', encoding="utf-8")
            self.assertEqual(run(sys.executable, "greeting.py").strip(), "Welcome")
            run("git", "add", "greeting.py")
            run("git", "commit", "-m", "Fix fixture greeting")
            revision = run("git", "rev-parse", "HEAD").strip()
            command = [sys.executable, str(helper / "tasks.py"), "--task", "greeting"]
            data = json.loads(run(*command, "create", "--size", "small", "--source", "manual:fixture", "--scope", "Print Welcome"))
            self.assertEqual(data["stage"], "implement")
            run(*command, "candidate", "--revision", revision)
            run(*command, "review", "--revision", revision, "--standards", "pass", "--spec", "pass", "--evidence", "Fixture inspected greeting and executed Python")
            plan = json.loads(run(*command, "ship-plan"))
            self.assertFalse(plan["allowed"])
            self.assertIn("Ship action not configured", plan["errors"])
            self.assertIn("Explicit current ship request required", plan["errors"])
            self.assertEqual(plan["revision"], revision)


if __name__ == "__main__":
    unittest.main()

