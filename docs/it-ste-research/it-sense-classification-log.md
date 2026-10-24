# IT-STE independent IT-sense classification log

State: active
Baseline register: `docs/it-ste-research/needs-review-38.md`
Skill: `.agents/skills/it-ste-it-sense-classification/SKILL.md`
Policy: `docs/it-ste-it-sense-policy.md`
Started: 2026-10-24
Last checkpoint: 2026-10-24, after legacy-import reconciliation
Requested iterations: not set; use an explicit bounded count for each run
Completed slices: 22 legacy classification slices
Processed records: 38
Disposition changes: 2 records changed from `needs-review` to `restricted`
Remaining `needs-review`: 36

## Purpose and evidence policy

This log records an independent IT-sense classification layer for ASD-derived candidates. ASD-STE100 remains provenance and source evidence, not an IT ontology. Every decision must distinguish ASD facts, authoritative external facts, and editorial inference.

Primary/expert sources are required for substantive IT claims. Reddit and Stack Overflow are permitted only as discovery aids; they are never evidence and must be marked `discovery only`. Search snippets, AI summaries, inaccessible pages and uninspected claims are not evidence.

## Legacy import — completed bounded classification slices

The following completed slices were researched and committed before this log was created. Their detailed evidence remains in the linked per-slice notes; the aggregate old/new register is `docs/it-ste-research/needs-review-38.md`.

| Slice | IDs | Result | Commit |
|---:|---|---|---|
| 1 | `D-P201-004/005` | `needs-review` → `restricted` | `48e5f10` |
| 2 | `D-P206-001/003` | unchanged `needs-review` | `d5fba18` |
| 3 | `D-P209-004/005` | unchanged `needs-review` | `32d8ec2` |
| 4 | `D-P230-003/004` | unchanged `needs-review` | `159b4ea` |
| 5 | `D-P273-004/005` | unchanged `needs-review` | `64e2e5d` |
| 6 | `D-P280-003/004` | unchanged `needs-review` | `d538add` |
| 7 | `D-P349-003` | unchanged `needs-review` | `af85563` |
| 8 | `D-P351-001` | unchanged `needs-review` | `8200f26` |
| 9 | `D-P365-011` | unchanged `needs-review` | `3676f57` |
| 10 | `D-P368-010` | unchanged `needs-review` | `912df72` |
| 11 | `D-P374-005/006` | unchanged `needs-review` | `a7cbb8b` |
| 12 | `D-P379-002` | unchanged `needs-review` | `14c7bf7`, register reference `03ebe72` |
| 13 | `D-P391-003/005` | unchanged `needs-review` | `a3cd0cf` |
| 14 | `D-P397-005/006/007` | unchanged `needs-review` | `c8a00d4` |
| 15 | `D-P398-001` | unchanged `needs-review` | `8651ffc` |
| 16 | `D-P413-005/006` | unchanged `needs-review` | `4d8d10a` |
| 17 | `D-P413-009/010` | unchanged `needs-review` | `71aed85` |
| 18 | `D-P415-004/005` | unchanged `needs-review` | `e956610` |
| 19 | `D-P416-006` | unchanged `needs-review` | `efc090c` |
| 20 | `D-P417-006/007` | unchanged `needs-review` | `d4be85a` |
| 21 | `D-P417-008/009` | unchanged `needs-review` | `7bdcb63` |
| 22 | `D-P419-006/007` | unchanged `needs-review` | `de5fb40` |

The legacy slices inspected exact ASD entries and authenticated PDF pages and recorded authoritative-source limitations. No legacy slice claimed vocabulary approval, release, publication, or SFT readiness.

## Current checkpoint

Fresh canonical counts after the legacy slices:

- total: `2,196` records / `55` batches;
- `allowed`: `120`;
- `restricted`: `1,485`;
- `prohibited`: `407`;
- `not-applicable`: `148`;
- `needs-review`: `36`.

The 36 remaining records are listed in `needs-review-38.md`. Their evidence is not sufficient to force a new disposition. The next run must recompute the canonical queue and select a genuinely new bounded question; it must not cosmetically repeat a blocked slice.

Exact next policy question: determine whether the project owner wants an explicit IT-scope policy for aviation-derived physical, hardware, networking, security, and observability senses. Without that policy or new controlling evidence, keeping a record `needs-review` is safer than inventing an IT sense.

## Required entry format for future slices

For every future slice append a compact entry containing:

- run/slice number and exact IDs, batch, POS, and physical page;
- old/new disposition for each ID;
- ASD Issue/revision, exact entry locator, PDF hash, and visual findings;
- one concrete IT question and excluded meanings;
- authoritative sources actually inspected, URLs, versions/status, findings and limitations;
- any Reddit/Stack Overflow discovery marked `discovery only`;
- alternatives and rejected outcomes;
- changed canonical wording/fields, if any;
- validation and diagnostics results;
- commit hash and explicit paths, or the reason no commit was safe;
- one exact next action.

No future entry may claim vocabulary approval, release, publication, canonicalization, or SFT readiness.
