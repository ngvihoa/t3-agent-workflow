# T3 Agent Workflow — v1 Ticket Plan

Status: Approved by the user in this thread ("ok"). Implementation is authorized within the approved specification and ticket scope.

Parent: [Approved v1 specification](SPEC.md).

## Delivery Rules

- Each ticket delivers a verifiable path through the package, including relevant instructions, resources, and behavioral validation. Documentation is written in English.
- After approval, create one local ticket file per ticket, with these identifiers and blocking relationships. No external tracker is configured for this new repo yet.
- Work only on tickets whose blockers are complete. The graph permits independent work but does not itself request parallel agents or authorize provider changes.
- Keep each completed ticket reviewable in its own commit where practical. Preserve upstream provenance and applicable license/credit notices throughout.
- Record actual results and known compatibility limits. Sandbox results do not establish live service integration or provider loading.
- Implementation begins after the user approves this plan. A material change to the approved product scope returns to the spec approval gate.

## Proposed Breakdown

| ID | Ticket | Blocked by | Demonstrable outcome |
| --- | --- | --- | --- |
| T01 | Install a pinned, namespaced skill bundle safely | None | Preview and install a complete baseline into an isolated destination without overwriting existing skills. |
| T02 | Configure a project through repeatable onboarding | T01 | Inspect a fixture repo, resolve missing choices, save valid configuration, and rerun without duplication. |
| T03 | Complete and resume a small task through a draft PR | T02 | Manual/GitHub input follows the small path with traceable state and a draft PR action plan. |
| T04 | Execute larger work behind separate approval gates | T03 | A feature pauses at spec approval and ticket approval, then executes its dependency graph through T3. |
| T05 | Produce separate review findings and revision-bound QA evidence | T03 | A candidate has standards/spec findings and honest QA results for its revision. |
| T06 | Ship only the configured action on explicit request | T04, T05 | A ship request checks the correct revision and executes only the configured effect. |
| T07 | Maintain PRs within configured hours and permissions | T05 | Events/reconciliation yield deduplicated, authorized repairs and terminal-state cleanup. |
| T08 | Validate, document, and publish the reusable package | T06, T07 | A release has reproducible checks, accurate compatibility claims, and a public GitHub source. |

### T01 — Install a Pinned, Namespaced Skill Bundle Safely

**What to build:** A developer can obtain the package, inspect exactly which skills will be installed and where, then install its complete pinned baseline without damaging an existing installation. The installer continues to include companions added by subsequent tickets through a validated bundle manifest.

**Blocked by:** None.

**Acceptance criteria:**

- [ ] Adapt the orchestrator and required upstream dependency closure from the spec's pinned commit; include all referenced guides/templates and preserve licenses and inherited credits.
- [ ] Namespace adapted companions consistently and resolve internal skill calls and links inside this bundle, without relying on a separately installed Matt Pocock skill.
- [ ] Record upstream paths, commit, original/adapted hashes, and adaptation notes; verify the packaged content against that record.
- [ ] Preview reports provider/destination, additions, conflicts, and replacement choices without writing. Accept an explicit destination when a provider convention has not been verified.
- [ ] Standard-library Python installation validates the whole plan before writing, rejects path escapes, preserves unrelated files, and supports an explicitly chosen replacement or a consistently renamed side-by-side bundle.
- [ ] Reinstallation recognizes local edits. A simulated interrupted install restores prior content or clearly reports recovery required; it never reports partial content as a successful full bundle.
- [ ] Installed baseline instructions respect the spec's task scope and approval/ship boundaries. Missing project configuration routes to setup instead of executing upstream defaults.
- [ ] Introduce the root README's accurate install/load prerequisites and package licensing. Later tickets extend this same README.

**Verification:** Temporary-directory installs, preview/no-write checks, existing-content and failure-recovery cases, manifest/reference validation. Do not modify the user's live skill directories as a test.

### T02 — Configure a Project Through Repeatable Onboarding

**What to build:** Setup inspects a project and the runtime, asks only unresolved questions, then produces usable shared policy and separate local preferences/state. It explains and verifies selected optional dependencies rather than assuming they exist.

**Blocked by:** T01.

**Acceptance criteria:**

