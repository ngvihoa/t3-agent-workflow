# T05 — Produce Separate Review Findings and Revision-Bound QA Evidence

Status: ready-for-agent

Parent: [Approved spec](../../../SPEC.md)

**What to build:** A draft candidate receives separate standards/spec review and project-appropriate QA. The result makes revision coverage, actionable failures, missing evidence, and human acceptance requirements visible.

**Blocked by:** T03. It can be developed independently of T04; integration with the full path is verified before release.

**Acceptance criteria:**

- [ ] Review the intended diff/base against repository standards and the approved spec or recorded small-task criteria. Report the two axes separately and label missing spec evidence.
- [ ] Apply the configured independent-review policy and bounded repair/review attempts; do not silently switch providers or expand task scope.
- [ ] Record the reviewed revision, findings, resolutions, and relevant reruns. A newer revision does not inherit stale review/QA approval automatically.
- [ ] Run configured relevant build/test/preview checks and record command, environment, revision, result, and URLs where available.
- [ ] Respect runtime browser restrictions. A QR code or preview URL is never recorded as proof that human/device QA ran.
- [ ] Support project-selected Expo/device instructions without requiring Expo for other projects. Report required pending checks and optional skips accurately.
- [ ] Update the existing draft PR evidence only within configured write permissions; leave it as a draft.

**Verification:** Standards-pass/spec-fail and inverse scenarios; missing spec/device/browser; failed required check; a changed revision; bounded repeated repair. Use a small fixture command for executed QA evidence.

