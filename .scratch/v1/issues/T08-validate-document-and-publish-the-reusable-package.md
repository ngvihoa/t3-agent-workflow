# T08 — Validate, Document, and Publish the Reusable Package

Status: ready-for-agent

Parent: [Approved spec](../../../SPEC.md)

**What to build:** A new user can install and use the release from public GitHub with a single accurate root README, a complete bundle, and explicit evidence of what has and has not been verified.

**Blocked by:** T06, T07. These dependencies transitively include all earlier tickets.

**Acceptance criteria:**

- [ ] Run the package validator and installer/configuration tests against the final bundle, including all new companions and supporting resources.
- [ ] Exercise small and full workflow scenarios end to end, including approval gates, revision changes, review/QA, explicit ship, and maintenance cleanup. Record observed actions rather than merely checking instruction wording.
- [ ] Add reproducible CI for deterministic package/installer/configuration checks. Separate agent scenario results and live integrations from those automated checks.
- [ ] Finish the single root README: prerequisites, install/preview/update/recovery, first-use setup, examples, permissions, compatibility, upstream attribution, and limitations. Do not claim autonomous Linear/Slack intake in v1.
- [ ] Report tested provider loading, operating systems, external service writes, hosted preview, and device QA separately from simulated coverage; leave untested combinations explicitly unverified.
- [ ] Confirm the public tree excludes credentials, personal paths, private project configuration, and employer-specific assets. Verify notices and the pinned upstream manifest.
- [ ] Resolve the authorized GitHub account and repository identity, publish `t3-agent-workflow` publicly, and report its URL and exact published commit. Existing repositories/content are not replaced without resolving that conflict.
- [ ] If a PR is created/pushed during delivery, perform the runtime's required linking immediately; a documentation-only claim of publication does not satisfy this ticket.

**Verification:** Final clean-destination installation, complete validation report, local fixture scenarios, actual public repository/commit verification. Do not imply live feature integrations were proven by publishing this package.
