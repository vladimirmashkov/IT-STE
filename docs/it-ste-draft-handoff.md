# Draft remediation handoff

[Русское резюме](it-ste-draft-handoff.ru.md)

English is authoritative. Read this after the root `AGENTS.md` when continuing draft remediation in an independent thread. This is a work handoff, not an approval or a new standard version. Do not read the complete generated draft or source extraction to bootstrap.

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

### W1 — Resolve the 217 explicit blockers first

These are unresolved decisions, **not 217 proven extraction errors**. At baseline 103 have source extraction warnings; 114 do not. Warning absence is not semantic verification. Examples: adjacent-row overlap (`D-P156-005`/`006`), insufficient noun context (`D-P157-003`, advance), physical fastening versus information security (`D-P370-004`, security), and setting a number to zero versus calibration/sanitization (`D-P433-007`, zero).

For each selected record:

1. Inspect its existing proposal, rationale, warning/ambiguity evidence, and exact source sense. Verify the cited PDF page visually if layout is in question; source examples can help only when bounded retrieval is insufficient.
2. Decide independently which IT sense and grammatical function to propose. An aviation meaning is not an IT whitelist/ban. `not-applicable` concerns the stated source sense, not every use of the spelling.
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

Before finishing, follow the root Git review/commit-proposal instructions and append a concise handoff delta here: IDs/pages resolved, evidence used, blockers left, new files/contracts, and actual checks run. Preserve unrelated work. A fresh thread must be able to resume from records without the chat transcript.

Release/SFT readiness is **not** established by successful checks or zero unprocessed rows. Require approved technical/editorial content, canonical vocabulary/release validation, and separate dataset review (rights, unresolved examples, splits/evaluation, versioned provenance) before publishing an approved lexicon or training export.

Original editorial content: IT-STE contributors, [CC BY-SA 4.0](../LICENSE-CONTENT.md). ASD source rights remain separate; source PDF publication is forbidden. Mandatory project attribution: https://github.com/vladimirmashkov/IT-STE.
