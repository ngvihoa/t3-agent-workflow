#!/usr/bin/env python3
"""Revision-bound task/action records. Bookkeeping only; no Git/host execution."""
import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
from datetime import datetime, timezone

from workflow import checked_path, load_config, read_json, TASKS, utcnow, write_json
from maintenance import in_window


def sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def task_path(repo, task):
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", task):
        raise ValueError("Task ID must be a lowercase slug")
    return checked_path(repo, TASKS + "/" + task + ".json")


@contextmanager
def edit(repo, task):
    p = task_path(repo, task)
    p.parent.mkdir(parents=True, exist_ok=True)
    lock = p.with_suffix(".lock")
    checked_path(repo, str(lock.relative_to(Path(repo).resolve())))
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ValueError("Task is locked; reconcile an interrupted writer before removing its lock") from exc
    try:
        with os.fdopen(fd, "w") as f:
            f.write(str(os.getpid()))
        data = read_json(p) if p.exists() else None
        yield data
        if data is not None:
            data["updated_at"] = utcnow()
            write_json(p, data)
    finally:
        lock.unlink(missing_ok=True)


def create(repo, task, size, source, scope):
    load_config(repo)
    if size not in {"small", "full"} or not source.strip() or not scope.strip():
        raise ValueError("Task requires size, source and concrete scope")
    p = task_path(repo, task)
    p.parent.mkdir(parents=True, exist_ok=True)
    data = {"version": 1, "id": task, "size": size, "source": source, "scope": scope, "stage": "implement" if size == "small" else "clarify", "documents": {}, "approvals": {}, "revision": None, "review": None, "checks": {}, "ship_request": None, "actions": {}, "maintenance": {"handles": {}, "events": []}, "updated_at": utcnow()}
    # Exclusive creation prevents two intake runs silently overwriting one another.
    try:
        with p.open("x", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
    except FileExistsError:
        existing = read_json(p)
        if (existing["size"], existing["source"], existing["scope"]) != (size, source, scope):
            raise ValueError("Existing task differs; reconcile scope instead of overwriting it")
        return existing
    return data


def doc_digest(repo, rel):
    return hashlib.sha256(checked_path(repo, rel).read_bytes()).hexdigest()


def approvals_current(repo, data):
    if data["size"] == "small":
        return True
    for kind in ["spec", "tickets"]:
        doc, approval = data["documents"].get(kind), data["approvals"].get(kind)
        if not doc or not approval or approval["sha256"] != doc["sha256"]:
            return False
        if doc_digest(repo, doc["path"]) != approval["sha256"]:
            return False
    return True


def set_document(repo, task, kind, path):
    if kind not in {"spec", "tickets"}:
        raise ValueError("Document must be spec or tickets")
    with edit(repo, task) as data:
        if data is None or data["size"] != "full":
            raise ValueError("Full task required")
        if kind == "tickets":
            spec, approved = data["documents"].get("spec"), data["approvals"].get("spec")
            if not spec or not approved or doc_digest(repo, spec["path"]) != approved["sha256"]:
                raise ValueError("Spec approval required before ticket planning")
        document = {"path": path, "sha256": doc_digest(repo, path)}
        if data["documents"].get(kind) != document:
            data["documents"][kind] = document
            data["approvals"].pop(kind, None)
            if kind == "spec":
                data["approvals"].pop("tickets", None)
                data["documents"].pop("tickets", None)
            data["review"], data["checks"], data["ship_request"] = None, {}, None
        data["stage"] = kind + "-review"
    return data


def approve(repo, task, kind, evidence):
    if kind not in {"spec", "tickets"} or not evidence.strip():
        raise ValueError("Approval needs a document kind and source-cited user statement")
    with edit(repo, task) as data:
        if data is None or kind not in data["documents"]:
            raise ValueError("No document to approve")
        if kind == "tickets":
            spec, approved = data["documents"].get("spec"), data["approvals"].get("spec")
            if not spec or not approved or doc_digest(repo, spec["path"]) != approved["sha256"]:
                raise ValueError("Spec approval is stale or absent")
        doc = data["documents"][kind]
        if doc_digest(repo, doc["path"]) != doc["sha256"]:
            raise ValueError("Document changed; present the new version before approval")
        data["approvals"][kind] = {"sha256": doc["sha256"], "user_statement": evidence, "at": utcnow()}
        data["stage"] = "ticket-planning" if kind == "spec" else "implement"
    return data


def candidate(repo, task, revision):
    if not revision.strip():
        raise ValueError("Candidate needs a revision")
    with edit(repo, task) as data:
        if data is None or not approvals_current(repo, data):
            raise ValueError("Implementation requires current spec and ticket approvals")
        if data["revision"] != revision:
            data["review"], data["checks"], data["ship_request"] = None, {}, None
        data["revision"], data["stage"] = revision, "review-qa"
    return data


def record_review(repo, task, revision, standards, spec, evidence, independent=False):
    if standards not in {"pass", "fail"} or spec not in {"pass", "fail"} or type(independent) is not bool or not evidence.strip():
        raise ValueError("Review needs findings/evidence")
    with edit(repo, task) as data:
        if data is None or data["revision"] != revision:
            raise ValueError("Review revision differs from candidate")
        data["review"] = {"revision": revision, "standards": standards, "spec": spec, "independent": independent, "evidence": evidence, "at": utcnow()}
        data["ship_request"] = None
    return data


def record_check(repo, task, revision, check, status, origin, evidence):
    config = load_config(repo)
    if check not in {q["id"] for q in config["qa"]} or status not in {"pass", "fail", "pending", "skipped"} or origin not in {"executed", "human", "simulation"} or not evidence.strip():
        raise ValueError("Check must be configured with valid status, origin and evidence")
    with edit(repo, task) as data:
        if data is None or data["revision"] != revision:
            raise ValueError("QA revision differs from candidate")
        definition = next(q for q in config["qa"] if q["id"] == check)
        data["checks"][check] = {"revision": revision, "definition_sha256": sha(definition), "status": status, "origin": origin, "evidence": evidence, "at": utcnow()}
        data["ship_request"] = None
    return data


def ship_errors(repo, data, config, require_request=True):
    errors = []
    if not data.get("revision"):
        errors.append("No candidate revision")
    if not approvals_current(repo, data):
        errors.append("Spec/ticket approvals are stale or missing")
    review = data["review"]
    if not review or review["revision"] != data["revision"] or review["standards"] != "pass" or review["spec"] != "pass":
        errors.append("Passing standards/spec review required for candidate")
    if config["review"]["independent"] and (not review or not review.get("independent")):
        errors.append("Independent review is required by project policy")
    for q in config["qa"]:
        result = data["checks"].get(q["id"])
        if q["required"] and (not result or result["revision"] != data["revision"] or result.get("definition_sha256") != sha(q) or result["status"] != "pass" or result["origin"] == "simulation"):
            errors.append("Required QA missing/failing/simulated: " + q["id"])
    if config["ship"]["action"] == "unconfigured":
        errors.append("Ship action not configured")
    request = data["ship_request"]
    if require_request and (not request or request["revision"] != data["revision"] or request["policy_sha256"] != sha(config)):
        errors.append("Explicit current ship request required")
    return errors


def request_ship(repo, task, revision, evidence):
    config = load_config(repo)
    with edit(repo, task) as data:
        if data is None or data["revision"] != revision or not evidence.strip():
            raise ValueError("Ship needs exact candidate revision and explicit user statement")
        errors = ship_errors(repo, data, config, require_request=False)
        if errors:
            raise ValueError("; ".join(errors))
        data["ship_request"] = {"revision": revision, "policy_sha256": sha(config), "user_statement": evidence, "at": utcnow()}
    return data


def reserve_action(repo, task, key, kind, target):
    config = load_config(repo)
    if kind not in {"issue-update", "pr-comment", "notify", "pr-create", "push", "ship", "repair", "schedule"} or not key.strip() or not target.strip():
        raise ValueError("Action requires supported kind, stable key and explicit target")
    with edit(repo, task) as data:
        if data is None:
            raise ValueError("Unknown task")
        existing = data["actions"].get(key)
        if existing:
            if (existing["kind"], existing["target"], existing["revision"]) != (kind, target, data["revision"]):
                raise ValueError("Action key reused for a different effect/revision")
            raise ValueError("Action already recorded; reconcile its outcome before retrying")
        if kind == "ship":
            errors = ship_errors(repo, data, config)
            if any(a["kind"] == "ship" and a["status"] in {"started", "uncertain"} for a in data["actions"].values()):
                errors.append("A ship action is unresolved; reconcile it first")
            if target != config["ship"]["target"]:
                errors.append("Target differs from configured ship action")
            if errors:
                raise ValueError("; ".join(errors))
        if kind == "notify" and target not in config["permissions"]["notifications"]:
            raise ValueError("Notification destination is not authorized")
        if kind in {"pr-comment", "issue-update"} and not config["permissions"][{"pr-comment": "pr_comments", "issue-update": "issue_updates"}[kind]]:
            raise ValueError("External write is not authorized")
        if kind in {"repair", "schedule"} and not config["maintenance"]["enabled"]:
            raise ValueError("Maintenance is not enabled")
        if kind == "repair":
            if target not in config["maintenance"]["repairs"]:
                raise ValueError("Repair class is not authorized")
            if not in_window(config["maintenance"], datetime.now(timezone.utc)):
                raise ValueError("Maintenance repair is outside configured working hours")
        data["actions"][key] = {"kind": kind, "target": target, "revision": data["revision"], "status": "started", "at": utcnow(), "result": None}
    return data


def finish_action(repo, task, key, outcome, evidence):
    if outcome not in {"succeeded", "failed", "uncertain"} or not evidence.strip():
        raise ValueError("Action needs a valid outcome and observed evidence")
    with edit(repo, task) as data:
        action = data["actions"].get(key) if data else None
        if not action or action["status"] == "succeeded":
            raise ValueError("No unresolved action with this key")
        action["status"], action["result"], action["finished_at"] = outcome, evidence, utcnow()
        if action["kind"] == "ship" and outcome == "succeeded" and action["revision"] == data["revision"]:
            data["stage"] = "shipped"
            data["ship_request"] = None
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--task", required=True)
    sub = parser.add_subparsers(dest="op", required=True)
    sub.add_parser("show")
    p = sub.add_parser("create")
    p.add_argument("--size", choices=["small", "full"], required=True)
    p.add_argument("--source", required=True)
    p.add_argument("--scope", required=True)
    p = sub.add_parser("document")
    p.add_argument("--kind", choices=["spec", "tickets"], required=True)
    p.add_argument("--path", required=True)
    p = sub.add_parser("approve")
    p.add_argument("--kind", choices=["spec", "tickets"], required=True)
    p.add_argument("--evidence", required=True)
    p = sub.add_parser("candidate")
    p.add_argument("--revision", required=True)
    p = sub.add_parser("review")
    p.add_argument("--revision", required=True)
    p.add_argument("--standards", choices=["pass", "fail"], required=True)
    p.add_argument("--spec", choices=["pass", "fail"], required=True)
    p.add_argument("--evidence", required=True)
    p.add_argument("--independent", action="store_true", help="Record an actually observed independent review")
    p = sub.add_parser("check")
    p.add_argument("--revision", required=True)
    p.add_argument("--check", required=True)
    p.add_argument("--status", choices=["pass", "fail", "pending", "skipped"], required=True)
    p.add_argument("--origin", choices=["executed", "human", "simulation"], required=True)
    p.add_argument("--evidence", required=True)
    p = sub.add_parser("ship-request")
    p.add_argument("--revision", required=True)
    p.add_argument("--evidence", required=True)
    sub.add_parser("ship-plan")
    p = sub.add_parser("action-start")
    for key in ["key", "kind", "target"]:
        p.add_argument("--" + key, required=True)
    p = sub.add_parser("action-finish")
    p.add_argument("--key", required=True)
    p.add_argument("--outcome", required=True)
    p.add_argument("--evidence", required=True)
    args = parser.parse_args()
    values = vars(args).copy()
    op, repo, task = values.pop("op"), values.pop("repo"), values.pop("task")
    if op == "show":
        result = read_json(task_path(repo, task))
    elif op == "ship-plan":
        data, config = read_json(task_path(repo, task)), load_config(repo)
        errors = ship_errors(repo, data, config)
        result = {"allowed": not errors, "errors": errors, "effect": config["ship"], "revision": data["revision"]}
    else:
        fn = {"create": create, "document": set_document, "approve": approve, "candidate": candidate, "review": record_review, "check": record_check, "ship-request": request_ship, "action-start": reserve_action, "action-finish": finish_action}[op]
        result = fn(repo, task, **values)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as exc:
        raise SystemExit(str(exc))

