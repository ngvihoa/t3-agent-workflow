---
name: t3-agent-workflow
description: Coordinate a development task in T3 Code from intake and clarification through implementation, review, QA, explicit shipping, and optional PR maintenance. Use for this end-to-end workflow or to resume its task records.
---

# T3 Agent Workflow

Read [shared policy](references/policy.md) and the project's workflow config first. Use existing authorization; do not treat every stage as a new request for permission.

If `.t3-workflow/project.json` is absent, load [setup](../t3-workflow-setup/SKILL.md). Verify optional capabilities before relying on them.

Load only the relevant companion SKILL.md, directly if no skill loader exists:

| Intent | Companion |
| --- | --- |
| Configure project tools, permissions, commands | [Setup](../t3-workflow-setup/SKILL.md) |
| Accept, classify, implement, resume | [Task workflow](../t3-task-workflow/SKILL.md) |
| Clarify requirements | [Grill with docs](../t3-grill-with-docs/SKILL.md) |
| Draft spec | [To spec](../t3-to-spec/SKILL.md) |
| Plan tickets | [To tickets](../t3-to-tickets/SKILL.md) |
| Execute approved graph | [Implement spec](../t3-implement-spec/SKILL.md) |
| Review standards and spec | [Code review](../t3-code-review/SKILL.md) |
| Write PR evidence | [PR](../t3-pr/SKILL.md) |
| Gather checks and human evidence | [QA](../t3-qa/SKILL.md) |
| Explicitly ship | [Ship](../t3-ship/SKILL.md) |
| Opt into or handle maintenance | [Babysit PR](../t3-babysit-pr/SKILL.md) |

Keep the root agent available to the user. Delegate scoped work when authorized and useful, following runtime orchestration rules. Maintain source pointers and dated knowledge, not unrequested refactors. Report changes, validated revision, limitations, and actual next state.
