# T04 — Execute Larger Work Behind Separate Approval Gates

Status: delivered. See [validation results](../../../VALIDATION.md) for executed checks and unverified live integrations.

Parent: [Approved spec](../../../SPEC.md)

**What to build:** A larger feature moves from clarification and durable decisions to spec, tickets, and implementation. The user approves the spec and ticket plan independently, after which the agent works the ready frontier using the runtime's supported execution tools.

**Blocked by:** T03.

**Acceptance criteria:**

- Adapt the planning/implementation companions and task-workflow routing to create only meaningful glossary/ADR updates and maintain source-cited, dated knowledge.
- Spec generation stops for explicit approval. Ticket planning starts only after that approval and stops again before implementation; record the approved versions.
- An approved ticket plan contains blocking relationships and independently checkable outcomes. Execute only tickets whose blockers are satisfied.
- Material requirement changes invalidate the relevant approval and return to the user; routine implementation decisions do not restart planning.
- Choose native or T3 delegation according to runtime instructions; read capabilities before T3 delegation and use isolated workspaces when needed without creating them manually against runtime rules.
- Supply bounded delegate briefs and context pointers, respect returned continuation instructions, cancel superseded work, and avoid mandatory recursive delegation or unsolicited top-level threads.
- TDD is used where it tests meaningful behavior. Retro/improvement suggestions remain within authorized scope and do not trigger unrelated refactors.
- Implementation completion leaves any PR as a draft and hands its candidate revision to review/QA.

**Verification:** A feature scenario paused at each approval gate; changed requirements after approval; a dependency graph with blocked/ready tickets; unavailable provider; event-driven continuation and cancellation cases.

