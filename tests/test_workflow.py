from datetime import datetime
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/t3-agent-workflow/scripts"))
import workflow as w
import tasks as t
import maintenance as m


class WorkflowTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        self.config, _ = w.init_config(self.repo)

    def tearDown(self):
        self.temp.cleanup()

    def save(self):
        w.write_json(self.repo / w.CONFIG, self.config)

    def ready(self, size="small"):
        self.config["ship"] = {"action": "ready", "target": "https://example.test/pull/7", "command": ""}
        self.config["qa"] = [{"id": "test", "command": "python -m unittest", "kind": "command", "required": True}]
        self.save()
        t.create(self.repo, "task", size, "manual:fixture", "Return the requested behavior")
        if size == "full":
            self.approve_full()
        t.candidate(self.repo, "task", "revision-a")
        t.record_review(self.repo, "task", "revision-a", "pass", "pass", "Fixture reviewer observed scope/standards")
        t.record_check(self.repo, "task", "revision-a", "test", "pass", "executed", "Fixture test process exited 0")

    def approve_full(self):
        for kind in ["spec", "tickets"]:
            (self.repo / (kind + ".md")).write_text("Approved " + kind)
            t.set_document(self.repo, "task", kind, kind + ".md")
            t.approve(self.repo, "task", kind, "Observed user approval in fixture conversation")

    def test_setup_preserves_existing_configuration_and_instructions(self):
        (self.repo / "AGENTS.md").write_text("Existing instructions")
        self.config["docs"]["wiki"] = "existing/wiki"
        self.save()
        config, created = w.init_config(self.repo)
        self.assertFalse(created)
        self.assertEqual(config["docs"]["wiki"], "existing/wiki")
        self.assertEqual((self.repo / "AGENTS.md").read_text(), "Existing instructions")

    def test_invalid_config_and_unproved_capability_rejected(self):
        self.config["capabilities"]["github"] = {"status": "verified", "evidence": ""}
        with self.assertRaises(ValueError):
            w.validate_config(self.config)
        self.config["capabilities"] = {}
        self.config["maintenance"]["weekdays"] = [7]
        with self.assertRaises(ValueError):
            w.validate_config(self.config)

    def test_indexed_repo_scan_does_not_read_manifests(self):
        (self.repo / ".codegraph").mkdir()
        (self.repo / "package.json").write_text("not valid JSON")
        result = w.scan(self.repo)
        self.assertTrue(result["indexed"])
        self.assertNotIn("scripts", result)

    def test_full_task_has_two_distinct_gates(self):
        t.create(self.repo, "task", "full", "manual:feature", "Implement feature")
        (self.repo / "spec.md").write_text("Requested feature")
        (self.repo / "tickets.md").write_text("Planned tasks")
        with self.assertRaises(ValueError):
            t.candidate(self.repo, "task", "a")
        with self.assertRaises(ValueError):
            t.set_document(self.repo, "task", "tickets", "tickets.md")
        t.set_document(self.repo, "task", "spec", "spec.md")
        t.approve(self.repo, "task", "spec", "User approved spec")
        with self.assertRaises(ValueError):
            t.candidate(self.repo, "task", "a")
        t.set_document(self.repo, "task", "tickets", "tickets.md")
        t.approve(self.repo, "task", "tickets", "User approved tickets")
        self.assertEqual(t.candidate(self.repo, "task", "a")["stage"], "review-qa")

    def test_changed_approved_document_blocks_candidate_and_ship(self):
        self.ready("full")
        (self.repo / "spec.md").write_text("New unapproved behavior")
        with self.assertRaises(ValueError):
            t.candidate(self.repo, "task", "b")
        with self.assertRaises(ValueError):
            t.request_ship(self.repo, "task", "revision-a", "Ship")

    def test_small_task_resumes_but_conflicting_scope_is_rejected(self):
        a = t.create(self.repo, "task", "small", "manual:typo", "Fix typo")
        b = t.create(self.repo, "task", "small", "manual:typo", "Fix typo")
        self.assertEqual(a, b)
        with self.assertRaises(ValueError):
            t.create(self.repo, "task", "small", "manual:typo", "Change behavior")

    def test_ship_requires_instruction_and_consumes_it(self):
        self.ready()
        target = self.config["ship"]["target"]
        with self.assertRaises(ValueError):
            t.reserve_action(self.repo, "task", "ship-1", "ship", target)
        t.request_ship(self.repo, "task", "revision-a", "User explicitly said ship this candidate")
        t.reserve_action(self.repo, "task", "ship-1", "ship", target)
        with self.assertRaises(ValueError):
            t.reserve_action(self.repo, "task", "ship-2", "ship", target)
        data = t.finish_action(self.repo, "task", "ship-1", "succeeded", "Fake host returned ready=true")
        self.assertEqual(data["stage"], "shipped")
        with self.assertRaises(ValueError):
            t.reserve_action(self.repo, "task", "ship-2", "ship", target)

    def test_new_revision_invalidates_evidence_and_ship_request(self):
        self.ready()
        t.request_ship(self.repo, "task", "revision-a", "Ship candidate a")
        data = t.candidate(self.repo, "task", "revision-b")
        self.assertIsNone(data["review"])
        self.assertEqual(data["checks"], {})
        self.assertIsNone(data["ship_request"])

    def test_required_simulation_and_changed_qa_definition_do_not_pass(self):
        self.ready()
        t.record_check(self.repo, "task", "revision-a", "test", "pass", "simulation", "Tabletop scenario only")
        with self.assertRaises(ValueError):
            t.request_ship(self.repo, "task", "revision-a", "Ship")
        t.record_check(self.repo, "task", "revision-a", "test", "pass", "executed", "Fixture process passed")
        self.config["qa"][0]["command"] = "a-different-check"
        self.save()
        with self.assertRaises(ValueError):
            t.request_ship(self.repo, "task", "revision-a", "Ship")

    def test_separate_axes_and_required_independence(self):
        self.ready()
        t.record_review(self.repo, "task", "revision-a", "pass", "fail", "Spec requirement missing")
        with self.assertRaises(ValueError):
            t.request_ship(self.repo, "task", "revision-a", "Ship")
        t.record_review(self.repo, "task", "revision-a", "pass", "pass", "Self review")
        self.config["review"]["independent"] = True
        self.save()
        with self.assertRaises(ValueError):
            t.request_ship(self.repo, "task", "revision-a", "Ship")
        t.record_review(self.repo, "task", "revision-a", "pass", "pass", "Independent fixture reviewer", independent=True)
        t.request_ship(self.repo, "task", "revision-a", "Ship")

    def test_unauthorized_notifications_and_duplicate_actions_block(self):
        self.ready()
        with self.assertRaises(ValueError):
            t.reserve_action(self.repo, "task", "notice", "notify", "new-channel")
        t.reserve_action(self.repo, "task", "pr-create", "pr-create", "fixture:repo")
        t.finish_action(self.repo, "task", "pr-create", "uncertain", "Timeout; reconcile fake host")
        with self.assertRaises(ValueError):
            t.reserve_action(self.repo, "task", "pr-create", "pr-create", "fixture:repo")

    def test_ship_policy_change_invalidates_instruction(self):
        self.ready()
        t.request_ship(self.repo, "task", "revision-a", "Mark ready")
        self.config["ship"]["action"] = "merge"
        self.save()
        with self.assertRaises(ValueError):
            t.reserve_action(self.repo, "task", "ship", "ship", self.config["ship"]["target"])


