---
name: it-ste-it-sense-classification
description: Classify ASD-derived vocabulary for an independent IT-STE sense, using authoritative web evidence, explicit scope decisions, and an interruption-safe classification log; never force a disposition merely to empty needs-review.
disable-model-invocation: true
---

# IT-STE independent IT-sense classification

Use this project-local skill when the task is to decide whether an ASD-derived word belongs in IT-STE, what IT domain and sense it has, and whether it should be retained, restricted, excluded, or split. Read `docs/it-ste-it-sense-policy.md` before classification. ASD-STE100 is provenance and source evidence; it is not the IT ontology and its aviation categories are not automatic IT decisions.

This skill is intentionally manual-only. The caller must explicitly request the run and provide a bounded iteration count or an explicit bounded ID/page slice.

## Core principles

1. Treat the ASD row and the proposed IT sense as separate objects. Preserve ASD Issue, revision, physical PDF page, exact retrieval locator, source hash, spelling, POS, examples, warnings, raw metadata, rights, IDs, and sequence.
2. Decide independently whether the word is needed in IT-STE. A word may be `not-applicable` even when it is valid aviation terminology. A useful word may require a narrower `restricted` sense, a `prohibited` draft recommendation, or several proposed IT senses.
3. Do not force a disposition to reduce `needs-review`. If evidence cannot select a bounded IT scope, keep `needs-review` and record the exact missing policy or evidence.
4. Keep all canonical records `status: draft` and `review_status: editorial-review-needed`. Never claim vocabulary approval, canonicalization, release, publication, or SFT readiness.
5. Distinguish source facts, external-source facts, and editorial inference in every decision.

## Required classification outcomes

For each selected record, explicitly consider:

- `retain/restricted`: useful in IT only with a named object, domain, operation, criterion, relation, or condition;
- `retain/allowed`: only when a bounded, portable IT sense is supported and ambiguity is acceptably controlled;
- `exclude/prohibited`: the proposed IT wording is misleading or materially safer when rewritten, but do not imply a universal ban on the English word;
- `not-applicable`: the ASD sense is outside the project's IT scope;
- `split/proposal`: one ASD row appears to cover multiple IT senses. Record proposed senses and their boundaries in the note/log, but do not add new canonical records or schema fields without owner approval;
- `needs-review`: evidence or project policy remains insufficient.

A classification is not complete until it states why the other plausible outcomes were rejected, including keeping the current status.

## Evidence policy

### Required authoritative evidence

For ASD facts, always use the authenticated derivative workflow:

```sh
python3 tools/asd_ste100_local.py doctor
python3 tools/asd_ste100_local.py entry <ID> --compact-json
python3 tools/asd_ste100_local.py page <PDF_PAGE>
```

Render only the cited local PDF page under ignored `.local/review-images/` when row layout, wrapping, columns, or typography matters. Keep Issue, revision, physical page, printed page, exact locator, and PDF SHA-256 in the note.

For IT meaning, prefer in this order:

1. applicable primary standards/specifications (IETF RFCs, W3C/WHATWG specifications, NIST publications, ISO/IEC material where accessible and applicable);
2. official technology or manufacturer documentation for the named product/domain;
3. authoritative specialist or professional guidance with clear scope and authorship;
4. established technical-writing guidance for clarity questions only.

Check the source's version/date/status, publisher competence, domain, normative versus informative status, applicability, and limitations. One controlling specification can settle a narrow factual claim; repeated copies of one claim are not independent corroboration.

### Discovery-only sources

Reddit and Stack Overflow may be used only to discover terminology, edge cases, search terms, or candidate primary sources. They are not evidence and must never be cited as support for a disposition. If a forum points to a useful source, inspect and cite that source directly. Record forum use as `discovery only` when it materially shaped the search; do not present votes, anecdotes, or accepted answers as authority.

Never use search snippets, AI summaries, uncited rankings, inaccessible pages, marketing claims outside their scope, or uninspected URLs as evidence. If an authoritative source is blocked, record the limitation and do not infer its content.

## Interruption-safe state and logs

### Baseline register

Use `docs/it-ste-research/needs-review-38.md` when it exists. It is the frozen problem inventory and must not be rewritten to erase history. Add a result entry for every processed ID showing old and new disposition, even when unchanged.

If a different queue is selected, create an equivalent baseline register before editing canonical records.

### Classification log

Maintain exactly one aggregate state file:

`docs/it-ste-research/it-sense-classification-log.md`

Create it on the first classification run if absent. Its header must contain:

