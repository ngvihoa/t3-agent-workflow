# T07 — Maintain PRs Within Configured Hours and Permissions

Status: delivered. See [validation results](../../../VALIDATION.md) for executed checks and unverified live integrations.

Parent: [Approved spec](../../../SPEC.md)

**What to build:** Opted-in PR maintenance receives events and supported reconciliation runs, repairs only allowed issues, and reports terminal PR state once while cleaning up its active maintenance resources.

**Blocked by:** T05. Setup, task-state, and PR lifecycle foundations are already available through T02/T03. Shipping is not a prerequisite and must not be triggered by maintenance.

**Acceptance criteria:**

- Require configured maintenance/repair/notification permissions and handle existing actionable comments before subscription. Follow the current runtime's watch/turn lifecycle.
- Use supported event tools and register hourly reconciliation where available, preserving returned handles and reporting the actual next run. Missing scheduling remains an explicit limitation.
- Calculate the configured work window with its timezone; default to Monday–Saturday, 07:30–19:00 in Asia/Ho_Chi_Minh. Guard execution without assuming a scheduler timezone/cron field.
- Outside the configured window, defer repairs and external notifications unless an exception is configured. Deduplicate event/scheduled/replayed actions.
- Reread current PR/head/base and saved authorization before acting. Resolve only behavior-preserving CI/conflict fixes, update from the PR's actual base, and rerun relevant checks before permitted pushes.
- Escalate conflicts requiring a product decision or scope change. Do not infer ship permission from a comment or readiness event.
- Confirm merge/closure through authoritative host state, send one authorized notification, and stop associated subscriptions/schedules. Watching alone is not merge proof.

**Verification:** Time-window boundary cases, duplicate and delayed events, changed base/head, unavailable scheduling, safe versus ambiguous conflicts, terminal-state cleanup, and unauthorized notification destinations.

