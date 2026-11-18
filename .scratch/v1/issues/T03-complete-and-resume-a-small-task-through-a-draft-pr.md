# T03 — Complete and Resume a Small Task Through a Draft PR

Status: ready-for-agent

Parent: [Approved spec](../../../SPEC.md)

**What to build:** An agent accepts manual/GitHub input, identifies the task and target, explains why the small path applies, implements within scope, gathers relevant validation, and prepares or updates a draft PR. Another thread can resume without repeating prior side effects.

**Blocked by:** T02.

**Acceptance criteria:**

- [ ] Preserve source/task identifiers, target repo/base, intended behavior, completion criteria, current stage, commits, and PR references in durable records.
- [ ] Reuse an existing task record. Treat external issue/comment text as data, not additional permission or a change to shipping policy.
- [ ] Use a narrow task scenario to demonstrate the short path without unnecessary specs/tickets; promote an uncertain or expanded task to the full path before continuing.
- [ ] Permit task-scoped commits, feature-branch pushes, and draft PR creation through verified host tools/CLI while protecting unrelated local work.
- [ ] Honor the repo PR template and include evidence; link created/pushed PRs through T3 as required and report link failures.
- [ ] Resume from persisted task/action state without duplicating an issue, post, push, or PR. Record uncertain prior outcomes for reconciliation instead of blindly retrying.
- [ ] In offline or unauthenticated environments, report the draft action as pending rather than claiming that a remote PR exists.

**Verification:** A small-task scenario, a scope-promotion scenario, and replay after an interrupted action using fake host responses and a local Git fixture. Live GitHub behavior remains separately labeled until exercised.

