# Standard storage

[Русский](storage.ru.md)

## 1. Independent coordinates

| Coordinate | Meaning |
| --- | --- |
| `standard` | `asd-ste100` or `it-ste`; namespaces never mix |
| `version` | Exact ASD-STE100 edition designation or an IT-STE SemVer version |
| `revision` | Snapshot of this representation: `r0001`, `r0002`, and so on |
| `language` | BCP 47 language tag of one record, such as `en` or `ru` |

A new translation, corrected extraction, or metadata update does not change the source-standard edition. Publish a new `revision` for those changes. A change to primary normative IT-STE text requires a new `version`.

English (`en`) is the primary and authoritative language. Russian (`ru`) is the preferred secondary language, but it and all other translations are optional. `primary_language` is `en`; `languages` lists only languages represented in a snapshot. See the [language policy](language-policy.md).

`catalog.json` lists released snapshots. Each `releases` item contains `version`, `revision`, and a repository-relative `manifest` path. The initial lists are empty: no actual ASD-STE100 edition or IT-STE version has been registered.

## 2. Snapshot directory

This structure describes future snapshots, not an already published edition:

```text
standards/<standard>/versions/<version>/revisions/<revision>/
  manifest.json
  sources/
    <source-id>.json
  content/
    en/
      rules/<id>.json
      terms/<id>.json
    ru/
      rules/<id>.json
      terms/<id>.json
    <other-bcp47-tag>/
      rules/<id>.json
      terms/<id>.json
  relations.jsonl
```

`manifest.json` explicitly lists record and source-metadata files in its `records` and `sources` arrays. `relations` is a path to a JSONL relationship file or `null`. Paths are relative to the manifest directory and cannot escape it. Merely placing a file in the directory does not include it in the corpus.

Other manifest fields are `schema_version`, `standard`, `version`, `revision`, `status`, `primary_language`, `languages`, `language_coverage`, `supersedes`, and `released_at`. `languages` lists only represented languages. `language_coverage` maps each listed language to `partial` or `complete`. `supersedes` is a `{standard, version, revision}` reference to the previous snapshot or `null`.

For a released IT-STE snapshot, `en` must be listed and `language_coverage.en` must be `complete`. Additional languages can be absent or partial. The keys of `language_coverage` must exactly match `languages`.

`schema_version` is the data-format version, not the standard version. An incompatible data-format change requires a new schema major version. Documents and templates describe the general format; executable JSON Schemas do not exist yet. The narrow [canonical draft pilot](it-ste-canonical-pilot.md) adds profile `it-ste-pilot-v1` in format `1.1.0`, with an executable standard-library validator, structured source/facet locators, and prose/literal example segments. It does not implement general release or translation validation.

## 3. Canonical records

One UTF-8 JSON file stores one rule or one term sense in one language. Do not maintain an independently editable Markdown copy. Common fields are shown in the [rule template](../templates/rule.json) and [term template](../templates/term.json).

- `id` is a stable identifier, such as `ITSTE-R-0001` or `ITSTE-T-0001`. Never reuse it for another entity. The `ITSTE` and `ASDSTE` prefixes distinguish project namespaces; they are not official ASD numbering.
- `kind` is `rule` or `term`. A different term sense gets a different ID even when its spelling is identical.
- `language` identifies the record language. A translation retains the source entity ID.
- `status` is `draft`, `review`, `approved`, or `withdrawn`.
- `origin` is `original`, `upstream`, `adaptation`, or `translation`.
- `source_refs` contains `{source_id, locator}` references to source metadata and an exact rule, section, or page location.
- `rights` contains the license and URL, redistribution and adaptation rights, attribution, and evidence for those rights. Never infer a license from the directory name.

A rule separately stores `title`, normative `text`, `applies_to`, and permitted/prohibited `examples`. A term stores `term`, `part_of_speech`, `definition`, `usage`, `alternatives`, and `examples`. `usage` is `allowed`, `restricted`, or `prohibited`. `alternatives` contains term IDs from the same snapshot and language.

A record reference always includes every coordinate:

