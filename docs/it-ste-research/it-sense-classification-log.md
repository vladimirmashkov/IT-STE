# IT-STE independent IT-sense classification log

State: active
Baseline register: `docs/it-ste-research/needs-review-38.md`
Skill: `.agents/skills/it-ste-it-sense-classification/SKILL.md`
Policy: `docs/it-ste-it-sense-policy.md`
Started: 2026-10-24
Last checkpoint: 2026-10-24, after new-policy slice 9/36
Requested iterations: 36 (user-authorized); this run executes slice 9/36 only
Completed slices: 22 legacy classification slices + new-policy slices 1–9/36
Processed records: 51
Disposition changes: 11 records changed from `needs-review` to `restricted`
Remaining `needs-review`: 25

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

Fresh canonical counts after new-policy slice 9/36:

- total: `2,196` records / `55` batches;
- `allowed`: `120`;
- `restricted`: `1,495`;
- `prohibited`: `407`;
- `not-applicable`: `148`;
- `needs-review`: `26`.

The 25 remaining records are listed in `needs-review-38.md`; this log retains the baseline register and records each disposition change. Slices 7 and 8 intentionally left their selected records unresolved; slice 9 changed only `D-P365-011` under the explicit all-IT policy and did not approve vocabulary or release content. Already-resolved records were excluded. The legacy table above is historical and is not the new-policy sequence.

Exact next policy question: after fresh offset-0 recomputation in a future authorized run, inspect only `D-P349-003` (batch 038, physical PDF page 349), and do not start slice 10/36 here.

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
- Validation/commit: affected batch-012 check; adaptation; corpus; all-batch vocabulary check; document build/check; 118 unit tests with `ResourceWarning` as errors; authenticated source doctor before and after validation; diagnostics with no errors/warnings; `git diff --check`; exact ASD entries/page retrieval; and offset-0 recomputation all passed. Automatic commit: `57e5c32` (`Classify page 206 IT senses`), explicit paths `docs/IT-STE-draft.md`, `docs/it-ste-draft-handoff.md`, `docs/it-ste-research/W1-D-P206.md`, `docs/it-ste-research/it-sense-classification-log.md`, `docs/it-ste-research/needs-review-38.md`, `standards/it-ste/vocabulary-reviews/asd-ste100/issue-9/r0001/batch-012.json`, and `tests/test_it_ste_vocabulary.py`. Next action is recompute offset 0 and stop before slice 2/36.

### Policy classification slice 2/36 — `D-P209-004` / `D-P209-005`

