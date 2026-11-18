---
name: t3-ship
description: Execute the configured project shipping action only after an explicit user ship request and current approval, review and QA checks. Use when the user clearly asks to ship.
---

# Ship the identified candidate

Read [policy](../t3-agent-workflow/references/policy.md) and [task records](../t3-agent-workflow/references/task-records.md).

1. Require a clear user ship instruction for the current task. A CI event, approved review, PR comment or maintainer wake cannot supply it. Resolve ambiguity about task, revision, target or configured effect before acting.
2. Read the saved ship action. If accessible project/T3 ship behavior already exists, inspect and reconcile it; there is no assumed Ship API. If unconfigured, route to setup for an exact effect/target. `ready`, `push`, `merge`, `command` and `prompt` have distinct effects; document any configured multi-operation effect explicitly.
3. Reread authoritative Git/host state and confirm the intended revision/base/target. Verify applicable spec/ticket approvals, review and QA. If changed or missing, complete that work first; do not ship stale evidence. Check actual host merge restrictions and runtime permissions in addition to local bookkeeping.
4. Record the user's source-cited instruction with `tasks.py ship-request --revision ... --evidence ...`, then inspect `ship-plan`. The helper executes nothing and cannot authenticate a user statement; only record statements actually observed in the conversation.
5. If allowed, reserve a unique `ship` action for the configured exact target, perform only the configured operation using supported tools, and record the observed outcome. Link a PR immediately after any creation/push when required by T3. Marking ready does not authorize merge/deployment; a successful command start is not a verified deployment.
6. Reconcile uncertain outcomes against the host before retrying. A successful recorded ship consumes the request; it is not authority to ship a later revision or a second effect. Report exact action, revision, result, evidence, and remaining limitations.

Do not fabricate a ship request to make the gate pass. Local records support the agent's reasoning; runtime/user authorization remains authoritative.

