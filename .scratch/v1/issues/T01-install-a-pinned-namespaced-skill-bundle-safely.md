# T01 — Install a Pinned, Namespaced Skill Bundle Safely

Status: ready-for-agent

Parent: [Approved spec](../../../SPEC.md)

**What to build:** A developer can obtain the package, inspect exactly which skills will be installed and where, then install its complete pinned baseline without damaging an existing installation. The installer continues to include companions added by subsequent tickets through a validated bundle manifest.

**Blocked by:** None.

**Acceptance criteria:**

- [ ] Adapt the orchestrator and required upstream dependency closure from the spec's pinned commit; include all referenced guides/templates and preserve licenses and inherited credits.
- [ ] Namespace adapted companions consistently and resolve internal skill calls and links inside this bundle, without relying on a separately installed Matt Pocock skill.
- [ ] Record upstream paths, commit, original/adapted hashes, and adaptation notes; verify the packaged content against that record.
- [ ] Preview reports provider/destination, additions, conflicts, and replacement choices without writing. Accept an explicit destination when a provider convention has not been verified.
- [ ] Standard-library Python installation validates the whole plan before writing, rejects path escapes, preserves unrelated files, and supports an explicitly chosen replacement or a consistently renamed side-by-side bundle.
- [ ] Reinstallation recognizes local edits. A simulated interrupted install restores prior content or clearly reports recovery required; it never reports partial content as a successful full bundle.
- [ ] Installed baseline instructions respect the spec's task scope and approval/ship boundaries. Missing project configuration routes to setup instead of executing upstream defaults.
- [ ] Introduce the root README's accurate install/load prerequisites and package licensing. Later tickets extend this same README.

**Verification:** Temporary-directory installs, preview/no-write checks, existing-content and failure-recovery cases, manifest/reference validation. Do not modify the user's live skill directories as a test.

