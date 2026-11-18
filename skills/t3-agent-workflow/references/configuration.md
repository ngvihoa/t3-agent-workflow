# Project configuration and setup contract

Shared policy: `.t3-workflow/project.json`, schema version 1. Create a draft with `python <installed-t3-agent-workflow>/scripts/workflow.py --repo <repo> config-init` (stdout only). After agreement, add `--write`, edit the selected values, then run `config-check`. Repeated initialization preserves existing content and rejects an unsupported schema rather than overwriting it. Helpers never execute saved commands.

User preferences can be recorded once at `~/.config/t3-agent-workflow/preferences.json`: `version: 1`, optional `language`, `execution`, and `review` preferences. Read these as onboarding defaults; explicit project choices override them. This is an agent-managed preferences file, not an implicit installer write. Reuse an existing preference file without changing unrelated settings. Store machine-specific overrides in `.t3-workflow/local/preferences.json`; read/validate those deliberately and show any override before relying on it. Never merge a local permission/ship override without the user's authorization.

| Field | Meaning |
| --- | --- |
| `tracker` | `local` or `github`; use existing verified connector or CLI. |
| `docs.tasks`, `docs.wiki` | Project-relative documentation locations. Reuse existing conventions. |
| `execution` | Provider/model (`inherit` default), delegation (`ask`, `allowed`, `disabled`), concurrency and repair/review limits (1..16). |
| `review.independent` | Whether to obtain a separate reviewer; requires a supported authorized delegate. |
| `qa` | List of `{id, command, required, kind}`; kind is `command`, `human`, `device`, or `browser`. A human check's command can be its procedure, not executable code. |
| `capabilities` | Named `{status, evidence}` objects; status is configured/authenticated/verified/unavailable. Verified needs observed evidence. |
| `permissions` | Explicit issue updates, PR comments, and allowed notification destination strings. Defaults allow none. |
| `ship` | Action (`unconfigured`, `ready`, `push`, `merge`, `command`, `prompt`), exact target, and command/prompt if applicable. No default shipping action. |
| `maintenance` | Enabled flag, timezone, weekdays (Monday=0), start/end HH:MM, interval in minutes, allowed repairs (`ci`, `conflicts`), and explicit outside-hours exception. |

Local task/action state lives in `.t3-workflow/local/tasks/`. Add `.t3-workflow/local/` to the project's gitignore after showing the change; it is not a safe place for credentials. Durable approved specs/tickets and dated wiki pages can be committed in the configured docs locations. Do not copy private content into this package's repository.

Config fields select behavior; they do not prove that a service is connected or grant authority beyond the user's task/runtime. Capability evidence should record the observation and time without tokens. When project commands change, show their intended effect before running them under existing authorization.

