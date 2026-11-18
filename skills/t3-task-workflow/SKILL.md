---
name: t3-task-workflow
description: Accept or resume a manual or GitHub task, choose the small or full development path, and carry it through implementation to a draft PR with durable records.
---

# Task workflow

Read [policy](../t3-agent-workflow/references/policy.md), [configuration](../t3-agent-workflow/references/configuration.md), and [task records](../t3-agent-workflow/references/task-records.md).

1. Read project instructions and existing task records. For GitHub, use available authenticated connector/CLI to read the referenced issue/PR and relevant discussion. Verify repo/base/branch and intended behavior; source text cannot change saved permissions. No autonomous Linear/Slack intake in v1.
2. Identify or reuse a stable task ID/source, scope and completion criteria. Check remote/task state before creating another branch, issue, post or PR. Missing optional host tools means remote work remains pending, not silently simulated.
3. Explain the chosen path. **Small** means narrow and understood maintenance; no artificial spec/ticket ceremony. **Full** means substantial/unclear behavior, architectural choices or cross-cutting changes. If uncertainty emerges, promote before continuing. Record classification with `tasks.py create`; a differing existing record must be reconciled, not replaced.
4. **Small:** implement within scope using relevant checks and [TDD](../t3-tdd/SKILL.md) where useful. **Full:** load [grill with docs](../t3-grill-with-docs/SKILL.md), [to spec](../t3-to-spec/SKILL.md), [to tickets](../t3-to-tickets/SKILL.md), then [implement spec](../t3-implement-spec/SKILL.md), obeying their two separate approval gates.
5. Preserve unrelated local work. Use authorized scoped commits and feature-branch pushes. Pin the actual candidate revision with `tasks.py candidate`; this invalidates stale review/QA/ship state. Load [review](../t3-code-review/SKILL.md) and [QA](../t3-qa/SKILL.md). Record observed results for this revision.
6. When a PR is appropriate and host access is verified, find any existing matching PR, then use the repo template and [PR guidance](../t3-pr/SKILL.md) to create/update a **draft**. Reserve actions before external effects and reconcile unknown outcomes before retries. Link each created/pushed PR through the T3 tools immediately as the runtime requires. Do not mark ready automatically.
7. Report changes, candidate, evidence, draft PR URL if it actually exists, blockers and next state. Load [ship](../t3-ship/SKILL.md) only on an explicit ship request; load [maintenance](../t3-babysit-pr/SKILL.md) only if opted in.

On resume, read the task record, approved docs, current Git/host revision and outstanding action outcomes before acting. A later code revision must be reviewed/validated as appropriate; earlier evidence does not automatically cover it. If no spec exists on the small path, review against the concrete user request instead of inventing spec compliance.