- Run/slice: user-authorized slice 2/36; batch `012`; physical PDF page `209`; POS `n` for both records.
- Old/new: `D-P209-004` (`DECISION`) changed `needs-review` → `restricted`; `D-P209-005` (`decontamination`) remains `needs-review`.
- ASD evidence: Issue 9, revision `r0001`, exact entries `D-P209-004` / `D-P209-005`, printed page `2-1-D3`, sequences `477–478`, authenticated PDF SHA-256 `d1f4ea9e7cd6e46b47aa9057209f99e78c0e9cfc4e27a5b07895b05c1a166431`. Exact retrieval passed. Visual inspection confirms `DECISION` row 4 with complete definition `The result after you think about a problem`; `REMOVE` starts row 5. Row 5 is wrapped-headword `decontamination` with `REMOVE CONTAMINATION` and `CLEAN (v)` alternatives. Mechanical warning/ambiguity metadata was preserved.
- IT question and exclusions: can the policy admit a bounded choice/evaluation sense across named IT design, operations, policy, and automation contexts without importing unrestricted ordinary decision, asserted correctness, execution success, incident-response, sanitization, malware-removal, or cloud meanings? `DECISION` yes as restricted; `decontamination` no.
- Sources actually inspected: ADR GitHub organization, “Architectural Decision Records,” `https://adr.github.io/` (accessed 2026-10-24), defines justified architectural design choices and rationale/trade-off decision records, with software/hardware and decision-log coverage; limitation: community guidance, not a universal dictionary. NIST AI RMF (`https://www.nist.gov/itl/ai-risk-management-framework`, AI RMF 1.0 released 2023-01-26, accessed 2026-10-24) supports evaluation/governance for AI products, services, and systems; limitation: it does not define universal `DECISION` wording. NIST SP 800-88 Rev. 1 (`https://csrc.nist.gov/pubs/sp/800/88/r1/final`, withdrawn 2025-09-26 and superseded by Rev. 2, accessed 2026-10-24) defines media sanitization, not decontamination. NIST SP 800-61 Rev. 3 (`https://csrc.nist.gov/pubs/sp/800/61/r3/final`, published 2025-04, accessed 2026-10-24) supports incident response terms but not `decontamination`. AWS/NIST glossary/CDC retrieval failures were not used as evidence.
- Canonical changes: `D-P209-004` received bounded definition, domains, alternatives, examples, rationale, and `restricted`; `D-P209-005` canonical wording/disposition unchanged. IDs, sequences, source pins, warnings, raw metadata, rights, fixed retrieval commands, `status: draft`, and `review_status: editorial-review-needed` preserved. A future schema/editorial split may separate architectural, operational, and automated-decision profiles.
- Decision and limits: `restricted` is preferred for `DECISION` over `allowed` because object, actor, evaluation, record, and criteria must be named; `prohibited`/`not-applicable` reject evidenced IT uses. `decontamination` remains unresolved because inspected authorities distinguish sanitization/incident response and provide no competent support for cloud-infrastructure use. No vocabulary approval, release, publication, canonicalization, or SFT readiness.
- Validation/commit: affected batch-012 check passed; the initial shorthand `--batch 012` invocation was rejected as an invalid path and was rerun with the canonical batch path. Adaptation, corpus, all-batch vocabulary check, document build/check, source doctor, diagnostics, and `git diff --check` passed; the first unit run exposed the expected stale count assertion; the expectation was updated and the rerun passed 118/118 tests. Offset-0 recomputation after the change: `2,196` total; `allowed 120`, `restricted 1,488`, `prohibited 407`, `not-applicable 148`, `needs-review 33`; next live record `D-P209-005` page 209. Commit hash is appended after final review.
- Next action: stop after slice 2/36; next run must begin with fresh offset-0 recomputation and may process only `D-P209-005` as the next live record, without starting slice 3 here.

### Policy classification slice 3/36 — `D-P209-005`

- Run/slice: user-authorized slice 3/36; batch `012`; physical PDF page `209`; POS `n` (`decontamination`).
- Old/new: `D-P209-005` changed `needs-review` → `restricted`.
- ASD evidence: Issue 9, revision `r0001`, exact entry `D-P209-005`, printed page `2-1-D3`, sequence `478`, authenticated PDF SHA-256 `d1f4ea9e7cd6e46b47aa9057209f99e78c0e9cfc4e27a5b07895b05c1a166431`. Exact retrieval and page retrieval passed. Visual inspection confirms row 5, wrapped headword `decontamination`, alternatives `REMOVE CONTAMINATION` and `CLEAN (v)`, and the preceding `REMOVE` fragment belongs to this row. The warning and mechanically extracted source status remain preserved.
- IT question and exclusions: can policy admit a bounded physical-IT maintenance sense for removal of contamination from a named component, surface, device, or connector under a documented procedure, without importing media sanitization, cloud deletion, malware remediation, or unrestricted cleaning? Yes, as restricted physical IT only.
- Sources actually inspected: Apple, “How to clean your Apple products,” `https://support.apple.com/en-us/103258` (accessed 2026-10-24), gives manufacturer procedures and safety limits for computers, displays, peripherals, and cables; limitation: Apple-specific, not a universal terminology authority. NIST SP 800-88 Rev. 2, `https://csrc.nist.gov/pubs/sp/800/88/r2/final` (published 2025-09, accessed 2026-10-24), defines media sanitization as making access to data on media infeasible; limitation: distinct security/data operation, not physical residue removal. AWS Well-Architected Security Pillar “Data protection,” `https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/data-protection.html` (accessed 2026-10-24), distinguishes cloud data classification and protection at rest/in transit; limitation: no `decontamination` term or physical cleaning authority. NIST SP 800-61 Rev. 3, `https://csrc.nist.gov/pubs/sp/800/61/r3/final` (published 2025-04, accessed 2026-10-24), does not support malware response as `decontamination`.
- Canonical changes: bounded definition, physical-IT domains, alternatives, examples, rationale, exclusions, and `restricted` disposition only. IDs, sequence, source pins, wrapped-headword warning, raw metadata, rights, fixed retrieval command, `status: draft`, and `review_status: editorial-review-needed` preserved. No generated Markdown was edited by hand.
- Decision and limits: `restricted` is preferred over `allowed` because object, procedure, and physical boundary must be named. `prohibited` is rejected because named hardware-cleaning procedures are evidenced; `not-applicable` is rejected because physical IT is in policy scope. Media sanitization, cloud deletion, and malware-remediation profiles are rejected as distinct or unsupported meanings. This remains a draft policy classification, not vocabulary approval, release, publication, canonicalization, or SFT readiness.
- Validation/commit: affected batch-012 vocabulary check, adaptation, corpus, all-batch vocabulary check, document build/check, 118 unit tests with `ResourceWarning` as errors, source doctor before and after evidence use, project diagnostics with no errors/warnings, `git diff --check`, exact ASD entry/page retrieval, and offset-0 recomputation all passed. Automatic commit: `85fd3be` (`Classify page 209 decontamination`), explicit paths `docs/IT-STE-draft.md`, `docs/it-ste-draft-handoff.md`, `docs/it-ste-research/W1-D-P209.md`, `docs/it-ste-research/it-sense-classification-log.md`, `docs/it-ste-research/needs-review-38.md`, `standards/it-ste/vocabulary-reviews/asd-ste100/issue-9/r0001/batch-012.json`, and `tests/test_it_ste_vocabulary.py`.
- Next action: stop after slice 3/36; after fresh offset-0 recomputation, set the next live slice only in the handoff. Do not start slice 4/36.

