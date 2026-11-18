# Validation results

This report separates package checks, observed agent behavior and unverified integrations. It is release evidence, not a claim that every described runtime capability has run live.

## Deterministic checks

Local environment: Linux, Python 3.13.9. The package's standard-library validator checks bundle hashes, manifest/artifact coverage, skill entrypoints, UI metadata presence, local Markdown links outside examples, upstream adaptation hashes and license presence.

The unittest suite covers:

- Preview without writes; clean/repeated installation; local-edit preservation; explicit replacement and independent namespace installation.
- Failure rollback, interrupted-transaction recovery, source-integrity/path rejection and symlink destination rejection.
- Existing configuration/instructions, unavailable verification evidence, config validation and indexed-repo discovery behavior.
- Separate spec and ticket approval gates, changed approved documents, small-task resume/promotion, revision invalidation, distinct review axes and required independent review.
- Required QA simulation rejection, changed check definitions, explicit/consumed ship instructions, policy changes, unauthorized notifications and duplicate/uncertain actions.
- Vietnam work-window boundaries, hourly alignment, Saturday-to-Monday UTC scheduling, disabled scheduling and naive timestamp rejection.
- A real temporary install followed by installed CLI setup, a local Git commit, candidate/review bookkeeping and a blocked unconfigured ship plan.

Each skill also passed the available skill-creator frontmatter validator. That validator is a development check, not a runtime dependency. CI runs the package validator and unittest suite on Linux/macOS/Windows with Python 3.11 and 3.13. A configured matrix is not proof that those jobs have finished; consult the repository's actual Actions results.

## Independent forward test

A separate agent used the installed bundle in disposable repositories without modifying package source, calling external services, or creating real PRs/schedules.

- **Small maintenance:** reproduced a failing Python CLI unittest for `Welcom`, changed only the literal to `Welcome`, reran the passing test, committed the result, inspected the diff, and recorded actual review/QA for that fixture revision. The fixture worktree was clean. No remote/PR was claimed; ship planning remained blocked because shipping was unconfigured and no explicit request existed.
- **Unclear feature:** a configurable greeting-language request stayed in full-path clarification. The agent recorded pending questions about languages/configuration/fallback behavior; it did not invent approvals or start implementation.
- **Interrupted action:** a saved started reservation survived fresh helper processes. Duplicate reservation was rejected; the agent reconciled it after verifying that no external effect happened. This tests bookkeeping restart, not a real remote transaction.
- **Usability finding fixed:** read-only `config-init` originally displayed fresh defaults even when saved config existed. It now previews the validated existing config; an installed-CLI regression check covers this behavior.

The independent pass read the actual skills and executed fixture operations. It is distinct from deterministic tests, which verify helper behavior but cannot prove an agent will always follow instructions.

## Unverified live capabilities

- Automatic skill discovery/loading across T3 providers and operating systems.
- Live GitHub task issue/PR writes, merge/readiness operations, review delivery and repair pushes.
- T3 watch/scheduler registration, event delivery, terminal cleanup and notifications.
- Platform/tool installation, external account connections, hosted preview and browser QA.
- Expo QR/device testing and production/database/deployment access.

Publishing this source repository is separately observable and does not establish any of those integrations. Run project setup and verify only selected capabilities before relying on them.
