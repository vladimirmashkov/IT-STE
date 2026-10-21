# ASD-STE100 Issue 9 derivative reference

[Русский](asd-ste100-local-reference.ru.md)

This repository includes an authorized machine-readable derivative of ASD-STE100 Issue 9 for token-efficient agent retrieval. The source PDF is not published. It remains under `.local/` only when a repository maintainer needs to reproduce the database.

The authoritative source remains the PDF obtained from ASD. The published database is a mechanical, semantically unreviewed extraction. Table columns, typography, diagrams, and wrapped text can be parsed incorrectly. Use the reported physical PDF page for verification when exact wording or classification matters.

## Published artifacts

```text
standards/asd-ste100/versions/issue-9/revisions/r0001/derived/
  reference.sqlite3  # Queryable page, rule, guidance, dictionary, and FTS data
  manifest.json      # Source/database hashes, counts, generator, and rights state
  NOTICE.md          # Ownership, permission, attribution, and review notice
```

The index contains:

- all 434 physical pages as a page-preserving layout-text fallback;
- 53 addressable Part 1 rules;
- 8 addressable general recommendations (`GR-1` through `GR-8`);
- 2,196 dictionary row blocks split into four labeled columns;
- SQLite FTS indexes for compact discovery.

No embeddings or external API calls are required. Exact lexical and structural lookup is deterministic and avoids loading the complete standard into context.

## Validate and query

The published derivative works without the source PDF or Poppler:

```sh
python3 tools/asd_ste100_local.py doctor
python3 tools/asd_ste100_local.py overview
```

`doctor` verifies the database SHA-256 against its manifest, SQLite integrity and foreign keys, metadata, table and FTS counts, exact rule/recommendation ID sets, publication flags, and SHA-256 values for the notice and permission record. If the local source PDF is present, it also verifies its SHA-256 and the Poppler prerequisites.

Use progressive disclosure:

```sh
# Discover only relevant headings or snippets.
python3 tools/asd_ste100_local.py rules --section 5
python3 tools/asd_ste100_local.py search "passive voice" --scope rules

# Read a compact rule card first; request full text only when required.
python3 tools/asd_ste100_local.py rule 5.1
python3 tools/asd_ste100_local.py rule 5.1 --full

# Read meaning/alternatives first; add examples only when required.
python3 tools/asd_ste100_local.py word test
python3 tools/asd_ste100_local.py word test --pos n --full

# Use raw page output only as a verification fallback.
python3 tools/asd_ste100_local.py page 87
```

All retrieval commands support `--json`. `search` supports `--scope rules`, `dictionary`, `pages`, or `all`. The `--limit` range is 1–20 and applies globally across scopes. Full JSON avoids duplicating aggregate text and its page/column components.

## Reproduce and publish a new build

Maintainers need:

- `.local/sources/ASD-STE100-issue-9.pdf`;
- Python 3.11 or later;
- Poppler commands `pdftotext` and `pdfinfo`;
- source SHA-256 `d1f4ea9e7cd6e46b47aa9057209f99e78c0e9cfc4e27a5b07895b05c1a166431`.

Run from the repository root:

```sh
python3 tools/asd_ste100_local.py build --force
python3 tools/asd_ste100_local.py publish --force
python3 tools/asd_ste100_local.py doctor
python3 -m unittest tests/test_asd_ste100_local.py
```

`build` writes staging artifacts only to `.local/`. `publish` authenticates them and copies only the derivative database and manifest to the fixed versioned directory. It never copies the PDF. Build inputs and outputs cannot overlap, and arbitrary public output paths are rejected.

## Reliability rules

- Treat uppercase/lowercase dictionary rows as separate candidates. Never merge them case-insensitively.
- A dictionary lookup without `--full` intentionally omits examples, not the meaning/alternatives column.
- A rule lookup without `--full` returns the exact heading, citations, and detail size, not a generated semantic summary.
- `wrapped-headword` is a structural warning. Preserve displayed source spelling and verify the cited page before repairing a line-break hyphen.
- If a query is absent or ambiguous, use `search`, then inspect one cited `page`. Do not read all pages.
- Cite ASD-STE100 Issue 9 and the physical PDF page. The printed page label is also returned when available.
- Do not present mechanical extraction, an LLM response, or an IT-STE adaptation as official ASD guidance.

## Rights boundary

The repository owner records offline written authorization to publish derivative files from Issue 9, including this machine-readable database. Publication of the source PDF is explicitly excluded. See the [permission record](permissions/asd-ste100-issue-9-derivatives.md) and the artifact `NOTICE.md`.

The authorization does not establish a broader downstream license or relicense ASD source material under the IT-STE project licenses. Retain ASD ownership information, the derivative notice, and the required IT-STE project link. Never add the source PDF to Git.