### New-policy classification slice 5/36 — `D-P273-004` / `D-P273-005`

- Run/slice: user-authorized new-policy slice 5/36; batch `024`; physical PDF page `273`; POS `adj` (`HYDRAULIC`) and `adv` (`HYDRAULICALLY`).
- Old/new: both records changed `needs-review` → `restricted`.
- ASD evidence: Issue 9, revision `r0001`, exact entries `D-P273-004` / `D-P273-005`, printed page `2-1-H7`, sequences `959–960`, authenticated PDF SHA-256 `d1f4ea9e7cd6e46b47aa9057209f99e78c0e9cfc4e27a5b07895b05c1a166431`; exact retrieval and page retrieval passed. Visual findings confirm separate hydraulic adjective and adverb rows, with `HYDRAULICALLY` wrapped across two lines; mechanical overlap and wrapped-headword warnings remain preserved.
- IT question and exclusions: with physical IT explicitly in policy, is there a bounded hydraulic sense for a named OT/industrial-control component? Yes, but only for the physical hydraulic component and its documented OT operation; exclude generic machinery, cloud routing, API behavior, software expansion, and safety authorization.
- Sources actually inspected: NIST SP 800-82 Rev. 3 (final September 2023), `https://csrc.nist.gov/pubs/sp/800/82/r3/final`, defines OT as programmable systems/devices interacting with the physical environment; limitation: OT scope authority, not hydraulic terminology or safety procedure. CISA, “Industrial Control Systems,” `https://www.cisa.gov/topics/industrial-control-systems`, accessed 2026-10-24, describes ICS/OT systems and devices interacting with the physical environment; limitation: scope/guidance page, not a lexical authority. Bosch Rexroth, “Connected Hydraulics,” `https://www.boschrexroth.com/en/us/connected-hydraulics/`, accessed 2026-10-24, documents software, digital twins, sensors, predictive analytics, and service tools around hydraulics; limitation: product-domain manufacturer evidence. CCOHS hydraulic-energy guidance was also inspected for the physical mechanism and safety boundary, but not used as IT-scope authority.
- Canonical changes: bounded definitions, domain labels, alternatives, examples, rationales, and `restricted` dispositions only. IDs, sequences, source pins, warnings, raw metadata, rights, fixed retrieval commands, `status: draft`, and `review_status: editorial-review-needed` preserved. Generated Markdown was rebuilt, not edited by hand.
- Decision and limits: `restricted` is preferred over `allowed` because the named OT component and physical boundary are required; `not-applicable` is rejected because policy includes physical IT/OT; `prohibited` is rejected because the evidenced use is reviewable; retaining `needs-review` is no longer necessary under the new policy. No vocabulary approval, release, publication, canonicalization, or SFT readiness.
- Validation/commit: full required validation, source doctor, exact ASD retrieval/page review, diagnostics, diff check, queue recomputation, and final worktree/index review are recorded in the handoff and completion report.
- Next action: stop after slice 5/36; recompute offset 0 in the next run and inspect only the next live slice, expected `D-P280-003` / `D-P280-004`. Do not start slice 6/36.

