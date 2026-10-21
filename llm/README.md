# Representations for LLM use

[Русский](README.ru.md)

This directory defines a format; it does not contain an implemented exporter. Canonical data lives in `standards/`. JSONL, Markdown packages, and indexes must be generated from that data. Training pairs, synthetic examples, and model output are not normative text.

## Language behavior

English (`en`) is the primary language and the default for exports. Russian (`ru`) is the preferred secondary language. Russian and all other translations are optional and can have partial coverage.

Export one language at a time unless a mixed-language package is explicitly requested and described by its manifest. An application must not silently use another language when the requested translation is unavailable. It can either fall back through an explicit application policy or report that the requested record is unavailable. See the [language policy](../docs/language-policy.md).

## Corpus selection

An export requires explicit `standard`, `version`, `revision`, `language`, and full repository commit ID values. Do not use an implicit `latest`. Do not combine ASD-STE100 with IT-STE, different versions, or different languages in one package unless its composition is explicit.

By default, include only:

- records from a `released` snapshot manifest registered in `catalog.json`;
- `approved` records without a `template` marker;
- records with verified redistribution rights and satisfied license conditions;
- translations with a resolvable `translation_of` reference and matching `source_sha256`.

Source metadata for restricted material is not permission to export the source text. Do not index drafts, withdrawn records, templates, or local PDF files as normative rules.

## Authorized derivative retrieval

Issue 9 has an authorized machine-readable derivative under its versioned, Git-tracked `reference/` directory. It is a preserved publication artifact, not disposable build output. The source PDF remains private and is not part of the repository. See the [ASD-STE100 derivative-reference guide](../docs/asd-ste100-local-reference.md) and [permission record](../docs/permissions/asd-ste100-issue-9-derivatives.md).

The index uses compact discovery, stable-ID retrieval, bounded cited excerpts, and explicit `--full` retrieval instead of loading the complete standard into an LLM context. Prefer `search → excerpt` for rules and `word/search → entry` for dictionary rows. Use deterministic `--compact-json` when structured output is required. The index preserves source hash, edition, physical page citations, raw-page fallback, extraction warnings, rights state, and the boundary between ASD source-derived content and project-owned metadata. Regenerate it only through the authenticated `build` and `publish` workflow.

## Export directory

```text
exports/<standard>/<version>/<revision>/<language>/<commit>/
  manifest.json
  rules.jsonl
  terms.jsonl
```

`exports/` is excluded from Git. A completed package can be published separately when its licenses permit this. Vector indexes and embeddings are a separate `.cache/` artifact pinned to this snapshot and to a specific embedding model.

The export manifest records `schema_version`, exact snapshot coordinates and language, language coverage, commit ID, canonical manifest path and SHA-256, exporter version, record counts, output-file hashes, and attribution. Exclude build time from hashed content when byte-for-byte reproducibility is required.

## JSONL unit

One line contains one self-contained rule or term-sense object. An exported object has these fields:

| Field | Purpose |
| --- | --- |
| `schema_version` | Export format version |
| `record_key` | `standard@version#revision/language/kind/id` |
| `standard`, `version`, `revision` | Exact standard and snapshot; retrieval filters |
| `language`, `kind`, `id` | Language, record type, and stable ID |
| `text` | Deterministic textual representation of the complete record for LLM use |
| `record` | Complete canonical JSON record without field loss |
| `source_path`, `source_sha256` | Repository-relative path and SHA-256 of the canonical record bytes |
| `source_url` | Permanent link to the file at the exact commit, not to the `main` branch |
| `source_refs`, `translation_of` | Provenance and exact translation relationship copied from the record |
| `rights` | Terms for the record itself, copied without replacing them with the project license |
| `project_attribution` | Attribution name, project URL, and license for project-owned material and metadata from `catalog.json` |

Some envelope fields intentionally duplicate canonical fields for filtering. They are derived metadata, not a second editable source, and must match `record` and the canonical manifest.

For a rule, `text` includes the rule, its constraints, and clearly distinguished permitted and prohibited examples. For a term, it preserves the sense, part of speech, usage status, alternatives, and examples. Never detach a prohibited example from its label and turn it into a recommendation.

Sort records by `(kind, id)` and serialize JSON deterministically as UTF-8 with LF line endings. Export must fail on duplicate keys, unresolved references, checksum mismatches, unverified rights, or unsatisfied license conditions instead of silently discarding provenance. These checks are not automated yet.

## RAG use

1. Select the standard, version, revision, and language before retrieval. Preserve provenance labels on every result when comparing standards.
2. Put a complete semantic unit with examples and metadata into the context, not only the matched sentence.
3. Show the record ID, version, permanent source link, and license-required attribution. The canonical project URL is **https://github.com/vladimirmashkov/IT-STE**.
4. If the requested version or language is unavailable, report that fact instead of silently substituting another one.

Retaining licenses and links in JSONL supports correct reuse, but it does not guarantee that an LLM will reproduce them. The application using the corpus is responsible for presenting attribution. Terms for third-party material remain separate from the license for project-owned annotations.
