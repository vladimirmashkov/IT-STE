# Draft remediation handoff

[Русское резюме](it-ste-draft-handoff.ru.md)

English is authoritative. Read this after the root `AGENTS.md` when continuing draft remediation in an independent thread. This is a work handoff, not an approval or a new standard version. Do not read the complete generated draft or source extraction to bootstrap.

## Current checkpoint — read before historical baseline

- Standing assignment: apply the [evidence-based research method](it-ste-research-method.md) for substantive W1/W2/W3 decisions. Canonical records control dispositions; notes contain evidence, not approval or release authority. Read only active notes, not the research history.
- Active workstream: **W1**. Fresh `checked_all()` recomputation gives **40 needs-review**. Earlier blocked scopes remain unresolved; previously resolved-draft scopes and their evidence remain unchanged. The offset-0 queue begins with `D-P201-004`, `D-P201-005` (batch 011, page 201), `D-P206-001`, `D-P206-003` (batch 012, page 206), `D-P209-004`, `D-P209-005` (batch 012, page 209), `D-P230-003`, `D-P230-004` (batch 016, page 230). Recompute from offset 0 before future edits; do not infer resolution from this resume pointer.
- Last completed slice: **`D-P408-005`, batch 051, physical PDF page 408**, in separately authorized continuation iteration 3/10. The new [page-408 note](it-ste-research/W1-D-P408-005.md) records exact ASD evidence, visual findings, targeted W3C/MDN sources and the bounded visual UI/material decision. Canonical edits are limited to this record's evidence-linked rationale, draft disposition `allowed`, and PDF layout verification; `status: draft` and `review_status: editorial-review-needed` are preserved. Earlier page-397/page-398 evidence and blockers remain unchanged.
- Blocked/unresolved question and inspected evidence: authenticated Issue 9 page 408 confirms the distinct `TRANSPARENT (adj)` row, meaning `Easy to see through`, with `(adj)` wrapped to the next line, and separate boundaries after `TRANSMIT` and before `transport`. W3C CSS Color 4 §§3.3–3.4 and 4 describe opacity/alpha as allowing the backdrop to be seen through a rendered element or color; MDN's opacity reference corroborates the UI behavior and limits it to visual rendering rather than semantic/security visibility. These sources support the bounded visual draft sense but do not establish readability, proxy behavior, security visibility, or vocabulary approval. Editorial review of wording/examples remains open. Earlier blockers, including page-201/206/209/230, page-391, page-397 and page-398 questions, remain unresolved.
- Recomputed counts: **2,196 records / 55 batches: 120 allowed, 1,481 restricted, 407 prohibited, 148 not-applicable, 40 needs-review**. The offset-0 live queue remains `D-P201-004`, `D-P201-005`, `D-P206-001`, `D-P206-003`, `D-P209-004`, `D-P209-005`, `D-P230-003`, `D-P230-004`; the preserved later queue includes `D-P397-005`–`D-P397-007`, `D-P398-001`, then `D-P413-005`–`D-P413-010`. `D-P408-004` and `D-P408-005` are no longer in the needs-review queue after visual source verification and bounded draft dispositions.
- Latest content validation (fresh run, 2026-10-24): affected batch-051 vocabulary check passed with the canonical batch path, then adaptation, corpus, all-batch vocabulary, document build/check and `python3 -W error::ResourceWarning -m unittest discover -s tests` passed (118 tests). Source doctor passed with PDF SHA-256 `d1f4ea9e7cd6e46b47aa9057209f99e78c0e9cfc4e27a5b07895b05c1a166431`; page 408 was rendered and visually inspected. Project diagnostics and `git diff --check` are to be recorded after this checkpoint edit. Post-check `checked_all()` counts and offset-0 queue match the snapshot above. Generated Markdown was rebuilt and checked; these checks are not semantic approval.
- Exact next action / resume budget: **stop after this single-record page-408 slice; do not start iteration 4.** Preserve `D-P408-005` as `allowed` draft pending editorial review of wording/examples; it does not claim readability, proxy transparency, security visibility, or semantic invisibility. For a separately authorized continuation, recompute offset 0; the next live slice is `D-P201-004` / `D-P201-005`, batch 011, physical PDF page 201, while later queue blockers remain preserved. No vocabulary approval, release, publication or SFT readiness is established.

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
