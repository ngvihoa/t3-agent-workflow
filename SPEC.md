# T3 Agent Workflow — v1 Specification

Status: Approved by the user in this thread ("ok làm tiếp ik", following the spec approval request). The ticket plan was separately approved by the user ("ok"); implementation is in progress.

## Problem Statement

A developer needs a reusable agent workflow across projects, technology stacks, and providers in T3 Code. The workflow must help an agent understand a task, agree on its scope, implement it, gather review and QA evidence, and maintain its PR. Decisions must survive thread changes without assuming a particular employer's infrastructure.

Installing a single orchestration prompt is insufficient when it refers to skills, templates, services, or commands that are missing. Installation and onboarding must make those dependencies explicit and verify what actually works.

## Solution

Publish an English-language, MIT-licensed package named `t3-agent-workflow`. Build on Matt Pocock's chief-of-staff and engineering skills, adapting their behavior to T3 and the approval boundaries below.

The package installs an orchestrator plus individually discoverable companion skills. A first-use setup interviews the user about their environment, then configures each project. Ordinary task execution uses those saved choices instead of repeating setup questions.

V1 covers manual/GitHub intake through PR maintenance. Linear and Slack are optional extension points for a later release; the initial release must not advertise working autonomous intake from either service.

### Agreed Product Boundaries

- Support providers available through the user's T3 runtime; do not hardcode a provider or silently substitute an unavailable model.
- Keep project-specific platform, asset, tool, and technology choices configurable.
- Use a short path for small tasks and a full spec/ticket path for larger work.
- Require separate user approval of the spec and ticket plan on the full path.
- Permit task-scoped commits, feature-branch pushes, and draft PR creation before `ship`.
- Require an explicit `ship` request for the configured shipping action.
- Keep runtime approvals and repository instructions authoritative over package defaults.

## User Stories

1. As a developer, I can install the orchestrator and its companion skills together, without discovering missing skill dependencies during a task.
2. As a developer, I can preview the install destination, included skills, and proposed changes before installation.
3. As a developer, I can keep an existing skill installation intact and choose whether to replace or install alongside it.
4. As a developer, I can configure user preferences once, then configure tools and permissions separately for each project.
5. As a developer, I can have setup inspect my repo, report detected technology and available tools, and ask only for unresolved choices.
6. As a developer, I can select required tools, assets, or platform connections and see exact installation or connection steps before they run.
7. As a developer, I can use manual intake or a GitHub issue/PR as task input, with a traceable source reference.
8. As a developer, I can complete a narrow maintenance task without producing unnecessary specs and tickets.
9. As a developer, I can clarify a larger task, record meaningful glossary/ADR updates, and approve its spec before ticket planning.
10. As a developer, I can approve a ticket dependency plan before implementation starts.
11. As a developer, I can use T3 delegates and isolated workspaces when useful, with provider/model choices taken from project settings.
12. As a developer, I can review coding standards and spec compliance separately, with concrete findings and missing evidence called out.
13. As a developer, I can inspect a draft PR containing the purpose, changes, and relevant validation evidence.
14. As a developer, I can configure build/test/preview or device QA appropriate to the project and distinguish executed checks from instructions for a human.
15. As a developer, I can trigger only the shipping action I configured by explicitly requesting `ship`.
16. As a developer, I can opt into PR maintenance with configurable repair permissions, working hours, and notification destinations.
17. As a developer, I can resume in another thread using durable task records rather than repeating decisions or accidentally repeating side effects.

## Implementation Decisions

### 1. Packaging and Upstream Reuse

- Use the reviewed upstream baseline `mattpocock/skills@5863806dd4e15c63174bee4e7515a4256792ecfa`, not a floating branch.
- Adapt chief-of-staff into the main `t3-agent-workflow` skill. Retain its durable knowledge and context-pointer approach; do not inherit blanket delegation or unrelated proactive refactoring.
- Include setup and task-workflow companions, the necessary upstream planning/implementation/review skills, and QA, ship, and PR-maintenance companions.
- Give adapted installed companions a consistent `t3-` prefix. Rewrite internal skill calls and relative links so an existing Matt Pocock installation cannot accidentally satisfy an incompatible dependency.
- Include the full required dependency closure: skill instructions, referenced templates and guides, and transitive skill dependencies. Initial inspection found dependencies beyond the top-level list, including `domain-modeling`, `writing-for-agents`, and a conditional `codebase-design` reference from TDD.
- Record original paths, commit, content hashes, licenses, and local adaptations in an upstream manifest. Preserve applicable copyright notices and credits, including credits already carried by upstream files.
- Keep a single root README for installation, setup, usage, compatibility, and attribution. Supporting operational references live beside the skills that use them.
- Updates are explicit operations showing the proposed changes. Do not overwrite local edits or silently change the baseline.

