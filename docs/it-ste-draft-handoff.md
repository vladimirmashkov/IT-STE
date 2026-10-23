# Draft remediation handoff

[Русское резюме](it-ste-draft-handoff.ru.md)

English is authoritative. Read this after the root `AGENTS.md` when continuing draft remediation in an independent thread. This is a work handoff, not an approval or a new standard version. Do not read the complete generated draft or source extraction to bootstrap.

## Current checkpoint — read before historical baseline

- Standing assignment: apply the [evidence-based research method](it-ste-research-method.md) for substantive W1/W2/W3 decisions. Read it once per fresh session; then read only the active note(s), not all research history. Make supported draft decisions autonomously; escalate missing evidence or owner-policy choices. No approval/release authority is implied.
- Active workstream: **W1**. The recomputed live queue at offset 0 has **97** entries and begins with **`D-P201-004` / `D-P201-005`, batch 011, physical PDF page 201**; this bounded slice remains `needs-review` because its narrow physical cloud-infrastructure scope needs editorial review. `D-P206-001` / `D-P206-003` remain page-206 blockers, `D-P209-004` / `D-P209-005` remain blocked for substantive scope, `D-P230-003` / `D-P230-004` remain blocked on the electrical-safety question, and `D-P273-004` / `D-P273-005` remain blocked on missing hydraulic IT-scope evidence. The page-280 entries remain substantively blocked after layout resolution; pages 281, 282, 289, 290, 297, 302, 303, 305, 308, 309, 310, 311, 312, 313, and 322 are resolved-draft, with `D-P287-001` restricted on compatibility/intended-use grounds, page-297 `D-P297-004` allowed as a bounded lower-bound quantifier, and `D-P289-001` / `D-P289-002` / `D-P289-009` / `D-P289-010` / `D-P290-004` / `D-P290-005` / `D-P302-005` / `D-P302-006` / `D-P303-001` / `D-P303-002` / `D-P303-003` / `D-P305-001` / `D-P305-002` / `D-P308-004` / `D-P308-005` / `D-P309-003` / `D-P309-004` / `D-P310-003` / `D-P310-004` / `D-P311-005` / `D-P312-003` / `D-P313-002` / `D-P322-007` restricted to bounded observational, evidence-review, measurable-condition, temporal-status, physical-axis, physical-magnetic, physical-fit, display-finish, physical-mechanism, physical-toothed-component, weather-observation-data, defined-residual-category, explicit-resource-baseline, or approved-maintenance-interval scopes; `D-P311-004` is allowed only for explicit arithmetic subtraction. The next independent actionable slice is **`D-P325-002`**, batch 034, physical PDF page 325. Recompute the live queue from offset 0 before editing; do not rely on historical offsets.
- Last completed slice: **`D-P322-007`, batch 034, physical PDF page 322**. The authenticated PDF layout, exact-entry evidence, and bounded IT comparison are in [the page-322 note](it-ste-research/W1-D-P322.md). The record changed from `needs-review` to `restricted`: the PDF isolates `opportunity (n)` with `If it is possible, be accurate.` and separate STE/non-STE examples; AWS Maintenance Windows and Kubernetes upgrade guidance support explicit maintenance intervals, conditions, and sequencing rather than an unspecified next opportunity. `D-P313-002` remains the preceding completed slice. All page-289/290/297/302/303/305/308/309/310/311/312/313/322 records remain `draft` / `editorial-review-needed`; this does not establish vocabulary approval or release.
- In-progress research: **page 289 `INTERMITTENT` / `INTERMITTENTLY`, `investigate` / `INVESTIGATION`, page 290 `irregularity` / `IRREGULARLY`, page 297 `least (at least)`, page 302 `LONG` / `long (as long as)`, page 303 `long (no longer)` / `LONGITUDINAL` / `LONGITUDINALLY`, page 305 `MAGNETIC` / `MAGNETICALLY`, page 308 `MATING` / `MATT (or MATTE)`, page 309 `MECHANICAL` / `MECHANICALLY`, and page 310 `mesh` / `meteorological` are resolved-draft with visually verified rows and bounded observational/lower-bound/measurable-condition/temporal-status/physical-axis/physical-magnetic/physical-fit/display-finish/physical-mechanism/physical-toothed-component/weather-observation-data scopes; page 311 `MINUS` is resolved-draft for explicit arithmetic subtraction and `miscellaneous` for a defined residual category; page 312 `MODERATE`, `MODERATELY`, `moisten`, and `MOMENTARILY` are resolved-draft for thresholded classification/measurement, manufacturer-constrained cleaning, and explicit-duration scopes; page 313 `MORE (adj)` is resolved-draft for explicit resource/property baselines; page 322 `opportunity` is resolved-draft for approved maintenance intervals or conditions; page-280 remains substantively blocked, while page-273 `HYDRAULIC` / `HYDRAULICALLY`, `D-P279-003`, and the earlier queue blockers remain unresolved**. The exact next action is to recompute offset 0 and retrieve only `D-P325-002` (batch 034, physical PDF page 325), verify its authenticated-PDF row boundary, and research only that bounded substantive question; leave page 280 and all earlier blockers unresolved unless new controlling evidence or an accountable owner decision appears.
- Recomputed at this documentation checkpoint: **97 needs-review**; 118 allowed, 1,430 restricted, 403 prohibited, 148 not-applicable; 2,196 total / 55 batches. Offset-0 queue slice: `D-P201-004`, `D-P201-005`, `D-P206-001`, `D-P206-003`, `D-P209-004`, `D-P209-005`, `D-P230-003`, `D-P230-004`. Next live-queue entries after those eight remain `D-P273-004`, `D-P273-005`, `D-P279-003`, `D-P280-003`, `D-P280-004`; the next independent actionable slice is `D-P325-002`, batch 034, physical PDF page 325. The live canonical data overrides this snapshot if records change.
- Latest content validation: affected batch-034 and all-batch vocabulary checks; adaptation, corpus, document build/check; authenticated source doctor; exact page-322 source entry and authenticated PDF SHA-256/layout evidence; AWS Systems Manager Maintenance Windows and Kubernetes cluster-upgrade documentation inspected for the bounded approved-maintenance-interval question; project diagnostics with no errors or warnings; `git diff --check`. `python3 -W error::ResourceWarning -m unittest discover -s tests` passed after updating the aggregate expectation. The page-322 research note, canonical rationale/disposition/layout update for `D-P322-007`, updated aggregate test expectation, and regenerated draft are recorded. All decisions remain `draft` / `editorial-review-needed`; these checks do not establish vocabulary approval or release.
- Resume budget: root instructions → this handoff → research method → active note(s), if any → at most eight queue locators → selected exact records. The next session should read only [the page-322 note](it-ste-research/W1-D-P322.md), then recompute offset 0 and retrieve `D-P325-002`. Historical sections below are reference, not instructions to reread all completed work. Read only the validation/source-contract sections needed for the selected change.

