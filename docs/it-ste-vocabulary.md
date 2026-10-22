# Sequential IT-STE vocabulary review

[Русский](it-ste-vocabulary.ru.md)

English is authoritative. This is an editorial review queue, not an approved vocabulary, a released standard, or official ASD guidance.

## Current progress

The first 40 dictionary rows from ASD-STE100 Issue 9, representation `r0001`, have original draft IT sense definitions, applicability, rationales, contextual alternatives, and positive/problematic examples. They are stored in:

```text
standards/it-ste/vocabulary-reviews/asd-ste100/issue-9/r0001/batch-001.json
```

The sequence is physical PDF page order, then numeric row order within the page. Batch 001 covers `D-P149-001` (A) through `D-P154-006` (acrid), physical PDF pages 149–154, without filtering out inconvenient or ambiguous entries.

| Draft proposal | Rows |
| --- | ---: |
| allowed | 1 |
| restricted | 20 |
| prohibited | 9 |
| not-applicable | 4 |
| needs-review | 6 |
| Total considered | 40 |
| Still unreviewed | 2,156 |
| Source rows | 2,196 |

All 40 decisions remain `draft` / `editorial-review-needed`; **none is an editorial approval**. A disposition concerns the stated sense and context, not every use of a spelling. No canonical `ITSTE-T-*` IDs are allocated. Alternatives are contextual expressions, not approved term IDs. Physical-equipment senses can need separate specialist review even when they have no general software application.

The source approval field is a raw mechanical capitalization signal. It is retained for provenance, not transferred to IT-STE. Source definitions and examples are not copied into this batch; the IT definitions and examples are original editorial work. Known extraction problems require `needs-review`, including two adjacent-row overlaps not flagged by the original extractor. Visual source verification remains outstanding for those ambiguous cases; do not silently settle them by copying neighboring text.

## Checks and bounded retrieval

```sh
python3 tools/asd_ste100_local.py doctor
python3 tools/it_ste_vocabulary.py check --compact-json
python3 tools/it_ste_vocabulary.py entry D-P149-001 --compact-json
```

The checker authenticates the published source, permission record, and domain registry; compares every row's ID, headword, extracted part of speech, physical page, raw approval, and warnings against the first 40 source rows; and verifies sequence, draft boundaries, required editorial fields, rights separation, and remaining counts. It does not approve meanings or prove semantic or PDF-layout accuracy. It works without the private PDF. The present checker intentionally covers batch 001 only, not arbitrary future batches.

The next unreviewed row is **`D-P154-007`**. Continue from that row without skipping source rows. Retrieve bounded metadata first, then exact entries as needed. Do not load all dictionary definitions into an agent's context.

For each subsequent batch:

1. Preserve source pins and exact sequence; assign no blanket disposition from the ASD approval signal.
2. Separate the source sense from a proposed IT sense, including limits, domains, grammar, and examples. A different IT sense needs a distinct editorial decision.
3. Record ambiguities and unresolved senses explicitly. Preserve literal names and syntax regardless of prose preference.
4. Keep source and project rights separate and retain the required project link.
5. Extend batch-aware validation and tests before registering a later batch; the current fixed first-batch checker must not be misrepresented as validating it.
6. Approve and materialize term senses only through a separate editorial decision. Draft candidates must not enter an approved lexicon or training corpus automatically.

## Single-file reading copy

[IT-STE-draft.md](IT-STE-draft.md) is generated from all 31 canonical draft rules and this first vocabulary batch:

```sh
python3 tools/it_ste_document.py build
python3 tools/it_ste_document.py check
```

The only supported output is `docs/IT-STE-draft.md`. `build` refuses an unrelated existing file or a symlink; `check` compares deterministic bytes and does not write. Edit the canonical records or batch and rebuild, not the generated document. The document carries warnings, source references, and hashes; it does not turn candidates into approved vocabulary. Agents can use exact JSON records and the bounded entry command instead of loading the whole Markdown file.

Original editorial content: IT-STE contributors, [CC BY-SA 4.0](../LICENSE-CONTENT.md). ASD owns the source standard. [Derivative permission](permissions/asd-ste100-issue-9-derivatives.md) does not establish broader downstream source licensing or permit PDF publication. Required project attribution: https://github.com/vladimirmashkov/IT-STE.