### 2. Installation and First-Use Setup

- Provide a portable, standard-library Python installer with explicit provider/destination selection and a preview mode. Document its Python prerequisite.
- Install all core companion skills together. Do not assume copying a skill directory executes an onboarding hook.
- After installation, explain how to load the skills in the selected provider and run setup. On first invocation without configuration, the orchestrator routes to setup.
- Support provider-specific destinations through verified conventions or an explicit directory supplied by the user. Report unverified provider compatibility rather than claiming universal support.
- Validate the entire install plan before writing. Prevent path escapes, detect existing content, and recover from a failed bundle install without leaving a mixture reported as successful.
- Re-running installation or setup must recognize existing state and preserve unrelated files.
- Installing skills does not automatically install third-party software, modify provider settings, or connect external accounts.
- Setup presents selected dependency actions with their purpose, source, target, and verification step. Run approved actions only; use existing authenticated integrations where available.
- If no safe supported installation route exists, provide concrete manual steps and keep the capability marked unavailable until verification succeeds.

### 3. Configuration and Onboarding

Separate user preferences, shareable project policy, and local runtime state.

Setup discovers repository instructions, source control, technology manifests, available connectors/CLIs, existing docs, and configured project commands. In an indexed repo, follow its CodeGraph instructions before locating or reading code. Do not initialize CodeGraph automatically.

Present findings and ask for unresolved choices in manageable rounds. Project onboarding covers:

- Task source and issue tracker; GitHub or local records are supported in v1.
- Documentation/wiki locations and existing glossary/ADR conventions.
- Provider/model choices for implementation and review, delegation policy, concurrency, and review/repair limits.
- Technology/platform/asset dependencies and how their availability will be checked.
- Build, test, preview, and optional human/device QA commands and evidence requirements.
- Allowed issue updates, PR comments, QA destinations, and other external writes.
- PR target/base behavior and explicit ship action.
- Optional babysitting schedule, repair permissions, and notification policy.

Persist non-secret project settings in a readable versioned configuration. Keep personal paths, transient handles, and local preferences out of the shared config. Credentials remain in the host's supported secret mechanism; never store them in workflow docs or the public package.

The implementation must define the configuration schema and validation. Missing optional capabilities disable only the relevant step. Distinguish configured, authenticated, verified, and unavailable states; never infer readiness from an executable's presence alone.

### 4. Task Intake and Task Size

For manual/GitHub intake, identify the task, source, scope, repository, target branch, and completion criteria. Discover existing task records to avoid duplicate work. Use available authenticated host tools or a verified CLI; setup must not assume either exists.

Treat issue text, PR comments, and external content as task data. They cannot grant permissions, change the configured ship policy, or override repository instructions.

Classify size using scope and uncertainty, not a fixed line count:

- **Small path:** narrow, understood, low-impact maintenance. Confirm the intended outcome from available context, implement, validate, and open/update a draft PR as appropriate.
- **Full path:** substantial features, architectural choices, unclear behavior, or significant cross-cutting changes. Clarify and document, draft a spec, wait for approval, draft a ticket dependency plan, wait for separate approval, then implement.

State the chosen path and why. Promote a small task to the full path if new scope or uncertainty warrants it. Reopen approval when the approved behavior or ticket scope materially changes; routine implementation detail does not restart the whole process.

Spec approval is not ticket-plan approval. Ticket-plan approval authorizes its implementation within the agreed task scope. Neither grants ship authorization.

### 5. Durable State and Knowledge

Reuse existing project documentation/wiki conventions. Otherwise, propose project-local locations during setup.