```text
# IT-STE independent IT-sense classification log
State: active | paused | complete
Baseline register: <path>
Started: <date>
Last checkpoint: <date/time>
Requested iterations: <count or bounded scope>
Completed slices: <count>
Remaining records: <count>
```

For every slice append or update one compact entry with:

- slice number and run identifier;
- exact canonical IDs, batch, POS, headword, physical PDF page;
- old disposition and new disposition for every selected record;
- ASD Issue/revision, printed page, exact entry locator, PDF SHA-256, visual findings;
- IT question and scope, including excluded meanings/domains;
- authoritative sources actually inspected, URLs, access date, version/status, finding, competence and limitation;
- Reddit/Stack Overflow discovery, if any, explicitly marked `discovery only` and never used as evidence;
- alternatives considered and why they were rejected;
- decision: retain/restricted, allowed, prohibited, not-applicable, split proposal, or needs-review;
- changed canonical fields, if any;
- validation commands/results;
- commit hash and exact committed paths, or the reason no commit was safe;
- one concrete next action and resume pointer.

Write the log before or together with the canonical change so an interrupted run remains recoverable. Never use an offset alone: record IDs, page, batch, and the last completed decision.

## Bounded execution

1. Read `AGENTS.md`, `docs/it-ste-it-sense-policy.md`, only the Current checkpoint in `docs/it-ste-draft-handoff.md`, `docs/it-ste-research-method.md`, the baseline register, the classification log, and the active note(s).
2. Capture the complete initial Git status/index/diff/name-status inventory. Require a clean nonignored worktree unless the user explicitly identifies and authorizes an existing classification run to resume.
3. Recompute canonical counts and the offset-0 queue. Treat checkpoint counts and pointers as stale if they differ.
4. Select one coherent slice: normally one physical PDF page and no more than two related records; a grammatical trio is allowed only when the third row is necessary to resolve the selected question. Do not repeat a completed blocked slice without genuinely new evidence or an explicit owner decision.
5. Retrieve only selected canonical records and exact ASD entries. Authenticate and visually verify the cited page where needed.
6. Research one concrete IT-sense question with authoritative sources. Compare the current wording, alternatives, and exclusion of aviation-only or unrelated IT meanings.
7. Update exactly one compact per-slice research note and the aggregate classification log. Apply only justified draft changes to canonical JSON. Never hand-edit generated Markdown.
8. Run the affected batch check first, then:

```sh
python3 tools/it_ste_adaptation.py check
python3 tools/it_ste_corpus.py check
python3 tools/it_ste_vocabulary.py check --compact-json
python3 tools/it_ste_document.py build
python3 tools/it_ste_document.py check
python3 -W error::ResourceWarning -m unittest discover -s tests
python3 tools/asd_ste100_local.py doctor
git diff --check
```

Run project diagnostics and recompute all counts/queue after edits.

9. Update the Current checkpoint with the actual slice, evidence note, count, unresolved question, exact next action, and next live IDs. Keep the classification log's checkpoint consistent with it.
10. Review the entire worktree and index, including all added/untracked content and every diff/name-status view. Do not include PDFs, renderings, secrets, unrelated work, mixed files, or accidental changes.
11. If and only if the user explicitly authorized automatic commits for this run, stage explicit reviewed paths and create one safe commit per bounded slice:

```sh
git add -A -- <explicit-reviewed-paths>
GIT_EDITOR=true git commit --only -m "<imperative message <=50 chars>" -- <explicit-reviewed-paths>
```

Otherwise leave changes unstaged and provide the exact safe command. Verify the commit hash, paths, and clean worktree before the next slice.

## Stop conditions

Stop and preserve the log when:

- a pre-existing nonignored change or ownership boundary appears;
- source authentication, required PDF evidence, diagnostics, validation, or commit fails and cannot be fixed safely;
- a needed authoritative source is unavailable and no bounded classification can be supported;
- only cosmetic repetition remains;
- a proposed split requires a schema or owner-policy change;
- the queue has no independent eligible slice;
- the requested iteration count is reached.

At a stop, do not force records out of `needs-review`. Report completed slices, unchanged blockers, exact missing decisions/evidence, the log checkpoint, and a safe next action.

## Final report

Report in Russian:

- baseline path and requested/completed scope;
- every processed ID with old/new disposition;
- authoritative sources actually inspected and limitations;
- discovery-only Reddit/Stack Overflow use, if any;
- canonical/research/log files changed;
- validation results and diagnostics;
- commit hashes and exact paths, or safe uncommitted commands;
- final canonical counts and remaining `needs-review` IDs;
- ignored local artifacts;
- explicit confirmation that no vocabulary approval, release, publication, or SFT readiness was claimed.
