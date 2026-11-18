# T02 — Configure a Project Through Repeatable Onboarding

Status: ready-for-agent

Parent: [Approved spec](../../../SPEC.md)

**What to build:** Setup inspects a project and the runtime, asks only unresolved questions, then produces usable shared policy and separate local preferences/state. It explains and verifies selected optional dependencies rather than assuming they exist.

**Blocked by:** T01.

**Acceptance criteria:**

- [ ] Define and validate the configuration format, versioning, user/project precedence, and separation of non-secret policy from local state and credentials.
- [ ] Detect repository instructions, existing documentation, technology manifests, source control, available connectors/CLIs, and configured commands. Respect indexed-repo CodeGraph instructions without creating an index.
- [ ] Ask for the unresolved tracker/docs, provider/model and review policy, concurrency/repair limits, QA commands, external-write permissions/destinations, ship effect/target, and optional maintenance policy.
- [ ] Present selected technology/tool/asset/connection actions with their source, target, purpose, and verification. Execute only selected/approved changes; otherwise provide manual steps and keep the capability unavailable.
- [ ] Distinguish configured, authenticated, verified, and unavailable capabilities. An installed executable alone cannot make a platform verified.
- [ ] Re-running setup updates its own configuration without duplicating blocks or overwriting unrelated instructions; no credentials enter shared files.
- [ ] Absent optional tools disable only their affected path. Report unavailable provider choices without silent substitution.

**Verification:** Fresh and preconfigured repo fixtures; repeated setup; invalid configuration; missing CLI/auth; declined dependency changes. No live external writes are required to verify these cases.

