---
name: it-ste-vocabulary-gate-slice
description: Review one exact IT-STE vocabulary group with compact input/output state; never turn a structural review into approval.
disable-model-invocation: true
---

# IT-STE vocabulary gate slice

Use only under release-readiness or for one explicitly bounded vocabulary review. Accept one canonical batch path or an enumerated group of entry IDs/pages; never all batches.

## Contract

1. Read `current.json` with `python3 tools/it_ste_resume.py show --compact`, then one input whose `scope` contains exact batch/IDs/pages, old dispositions, excluded meanings, and next-group pointer. No exact input means `needs-scope`, not a history scan.
2. Read only the selected batch projection/entries and active note/register named by `read_set`. Authenticate ASD with `doctor`; retrieve exact entries and the PDF page only when layout matters. Never stage the PDF/rendering.
3. For each entry inspect competent direct evidence and record source facts, editorial inference, alternatives, limitations, and one of `allowed`, `restricted`, `prohibited`, `not-applicable`, unchanged, or `needs-review`. Preserve raw fields, IDs, order, warnings, fixed locators, rights, draft status, and review status.
4. Change canonical JSON only when justified by the selected evidence. Do not edit ASD rows, schema, relations, or unrelated term records. Update one compact note, handoff/plan checkpoint, counts, and exact next group.
5. Run the affected full-path batch check, then the standard checks from the compact protocol, diagnostics, and full Git review. Write `output.json`, run `finish`, and commit only explicit paths when per-run authorization permits.

A passing slice is only a recorded draft review. It is not vocabulary approval, release readiness, publication, conformance, or SFT readiness. Stop and preserve `blocked`/`needs-review` for missing evidence, owner/policy decisions, failed checks, or ambiguous ownership.