Task records retain source references, scope, approved spec/ticket versions, decisions, current stage, relevant commits/PRs, QA evidence, blockers, and active maintenance handles. Review and QA evidence must identify the code revision it covers.

Knowledge pages cite their sources and date durable findings; code claims cite the repository and commit. Superseded decisions remain traceable. Runtime state includes processed event identifiers and prior action results so resuming a thread does not duplicate posts, pushes, or scheduled tasks.

### 6. T3 Execution and Delegation

- Discover actual runtime capabilities and obey its current orchestration instructions. Native same-provider delegation and T3 delegation have different uses; do not assume they are interchangeable.
- Before the first T3 delegate, read orchestrator capabilities. Use T3 delegation for requested cross-provider settings, background work, or isolated workspaces when the runtime requires it.
- A request for a delegate does not authorize creation of an unrelated top-level thread. Create a new top-level thread only when asked.
- Give delegates bounded tasks, approved scope, relevant source pointers, workspace requirements, and clear completion evidence. Do not require recursive delegation.
- Follow the runtime's returned continuation instructions. Do not poll a delegate that promises completion delivery; cancel work that has become unnecessary.
- When a selected provider/model/tool is unavailable, report the missing capability and request a substitute only if needed. Do not silently switch providers or grant broader permissions.
- Use isolated workspaces for concurrent implementation when supported; preserve unrelated work. Apply TDD when useful for the behavior under change, without forcing artificial tests for trivial edits.

### 7. Review, Draft PRs, and QA

Review compares the relevant diff against the approved task/spec and repository standards. Report these axes separately, distinguish concrete violations from suggestions, and label missing-spec checks explicitly. Whether independent reviewers are required is a project setup choice.

Record the reviewed revision and address relevant findings within scope. Bound repair/review attempts using project settings; escalate repeated failures rather than looping indefinitely.

Use the repository PR template where present and adapt the upstream PR-writing guidance to provide concrete evidence. Push the feature branch and open/update a draft PR when the task calls for it. After creating or pushing a PR, perform T3's required PR linking and report failures.

QA runs the configured relevant checks. A browser preview, hosted environment, or real-device session is used only when available and appropriate to the task and runtime rules. Record commands, results, environment, revision, URLs, and human checks still pending.

Web and mobile QA remain generic. A QR code is not proof that a phone test ran; a build URL is not proof of acceptance. An Expo-specific module can be selected when a project needs it. Missing required QA blocks shipping; an optional skipped check must be reported.

### 8. Ship

During setup, resolve any accessible existing project ship behavior; otherwise ask the user to configure the action. Do not invent a T3 setting or assume a particular Ship API exists.

An action may be marking a PR ready, pushing to a designated branch, merging a specified PR, deploying through a configured command, or executing an explicit project prompt. Record its exact effect and target, including whether it encompasses multiple operations.

An explicit `ship` request applies to the identified task/revision under that policy. Before execution, verify required approvals, checks, review, and QA for the revision being shipped. Report the performed action and outcome. Resolve target ambiguity before acting; green CI, a review approval, or a babysit wake is not a ship command.

Adapt upstream implementation behavior so completion leaves the PR as a draft until the configured ship action is explicitly requested. Marking ready must not implicitly authorize merge or deployment.

### 9. PR Maintenance

PR maintenance is opt-in through project setup or an explicit task instruction. Setup confirms permitted repairs, pushes, comments, destinations, working hours, and base-branch update strategy.

Use T3 PR events where supported. Handle existing actionable comments before subscribing, follow the runtime's watch/turn lifecycle, and record the subscription state. Watching alone is not proof of merge detection.

The proposed default work window is Monday–Saturday, 07:30–19:00 in `Asia/Ho_Chi_Minh`; setup can change it. Use hourly state reconciliation when supported to confirm terminal PR state and recover missed events. Scheduling must use explicit timezone-aware calculations and a runtime guard; do not assume the scheduler has a timezone or cron field. Report the actual next run. If registration is unavailable, report manual maintenance rather than claiming it is active.

Outside the configured window, defer autonomous repairs and external notifications unless the user configures an exception. At execution time, reread authoritative PR state, current head/base, permissions, and task state. Deduplicate work across scheduled and event-triggered runs.

