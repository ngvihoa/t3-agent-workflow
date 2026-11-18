---
name: t3-to-tickets
description: Break an approved spec into independently verifiable tickets with blocking relationships and obtain separate plan approval.
---

# Plan tickets

Read [policy](../t3-agent-workflow/references/policy.md) and [task records](../t3-agent-workflow/references/task-records.md). Confirm the exact spec version has user approval before decomposition.

Draft tickets as small, independently verifiable end-to-end outcomes. For each, state title, what it delivers, real blockers, acceptance evidence and scope. Avoid a horizontal list of layers or gratuitous prefactoring. Where a genuinely wide mechanical refactor cannot land in slices, explain its expand/migrate/contract ordering and final integration check.

Present the concrete dependency graph and ask whether the division and blocking edges fit. Wait for a separate ticket-plan approval. Record the plan's exact file hash and approval using `tasks.py document/approve --kind tickets`. Spec approval does not approve this plan.

Publish approved tickets only through authorized tracker writes. For local work, create one file per ticket with status, source spec, blockers and acceptance criteria; the plan document can remain the index. Do not close the parent issue. Execute only the ready frontier via [implement spec](../t3-implement-spec/SKILL.md). Graph parallelism is an opportunity, not permission to use extra providers/delegates.
