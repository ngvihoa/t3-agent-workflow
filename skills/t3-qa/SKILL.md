---
name: t3-qa
description: Run project-configured QA and record command, browser, human or device evidence for the exact candidate revision. Use before shipping or when QA is requested.
---

# QA a candidate

Read [policy](../t3-agent-workflow/references/policy.md) and [task records](../t3-agent-workflow/references/task-records.md). Load the project config and task, pin the current revision, and inspect the configured required/optional checks.

Run only relevant checks under the task's authorization and runtime rules. Report command, environment, revision, result and evidence location. Use `tasks.py check` for configured checks; `origin` is `executed`, `human` or `simulation`. A simulation cannot satisfy required shipping QA.

For browser QA, use the runtime's supported browser only when authorized for this task. For hosted preview, use the configured build/preview command and verify its actual result/URL. Do not assume a deployment vendor, staging database, port or portal. For human/device checks, record the person's actual observation and revision; an instruction to test is still pending.

If the project selects Expo, verify its configured dev-build procedure and existing device-build compatibility. Generate/share a QR only through the supported selected tool. Wait for actual phone observations before recording a device pass. Do not install Expo or publish a dev server merely because the project has mobile code.

Record unavailable browser/device/service access as pending. Distinguish failed checks from optional skipped checks. Required pending/failing checks block ship. An empty configured QA list means no checks selected; report that limitation rather than claiming QA passed.

After a fix changes the candidate, refresh the revision and rerun relevant checks. Update PR evidence only with configured permission, leave the PR draft, and report remaining human acceptance. Never infer permission to ship from a QA pass.

