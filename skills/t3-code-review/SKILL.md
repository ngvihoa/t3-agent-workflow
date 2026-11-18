---
name: t3-code-review
description: Review a candidate along separate repository-standards and approved-task/spec axes, recording evidence for its exact revision.
---

# Review standards and spec separately

Read [policy](../t3-agent-workflow/references/policy.md) and [task records](../t3-agent-workflow/references/task-records.md). Resolve the intended comparison base and actual candidate revision. Reuse a task/PR's known base; ask only if ambiguous. Check a nonempty diff and read the relevant approved spec or small-task criteria.

**Standards:** inspect repository instructions, CODING_STANDARDS/CONTRIBUTING and applicable conventions. Cite the rule and exact changed location for violations. Separate heuristics/suggestions from documented breaches, and avoid duplicating failures already covered by tooling.

**Spec:** identify missing/partial behavior, wrong behavior and scope creep. Cite the requirement and changed location; do not invent proof from naming or test existence. If no spec exists, review the concrete recorded user request. If neither is available, report the missing source and do not record a pass for that axis.

If project configuration requires an independent reviewer, obtain one through the supported authorized delegate path. When two reviewers are useful and authorized, give each a bounded standards/spec brief with the base, revision and source pointers. Do not force subagents when disabled or unavailable; report any unmet independent-review requirement.

Present findings under separate Standards and Spec reports, with per-axis severity and totals. Apply fixes only within task authorization, then refresh relevant review/checks for the new revision. Respect configured attempt limits and escalate unresolved product decisions. Record `tasks.py review` only for results actually observed; failing or unperformed axes are not passes. Record reviewer identity/independence in evidence when required.

Then load [QA](../t3-qa/SKILL.md). A clean review is not ship permission. Leave any PR draft.