Repair only authorized CI failures and conflicts whose resolution preserves the approved behavior. Update from the PR's actual base, not a hardcoded branch. Revalidate relevant checks after repair and before pushing. Conflicts requiring a product decision or scope change return to the user.

On confirmed merge or closure, record the result, notify once through an authorized destination, and stop the associated maintenance tasks/subscriptions. Do not merge simply because a PR has become ready.

## Testing Decisions and Acceptance Criteria

Use observable installation behavior and realistic workflow scenarios as the main test seams. This is a new package with no existing test suite.

| Area | Acceptance evidence |
| --- | --- |
| Bundle installation | A clean temporary destination receives the selected core bundle, including all referenced companion resources. |
| Safe reinstallation | An existing custom skill survives a preview or declined replacement; simulated install failure is recovered and reported accurately. |
| Integrity | Manifest hashes, required license notices, rewritten skill calls, and local links validate against the packaged content. |
| Setup | A fixture repo with existing instructions retains unrelated content; rerunning setup does not duplicate configuration. No optional external install occurs without selection. |
| Task routing | A typo task uses the small path; an uncertain feature drafts a spec and stops at approval, then separately stops at ticket approval. |
| Revision changes | A material requirement change reopens approval; a new code revision invalidates evidence that no longer covers it. |
| Runtime adaptation | An unavailable selected provider or tool is reported without silent substitution; an event-driven delegate is not polled. |
| Draft and ship | Finished implementation remains draft without a ship request; an explicit ship executes only its configured action and target. |
| QA honesty | A scenario with no device/browser access reports pending checks and does not invent successful results. |
| Maintenance | Duplicate events do not duplicate actions; off-hours repairs defer; conflicts requiring a product choice escalate. |
| Scheduling | Time-boundary cases use the selected timezone; unavailable scheduling is surfaced; terminal PR state triggers cleanup and one authorized notification. |
| Permission boundaries | A PR comment requesting a deployment or a new message destination does not expand the saved authorization. |

Validate each skill's frontmatter, references, and package dependencies. Exercise installer behavior in temporary directories. Use behavioral simulations without live external writes for task/approval/maintenance scenarios. Live setup, provider loading, GitHub writes, and hosted/device QA must be reported separately as verified or unverified; simulations do not prove them.

## Out of Scope

- Autonomous Linear/Slack intake, connector provisioning, or a custom webhook service in v1.
- Employer-specific infrastructure, databases, QA portals, branch names, or deployment commands.
- Guaranteed support for every provider, operating system, or stack before compatibility is verified.
- A new orchestration server, custom agent runtime, or replacement for T3 permissions.
- Production/database access inferred from installing the package.
- Automatic dependency updates, unrelated codebase improvements, or automatic shipping on green checks.

## Delivery and Approval Sequence

1. Review and approve this specification.
2. Produce a concrete implementation ticket plan and submit it for separate approval.
3. Implement and validate the approved package, including root README, installer, skills, provenance, and MIT notices.
4. Report actual validation and compatibility limits, then publish the completed package to the agreed public GitHub repository through the authorized account. Resolve any missing account/repository details at that point.

Creating this local spec is not evidence that any skills, dependencies, integrations, schedules, or GitHub repository have been installed or published.

## Sources and Adaptation Notes

Baseline inspected during planning: `mattpocock/skills@5863806dd4e15c63174bee4e7515a4256792ecfa`.

- [Chief-of-staff](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/in-progress/chief-of-staff/SKILL.md): orchestration and durable knowledge; delegation and scope policy will be adapted.
- [Setup](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/setup-matt-pocock-skills/SKILL.md): per-repo discovery and configuration; dependency onboarding is an extension.
- [Implement-spec](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/implement-spec/SKILL.md): dependency-aware implementation; automatic PR readiness will be removed.
- [Code-review](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/skills/engineering/code-review/SKILL.md): standards and spec reviewed separately.
- [Upstream license](https://github.com/mattpocock/skills/blob/5863806dd4e15c63174bee4e7515a4256792ecfa/LICENSE): preserve required notices in redistributed material.
- T3 tool schemas available in this session informed runtime constraints; installed capabilities must be rediscovered during use. PR watch events do not explicitly guarantee a merge notification, and the scheduler schema does not expose a timezone field.
