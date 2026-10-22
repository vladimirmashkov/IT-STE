# Sequential IT-STE vocabulary review

[Русский](it-ste-vocabulary.ru.md)

English is authoritative. This is an editorial review queue, not an approved vocabulary, a released standard, or official ASD guidance.

For an independent continuation thread, start with the [compact remediation handoff](it-ste-draft-handoff.md): completed work, live paginated blocker retrieval, and the separate editorial/IT-only coverage tasks. Do not read the full generated draft to bootstrap.

## Current progress

All **2,196 source dictionary rows** from ASD-STE100 Issue 9, representation `r0001`, have draft IT sense proposals, applicability, rationales, contextual alternatives, and positive/problematic examples. They are stored in **55 batches**, `batch-001.json` through `batch-055.json`, under:

```text
standards/it-ste/vocabulary-reviews/asd-ste100/issue-9/r0001/
```

The sequence is physical PDF page order, then numeric row order within the page, from `D-P149-001` through the final row `D-P433-007` (zero). No source rows remain unprocessed; ambiguous and inapplicable rows are included rather than skipped.

| Draft proposal | Rows |
| --- | ---: |
| allowed | 90 |
| restricted | 1,368 |
| prohibited | 403 |
| not-applicable | 146 |
| needs-review | 189 |
| Total draft source-row coverage | 2,196 |
| Unprocessed source rows | 0 |

All 2,196 decisions remain `draft` / `editorial-review-needed`; **none is an editorial approval**. A disposition concerns the stated sense and context, not every use of a spelling. No canonical `ITSTE-T-*` IDs are allocated. Alternatives are contextual expressions, not approved term IDs. Physical-equipment senses can need separate specialist review even when they have no general software application.

**Complete source-row draft coverage is not a complete approved IT vocabulary.** IT-only terms still require a separate inventory and sense-level editorial decisions. There is no approved lexicon, canonical term set, release readiness, or SFT readiness.

The source approval field is a raw mechanical capitalization signal. It is retained for provenance, not automatically transferred to IT-STE. Source definitions and examples are not copied into the batches; the IT definitions and examples are original editorial work. The six initial ambiguity cases in batch 001 were resolved after visual inspection of physical PDF pages 153–154. Three more blockers in batch 002 were resolved after visual inspection of pages 156–157. Other rows have not been visually verified in this work: **195 rows still need sense/layout review**. Their inclusion in a draft is not verification of their meaning or extracted layout.

## Checks and bounded retrieval

```sh
python3 tools/asd_ste100_local.py doctor
python3 tools/it_ste_vocabulary.py check --compact-json
python3 tools/it_ste_vocabulary.py entry D-P433-007 --compact-json
python3 tools/it_ste_vocabulary.py check --batch standards/it-ste/vocabulary-reviews/asd-ste100/issue-9/r0001/batch-001.json --compact-json
python3 tools/it_ste_vocabulary.py entry D-P149-001 --batch standards/it-ste/vocabulary-reviews/asd-ste100/issue-9/r0001/batch-001.json --compact-json
```

By default, `check` validates all batches and `entry` searches all batches; `--batch standards/it-ste/vocabulary-reviews/asd-ste100/issue-9/r0001/batch-001.json` selects one batch. The checker authenticates the published source, permission record, and domain registry; compares each row's ID, headword, extracted part of speech, physical page, raw approval, and warnings against the source; and verifies sequence, draft boundaries, required editorial fields, rights separation, and coverage counts. It does not approve meanings or prove semantic or PDF-layout accuracy. It works without the private PDF.

There is no next unprocessed source row. Continue with the 199 unresolved sense/layout cases, further visual verification, and the IT-only term inventory. Retrieve bounded metadata first, then exact entries as needed. Do not load all dictionary definitions into an agent's context.

For further editorial review:

1. Preserve source pins and exact sequence; assign no blanket disposition from the ASD approval signal.
2. Separate the source sense from a proposed IT sense, including limits, domains, grammar, and examples. A different IT sense needs a distinct editorial decision.
3. Record ambiguities and unresolved senses explicitly. Preserve literal names and syntax regardless of prose preference.
4. Keep source and project rights separate and retain the required project link.
5. Keep batch-aware validation and tests aligned with the source sequence and coverage; passing structural checks does not establish semantic approval.
6. Approve and materialize term senses only through a separate editorial decision. Draft candidates must not enter an approved lexicon or training corpus automatically.

## Single-file reading copy

[IT-STE-draft.md](IT-STE-draft.md) is generated from all 31 canonical draft rules and all 55 vocabulary batches:

```sh
python3 tools/it_ste_document.py build
python3 tools/it_ste_document.py check
```

The only supported output is `docs/IT-STE-draft.md`. `build` refuses an unrelated existing file or a symlink; `check` compares deterministic bytes and does not write. Edit the canonical records or batches and rebuild, not the generated document. The document carries warnings, source references, and hashes; it does not turn candidates into approved vocabulary. Agents can use exact JSON records and the bounded entry command instead of loading the whole Markdown file.

Original editorial content: IT-STE contributors, [CC BY-SA 4.0](../LICENSE-CONTENT.md). ASD owns the source standard. [Derivative permission](permissions/asd-ste100-issue-9-derivatives.md) does not establish broader downstream source licensing or permit PDF publication. Required project attribution: https://github.com/vladimirmashkov/IT-STE.
