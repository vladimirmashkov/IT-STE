---
name: it-ste-w2-editorial-slice
description: Review one bounded W2 editorial slice from an exact input; preserve draft safeguards and write compact state output.
disable-model-invocation: true
---

# IT-STE W2 editorial slice

Use under `it-ste-release-readiness` or for an explicitly bounded W2 request. This is draft editorial/technical review, not vocabulary approval, release, publication, conformance, or SFT authorization.

## Input and read set

- Require `phase: w2`, one explicit `theme`, and normally 2–5 manifest-listed rule/term IDs or exact paths in `runs/<run-id>.input.json`.
- Run `show --compact`, read only this adapter, the input, and its `read_set`; if scope is absent, write `needs-scope` output without opening history.
- Read only selected records and directly affected references. Valid themes include lexical/POS, actors/modality, conditions/sequencing, safety/security, examples, source facets/rights, and cross-record consistency.

## Method

1. Start the input with `tools/it_ste_resume.py begin`; capture the baseline and recompute canonical counts/queue.
2. Inspect only the selected records and competent primary/expert sources. Fetch sources directly; record URL, publisher, version/date, section, finding, competence, limitation, and fact-versus-inference.
3. Compare current wording with alternatives, including unchanged wording. Preserve technical meaning, actors, conditions, modality, limits, safety/security context, schema, IDs, source pins, rights, `status: draft`, and `review_status: editorial-review-needed`.
4. Maintain one compact active note, normally `docs/it-ste-research/W2-editorial-review.md`. Do not touch ASD rows merely to add an IT sense and never hand-edit generated Markdown.
5. Apply only justified draft changes and update handoff/plan Current checkpoints with the exact next bounded scope.

## Checks and state

Run the affected check first, then the standard repository checks from `docs/it-ste-state/README.md`, diagnostics, and `git diff --check`. Put command output/full Git inventory in `.local`, not context. Review every change under `AGENTS.md`; commit only explicit wholly owned paths when `input.authorization.auto_commit` is explicitly true.

Write one compact `output.json`, run `finish`, and report no approval/release claim. Stop for unavailable evidence, schema/policy changes, mixed ownership, failed validation, or an unresolved safety question; preserve `blocked`/`needs-review`.
