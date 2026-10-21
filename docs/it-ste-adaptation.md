# IT-STE adaptation workflow

[Русский](it-ste-adaptation.ru.md)

This English document is authoritative. The adaptation plan converts a pinned ASD-STE100 source revision into reviewed editorial decisions before any normative IT-STE record is created.

## Current plan

The first plan is pinned to ASD-STE100 Issue 9, representation revision `r0001`:

```text
standards/it-ste/
  domains/v1.0.0.json
  adaptation-plans/asd-ste100/issue-9/r0001/
    manifest.json
    map.jsonl
```

`domains/v1.0.0.json` defines stable draft identifiers for IT contexts. `map.jsonl` has one record for each of the 53 source rules and 8 general recommendations. The plan manifest authenticates the source database, domain registry, and map by SHA-256.

The plan is not an IT-STE release, its heading-based candidate domains are not normative, and no target rule ID is allocated until an editorial decision requires one.

## Assessment states

Each source block moves through these independent fields:

- `assessment.status`: `unreviewed`, `in-review`, or `reviewed`;
- `assessment.applicability`: `pending`, `adopt`, `adapt`, `split`, `merge`, or `not-applicable`;
- `assessment.adaptation_action`: `pending`, `create-rule`, `create-rules`, `merge-into-rule`, or `record-rationale-only`.

A `reviewed` assessment requires a non-empty English `rationale` and one coherent decision:

| Applicability | Action | Target IDs |
| --- | --- | --- |
| `adopt` or `adapt` | `create-rule` | exactly one |
| `split` | `create-rules` | two or more |
| `merge` | `merge-into-rule` | exactly one; it can be shared only by other merge decisions |
| `not-applicable` | `record-rationale-only` | none |

Candidate domains must use IDs from the pinned `standards/it-ste/domains/v1.0.0.json` registry. Target IDs use the exact form `ITSTE-R-NNNN` and identify project-owned IT-STE rules rather than ASD rules.

## Review one source block

1. Authenticate the source and plan:

   ```sh
   python3 tools/asd_ste100_local.py doctor
   python3 tools/it_ste_adaptation.py check
   ```

2. Read the compact source card. Use a bounded excerpt for the exact question and `--full` only if the decision still lacks context:

   ```sh
   python3 tools/asd_ste100_local.py rule 5.2
   python3 tools/asd_ste100_local.py excerpt 5.2 "one instruction"
   python3 tools/asd_ste100_local.py rule 5.2 --full
   ```

3. Edit only that block's map record. Explain what applies to IT, what must change, and why. Do not copy source wording into an IT-STE rule by default.
4. Allocate target IDs only after deciding to create, split, or merge rules.
5. Refresh hashes and counts, then validate:

   ```sh
   python3 tools/it_ste_adaptation.py seal
   python3 tools/it_ste_adaptation.py check
   ```

`init` creates a plan only when neither plan file exists and never overwrites manual work. Use `seal` after map edits. If the pinned domain-registry bytes changed, `seal` stops until classifications are reviewed; only then use `seal --accept-domain-change` to record the explicit migration.

## From plan to standard

Reviewed map decisions are inputs to, not substitutes for, canonical IT-STE records. Author English rules under a versioned `standards/it-ste/versions/<version>/revisions/<revision>/content/en/` snapshot. Store exact source locators and rationale, keep Russian optional and subordinate to English, and generate human and LLM representations from the canonical records.

The current tool profile is intentionally pinned to Issue 9 `r0001`. A future upstream issue or corrected source representation gets a separate immutable plan path and trusted source profile; never repin this plan to another source.

This project is independent work and not official ASD guidance. Retain ASD ownership information for source-derived material and the required IT-STE attribution link: https://github.com/vladimirmashkov/IT-STE.
