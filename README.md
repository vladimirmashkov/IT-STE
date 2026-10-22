# IT-STE

[Русский](README.ru.md)

**IT-STE (IT Simplified Technical English)** is an open controlled-language project for IT documentation. It applies the principles of ASD-STE100 to software, infrastructure, APIs, security, and IT operations.

The goal is to make instructions and descriptions unambiguous, consistent, and useful to readers, translators, and LLM-based tools. The project combines the original IT-STE standard, translations, and a versioned corpus of material about ASD-STE100 while preserving the provenance and rights of each item.

IT-STE is an independent project. It is not an official ASD standard or translation. Public availability of a source standard does not by itself grant permission to republish or translate it.

## Language policy

**English (`en`) is the primary and authoritative language.** The unsuffixed project documentation and the normative IT-STE source records are written in English.

**Russian (`ru`) is the preferred secondary language.** Russian translations are welcome, but they are optional and may be published after the corresponding English material. Other languages are optional and use BCP 47 language tags. If a translation conflicts with the English IT-STE text, the English text controls.

See the [language policy](docs/language-policy.md) and its [Russian translation](docs/language-policy.ru.md).

## Repository contents

- **ASD-STE100:** separately versioned source metadata and, only when the necessary rights permit, structured rules, terms, and translations.
- **IT-STE:** original versions of IT-focused rules and vocabulary, examples, and documented relationships to adaptation sources.
- **Translations:** language-specific records pinned to an exact source version and source checksum.
- **LLM corpus:** derived JSONL exports that retain record IDs, versions, language, provenance, rights, and attribution.

## Structure

```text
catalog.json                       # Registry of standards and released snapshots
standards/
  asd-ste100/versions/             # ASD-STE100 versions, separate from IT-STE
  it-ste/
    domains/                       # Versioned draft IT domain identifiers
    adaptation-plans/              # Source-pinned editorial decisions
    versions/                      # Versions of the original IT-STE standard
      <version>/revisions/<revision>/
        manifest.json              # Exact contents of one snapshot
        sources/                   # Source and rights metadata
        content/<language>/
          rules/<id>.json          # One rule per record
          terms/<id>.json          # One term sense per record
        relations.jsonl            # Adaptation and replacement relationships
templates/                         # Record templates; not part of the standard
llm/                               # Contract for LLM-oriented exports
docs/storage.md                    # Storage and versioning rules
exports/                           # Generated JSONL; not committed to Git
```

Both standards use the same snapshot structure. A **standard version** and a **corpus revision** are different coordinates: a translation or metadata update does not invent a new ASD-STE100 edition. JSON records are the single canonical data source. Markdown views and LLM exports must be generated from them.

For details, see [storage and versioning](docs/storage.md), the [adaptation workflow](docs/it-ste-adaptation.md), the [LLM export contract](llm/README.md), and the [record templates](templates/).

## Status

No IT-STE rules or vocabularies have been released, and the release registry is empty. The first draft domain registry and a source-pinned adaptation plan cover all 53 rules and 8 recommendations from Issue 9. Sections 1 through 9 and all 8 general recommendations are reviewed: the 61 source blocks map to 31 planned IT-STE rule IDs. Source recommendations retain their non-normative provenance; target entries remain planning concepts, not canonical normative rules. A [cross-target review](docs/it-ste-plan-review.md) records their boundaries, three clarifications, and the prerequisites for canonical authoring. Issue 9 has tracked source metadata and an authorized, mechanically extracted [derivative retrieval database](docs/asd-ste100-local-reference.md). The source PDF is not tracked or published. All 31 targets now have English draft rules in snapshot `0.1.0-draft.1/r0001`, using the [canonical draft contract](docs/it-ste-canonical-pilot.md). The generator includes all 31 draft rules and all 55 vocabulary batches in the [single-file draft](docs/IT-STE-draft.md). The [sequential vocabulary proposals](docs/it-ste-vocabulary.md) cover all 2,196 source dictionary rows in batches 001–055: 90 `allowed`, 1,344 `restricted`, 402 `prohibited`, 146 `not-applicable`, and 214 `needs-review`. No source rows remain unprocessed, but 214 unresolved sense/layout cases remain. The six initial first-batch ambiguity cases were resolved after visual inspection of physical PDF pages 153–154; three more blockers in batch 002 were resolved after visual inspection of pages 156–157. Other rows have not been visually verified in this work. All vocabulary decisions remain `draft` / `editorial-review-needed`, with no approved lexicon or canonical term IDs. Source approval does not automatically transfer to IT-STE. Complete source-row draft coverage is not a complete approved IT vocabulary: IT-only terms still require a separate inventory. Run `python3 tools/it_ste_corpus.py check`, `python3 tools/it_ste_vocabulary.py check`, and `python3 tools/it_ste_document.py check`. The snapshot remains draft, not release-ready or SFT-ready: a complete approved vocabulary, general release validation, prose-conformance checking, and released LLM/SFT exports are not implemented. Vocabulary `check` and `entry` cover all batches by default; `--batch` selects one batch.

## Licensing and required project link

Original project text, translations, and data are licensed under **[CC BY-SA 4.0](LICENSE-CONTENT.md)**. When you share the material or adaptations, retain attribution and the project link in the manner required by the license:

> IT-STE — IT-STE contributors. https://github.com/vladimirmashkov/IT-STE. CC BY-SA 4.0.

Also retain the license link and indicate changes. See the [ready-to-use attribution](ATTRIBUTION.md). Distributed adaptations are subject to the ShareAlike terms.

Software tools are licensed under **GPLv3**; see [LICENSE](LICENSE). ASD-STE100 and other third-party material retain their own terms. The IT-STE license does not replace them.
