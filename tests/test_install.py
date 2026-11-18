import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("installer", ROOT / "install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.dest = Path(self.temp.name) / "skills"

    def tearDown(self):
        self.temp.cleanup()

    def test_preview_then_complete_idempotent_install(self):
        plan = installer.plan_install(self.dest)
        self.assertFalse(self.dest.exists())
        installer.apply_install(plan)
        self.assertTrue((self.dest / "t3-agent-workflow/SKILL.md").exists())
        self.assertTrue((self.dest / "t3-tdd/tests.md").exists())
        self.assertTrue((self.dest / "t3-domain-modeling/ADR-FORMAT.md").exists())
        self.assertTrue(all(x["action"] == "unchanged" for x in installer.plan_install(self.dest)["changes"]))

    def test_local_edits_preserved_until_explicit_replace(self):
        installer.apply_install(installer.plan_install(self.dest))
        target = self.dest / "t3-tdd/SKILL.md"
        target.write_text("user customization", encoding="utf-8")
        with self.assertRaises(ValueError):
            installer.apply_install(installer.plan_install(self.dest))
        self.assertEqual(target.read_text(), "user customization")
        installer.apply_install(installer.plan_install(self.dest, replace=True))
        self.assertIn("Test-Driven Development", target.read_text())

    def test_prefix_installs_resolving_independent_namespace(self):
        installer.apply_install(installer.plan_install(self.dest, prefix="team-"))
        content = (self.dest / "team-t3-agent-workflow/SKILL.md").read_text()
        self.assertNotIn("../t3-", content)
        self.assertIn("../team-t3-workflow-setup/SKILL.md", content)
        self.assertTrue((self.dest / "team-t3-workflow-setup/SKILL.md").is_file())

    def test_failure_restores_old_content_and_removes_new_content(self):
        self.dest.mkdir()
        old = self.dest / "t3-agent-workflow"
        old.mkdir()
        (old / "custom.txt").write_text("keep")
        (self.dest / "unrelated").mkdir()
        real_replace, calls = os.replace, 0

        def fail_once(src, dst):
            nonlocal calls
            calls += 1
            if calls == 3:
                raise OSError("simulated disk failure")
            return real_replace(src, dst)

        with patch.object(installer.os, "replace", side_effect=fail_once):
            with self.assertRaises(OSError):
                installer.apply_install(installer.plan_install(self.dest, replace=True))
        self.assertEqual((old / "custom.txt").read_text(), "keep")
        self.assertEqual(sorted(p.name for p in self.dest.iterdir()), ["t3-agent-workflow", "unrelated"])

    def test_interrupted_transaction_recovers(self):
        self.dest.mkdir()
        stage = self.dest / ".t3-install-interrupted"
        backup = stage / "backup/t3-agent-workflow"
        backup.mkdir(parents=True)
        (backup / "old").write_text("original")
        new = self.dest / "t3-agent-workflow"
        new.mkdir()
        (new / "new").write_text("partial")
        (stage / "journal.json").write_text(json.dumps({"destination": str(self.dest), "items": [{"name": "t3-agent-workflow", "existed": True}]}))
        with self.assertRaises(ValueError):
            installer.plan_install(self.dest)
        installer.recover(self.dest)
        self.assertEqual((new / "old").read_text(), "original")
        self.assertFalse((new / "new").exists())

    def test_symlink_destination_rejected(self):
        try:
            self.dest.symlink_to(Path(self.temp.name), target_is_directory=True)
        except OSError:
            self.skipTest("symlinks unavailable")
        with self.assertRaises(ValueError):
            installer.plan_install(self.dest)

    def test_modified_or_traversing_source_rejected(self):
        root = Path(self.temp.name) / "source"
        (root / "skills/t3-sample").mkdir(parents=True)
        (root / "skills/t3-sample/SKILL.md").write_text("changed")
        (root / "bundle.json").write_text(json.dumps({"version": 1, "skills": ["t3-sample"], "files": {"skills/t3-sample/SKILL.md": "wrong"}}))
        with self.assertRaises(ValueError):
            installer.plan_install(self.dest, root=root)
        (root / "bundle.json").write_text(json.dumps({"version": 1, "skills": ["t3-sample"], "files": {"../escape": "bad"}}))
        with self.assertRaises(ValueError):
            installer.plan_install(self.dest, root=root)


if __name__ == "__main__":
    unittest.main()