class MaintenanceTest(unittest.TestCase):
    def setUp(self):
        self.policy = w.default_config()["maintenance"]
        self.policy["enabled"] = True

    def test_vietnam_window_boundaries(self):
        self.assertFalse(m.in_window(self.policy, datetime.fromisoformat("2026-11-16T07:29:59+07:00")))
        self.assertTrue(m.in_window(self.policy, datetime.fromisoformat("2026-11-16T07:30:00+07:00")))
        self.assertTrue(m.in_window(self.policy, datetime.fromisoformat("2026-11-16T18:59:59+07:00")))
        self.assertFalse(m.in_window(self.policy, datetime.fromisoformat("2026-11-16T19:00:00+07:00")))

    def test_saturday_end_skips_sunday_and_returns_monday_utc(self):
        self.assertEqual(m.next_run(self.policy, datetime.fromisoformat("2026-11-21T18:30:00+07:00")), "2026-11-23T00:30:00+00:00")

    def test_hourly_alignment_and_disabled_schedule(self):
        self.assertEqual(m.next_run(self.policy, datetime.fromisoformat("2026-11-16T08:00:00+07:00")), "2026-11-16T01:30:00+00:00")
        self.policy["enabled"] = False
        self.assertIsNone(m.next_run(self.policy, datetime.fromisoformat("2026-11-16T08:00:00+07:00")))

    def test_naive_timestamp_rejected(self):
        with self.assertRaises(ValueError):
            m.in_window(self.policy, datetime(2026, 11, 16, 8))


if __name__ == "__main__":
    unittest.main()

