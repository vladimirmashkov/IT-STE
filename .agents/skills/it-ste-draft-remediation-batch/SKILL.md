---
name: it-ste-draft-remediation-batch
description: Run 1–100 sequential bounded remediation inputs with one compact output and optional commit per slice.
disable-model-invocation: true
---

# IT-STE remediation batch wrapper

Use only when the user supplies a positive integer `1..100` (`/it-ste-draft-remediation-batch --iterations=10`). The count means bounded slices, not records. This wrapper never invokes another slash command and never runs slices in parallel.

## Low-context loop

1. Read `current.json` with `show --compact`; validate branch/ownership and source doctor once before iteration 1. Do not read all history or carry previous output into chat.
2. For each iteration, derive one exact input from the fresh current state: one page/related pair, selected IDs/paths, question, read set, allowlist, baseline, and explicit commit authorization. Run `begin`.
3. Execute the single-slice adapter contract, write one `runs/<id>.output.json`, run `finish`, and verify clean recovery before the next iteration. Keep full logs/diffs under `.local/it-ste-state/<id>/`.
4. Stop immediately on invalid count, queue exhaustion, user change, ownership ambiguity, source/validation/diagnostic/commit failure, missing evidence without a bounded blocker, or failed clean recovery. Never reuse stale offsets/counts/IDs.

Each output must state IDs/pages, old/new disposition, evidence refs/limits, validation statuses, changed paths, commit metadata or blocker, and exact next action. Commit at most one explicit-path logical commit per slice only when input authorization allows it; never commit PDFs, renderings, secrets, ignored artifacts, mixed/unrelated work, or cosmetic no-op state. Report the compact aggregate and no-approval/no-release/no-SFT boundary without pasting logs.