- [ ] Define and validate the configuration format, versioning, user/project precedence, and separation of non-secret policy from local state and credentials.
- [ ] Detect repository instructions, existing documentation, technology manifests, source control, available connectors/CLIs, and configured commands. Respect indexed-repo CodeGraph instructions without creating an index.
- [ ] Ask for the unresolved tracker/docs, provider/model and review policy, concurrency/repair limits, QA commands, external-write permissions/destinations, ship effect/target, and optional maintenance policy.
- [ ] Present selected technology/tool/asset/connection actions with their source, target, purpose, and verification. Execute only selected/approved changes; otherwise provide manual steps and keep the capability unavailable.
- [ ] Distinguish configured, authenticated, verified, and unavailable capabilities. An installed executable alone cannot make a platform verified.
- [ ] Re-running setup updates its own configuration without duplicating blocks or overwriting unrelated instructions; no credentials enter shared files.
- [ ] Absent optional tools disable only their affected path. Report unavailable provider choices without silent substitution.

**Verification:** Fresh and preconfigured repo fixtures; repeated setup; invalid configuration; missing CLI/auth; declined dependency changes. No live external writes are required to verify these cases.

### T03 — Complete and Resume a Small Task Through a Draft PR

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

### T04 — Execute Larger Work Behind Separate Approval Gates

**What to build:** A larger feature moves from clarification and durable decisions to spec, tickets, and implementation. The user approves the spec and ticket plan independently, after which the agent works the ready frontier using the runtime's supported execution tools.

**Blocked by:** T03.

**Acceptance criteria:**

- [ ] Adapt the planning/implementation companions and task-workflow routing to create only meaningful glossary/ADR updates and maintain source-cited, dated knowledge.
- [ ] Spec generation stops for explicit approval. Ticket planning starts only after that approval and stops again before implementation; record the approved versions.
- [ ] An approved ticket plan contains blocking relationships and independently checkable outcomes. Execute only tickets whose blockers are satisfied.
- [ ] Material requirement changes invalidate the relevant approval and return to the user; routine implementation decisions do not restart planning.
- [ ] Choose native or T3 delegation according to runtime instructions; read capabilities before T3 delegation and use isolated workspaces when needed without creating them manually against runtime rules.
- [ ] Supply bounded delegate briefs and context pointers, respect returned continuation instructions, cancel superseded work, and avoid mandatory recursive delegation or unsolicited top-level threads.
- [ ] TDD is used where it tests meaningful behavior. Retro/improvement suggestions remain within authorized scope and do not trigger unrelated refactors.
- [ ] Implementation completion leaves any PR as a draft and hands its candidate revision to review/QA.

**Verification:** A feature scenario paused at each approval gate; changed requirements after approval; a dependency graph with blocked/ready tickets; unavailable provider; event-driven continuation and cancellation cases.

### T05 — Produce Separate Review Findings and Revision-Bound QA Evidence

**What to build:** A draft candidate receives separate standards/spec review and project-appropriate QA. The result makes revision coverage, actionable failures, missing evidence, and human acceptance requirements visible.

**Blocked by:** T03. It can be developed independently of T04; integration with the full path is verified before release.

**Acceptance criteria:**

- [ ] Review the intended diff/base against repository standards and the approved spec or recorded small-task criteria. Report the two axes separately and label missing spec evidence.
- [ ] Apply the configured independent-review policy and bounded repair/review attempts; do not silently switch providers or expand task scope.
- [ ] Record the reviewed revision, findings, resolutions, and relevant reruns. A newer revision does not inherit stale review/QA approval automatically.
- [ ] Run configured relevant build/test/preview checks and record command, environment, revision, result, and URLs where available.
- [ ] Respect runtime browser restrictions. A QR code or preview URL is never recorded as proof that human/device QA ran.
- [ ] Support project-selected Expo/device instructions without requiring Expo for other projects. Report required pending checks and optional skips accurately.
- [ ] Update the existing draft PR evidence only within configured write permissions; leave it as a draft.

**Verification:** Standards-pass/spec-fail and inverse scenarios; missing spec/device/browser; failed required check; a changed revision; bounded repeated repair. Use a small fixture command for executed QA evidence.

### T06 — Ship Only the Configured Action on Explicit Request

**What to build:** The agent interprets an explicit ship request against the saved project policy and verified candidate revision, then performs and reports exactly that action.

**Blocked by:** T04, T05.

**Acceptance criteria:**

- [ ] Resolve an accessible project ship policy or use the configured explicit action; do not invent a T3 Ship API/setting.
- [ ] Require an explicit ship instruction for the task/revision; CI success, reviewer approval, and maintenance events never supply it.
- [ ] Check required spec/ticket approvals, review, QA, target, and current revision; stop for ambiguity, stale evidence, or a failed required check.
- [ ] Exercise ready-for-review, designated-branch push, PR merge, and configured command/prompt behavior through safe fakes. Execute only the configured effect; marking ready does not imply merge/deploy.
- [ ] Reconcile a previously attempted ship before retrying and record outcome/evidence. Respect runtime permissions for external effects.

