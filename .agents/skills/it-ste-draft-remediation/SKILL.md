---
name: it-ste-draft-remediation
description: Run one bounded W1/W2/W3 draft slice from compact input, preserving provenance and draft safeguards.
---

# IT-STE draft remediation adapter

Use for one explicit W1/W2/W3 slice. The repository state, not chat, is the resume store. This skill does not approve vocabulary, release, publication, conformance, or SFT readiness.

## Compact startup

1. Run `python3 tools/it_ste_resume.py show --compact`; require one input with exact workstream, IDs/pages/paths, question, exclusions, read set, allowlist, baseline, and per-run authorization. Missing scope is `needs-scope`; do not read history to infer it.
2. Read only the selected active note/records and bounded method sections from `read_set`. Recompute canonical counts and offset-0 queue; treat checkpoint values as stale hints.
3. Run `begin`, authenticate ASD before using ASD evidence, retrieve only exact entries/page when needed, and inspect competent direct external evidence for substantive IT meaning. Keep source facts, inference, alternatives, limitations, fixed locators, warnings, rights, and PDF hash separate.

## Slice rules

Work one page/related pair and no more than two records unless the input justifies a narrower exception. Keep `status: draft` and `review_status: editorial-review-needed`; preserve IDs, sequence, source pins, and schema. Write/update one compact research note, apply only justified canonical changes, never hand-edit generated Markdown, and leave insufficient evidence `blocked`/`needs-review`.

Run affected then standard checks from `docs/it-ste-state/README.md`, diagnostics, complete Git review, and output/finish. Automatic commit is allowed only when the current input explicitly authorizes it; use explicit wholly owned paths and the safety commands in `AGENTS.md`. Store full logs in `.local`, not context. Report compact results, refs, changed paths, commit/blocker, next live slice, and reviewed exclusions.