Maintain this checkpoint in place after every slice, including blocked work and one exact next action. Put detailed external evidence in addressed notes, not a growing startup history. Canonical records remain the disposition authority. Preserve historical deltas below without treating their counts as current.

## Verified baseline and completed work

Baseline: Git commits `1f040c4` (`Complete draft rules and start vocabulary`) and `2089f95` (`Complete draft vocabulary coverage`). These identify completed work, not authorization to commit future changes. Recompute current status and counts; this baseline is historical if records change.

- Goal: an independent international controlled-English IT standard informed by ASD-STE100, not a literal translation or official ASD guidance. English is authoritative; Russian is the preferred optional second language. Keep upstream issue, IT version, and representation revision separate.
- ASD-STE100 Issue 9 (`2025-01-15`), representation `r0001`: authenticated derivative retrieval database; 53 rules, 8 guidance blocks, 2,196 dictionary rows. The private PDF remains ignored under `.local/sources/ASD-STE100-issue-9.pdf`.
- IT-STE `0.1.0-draft.1/r0001`: all 31 canonical English draft rules, 122 examples, and 61 exact source-block references. The existing source-pinned adaptation plan and source database were preserved.
- All 2,196 dictionary rows have individual original draft sense definitions, domains, rationales, contextual alternatives, and positive/problematic examples. There are 55 consecutive batches: 54 × 40 rows plus 36 in the final batch. Coverage runs from `D-P149-001` through `D-P433-007`; no source rows are unprocessed.
- Draft dispositions: **90 allowed, 1,342 restricted, 401 prohibited, 146 not-applicable, 217 needs-review**. Every decision remains `draft` / `editorial-review-needed`; no canonical `ITSTE-T-*` records or vocabulary approvals were created.
- Six initial row-boundary cases were visually resolved on physical PDF pages 153–154: `D-P153-001`, `D-P153-002`, `D-P153-004`, `D-P153-005`, `D-P154-002`, `D-P154-003`. Batch 001 retains historical extraction warnings and records the source hash and visual findings. Other source pages have not been visually verified in this work.
- Vocabulary validation now covers consecutive batches, exact source rows/pins/warnings, global numbering, final remainder, domains, rights, and draft boundaries. CLI `check` and `entry` use all batches by default; `--batch <path>` selects one. Python `check()` still checks batch 001 by default; use `check_all()` or `checked_all()` for the whole set.
- The deterministic Markdown generator now includes all rules and batches. Integration fixes distinguish capability from permission, deletion from sanitization, and clarify a traffic-flood example. Documentation was updated in EN/RU.
- Baseline validation: source `doctor`, adaptation/corpus/vocabulary/document checks, **117 unit tests**, and editor diagnostics passed. Complete pending-file inventory and structural checks were performed; semantic review was targeted, not independent expert approval of all senses. Finder `.DS_Store` files that blocked strict snapshot validation were preserved outside the snapshot under ignored `.local/review-images/`. Do not rely on local renderings/backups existing in another checkout.

