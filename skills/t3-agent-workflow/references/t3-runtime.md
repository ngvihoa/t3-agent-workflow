# T3 runtime adaptation

Discover the actual tool descriptions and follow system/runtime instructions. These names describe expected capabilities, not a promise that every deployment exposes them.

- Same-provider work can use native delegates when permitted by the runtime. Requested cross-provider options, background work and isolated workspaces may require T3 `delegate_task`. Call `orchestrator_capabilities` before the first T3 delegation; selected provider/model options must be available. Do not substitute silently.
- Let the runtime create a child's isolated workspace. Do not create a checkout in the shell and assume a child is bound to it. A delegate request is not a request for `t3_thread_launch`/new top-level threads.
- A child receives a bounded task plus source pointers: approved spec/tickets, revision, repo/workspace, expected result and evidence. Do not require recursive delegates. Follow its returned `next` instruction; completion-delivered work is not polled. Cancel superseded delegates with the runtime task cancellation tool.
- Link a PR immediately after creating/pushing it using `link_pull_request` or `link_pull_requests`, as required by runtime instructions. Report linking failures. Do not query the linked list merely as a ritual final check.
- Use `watch_pull_request` when maintaining/waiting on a PR, read old comments first, and follow its turn-ending directive. Reuse or stop persistent watches according to the current runtime; do not invent a polling loop. Stop watchers when maintenance ends or when runtime handoff rules require it.
- `schedule_task` can expose explicit objects for one-shot, interval, fixed-time or webhook scheduling. Inspect the current schema; do not invent a timezone/cron field. Use an explicit UTC one-shot and execution-time timezone guard when needed. Persist returned IDs and actual next run times. Never confuse a locally calculated timestamp with a registered schedule.
- Browser work uses the current runtime's browser contract. Do not open a server/tab just to prove a skill was written. For an actual authorized browser QA task, follow discovery, locator, completion and tab-lifecycle rules.
- Ship behavior must come from accessible project policy or explicit setup. Do not invent a T3 Ship tool. Secret input uses the host's supported secret mechanism; never request a token in plain chat.

Missing tools are a reported limitation. Continue independent authorized work; ask only when the missing choice blocks the requested outcome.

