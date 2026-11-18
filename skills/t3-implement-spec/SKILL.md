---
name: t3-implement-spec
description: Implement an approved spec and ticket dependency plan using the project execution policy, retaining a draft PR until explicit ship.
---

# Implement an approved graph

Read [policy](../t3-agent-workflow/references/policy.md), [task records](../t3-agent-workflow/references/task-records.md), and [T3 runtime contract](../t3-agent-workflow/references/t3-runtime.md). Verify both approvals and current document hashes before coding.

Read the ticket graph. Choose an integration branch consistent with the repo policy and preserve unrelated work. Work only tickets whose blockers are complete. Delegate only if allowed; use supported isolated workspaces for concurrent code changes and let the runtime create/bind them. A missing selected provider is a blocker for that choice, not permission to substitute.

Give each implementer an approved scope, source pointers, expected outcome and validation. Use [TDD](../t3-tdd/SKILL.md) where meaningful. Merge completed work through the repo's authorized integration process, resolve within scope, and validate affected behavior. Cancel superseded delegates and obey returned continuation instructions instead of polling.

Record completed tickets and coherent commits. Create/update a draft PR as appropriate once a real diff exists; write evidence with [PR](../t3-pr/SKILL.md) and immediately link created/pushed PRs through T3. Do not close issues early just because a command started.

On material scope change, return to affected approval gates. Otherwise continue the graph autonomously. At completion pin the candidate revision, run [code review](../t3-code-review/SKILL.md) and [QA](../t3-qa/SKILL.md), repair relevant findings within configured limits, then report the result. Leave the PR draft. Only [ship](../t3-ship/SKILL.md) on an explicit instruction may perform the configured readiness/merge/deployment effect.

Clean up only owned workspaces whose work has been integrated and verified. Suggest a [retro](../t3-retro/SKILL.md) when useful; do not turn its suggestions into unrelated changes.
