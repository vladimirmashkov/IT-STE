# Private ASD-STE100 Issue 9 reference

[Русский](asd-ste100-local-reference.ru.md)

This workflow converts a lawfully obtained local copy of ASD-STE100 Issue 9 into a **private retrieval index** for agents. The PDF, extracted text, SQLite database, and generated manifest stay under `.local/`, which Git ignores. They are not a publishable corpus.

The authoritative source is the PDF. Extraction is mechanical and unreviewed. Table columns, typography, diagrams, and wrapped text can be parsed incorrectly. Always use the reported physical PDF page for verification when wording or classification matters.

## Requirements

- `.local/sources/ASD-STE100-issue-9.pdf`
- Python 3.11 or later
- Poppler commands `pdftotext` and `pdfinfo`
- The reviewed source SHA-256: `d1f4ea9e7cd6e46b47aa9057209f99e78c0e9cfc4e27a5b07895b05c1a166431`

The builder refuses a different PDF hash. This prevents silent mixing of editions or modified files.

## Build and validate

Run from the repository root:

```sh
python3 tools/asd_ste100_local.py build
python3 tools/asd_ste100_local.py doctor
python3 -m unittest tests/test_asd_ste100_local.py
```

Use `build --force` only to replace an existing generated database after changing the extractor. The result is `.local/derived/asd-ste100/issue-9/reference.sqlite3` with a sibling `manifest.json`. The CLI rejects source, database, or manifest paths that resolve outside `.local/` and rejects overlapping input/output paths.

The index contains:

- all 434 physical pages as a page-preserving layout-text fallback;
- 53 addressable Part 1 rules;
- 8 addressable general recommendations (`GR-1` through `GR-8`);
- 2,196 dictionary row blocks split into four labeled columns;
- SQLite FTS indexes for compact discovery.

No embeddings or external API calls are required. Exact lexical and structural lookup is cheaper, deterministic, and sufficient for the standard's IDs and controlled vocabulary.

## Token-efficient agent workflow

Use progressive disclosure. Do not put the complete PDF extraction into an agent context.

```sh
# 1. Confirm the exact local source and index.
python3 tools/asd_ste100_local.py doctor

# 2. Read the small index summary.
python3 tools/asd_ste100_local.py overview

# 3. Discover only relevant rule headings.
python3 tools/asd_ste100_local.py rules --section 5
python3 tools/asd_ste100_local.py search "passive voice" --scope rules

# 4. Read a compact rule card first; request full text only when required.
python3 tools/asd_ste100_local.py rule 5.1
python3 tools/asd_ste100_local.py rule 5.1 --full

# 5. Read meaning/alternatives first; add examples only when required.
python3 tools/asd_ste100_local.py word test
python3 tools/asd_ste100_local.py word test --pos n --full

# 6. Use raw page output only as a verification fallback.
python3 tools/asd_ste100_local.py page 87
```

All retrieval commands support `--json` for programmatic use. `search` supports `--scope rules`, `dictionary`, `pages`, or `all`. Start with the narrowest scope and a small `--limit`; the accepted range is 1–20 and the limit is global across scopes. Full JSON output avoids duplicating aggregate text and its page/column components.

## Reliability rules

- Treat uppercase/lowercase dictionary rows as separate candidates. Never merge them case-insensitively.
- A dictionary lookup without `--full` intentionally omits examples. It does not omit the meaning/alternatives column.
- A rule lookup without `--full` returns the exact heading, citations, and detail size, not a generated semantic summary.
- `wrapped-headword` is a structural warning. Preserve the displayed source spelling and verify the cited page before repairing a line-break hyphen.
- If a query is absent or ambiguous, use `search`, then inspect one cited `page`. Do not read all pages.
- Cite the standard as ASD-STE100 Issue 9 and include the physical PDF page. The printed page label is also returned when available.
- Do not claim that mechanical extraction, an LLM response, or an IT-STE adaptation is official ASD guidance.

## Rights boundary

The source PDF says “All rights reserved” and restricts reproduction or publication, subject to specified special usage rights. Free access to a copy does not establish permission to publish it or its extraction. The tracked repository therefore contains only the extractor, source metadata, and operating instructions. Do not stage `.local/`, copy extracted text into tracked fixtures, or publish the generated database without documented authorization.
