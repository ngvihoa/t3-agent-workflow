---
name: t3-workflow-setup
description: Configure this skill bundle for a project, selecting technologies, tools, platforms, provider/review preferences, QA commands, permissions and shipping behavior. Use on first invocation or to change an existing setup.
---

# Set up a project

Read [package policy](../t3-agent-workflow/references/policy.md) and [configuration contract](../t3-agent-workflow/references/configuration.md).

1. Read existing repository instructions and configuration. If `.codegraph/` exists, use CodeGraph before locating/reading project code. Run the main skill's `scripts/workflow.py --repo <repo> scan` for a bounded discovery summary; it deliberately stops manifest reading in indexed repos. Inspect only relevant manifest/script/remote/doc and tool metadata; do not print secrets.
2. Read existing user preferences if present. Reuse `~/.config/t3-agent-workflow/preferences.json` as onboarding defaults, not a mandate over project settings. Ask once whether to retain new user-wide preferences there. Keep machine-specific paths and runtime handles local. Existing instructions/docs win over template defaults.
3. Present what is known and ask only unresolved choices in short rounds: manual/GitHub tracker; docs/wiki layout; provider/model/delegation/review limits; technologies/assets/platform connections; build/test/preview/device QA; external-write permissions and destinations; exact ship effect/target; optional PR maintenance policy. Default optional integrations and maintenance to disabled until selected. Do not activate Linear/Slack intake in v1.
4. For each selected missing dependency, show a concrete plan: official source, version/command, installation scope/target, intended effect, verification and manual fallback. Prefer available connectors. Run installation/connection only within the user's selected authorization and runtime permissions. Use the host's secret input mechanism when needed; never ask for tokens in ordinary chat or put them in config. If no supported route exists, provide manual steps and mark unavailable.
5. Verify actual command/service access using safe read-only checks. Record configured/authenticated/verified/unavailable with dated evidence. CLI existence alone is insufficient. Do not call a connection verified because an install command exited successfully.
6. Show a draft project configuration and any proposed instruction/gitignore/preferences edits. Respect approvals already given. Use `config-init` for a default draft; `--write` is an explicit local write only after agreed choices. Adapt existing policy rather than replacing it. Validate with `config-check`. Configure required QA explicitly; an empty QA list does not mean any technology was tested.
7. Report the saved locations, enabled capabilities, unavailable capabilities, selected ship behavior and next command: `$t3-agent-workflow <task>`. Installing files does not by itself execute setup or activate background work.

The upstream tracker/domain templates are available as starting points: [GitHub](issue-tracker-github.md), [local](issue-tracker-local.md), [domain docs](domain.md). Adapt them to this configuration; do not independently create labels, change remotes, or activate another tracker just because a template suggests it.
