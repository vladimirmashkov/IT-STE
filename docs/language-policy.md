# Language policy

[Русский](language-policy.ru.md)

## 1. Primary language

English (`en`) is the primary and authoritative language of IT-STE.

- Normative IT-STE rules and terms are authored and approved in English first.
- Every normative entity in a released IT-STE snapshot must have an approved English source record.
- The unsuffixed repository documentation, such as `README.md`, is English and is the canonical documentation.
- Machine-readable field names, identifiers, schemas, and contribution metadata are English.
- If a translation conflicts with the English IT-STE source, the English source controls.

The English source of ASD-STE100 also remains authoritative over any translation stored by this project. This policy does not change the rights in ASD-STE100 material.

## 2. Additional languages

Russian (`ru`) is the preferred secondary language. It is the first translation target, but it is not required for an English IT-STE release. A Russian translation can be complete or partial and can be added in a later corpus revision.

All other languages are optional. They use valid BCP 47 tags, for example `de`, `fr`, or `pt-BR`. No additional language becomes co-authoritative merely because it has complete coverage.

Documentation translations add the language tag before the extension:

```text
README.md       # canonical English
README.ru.md    # optional Russian translation
guide.md        # canonical English
guide.ru.md     # optional Russian translation
```

Each translated document should link to its English source. A missing or outdated translation must not delay a correction to the English source.

## 3. Standard records

Language is an explicit coordinate of every rule and term record:

```text
content/en/rules/ITSTE-R-0001.json
content/ru/rules/ITSTE-R-0001.json
```

A translation:

- uses the same entity ID and `kind` as its English source;
- sets its own BCP 47 `language` value;
- uses `origin: translation`;
- pins `translation_of` to the exact source standard, version, revision, language, kind, and ID;
- stores the SHA-256 checksum of the canonical source record;
- preserves the source's normative force, limitations, examples, provenance, and rights.

An adaptation is not a translation. It gets its own IT-STE ID and an explicit `adapted_from` relationship.

## 4. Manifests and coverage

`primary_language` is `en`. The `languages` array lists only languages that have records in the snapshot. `language_coverage` uses the same language tags and reports `partial` or `complete` coverage.

For a released IT-STE snapshot:

- `en` must be present in `languages`;
- `language_coverage.en` must be `complete`;
- Russian and other translations may be absent, `partial`, or `complete`;
- a translated record must not exist without a resolvable pinned source record.

Coverage is measured against the normative entities in the same snapshot, not by file count alone. A translation that intentionally omits a normative field is not complete.

## 5. LLM use

LLM exports are language-specific. English is the default when no application-level preference is supplied. Applications can explicitly request Russian or another available language, but they must not silently substitute a different language or version.

Every exported item retains its language, source link, translation link, rights, and project attribution. Mixed-language corpora require an explicit export manifest and language labels on every item.