## Minimal restart: current state, then a small queue

Run from the repository root:

```sh
git --no-pager --no-optional-locks status --short --untracked-files=all
python3 tools/asd_ste100_local.py doctor
python3 tools/it_ste_vocabulary.py check --compact-json
```

Get only the next eight unresolved locators and recorded reasons. Change `offset` to `next_offset` for the next page. This validates/reads JSON locally, but emits no full definitions or examples into the agent context. The queue is computed from canonical data, not a second, potentially stale list of 217 IDs.

```sh
python3 - <<'PY'
import json
from tools import it_ste_vocabulary as v
batches, summary = v.checked_all()
offset, limit = 0, 8
items = []
for batch in batches:
    for d in batch['decisions']:
        if d['it_disposition'] != 'needs-review':
            continue
        e = d['evidence']
        items.append(dict(batch=batch['batch_id'], id=d['entry_id'],
                          headword=d['headword'], pos=d['part_of_speech_as_extracted'],
                          physical_pdf_page=d['physical_pdf_page'],
                          warnings=e['extraction_warnings'], reasons=e['mechanical_ambiguities']))
end = min(offset + limit, len(items))
print(json.dumps(dict(total=len(items), offset=offset,
                      next_offset=end if end < len(items) else None,
                      items=items[offset:end]), ensure_ascii=False, separators=(',', ':')))
PY
```

At baseline the first unresolved record is **`D-P156-005` (ADJACENT), batch 002, physical PDF page 156**. Read only its IT proposal and exact source entry, then the adjacent entry if necessary:

```sh
python3 tools/it_ste_vocabulary.py entry D-P156-005 --compact-json
python3 tools/asd_ste100_local.py entry D-P156-005 --compact-json
```

Group work by physical page, preserving global order. Recompute the queue after edits: offsets shift when records are resolved. To resume reliably, record the last completed IDs/pages and remaining blockers, not only an offset. Add `--full` only when an exact source entry is insufficient; use a bounded page rendering for row boundaries/typography. If the authenticated PDF is unavailable, keep layout-dependent decisions unresolved rather than guess. See the [source retrieval guide](asd-ste100-local-reference.md) only when needed.

## Three distinct open workstreams

### W1 — Resolve explicit blockers first (217 at baseline)

These are unresolved decisions, **not 217 proven extraction errors**. At baseline 103 have source extraction warnings; 114 do not. Warning absence is not semantic verification. Examples: adjacent-row overlap (`D-P156-005`/`006`), insufficient noun context (`D-P157-003`, advance), physical fastening versus information security (`D-P370-004`, security), and setting a number to zero versus calibration/sanitization (`D-P433-007`, zero).

For each selected record:

