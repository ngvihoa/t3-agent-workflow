# T3 Agent Workflow

A reusable skill bundle for development in T3 Code: clarify, plan, implement, review, QA, explicitly ship, and optionally maintain a PR. Adapted from Matt Pocock's skills, with project-specific onboarding and T3 runtime rules.

Requires Python 3.11+ for the offline installer and helpers. Skills are Markdown and use the tools exposed by your agent runtime. No third-party Python runtime dependencies.

Preview an explicit skills directory, then apply the reviewed selection:

```sh
python install.py --dest /path/to/your/agent/skills
python install.py --dest /path/to/your/agent/skills --apply
```

`--provider codex` selects the `~/.codex/skills` convention; `--provider claude` selects `~/.claude/skills`. These are directory choices, not claims of live-tested provider loading. Other providers use `--dest` with their supported skills directory. Start a new agent turn/session if discovery requires it, then invoke `$t3-workflow-setup` in the target repo.

The installer defaults to preview. Existing conflicting content is preserved unless `--replace` is selected. `--prefix team-` installs a separate `team-t3-*` namespace and rewrites internal references together. Preview replacement/namespace changes before applying them.

An interrupted transaction blocks further installs. Run `python install.py --dest /path/to/your/agent/skills --recover`, inspect the restored destination, then preview again. Recovery errors are reported rather than claiming a partial bundle is complete.

Installing does not run setup, install technology tools, connect accounts, modify provider settings, or start schedules. First-use setup presents those choices separately.

Run deterministic checks:

```sh
python scripts/validate.py
python -m unittest discover -s tests -v
```

MIT. See [third-party notices](THIRD_PARTY_NOTICES.md), [upstream provenance](upstream.json), [spec](SPEC.md), and [approved plan](TICKET_PLAN.md). Updates require explicit source review, adaptation, manifest refresh, and revalidation.
