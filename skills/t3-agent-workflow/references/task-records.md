# Durable task and action records

The main skill's `scripts/tasks.py` is a local bookkeeping CLI; it does not call GitHub, execute commands, or prove that a user actually approved a document. The agent must observe authorization and results before recording them. Run it as `python <main-skill>/scripts/tasks.py --repo <repo> --task <slug> <operation>`.

| Operation | Arguments and effect |
| --- | --- |
| `create` | `--size small/full --source <reference> --scope <criteria>`; same identity resumes, conflicting scope is rejected. |
| `show` | Show the saved record, including unresolved actions and maintenance handles. |
| `promote` | `--evidence <new-uncertainty-or-scope-reason>`; preserve action history, move to full path, clear approvals/evidence. |
| `document` | `--kind spec/tickets --path <project-relative-file>`; records content hash. Tickets require prior spec approval. |
| `approve` | `--kind spec/tickets --evidence <observed-user-statement-and-source>`; separate current-version approval. Never invent a statement. |
| `candidate` | `--revision <actual-Git-SHA>`; requires full-path approvals; changing revision clears review/QA/ship evidence. |
| `review` | `--revision ... --standards pass/fail --spec pass/fail --evidence ...`; add `--independent` only for an actually observed independent review. Small-task scope is its spec criterion. |
| `check` | `--revision ... --check <configured-id> --status pass/fail/pending/skipped --origin executed/human/simulation --evidence ...` |
| `ship-request` | `--revision ... --evidence <actual-user-ship-instruction>`; checks approvals/review/required QA and binds policy/revision. |
| `ship-plan` | Report allowed/errors/effect; never performs shipping. |
| `action-start` | `--key <stable-effect-key> --kind <kind> --target <exact-target>`; reserve before effects. Reused keys require reconciliation. |
| `action-finish` | `--key ... --outcome succeeded/failed/uncertain --evidence ...`; record observations. A completed ship consumes its instruction. |

Supported action kinds: issue-update, pr-comment, notify, pr-create, push, ship, repair, schedule. The helper rejects disabled external writes, unauthorized notification destinations, missing ship readiness, disabled maintenance, and off-hours/unapproved repair classes. It cannot independently discover source-control state or constrain what another tool executes; inspect those conditions live.

State is in `.t3-workflow/local/tasks/`. Writes use per-task locks and atomic JSON replacement. An orphan `.lock` after a crashed writer must be reconciled manually (verify no writer/effect is still active), then removed deliberately; do not delete locks automatically on timeout.

Record action keys that identify an effect across retries (task, target, revision and event/action identity). `started`/`uncertain` means look up the actual remote result first. For a confirmed failure needing a new attempt, use a new attempt key only after recording the prior outcome and checking it cannot duplicate an effect.

Maintain `maintenance.handles` and its processed-event records with the task lock using the helper API `edit(repo, task)` when a CLI operation is insufficient. Preserve unknown fields. Store only service/task identifiers and result references, never credentials. Events deferred outside hours remain pending until handled. Stop resources using their saved IDs and record failed cleanup for later reconciliation.

Approval records bind document content; do not edit an approved document merely to update its status, which would change that hash. Keep approval/status metadata in task state. If requirements materially change, present the new spec, record its hash, and obtain the affected approvals again.