1. Inspect its existing proposal, rationale, warning/ambiguity evidence, and exact source sense. Verify the cited PDF page visually if layout is in question; source examples can help only when bounded retrieval is insufficient.
2. Use the [research method](it-ste-research-method.md) to investigate substantive IT questions, evaluate competent external evidence, compare alternatives, and record a bounded draft decision with an evidence-note reference. Decide independently which IT sense and grammatical function to propose. An aviation meaning is not an IT whitelist/ban. `not-applicable` concerns the stated source sense, not every use of the spelling.
3. Amend the existing decision in its batch, with original IT wording and examples. Preserve IDs, global sequence, raw source metadata/warnings, pins, and rights. Record what was verified and any still-open question. Do not silently repair the authenticated source database or blanket-clear `needs-review`.
4. For a visual resolution, the existing `evidence.pdf_layout_check` contract requires `performed: true`, `visual_verification_performed: true`, and a nonempty `method` containing the authenticated PDF SHA-256 and `Findings:` with row-specific findings. These are recorded assertions, not automated proof of inspection. Text extraction or a correct hash alone is not visual verification. Retain the source's mechanical/unreviewed status; row review does not certify the entire database.
5. Change the proposed disposition only when the recorded blocker is actually resolved. Keep `status: draft` and `review_status: editorial-review-needed`: resolving extraction is not human approval. If blocked, preserve the record and state exactly what evidence/decision is missing.

Deliverable: traceable row-level resolutions and an accurately recomputed remaining queue, including blockers that cannot yet be settled. Do not declare the standard complete just because the queue becomes empty.

### W2 — Editorial and technical review of the whole draft

All 31 rules and all 2,196 vocabulary decisions need sense/scope review, not only W1's flagged records. Check rule/lexicon consistency, POS, alternatives that might change meaning, positive/negative examples, conditions, modality, and safety/security effects. Physical meanings must not accidentally exclude needed software meanings. Example vocabulary is not automatically approved.

Deliverable: recorded review decisions and explicit outstanding questions for a responsible editor/technical owner. The current batch checker deliberately rejects approved states, and the canonical pilot is not a general vocabulary/release contract. Design and validate an explicit approval/canonical-term workflow before materializing approved terms; do not disable draft guards or treat an agent's inspection as human sign-off. Keep `catalog.json` unreleased until a separately authorized release process is ready.

### W3 — Inventory IT senses missing from the source

Full coverage of the aviation dictionary is not full IT coverage. Build a separate gap inventory by the existing domain registry: for example API, authentication/authorization, containers, transactions, distributed systems, and secret/key lifecycle concepts. These are candidate areas, not a verified list of absent words: check existing proposed senses before adding anything.

Deliverable: scoped missing concepts/senses with domain, POS, definition, rationale, examples, and origin. Reuse or split existing spellings by sense where appropriate; do not invent ASD provenance or append IT-only records to the fixed 2,196-row source sequence. Agree an explicit canonical contract and ID allocation before creating `ITSTE-T-*` records. A source-row replacement and an IT-only addition are different changes.

## Read only the files needed for the selected work

| Need | Entry point |
| --- | --- |
| One draft vocabulary decision | `python3 tools/it_ste_vocabulary.py entry <ID> --compact-json` |
| Edit that decision | `standards/it-ste/vocabulary-reviews/asd-ste100/issue-9/r0001/batch-NNN.json`; queue gives `NNN` |
| Queue semantics and validation limits | [Vocabulary guide](it-ste-vocabulary.md); relevant functions in `tools/it_ste_vocabulary.py` only if changing the contract |
| Domain IDs | `standards/it-ste/domains/v1.0.0.json` |
| One rule | `standards/it-ste/versions/0.1.0-draft.1/revisions/r0001/content/en/rules/ITSTE-R-NNNN.json` |
| Canonical rule/manifest changes | [Draft rule contract](it-ste-canonical-pilot.md), then only the relevant manifest/plan records |
| Publication/licensing changes | [Permission record](permissions/asd-ste100-issue-9-derivatives.md), `LICENSE-CONTENT.md` |

The generated `docs/IT-STE-draft.md` is approximately 4.7 MB at baseline. It is a reading/export copy, **not the editing source or the first context file**. Do not load all batch JSON, the SQLite payload, full PDF, or Git patch into the LLM context just to find the next task.