### New-policy classification slice 6/36 — `D-P280-003` / `D-P280-004`

- Run/slice: user-authorized new-policy slice 6/36; batch `025`; physical PDF page `280`; POS `adv` (`INBOARD`) and `prep` (`INBOARD OF`).
- Old/new: both records changed `needs-review` → `restricted`.
- ASD evidence: Issue 9, revision `r0001`, exact entries `D-P280-003` / `D-P280-004`, printed page `2-1-I6`, sequences `994–995`, authenticated PDF SHA-256 `d1f4ea9e7cd6e46b47aa9057209f99e78c0e9cfc4e27a5b07895b05c1a166431`; exact retrieval and page retrieval passed. Visual findings confirm the second `INBOARD` row is the adverb with its own landing-gear example, and `INBOARD OF` is a separate wrapped-headword row with its own flap-track example; mechanical ambiguity and wrapped-headword warning remain preserved.
- IT question and exclusions: can all-IT policy admit bounded inboard senses for a named physical IT object or an explicitly axis-defined technical diagram? Yes, but not generic network topology, firewall/database placement, cloud/software analogy, or unqualified UI prose.
- Sources actually inspected: RFC 9110 (IETF Standards Track, June 2022, `https://www.rfc-editor.org/rfc/rfc9110.html`, §§3.7, 7.3, 7.6) for inbound/outbound and upstream/downstream route relations; AWS security-groups documentation (`https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html`) for named resources, inbound sources, outbound destinations, and firewall rules; W3C SVG 2 coordinate systems (`https://www.w3.org/TR/SVG2/coords.html`, §§8.1, 8.4, 8.6, 8.8) for explicit axes/viewports/reference frames; and W3C CSS Positioned Layout Level 3 (`https://www.w3.org/TR/css-position-3/`) for containing blocks/reference rectangles and physical/flow-relative positioning. RFC/AWS do not support generic `inboard`; SVG/CSS support only explicit diagram/reference-frame wording. CSS is a Working Draft, not a stable Recommendation. NASA aircraft-axis retrieval returned 404 and an FAA PDF was not substantively inspected; neither is evidence.
- Canonical changes: bounded definitions, physical/UI-documentation domains, alternatives, examples, rationales, and `restricted` dispositions only. IDs, sequences, source pins, warnings, raw metadata, rights, fixed retrieval commands, `status: draft`, `review_status: editorial-review-needed`, and visual evidence were preserved. Generated Markdown was rebuilt, not edited by hand.
- Decision and limits: `restricted` is preferred over `allowed` because a named object and explicit longitudinal/diagram axis are required; `prohibited`/`not-applicable` reject evidenced physical IT and technical-diagram uses. The earlier blocked decision is superseded by this bounded evidence-based draft classification. No vocabulary approval, release, publication, canonicalization, or SFT readiness.
- Validation/commit: full required validation, authenticated source doctor, exact ASD retrieval/page review, diagnostics, diff check, queue/count recomputation, and final worktree/index review are recorded in the handoff and completion report.
- Next action: stop after slice 7/36; in a future separately authorized run recompute offset 0 and begin only `D-P351-001` (batch 039, physical PDF page 351). Do not start slice 8 here.

### New-policy classification slice 7/36 — `D-P349-003`