```json
{
  "standard": "it-ste",
  "version": "0.1.0",
  "revision": "r0001",
  "language": "en",
  "kind": "rule",
  "id": "ITSTE-R-0001"
}
```

This is an address example, not a declaration of an existing release. Build an index key as `standard@version#revision/language/kind/id`. A bare ID does not identify a version and is not a unique LLM-index key.

## 4. Translation is not adaptation

For a translation, `translation_of` contains a full source-record `ref` and `source_sha256`, the SHA-256 of the canonical source file bytes. It is `null` on a primary-language source record.

A changed source requires translation review. Do not silently replace the old checksum. Pin the relationship to an exact revision, never to `latest`. Preserve the distinction between borrowed examples, constraints, and meaning.

An IT-STE adaptation receives its own ID and `origin: adaptation`; it is not presented as an ASD-STE100 translation. Store its relationship in `relations.jsonl`:

- `adapted_from` — derived record → source record; `rationale` explains what was retained or changed;
- `replaces` — new entity → replaced entity;
- `related_to` — another explicitly justified relationship.

A relationship has `schema_version`, `relation`, `from`, `to`, and `rationale`. Both endpoints are full record references. Multiple lines support many-to-many relationships. If source text cannot be stored, use `source_refs` with an external source locator instead of pointing to a nonexistent record.

## 5. Sources and rights

The [source template](../templates/source.json) stores title, standard and edition, URL, retrieval date, source-artifact SHA-256, and rights. Use `null` for unknown information instead of inventing an edition or date.

Within `rights`:

- `license` is an SPDX ID or documented `LicenseRef-…`; `license_url` links to the terms;
- `redistribution` and `adaptation` are `allowed`, `forbidden`, or `unknown`;
- `attribution` lists supplied attribution names and URLs;
- `evidence` lists public URLs or repository-root-relative paths that establish rights, without secrets or private correspondence.

`allowed` means verified permission **under the stated license terms**, not an absence of restrictions. `unknown` is not permission. For third-party text, extraction, or translation, verify redistribution and the intended use. Do not substitute the project license for the source license. A translation or adaptation also requires the relevant rights to make a derivative work.

Until rights are verified, store only bibliographic metadata and original project descriptions, without protected text or examples. Free access to a PDF does not by itself permit republication or translation. Linking to a source and discussing general principles are not equivalent to republishing a standard.

Place local source artifacts under `.local/sources/`, which Git ignores. This prevents accidental commits; it does not grant rights. Publishing source artifacts requires a separate rights review, and the public corpus must not depend on a local PDF.

## 6. Lifecycle

1. Copy the [manifest template](../templates/manifest.json) to a new version/revision directory with `status: draft`.
2. Fill in sources, records, languages, coverage, and rights. Remove `template: true` only after completing the data; templates are not standard content.
3. Author and approve the English source records first. A released IT-STE normative set requires complete English coverage; Russian and other translations can follow in later revisions.
4. Verify unique addresses, resolvable references, path/language/ID agreement, translation source checksums, and rights. Review translations and adaptations separately for meaning.
5. Set records to `approved` or `withdrawn`. A released snapshot cannot contain `draft` or `review` records.
6. Set the manifest to `status: released`, provide an ISO 8601 `released_at` value, add the snapshot to `catalog.json`, and record it in Git. Pin public exports to a full commit ID.
7. Never overwrite a released snapshot. Create the next revision or version. Old snapshots remain addressable; `supersedes` and `replaces` preserve history.

JSON and JSONL files use UTF-8 without BOM, LF line endings, and a final newline. JSONL has exactly one object per line. Technical fields and IDs are English; record text uses the declared `language`.

## 7. Derived representations

Markdown, JSONL, and search indexes are not independently edited standards. Generate them from an explicitly selected released snapshot while retaining rights and attribution. The contract is in [llm/README.md](../llm/README.md).

Repository crawlers must not treat `templates/`, `docs/`, local sources, or unverified third-party text as the normative LLM corpus. `python3 tools/it_ste_corpus.py check` validates the draft pilot's structure and authenticated provenance only. General release checks, arbitrary-prose conformance, and exports remain future work; the three draft pilot records are not a released normative LLM corpus.
