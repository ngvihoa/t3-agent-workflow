# T06 — Ship Only the Configured Action on Explicit Request

Status: delivered. See [validation results](../../../VALIDATION.md) for executed checks and unverified live integrations.

Parent: [Approved spec](../../../SPEC.md)

**What to build:** The agent interprets an explicit ship request against the saved project policy and verified candidate revision, then performs and reports exactly that action.

**Blocked by:** T04, T05.

**Acceptance criteria:**

- Resolve an accessible project ship policy or use the configured explicit action; do not invent a T3 Ship API/setting.
- Require an explicit ship instruction for the task/revision; CI success, reviewer approval, and maintenance events never supply it.
- Check required spec/ticket approvals, review, QA, target, and current revision; stop for ambiguity, stale evidence, or a failed required check.
- Exercise ready-for-review, designated-branch push, PR merge, and configured command/prompt behavior through safe fakes. Execute only the configured effect; marking ready does not imply merge/deploy.
- Reconcile a previously attempted ship before retrying and record outcome/evidence. Respect runtime permissions for external effects.

**Verification:** Explicit and absent ship requests, ambiguous targets, changed head, incomplete QA, one successful configured action, and uncertain/replayed completion. Do not deploy or merge a live project as a test.