- Run/slice: user-authorized new-policy slice 7/36; batch `038`; physical PDF page `349`; POS `adj` (`RADIOACTIVE`). The exact selected ID is `D-P349-003`; `D-P336-009` was excluded because its canonical disposition is already `prohibited`.
- Old/new: `D-P349-003` remains `needs-review` → `needs-review`; no canonical field changed.
- ASD evidence: Issue 9, revision `r0001`, exact entry `D-P349-003`, sequence `1514`, printed page `2-1-R1`, authenticated PDF SHA-256 `d1f4ea9e7cd6e46b47aa9057209f99e78c0e9cfc4e27a5b07895b05c1a166431`; doctor, exact retrieval, and page retrieval passed. Fresh visual inspection of the ignored 150-dpi render confirms `RADIOACTIVE (adj)` is a distinct wrapped-headword row between `RADIALLY (adv)` and `raise (v)`; its meaning, contamination example, and row boundaries are separate. The historical wrapped-headword warning remains preserved.
- IT question and exclusions: can the physical radioactivity sense be extended to a bounded cloud-facility equipment context? Exclude unsupported software/log-file hazard metaphors and any inference that a cloud smoke sensor is radioactive.
- Sources actually inspected: U.S. EPA RadTown, “Americium in Ionization Smoke Detectors,” updated 2026-04-08, `https://www.epa.gov/radtown/americium-ionization-smoke-detectors`; and Amazon Web Services, “Data Center Controls,” current provider description, `https://aws.amazon.com/compliance/data-center/controls/`. EPA documents americium-241 in some household ionization smoke detectors and handling limits; AWS documents smoke sensors in networking, mechanical, and infrastructure spaces plus asset maintenance. EPA is household/radiation-education scope; AWS is provider self-description and does not identify sensor construction or supply an independently audited inventory.
- Canonical changes: none. The record remains `status: draft`, `review_status: editorial-review-needed`, with source pins, wrapped-headword warning, raw metadata, rights, fixed retrieval command, provisional wording, and visual evidence preserved. No generated Markdown or test expectation changed.
- Decision and limits: retain `needs-review`; the two sources establish separate facts but not a radioactive cloud-facility item or project inclusion boundary. Reject immediate `restricted`/`allowed` because the equipment-specific link is missing; reject `not-applicable` because a physical facility application remains plausible; do not force `prohibited` merely to clear the queue. No vocabulary approval, release, publication, canonicalization, or SFT readiness.
- Validation/commit: affected batch-038 check first; adaptation; corpus; all-batch vocabulary check; document build/check; 118 unit tests with `ResourceWarning` as errors; authenticated doctor before and after validation; diagnostics; `git diff --check`; exact ASD retrieval/page review; offset-0 queue/count recomputation; and final worktree/index review are recorded in the handoff and completion report.
- Next action: stop after slice 7/36; next authorized run must recompute offset 0 and inspect only `D-P351-001` (batch `039`, physical PDF page `351`); do not start slice 8 here.

### New-policy classification slice 8/36 — `D-P351-001`

- Run/slice: user-authorized new-policy slice 8/36; batch `039`; physical PDF page `351`; POS `adj` (`real`). Fresh offset-0 canonical recomputation selected only this record after slice 7; slice 9 was not started.
- Old/new: `D-P351-001` remains `needs-review` → `needs-review`; no canonical field or generated output changed.
- ASD evidence: Issue 9, revision `r0001`, exact locator `entry D-P351-001`, sequence `1530`, printed page `2-1-R3`, authenticated PDF SHA-256 `d1f4ea9e7cd6e46b47aa9057209f99e78c0e9cfc4e27a5b07895b05c1a166431`. Exact entry and bounded page retrieval passed. Fresh visual inspection confirms `real (adj)` as a distinct first row, `AGREE (v)` in the alternatives column, the gauge/fuel agreement example, and the boundary before `REAR`; the row gives no tolerance or general IT definition.
- IT question and exclusions: can `real` be classified as a named measurement/property sense or split into a bounded IT sense without conflating measured, indicated, current, true, verified, genuine, or non-simulated state? The selected record does not name the IT object, contrast, reference, comparison method, time/reset window, or tolerance; mathematical real numbers, authenticity, correctness, verification, and product-specific meanings remain excluded.
- External evidence actually inspected: JCGM VIM3 2.10 (`https://jcgm.bipm.org/vim/en/2.10.html`, accessed 2026-10-24) distinguishes measured quantity value from an indication and relates it to a measurement result; JCGM VIM3 2.11 (`https://jcgm.bipm.org/vim/en/2.11.html`, accessed 2026-10-24) distinguishes true quantity value and its practical limits; Prometheus Authors, “Metric types” (`https://prometheus.io/docs/concepts/metric_types/`, accessed 2026-10-24) distinguishes resettable cumulative counters from gauges that can rise or fall. These are competent primary/expert sources for metrology and observability semantics, but none defines ASD `real` or selects the project's IT sense. RFC 9110 evidence remains prior related research, not freshly fetched in this slice.
- Decision and limits: retain `needs-review`; the evidence supports splitting or replacing `real` only after an accountable IT object and comparison contract are named. Do not substitute `actual`, `measured`, `indicated`, `current`, `true`, `verified`, or `non-simulated`, and do not force `restricted`, `allowed`, `prohibited`, or `not-applicable`. Canonical record remains `status: draft` / `review_status: editorial-review-needed`; this is not vocabulary approval, release, publication, canonicalization, or SFT readiness. Detailed evidence is in [W1-D-P351-001](W1-D-P351-001.md).
- Validation/commit: affected batch-039 check first; adaptation; corpus; all-batch vocabulary check; document build/check; 118 unit tests with `ResourceWarning` as errors; authenticated doctor before and after validation; diagnostics; `git diff --check`; exact ASD retrieval/page review; and offset-0 queue/count recomputation. Automatic commit is recorded after final review.
- Next action: stop after slice 8/36; next authorized run must recompute offset 0 and inspect only `D-P365-011` (batch `042`, physical PDF page `365`); do not start slice 9 here.

