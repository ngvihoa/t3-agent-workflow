# T3 Agent Workflow

A reusable skill bundle for development in T3 Code: clarify, plan, implement, review, QA, explicitly ship, and optionally maintain a PR. Adapted from Matt Pocock's skills, with project-specific onboarding and T3 runtime rules.

Requires Python 3.11+ for the offline installer and helpers. Skills are Markdown and use the tools exposed by your agent runtime. No third-party Python runtime dependencies.

## Install

```sh
git clone https://github.com/ngvihoa/t3-agent-workflow.git
cd t3-agent-workflow
```

Preview an explicit skills directory, then apply the reviewed selection:

```sh
python install.py --dest /path/to/your/agent/skills
python install.py --dest /path/to/your/agent/skills --apply
```

`--provider codex` selects the `~/.codex/skills` convention; `--provider claude` selects `~/.claude/skills`. These are directory choices, not claims of live-tested provider loading. Other providers use `--dest` with their supported skills directory. Start a new agent turn/session if discovery requires it, then invoke `$t3-workflow-setup` in the target repo.

The installer defaults to preview. Existing conflicting content is preserved unless `--replace` is selected. `--prefix team-` installs a separate `team-t3-*` namespace and rewrites internal references together. Preview replacement/namespace changes before applying them.

An interrupted transaction blocks further installs. Run `python install.py --dest /path/to/your/agent/skills --recover`, inspect the restored destination, then preview again. Recovery errors are reported rather than claiming a partial bundle is complete.

Installing does not run setup, install technology tools, connect accounts, modify provider settings, or start schedules. First-use setup presents those choices separately.

## First use

Open the target project in T3 and ask your agent:

```text
Use $t3-workflow-setup for this repository.
```

Setup discovers existing repo instructions, technologies, commands and integrations; asks unresolved choices; then shows the proposed configuration and dependency actions. Select only the platforms/tools/assets you need. A missing supported installation route is reported with manual steps. Service readiness needs observed verification, not just saved settings or an installed CLI.

You choose provider/model and delegation policy, independent review and limits, docs/wiki locations, QA commands, exact ship behavior, optional PR maintenance hours and repair permissions. User preferences can be reused across projects; shared project config and machine-local state are separated. Credentials stay in host-supported secret storage.

Start a task with:

```text
Use $t3-agent-workflow to fix the login error described in this GitHub issue: <issue URL>.
```

Or describe a task manually. Small, understood maintenance goes directly to implementation and relevant validation. Larger/uncertain work follows clarification → **spec approval** → **ticket-plan approval** → implementation. Agent-scoped commits, feature-branch pushes and draft PRs are allowed within task/runtime authorization. The result remains draft until an explicit ship request under your project policy.

```text
Ship the reviewed candidate for this task using this project's configured action.
```

That can mean ready-for-review, a designated push, a PR merge, or an explicit project command/prompt. Marking ready does not imply merge/deploy. Required approvals, current review and QA still apply; a changed revision invalidates stale evidence.

## Included skills

| Skill | Role |
| --- | --- |
| `t3-agent-workflow` | Main entrypoint and routing |
| `t3-workflow-setup` | Per-project discovery and onboarding |
| `t3-task-workflow` | Intake, size classification and resume |
| `t3-grill-with-docs`, `t3-grilling`, `t3-domain-modeling` | Clarification, glossary and meaningful ADRs |
| `t3-to-spec`, `t3-to-tickets`, `t3-implement-spec` | Separately approved planning and implementation |
| `t3-tdd`, `t3-codebase-design` | Behavior-focused testing and interface references |
| `t3-code-review`, `t3-pr`, `t3-qa` | Separate standards/spec review, PR writing and QA evidence |
| `t3-ship`, `t3-babysit-pr` | Explicit shipping and optional maintenance |
| `t3-retro`, `t3-writing-for-agents` | Scoped retrospective and documentation references |

There are 18 namespaced skills, including their referenced templates/guides. The agent can load sibling SKILL.md files directly if its runtime has no skill-loader tool. No separately installed Matt Pocock skills are required.

## Configuration and helpers

The [configuration contract](skills/t3-agent-workflow/references/configuration.md) describes `.t3-workflow/project.json`, user preferences and local overrides. The [task-record guide](skills/t3-agent-workflow/references/task-records.md) explains local state and bookkeeping CLI operations.

Helpers are inside the installed main skill's `scripts/` directory. Examples from a checkout, with the target project explicitly selected:

```sh
python skills/t3-agent-workflow/scripts/workflow.py --repo /path/to/project scan
python skills/t3-agent-workflow/scripts/workflow.py --repo /path/to/project config-init
python skills/t3-agent-workflow/scripts/workflow.py --repo /path/to/project config-init --write
python skills/t3-agent-workflow/scripts/workflow.py --repo /path/to/project config-check
python skills/t3-agent-workflow/scripts/tasks.py --repo /path/to/project --task login-fix show
python skills/t3-agent-workflow/scripts/maintenance.py --repo /path/to/project
```

`config-init` is a preview without `--write`; repeated initialization preserves existing configuration. Setup edits the agreed values and validates them. Helpers do not run saved commands, call hosts, authenticate user statements or register schedules. They record approvals/evidence that the agent has actually observed and reject inconsistent transitions. Runtime permissions and real host state remain authoritative.

Task/action state uses atomic writes and per-task locks. A started/uncertain remote effect must be reconciled before retrying. For an orphan lock, verify no writer/effect remains active before deliberately removing it; no automatic timeout deletes it.

PR maintenance is opt-in. Default window is Monday–Saturday, 07:30 inclusive–19:00 exclusive in Vietnam; hourly reconciliation slots start at 07:30. The planner returns explicit UTC times, but the agent must register work with supported T3 tools and record their actual returned handles/times. Work is guarded again at execution. If tools are absent, maintenance remains manual. Merge/closure is confirmed from the host, with saved resources cleaned up and at most one authorized notification.

## Compatibility and limits

- Provider-neutral instructions adapt to the tools actually exposed by T3. The package does not install or replace the T3 runtime.
- Codex/Claude directory conventions are provided; actual automatic discovery/loading has not been live-tested across providers. Other providers use an explicit supported destination.
- Local deterministic tests and an independent temporary-repo forward test are documented in [validation results](VALIDATION.md). They do not prove live GitHub task writes, PR watch/scheduler behavior, platform installation, hosted previews, or real-device QA.
- GitHub/manual intake is in v1. Automatic Linear/Slack intake and a custom webhook service are not included.
- Browser, deployment, Expo/device and database capabilities are project-selected optional tools; there are no bundled employer-specific environments or credentials.
- Python helpers support 3.11+. CI is configured for Linux/macOS/Windows and Python 3.11/3.13; report actual CI results rather than treating the matrix definition as proof. Non-Vietnam IANA zones need the operating system's timezone database; unavailable timezone data is reported.

## Updating and validation

Review upstream/package changes before pulling or replacing an edited installation. Preview again, then select `--replace` only if intentional, or use a new prefix. The baseline never changes automatically. Maintainers update `upstream.json`, preserve source/credit notices, adapt references, run `scripts/build_manifest.py` deliberately, then validate; end users should not regenerate hashes merely to bypass an integrity error.

Run deterministic checks:

```sh
python scripts/validate.py
python -m unittest discover -s tests -v
```

MIT. See [third-party notices](THIRD_PARTY_NOTICES.md), [upstream provenance](upstream.json), [spec](SPEC.md), and [approved plan](TICKET_PLAN.md). Updates require explicit source review, adaptation, manifest refresh, and revalidation.
