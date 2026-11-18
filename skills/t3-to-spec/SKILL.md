---
name: t3-to-spec
description: Synthesize the agreed development request into a concrete spec and stop for approval of that version.
---

# Draft a spec

Read [policy](../t3-agent-workflow/references/policy.md) and [task records](../t3-agent-workflow/references/task-records.md). Synthesize the conversation, project instructions, glossary and relevant ADRs; do not restart an interview whose decisions are already settled.

Write the user problem, resulting behavior, meaningful user stories, architectural decisions, observable testing/acceptance criteria, and out-of-scope boundaries. Use enough detail to evaluate implementation without prescribing incidental internals. Reuse testing boundaries already agreed; ask only if a new boundary changes scope or required evidence.

Save a concrete draft in the configured task docs location. Publishing it to a tracker requires that project's write permission. Record its content with `tasks.py document --kind spec --path ...`. Present the exact version and wait for the user's approval; do not label it ready-for-agent merely because it was drafted.

Only after an observed user approval, record `tasks.py approve --kind spec --evidence ...`, then route to [to tickets](../t3-to-tickets/SKILL.md). If materially changed later, present the new version and obtain affected approvals. Keep status metadata in task state so it does not mutate approved document hashes.
