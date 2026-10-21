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
  it-ste/versions/                 # Versions of the original IT-STE standard
    <version>/revisions/<revision>/
      manifest.json                # Exact contents of one snapshot
      sources/                     # Source and rights metadata
      content/<language>/
        rules/<id>.json            # One rule per record
        terms/<id>.json            # One term sense per record
      relations.jsonl              # Adaptation and replacement relationships
templates/                         # Record templates; not part of the standard
llm/                               # Contract for LLM-oriented exports
docs/storage.md                    # Storage and versioning rules
exports/                           # Generated JSONL; not committed to Git
```

Both standards use the same snapshot structure. A **standard version** and a **corpus revision** are different coordinates: a translation or metadata update does not invent a new ASD-STE100 edition. JSON records are the single canonical data source. Markdown views and LLM exports must be generated from them.

For details, see [storage and versioning](docs/storage.md), the [LLM export contract](llm/README.md), and the [record templates](templates/).

## Status

The repository structure is ready. No rules or vocabularies have been released, and the release registry is empty. No ASD-STE100 text has been imported. Export and corpus-validation tools are not implemented yet.

## Licensing and required project link

Original project text, translations, and data are licensed under **[CC BY-SA 4.0](LICENSE-CONTENT.md)**. When you share the material or adaptations, retain attribution and the project link in the manner required by the license:

> IT-STE — IT-STE contributors. https://github.com/vladimirmashkov/IT-STE. CC BY-SA 4.0.

Also retain the license link and indicate changes. See the [ready-to-use attribution](ATTRIBUTION.md). Distributed adaptations are subject to the ShareAlike terms.

Software tools are licensed under **GPLv3**; see [LICENSE](LICENSE). ASD-STE100 and other third-party material retain their own terms. The IT-STE license does not replace them.
