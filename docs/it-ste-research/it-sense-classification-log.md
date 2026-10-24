# IT-STE independent IT-sense classification log

State: active
Baseline register: `docs/it-ste-research/needs-review-38.md`
Skill: `.agents/skills/it-ste-it-sense-classification/SKILL.md`
Policy: `docs/it-ste-it-sense-policy.md`
Started: 2026-10-24
Last checkpoint: 2026-10-24, after policy slice 1/36
Requested iterations: 36 (user-authorized); this run executes slice 1/36 only
Completed slices: 22 legacy classification slices + policy slice 1/36
Processed records: 40
Disposition changes: 4 records changed from `needs-review` to `restricted`
Remaining `needs-review`: 34

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

Fresh canonical counts after policy slice 1/36:

- total: `2,196` records / `55` batches;
- `allowed`: `120`;
- `restricted`: `1,487`;
- `prohibited`: `407`;
- `not-applicable`: `148`;
- `needs-review`: `34`.

The 34 remaining records are listed in `needs-review-38.md`. Slice 1 resolved only the selected page-206 records under the explicit policy; it did not approve vocabulary or release content. The next run must recompute the canonical queue and select the next bounded question; it must not start slice 2 in this run.

Exact next policy question: after fresh offset-0 recomputation, inspect only `D-P209-004` / `D-P209-005`, batch 012, physical PDF page 209. Do not start slice 2/36 here.

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

## Policy classification slice 1/36 — `D-P206-001` / `D-P206-003`

- Run/slice: user-authorized `--iterations=36`, slice 1/36; batch `012`; physical PDF page `206`; POS `adj` (`critical`) and `n` (`curvature`).
- Old/new: both records changed `needs-review` → `restricted`.
- ASD evidence: Issue 9, revision `r0001`, exact entries `D-P206-001` / `D-P206-003`, printed page `2-1-C24`, authenticated PDF SHA-256 `d1f4ea9e7cd6e46b47aa9057209f99e78c0e9cfc4e27a5b07895b05c1a166431`; exact entries and page retrieval passed. Visual findings: row 1 `critical` has separate `VERY IMPORTANT` and `CAREFUL (adj)` alternatives; row 3 `curvature` has separate `BEND (n)`, `CURVE (n)`, and `RADIUS (TN)` alternatives/examples. Mechanical ambiguity arrays remain preserved.
- IT question and exclusions: can policy admit bounded cross-domain IT senses without treating ordinary importance, ASD `CAREFUL`, generic curve/radius, physical bend radius, or connectivity outcomes as equivalent? Yes, as restricted domain profiles only.
- Sources actually inspected: FIRST CVSS v4.0 Specification v1.2 (`https://www.first.org/cvss/v4.0/specification-document`, accessed 2026-10-24) for named `Critical` severity, with CVSS-specific limitation; WHATWG HTML Living Standard Canvas 2D (`https://html.spec.whatwg.org/multipage/canvas.html#dom-context-2d-arc-dev`, current snapshot 2026-10-22) for curve/arc/radius path APIs, with Canvas-only limitation; W3C SVG 2 Paths (`https://www.w3.org/TR/SVG2/paths.html`, accessed 2026-10-24) for graphical path/curve/arc/radius geometry, with no universal lexical or physical bend-radius authority. ITIL was not applicable because these are monitoring/security and UI/graphics claims, not service-management concepts.
- Canonical changes: bounded definitions, domain-specific alternatives/examples/rationales, and dispositions only; IDs, sequence, source pins, warnings, raw metadata, rights, fixed retrieval commands, `status: draft`, and `review_status: editorial-review-needed` preserved. The prior historical W1 slice remains recorded as superseded, not deleted.
- Decision and limits: `restricted` is preferred by policy over `allowed` due to domain/polysemy boundaries; `prohibited`/`not-applicable` would reject evidenced IT uses; unresolved split proposals remain possible if future schema/editorial review requires separate profiles. No vocabulary approval, release, publication, canonicalization, or SFT readiness.
- Validation/commit: affected batch-012 check; adaptation; corpus; all-batch vocabulary check; document build/check; 118 unit tests with `ResourceWarning` as errors; authenticated source doctor before evidence use and after validation; diagnostics with no errors/warnings; `git diff --check`; exact ASD entries/page retrieval; and offset-0 recomputation all passed. Automatic commit: `584e0a5` (`Classify page 206 IT senses`), explicit paths `docs/IT-STE-draft.md`, `docs/it-ste-draft-handoff.md`, `docs/it-ste-research/W1-D-P206.md`, `docs/it-ste-research/it-sense-classification-log.md`, `docs/it-ste-research/needs-review-38.md`, `standards/it-ste/vocabulary-reviews/asd-ste100/issue-9/r0001/batch-012.json`, and `tests/test_it_ste_vocabulary.py`. Next action is recompute offset 0 and stop before slice 2/36.