## Validation and stopping rules

After row edits, check the affected batch first with `check --batch <path> --compact-json`, then run:

```sh
python3 tools/it_ste_adaptation.py check
python3 tools/it_ste_corpus.py check
python3 tools/it_ste_vocabulary.py check --compact-json
python3 tools/it_ste_document.py build
python3 tools/it_ste_document.py check
python3 -W error::ResourceWarning -m unittest discover -s tests
```

`tests/test_it_ste_vocabulary.py::VocabularyTests.test_complete_source_coverage_and_review_boundaries` intentionally pins baseline disposition counts; batch-001 tests and document tests also pin its six visual resolutions. After justified decisions, update affected expectations and EN/RU progress counts to the recomputed results without weakening total coverage, order, provenance, or draft boundaries. Update this handoff's **baseline** only deliberately; do not confuse historical counts with current invariants. Rebuild Markdown, never hand-edit it. Relevant tests are `tests/test_it_ste_vocabulary.py` and `tests/test_it_ste_document.py`.

Before finishing, follow the root Git review/commit-proposal instructions and update the Current checkpoint in place: IDs/pages resolved, evidence-note links, any in-progress or blocked question and exact next action, recomputed counts, new files/contracts, and actual checks run. Preserve unrelated work. Add a historical delta only for a material milestone; do not grow a mandatory startup transcript. A fresh thread must be able to resume from records without the chat transcript.

Release/SFT readiness is **not** established by successful checks or zero unprocessed rows. Require approved technical/editorial content, canonical vocabulary/release validation, and separate dataset review (rights, unresolved examples, splits/evaluation, versioned provenance) before publishing an approved lexicon or training export.

## W1 continuation delta — pages 156–157

- Resolved `D-P156-005` (ADJACENT) and `D-P156-006` (ADJACENT TO) in batch 002 as `restricted`, limited to an explicitly specified IT order/layout. Visual inspection confirmed the adjacent-row overlap and the preposition's displayed spelling/POS.
- Resolved `D-P157-003` (advance, noun) as `prohibited` for the stated cursor-movement prose sense, with explicit movement/displacement alternatives. Exact `--full` retrieval and visual inspection established the source movement sense; the decision does not cover the verb or other noun senses.
- Evidence: exact derivative entries plus visual inspection of page-specific PNG renderings of physical PDF pages 156–157, ASD-STE100 Issue 9, authenticated SHA-256 `d1f4ea9e7cd6e46b47aa9057209f99e78c0e9cfc4e27a5b07895b05c1a166431`. Each row records findings and verification flags. Raw warnings, historical mechanical ambiguities, source pins, global sequence, and mechanical/unreviewed provenance remain intact. The authenticated derivative was not modified; local PDF/renderings remain unpublished and are not required for resumption.
- Recomputed current dispositions: **90 allowed, 1,344 restricted, 402 prohibited, 146 not-applicable, 214 needs-review**. Remaining blockers: 102 with extraction warnings, 112 without. Batch 002 has no remaining W1 blockers, but all its senses still require editorial review. All 2,196 decisions remain `draft` / `editorial-review-needed`.
- Next unresolved pair: **`D-P161-005` (alternately) / `D-P161-006` (ALTERNATIVE), batch 003, physical PDF page 161**. Recompute the queue from offset 0; do not reuse the old offset. No other W1 rows were resolved in this continuation; W2 and W3 remain open.
- No new files, dependencies, or contracts. Updated batch 002, regression expectations/test, EN/RU progress documentation, and the deterministic generated draft. Historical baseline counts above remain historical.
- Actual validation: source `doctor`; affected-batch vocabulary check; adaptation, corpus, all-batch vocabulary, document build/check; **118 unit tests** with `ResourceWarning` treated as errors. All passed. The initial attempt to put `--full` in the fixed retrieval locator was rejected by validation; the canonical locator was restored and the additional retrieval recorded in evidence without changing the contract.

Original editorial content: IT-STE contributors, [CC BY-SA 4.0](../LICENSE-CONTENT.md). ASD source rights remain separate; source PDF publication is forbidden. Mandatory project attribution: https://github.com/vladimirmashkov/IT-STE.