### New-policy classification slice 9/36 — `D-P365-011`

- Run/slice: user-authorized new-policy slice 9/36; batch `042`; physical PDF page `365`; POS `adj` (`running`). Fresh offset-0 canonical recomputation selected only this record after slice 8; slice 10 was not started.
- Old/new: `D-P365-011` changed from `needs-review` to `restricted`. It remains `status: draft` / `review_status: editorial-review-needed`; no vocabulary approval, release, publication, canonicalization, or SFT readiness is implied.
- ASD evidence: Issue 9, revision `r0001`, exact locator `entry D-P365-011`, sequence `1670`, printed page `2-1-R17`, authenticated PDF SHA-256 `d1f4ea9e7cd6e46b47aa9057209f99e78c0e9fc4e27a5b07895b05c1a166431`; doctor and exact retrieval passed. Visual inspection of the authenticated page-365 render confirms `running (adj)` row 11 is separated from `run (v)`, that `FLUSH` and the water-cleaning examples belong to the adjective, and that `OPERATE` belongs to the separate verb row. The source remains mechanically extracted and unreviewed.
- IT question and exclusions: can the flowing-water source sense support useful, safe IT profiles across physical cleaning, OT, and software? Excluded are washing assembled or energized electronics, treating all OT equipment as washable, and equating a software/API `Running` state with operating correctly, health, readiness, availability, or safety.
- External evidence actually inspected: Apple, “How to clean your Apple products,” official manufacturer guidance, `https://support.apple.com/en-us/103258`, accessed 2026-10-24; it establishes product-specific cleaning and moisture boundaries but not flowing water for electronics or universal IT procedures. NIST SP 800-82 Rev. 3, `https://csrc.nist.gov/pubs/sp/800/82/r3/final`, September 2023; it establishes OT as physical-environment control/monitoring systems but does not authorize cleaning. Kubernetes Authors, “Pod Lifecycle,” `https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/`, accessed 2026-10-24; it distinguishes Pod phase Running from container state/readiness and warns against overinterpretation. Kubernetes Authors, “Configure Liveness, Readiness and Startup Probes,” `https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/`, accessed 2026-10-24; it establishes that running and readiness/liveness are distinct, but is connected documentation rather than independent corroboration.
- Decision and canonical changes: the restricted definition now covers continuously flowing water only on a named detached/removable washable component under an applicable manufacturer procedure; the corresponding named OT asset/component procedure; or a named software platform/API state documented as `Running`. It rejects `allowed` as unsafe without an object/procedure/platform contract, rejects `prohibited` and `not-applicable` because all three bounded uses are relevant, and rejects `operating`, `healthy`, `ready`, `available`, and `safe` as unbounded alternatives. Updated only the selected record's disposition, definition, domains, rationale, alternatives, examples, and review-required text; preserved IDs, sequence, source pins, fixed locator, warnings/ambiguity, raw metadata, rights, and draft statuses.
- Validation/commit: affected batch-042 check first; adaptation; corpus; all-batch vocabulary check; document build/check; 118 unit tests with `ResourceWarning` as errors; authenticated source doctor before and after validation; diagnostics with no errors or warnings; `git diff --check`; exact ASD entry/page review; and offset-0 queue/count recomputation passed for this run. The automatic commit includes only the reviewed slice files.
- Next action: stop after slice 9/36; after fresh offset-0 recomputation, the next authorized run must inspect only `D-P349-003` (batch `038`, physical PDF page `349`); do not start slice 10 here.
