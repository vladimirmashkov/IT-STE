---
name: it-ste-vocabulary-gate-slice
description: Review one explicit IT-STE vocabulary batch or thematic group for draft semantic dispositions and provenance, preserving unresolved decisions and making one validated explicit-path commit without claiming vocabulary approval.
disable-model-invocation: true
---

# IT-STE vocabulary gate slice

Use only under `it-ste-release-readiness` or when the user explicitly requests one bounded vocabulary review group. This skill reviews draft dispositions; it is not an approval workflow, release gate, ASD guidance, or SFT authorization.

## Bounded scope

Accept one full canonical batch path or one explicitly enumerated thematic group of entries. Never process all batches in one run. Record exact batch path, entry IDs, physical pages, old dispositions, and the next group. The offset-0 queue is a recomputation input, never a sufficient resume pointer.

## Evidence method

1. Read `AGENTS.md`, the Current checkpoint in `docs/it-ste-draft-handoff.md`, the release-readiness plan, `docs/it-ste-research-method.md`, and the active vocabulary note/register only.
2. Capture and inspect a clean baseline. Stop for unrelated, mixed, staged, deleted, renamed, binary, mode, or submodule changes.
3. Run ASD `doctor`, then retrieve only selected exact entries and the relevant full canonical batch path. Render the authenticated PDF page only when row boundaries, wrapping, columns, or typography require it; never stage the PDF or rendering.
4. For each selected entry, inspect competent primary/expert evidence for the proposed IT sense. Record URL, title, publisher, version/status, access date, section, fact, competence, limitation, and source-vs-inference boundary. Search snippets and uninspected pages are not evidence.
5. Compare `allowed`, `restricted`, `prohibited`, `not-applicable`, unchanged, and `needs-review`. Do not force a disposition to empty the queue. Preserve raw source fields, IDs, sequence, warnings, fixed retrieval commands, rights, `status: draft`, and `review_status: editorial-review-needed`.
6. Update one active compact vocabulary note/register with exact entry decisions, missing owner/policy questions, validations, and one next group. Do not create duplicate history notes.
7. Change canonical batch JSON only when evidence justifies it. Do not modify ASD source rows, source extraction, schema, relations, or term records in the same slice unless the plan explicitly names them and the contract supports them.
8. Run the affected full-path batch check first, then adaptation, corpus, full vocabulary, document build/check, unit tests, doctor, diagnostics, and `git diff --check`.
9. Recompute all counts/queue, update handoff and release-readiness plan, perform full diff review, and make one explicit-path commit only after all checks pass.

## Gate semantics

Passing this skill's checks means only that the selected draft review is recorded and structurally valid. It never means vocabulary approval. A separate human/editorial gate must record approval for the proposed release scope before release-candidate packaging.

## Commit policy and report

Automatic commits require explicit user authorization. Use one short imperative message such as `Review vocabulary batch 005`. Stage explicit paths only; never use `git add .` or pathless `git add -A`. Report in Russian the selected IDs, old/new dispositions, evidence/limits, counts, queue, all validations, exact commit/hash/paths, ignored artifacts, next group, and the explicit no-approval/no-release status.