**Verification:** Explicit and absent ship requests, ambiguous targets, changed head, incomplete QA, one successful configured action, and uncertain/replayed completion. Do not deploy or merge a live project as a test.

### T07 — Maintain PRs Within Configured Hours and Permissions

**What to build:** Opted-in PR maintenance receives events and supported reconciliation runs, repairs only allowed issues, and reports terminal PR state once while cleaning up its active maintenance resources.

**Blocked by:** T05. Setup, task-state, and PR lifecycle foundations are already available through T02/T03. Shipping is not a prerequisite and must not be triggered by maintenance.

**Acceptance criteria:**

- [ ] Require configured maintenance/repair/notification permissions and handle existing actionable comments before subscription. Follow the current runtime's watch/turn lifecycle.
- [ ] Use supported event tools and register hourly reconciliation where available, preserving returned handles and reporting the actual next run. Missing scheduling remains an explicit limitation.
- [ ] Calculate the configured work window with its timezone; default to Monday–Saturday, 07:30–19:00 in Asia/Ho_Chi_Minh. Guard execution without assuming a scheduler timezone/cron field.
- [ ] Outside the configured window, defer repairs and external notifications unless an exception is configured. Deduplicate event/scheduled/replayed actions.
- [ ] Reread current PR/head/base and saved authorization before acting. Resolve only behavior-preserving CI/conflict fixes, update from the PR's actual base, and rerun relevant checks before permitted pushes.
- [ ] Escalate conflicts requiring a product decision or scope change. Do not infer ship permission from a comment or readiness event.
- [ ] Confirm merge/closure through authoritative host state, send one authorized notification, and stop associated subscriptions/schedules. Watching alone is not merge proof.

**Verification:** Time-window boundary cases, duplicate and delayed events, changed base/head, unavailable scheduling, safe versus ambiguous conflicts, terminal-state cleanup, and unauthorized notification destinations.

### T08 — Validate, Document, and Publish the Reusable Package

**What to build:** A new user can install and use the release from public GitHub with a single accurate root README, a complete bundle, and explicit evidence of what has and has not been verified.

**Blocked by:** T06, T07. These dependencies transitively include all earlier tickets.

**Acceptance criteria:**

- [ ] Run the package validator and installer/configuration tests against the final bundle, including all new companions and supporting resources.
- [ ] Exercise small and full workflow scenarios end to end, including approval gates, revision changes, review/QA, explicit ship, and maintenance cleanup. Record observed actions rather than merely checking instruction wording.
- [ ] Add reproducible CI for deterministic package/installer/configuration checks. Separate agent scenario results and live integrations from those automated checks.
- [ ] Finish the single root README: prerequisites, install/preview/update/recovery, first-use setup, examples, permissions, compatibility, upstream attribution, and limitations. Do not claim autonomous Linear/Slack intake in v1.
- [ ] Report tested provider loading, operating systems, external service writes, hosted preview, and device QA separately from simulated coverage; leave untested combinations explicitly unverified.
- [ ] Confirm the public tree excludes credentials, personal paths, private project configuration, and employer-specific assets. Verify notices and the pinned upstream manifest.
- [ ] Resolve the authorized GitHub account and repository identity, publish `t3-agent-workflow` publicly, and report its URL and exact published commit. Existing repositories/content are not replaced without resolving that conflict.
- [ ] If a PR is created/pushed during delivery, perform the runtime's required linking immediately; a documentation-only claim of publication does not satisfy this ticket.

**Verification:** Final clean-destination installation, complete validation report, local fixture scenarios, actual public repository/commit verification. Do not imply live feature integrations were proven by publishing this package.

## Spec Coverage and Ordering

| Spec area | Owning tickets |
| --- | --- |
| Packaging, pinned reuse, licensing, safe installation and updates | T01, T08 |
| Setup, configuration, dependency selection, permissions, missing capabilities | T02 |
| Intake, task size, durable state, draft PRs and resume | T03, T04 |
| Approval gates, glossary/ADR/wiki, T3 delegation, meaningful TDD | T04 |
| Two-axis review, revision-bound evidence, generic web/mobile QA | T05 |
| Explicit configured shipping and readiness checks | T06 |
| Events, scheduling, timezone, repairs, deduplication and cleanup | T07 |
| Final behavioral acceptance, compatibility claims and public release | T08 |

Start with T01 → T02 → T03. Then T04 and T05 are independent work fronts. T06 requires both; T07 can proceed after T05. Finish T08 after T06 and T07.

The division into these eight tickets and their blocking edges is the remaining approval request. Once approved, routine implementation choices within these boundaries do not require another planning round.
