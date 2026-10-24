# IT-STE needs-review baseline — 38 records

State: baseline inventory

This file freezes the canonical `needs-review` set before the next remediation phase. It is a problem register, not an approval list. Every record below currently has `status: draft`, `review_status: editorial-review-needed`, and `it_disposition: needs-review`.

The planned remediation is evidence-based: inspect the exact ASD source entry and authenticated PDF page, research the stated IT sense in competent primary or expert sources, compare alternatives, and record any disposition change with rationale. A record must not be moved only to eliminate the count; insufficient evidence remains explicitly blocked.

Canonical source: `standards/it-ste/vocabulary-reviews/asd-ste100/issue-9/r0001/batch-*.json`.

| Batch | ID | Headword | POS | PDF page | Baseline draft IT wording |
|---|---|---|---|---:|---|
| 011 | `D-P201-004` | `contaminated` | adj | 201 | Affected by an unwanted physical substance or material; limited to a physical component or medium, provisionally. |
| 011 | `D-P201-005` | `CONTAMINATION` | n | 201 | An unwanted physical change to a material caused by a chemical or physical agent or another material; limited to physical infrastructure or media, provisionally. |
| 012 | `D-P206-001` | `critical` | adj | 206 | Very important to a stated outcome, provisionally; no severity taxonomy is approved here. |
| 012 | `D-P206-003` | `curvature` | n | 206 | The amount or form of bending in a stated geometric line or surface, provisionally. |
| 012 | `D-P209-004` | `DECISION` | n | 209 | A chosen outcome reached through an identified evaluation, provisionally. |
| 012 | `D-P209-005` | `decontamination` | n | 209 | Removal of unwanted physical substances under an identified maintenance procedure, provisionally. |
| 016 | `D-P230-003` | `ELECTRICAL` | adj | 230 | Concerning electricity in physical hardware or its supply. |
| 016 | `D-P230-004` | `ELECTRICALLY` | adv | 230 | By means of electrical power or an electrical connection. |
| 024 | `D-P273-004` | `HYDRAULIC` | adj | 273 | Using pressurized liquid to transmit force in physical equipment. |
| 024 | `D-P273-005` | `HYDRAULICALLY` | adv | 273 | By power transmitted through pressurized liquid. |
| 025 | `D-P280-003` | `INBOARD` | adv | 280 | Toward a specified physical longitudinal centerline. |
| 025 | `D-P280-004` | `INBOARD OF` | prep | 280 | Nearer a stated longitudinal centerline than a named reference object. |
| 038 | `D-P349-003` | `RADIOACTIVE` | adj | 349 | Having a physical property associated with radioactive material; no general software sense is proposed. |
| 039 | `D-P351-001` | `real` | adj | 351 | Provisionally, corresponding to an actual observed state rather than an assumption or simulation; source sense is unresolved. |
| 042 | `D-P365-011` | `running` | adj | 365 | Flowing continuously, provisionally describing water used in a physical cleaning procedure. |
| 043 | `D-P368-010` | `scored` | adj | 368 | Provisionally, having a physical groove caused by damage to an equipment surface. |
| 044 | `D-P374-005` | `serviceability` | n | 374 | Provisionally, the condition of meeting a hardware component's operating requirements. |
| 044 | `D-P374-006` | `SERVICEABLE` | adj | 374 | Fit for a specified IT hardware operation under stated acceptance criteria. |
| 045 | `D-P379-002` | `skid` | v | 379 | Provisionally, slide unintentionally across a physical supporting surface. |
| 047 | `D-P391-003` | `strain` | v | 391 | Provisionally, pass a physical liquid through a filter to remove particles. |
| 047 | `D-P391-005` | `stress` | v | 391 | Provisionally, apply a specified mechanical force to a physical IT component. |
| 049 | `D-P397-005` | `SYMBOL` | n | 397 | A visible mark that denotes a specified operation, object, or state in an IT representation. |
| 049 | `D-P397-006` | `SYMMETRICAL` | adj | 397 | Having matching shapes or positions on opposite sides of a specified axis in a diagram. |
| 049 | `D-P397-007` | `SYMMETRICALLY` | adv | 397 | In a way that preserves matching positions about a stated layout axis. |
| 049 | `D-P398-001` | `SYNCHRONIZED` | adj | 398 | In agreement for specified data or timing within a stated tolerance or checkpoint. |
| 052 | `D-P413-005` | `uncoil` | v | 413 | Straighten a coiled physical cable within its permitted bend and torsion limits. |
| 052 | `D-P413-006` | `uncontaminated` | adj | 413 | Free of specified unwanted physical substances under a stated inspection criterion. |
| 052 | `D-P413-009` | `undamaged` | adj | 413 | Without observed physical damage under a named inspection scope. |
| 052 | `D-P413-010` | `UNDEMANDED` | adj | 413 | Occurring without an identified initiating request or apparent cause, pending source clarification. |
| 052 | `D-P415-004` | `unintentional` | adj | 415 | Not intended by the responsible actor, where evidence supports the intent assessment. |
| 052 | `D-P415-005` | `unintentionally` | adv | 415 | Without intending the resulting action, with the actor and evidence identified. |
| 052 | `D-P416-006` | `unobstructed` | adj | 416 | Free of a specified physical blockage; no claim of unrestricted network access is proposed. |
| 052 | `D-P417-006` | `UNSATISFAC- TORILY` | adv | 417 | In a manner that does not meet a stated requirement or acceptance criterion. |
| 052 | `D-P417-007` | `UNSATISFAC- TORY` | adj | 417 | Not meeting a stated requirement or acceptance criterion. |
| 052 | `D-P417-008` | `unscrew` | v | 417 | Release a threaded fastener by turning it, usually to loosen or remove it. |
| 052 | `D-P417-009` | `UNSERVICEABLE` | adj | 417 | Not fit for its intended equipment function. |
| 053 | `D-P419-006` | `UPSTREAM` | adv | 419 | Toward the source of a specified data flow or dependency path. |
| 053 | `D-P419-007` | `UPSTREAM OF` | prep | 419 | Located before a named component along an explicitly defined processing flow. |

## Remediation result log

### Iteration 29 — batch012 / physical PDF page 209

- `D-P209-004` — old disposition: `needs-review`; new disposition: `needs-review`.
  ASD evidence: Issue 9, revision `r0001`, physical PDF page 209 / printed page `2-1-D3`, exact locator `entry D-P209-004`, authenticated PDF SHA-256 `d1f4ea9e7cd6e46b47aa9057209f99e78c0e9cfc4e27a5b07895b05c1a166431`; exact retrieval reports `DECISION (n)`, definition `The result after you think about a problem`, and no extraction warnings. Fresh visual review confirms row 4 and that `REMOVE` starts the following `decontamination` row. The source-layout blocker is resolved; mechanical metadata and historical ambiguity are preserved.
  External evidence actually inspected: ADR GitHub organization, “Architectural Decision Records,” `https://adr.github.io/` (accessed 2026-10-24), defines an architectural decision as a justified design choice and a decision record/log as its rationale and trade-offs; NIST AI RMF, `https://www.nist.gov/itl/ai-risk-management-framework` (accessed 2026-10-24), describes voluntary AI risk management across design, development, use, and evaluation. These support adjacent governance contexts, but neither establishes the proposed generic AI/logs sense or the failover example. Fact versus inference: ASD row/layout and external definitions are facts; retaining the provisional wording and requiring accountable scope review are editorial inferences. No wording, examples, rationale, or canonical field changed.

- `D-P209-005` — old disposition: `needs-review`; new disposition: `needs-review`.
  ASD evidence: Issue 9, revision `r0001`, physical PDF page 209 / printed page `2-1-D3`, exact locator `entry D-P209-005`, authenticated PDF SHA-256 `d1f4ea9e7cd6e46b47aa9057209f99e78c0e9cfc4e27a5b07895b05c1a166431`; exact retrieval reports `decontamination (n)` with `REMOVE CONTAMINATION` and `CLEAN (v)` alternatives and the preserved `wrapped-headword` warning. Fresh visual review confirms row 5, the wrapped headword, and both alternatives. The source-layout blocker is resolved; the physical source sense remains bounded but the proposed cloud-infrastructure scope is not substantiated.
  External evidence actually inspected: NIST SP 800-88 Rev. 1, `https://www.nist.gov/publications/guidelines-media-sanitization` (accessed 2026-10-24), defines media sanitization as making access to target data infeasible for a given effort; NIST SP 800-61 Rev. 2, `https://csrc.nist.gov/pubs/sp/800/61/r2/final` (accessed 2026-10-24), defines incident-response guidance for analyzing incident data and choosing responses, and is marked withdrawn/superseded by Rev. 3. These are competent adjacent IT/security sources, but neither calls cloud operations or malware removal `decontamination`; the NIST decontamination glossary URL was also inspected and returned 404. Fact versus inference: ASD physical row/layout and NIST scopes are facts; retaining the narrow provisional physical wording and requiring a directly applicable source or accountable owner are editorial inferences. No wording, examples, rationale, or canonical field changed.

Validation for this slice: batch-012 check; adaptation; corpus; all-batch vocabulary; document build/check; unit tests with `ResourceWarning` treated as errors; authenticated source doctor; diagnostics; `git diff --check`; fresh PDF page-209 rendering review; and canonical queue/count recomputation. Canonical all-batch final counts are 2,196 records / 55 batches: 120 allowed, 1,485 restricted, 407 prohibited, 148 not-applicable, 36 needs-review (batch-012 local check reports 40 candidates across its full batch-local scope). Both records remain `draft` / `editorial-review-needed`; this is not vocabulary approval.

### Iteration 28 — batch012 / physical PDF page 206

- `D-P206-001` — old disposition: `needs-review`; new disposition: `needs-review`.
  ASD evidence: Issue 9, revision `r0001`, physical PDF page 206 / printed page `2-1-C24`, exact locator `entry D-P206-001`, authenticated PDF SHA-256 `d1f4ea9e7cd6e46b47aa9057209f99e78c0e9cfc4e27a5b07895b05c1a166431`; exact retrieval reports `critical (adj)` with `VERY IMPORTANT` and `CAREFUL (adj)` alternatives and no extraction warnings. Visual review of the authenticated page confirmed one row with separate alternatives and examples; mechanical extraction ambiguity remains historical evidence.
  External evidence actually inspected: FIRST CVSS v4.0 specification (`https://www.first.org/cvss/v4.0/specification-document`, accessed 2026-10-24) defines `Critical` only as an optional CVSS qualitative severity rating for scores 9.0–10.0; this supports a distinct named policy taxonomy but not the ASD intent or ordinary importance. Fact versus inference: source row/layout and CVSS scope are facts; retaining the provisional ordinary-importance wording without a severity taxonomy and requiring accountable scope review are editorial inferences. No wording, examples, rationale, or canonical field changed.

- `D-P206-003` — old disposition: `needs-review`; new disposition: `needs-review`.
  ASD evidence: Issue 9, revision `r0001`, physical PDF page 206 / printed page `2-1-C24`, exact locator `entry D-P206-003`, authenticated PDF SHA-256 `d1f4ea9e7cd6e46b47aa9057209f99e78c0e9cfc4e27a5b07895b05c1a166431`; exact retrieval reports `curvature (n)` with separate `BEND (n)`, `CURVE (n)`, and `RADIUS (TN)` alternatives and no extraction warnings. Visual review confirmed row 3 and its separate examples; mechanical extraction ambiguity remains historical evidence.
  External evidence actually inspected: WHATWG HTML Living Standard Canvas 2D (`https://html.spec.whatwg.org/multipage/canvas.html#dom-context-2d-arc-dev`, accessed 2026-10-24) defines curves, arcs, and radius parameters; W3C SVG 2 Paths (`https://www.w3.org/TR/SVG2/paths.html`, accessed 2026-10-24), sections 9.1 and 9.3.6–9.3.8, describes path geometry and radii. These primary sources corroborate related geometry but do not establish `curvature` as the controlled IT-STE noun or resolve physical bend-radius scope. Fact versus inference: source row/layout and external geometry facts are facts; retaining the narrow provisional geometric wording and requiring accountable scope review are editorial inferences. No wording, examples, rationale, or canonical field changed.

  Validation: affected batch-012 check; adaptation; corpus; all-batch vocabulary; document build/check; 118 unit tests with `ResourceWarning` treated as errors; authenticated source doctor before and after evidence use; diagnostics (no errors/warnings); `git diff --check`; and canonical queue/count recomputation passed. Fresh counts remain 2,196 records / 55 batches: 120 allowed, 1,485 restricted, 407 prohibited, 148 not-applicable, 36 needs-review. No canonical, generated, or test file changed; PDF and rendering remain ignored.

### Iteration 27 — batch011 / physical PDF page 201

- `D-P201-004` — old disposition: `needs-review`; new disposition: `restricted`.
  ASD evidence: Issue 9, revision `r0001`, physical PDF page 201 / printed page `2-1-C19`, exact locator `entry D-P201-004`, authenticated PDF SHA-256 `d1f4ea9e7cd6e46b47aa9057209f99e78c0e9cfc4e27a5b07895b05c1a166431`; visual review confirmed the separate `contaminated (adj)` row, its `DIRTY (adj)` / `CONTAMINATION (n)` alternatives, and the physical connector examples. The extracted cross-row fragment remains a mechanical boundary artifact.
  External evidence actually inspected: ISO 14644-1:2015 official abstract (`https://www.iso.org/standard/53394.html`, accessed 2026-10-24) supports a measurable physical-cleanliness/airborne-particle context but is limited to cleanroom air; NIST CNSSI 4009-2022 contamination glossary (`https://csrc.nist.gov/glossary/term/contamination`, accessed 2026-10-24) supports a distinct unauthorized-information-transfer security sense, not this physical sense; AWS CloudFormation drift (`https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html`, accessed 2026-10-24) and NIST data poisoning (`https://csrc.nist.gov/glossary/term/data_poisoning`, accessed 2026-10-24) support excluding configuration and ML meanings. Fact versus inference: ASD row/layout and source terminology are facts; restricting the draft to a named physical component/medium and inspection or maintenance observation is editorial inference. Changed wording/rationale: “Affected by an unwanted physical substance or material on a named component or medium, as established by an inspection or maintenance observation”; generic database/malware/configuration/ML uses remain excluded.

- `D-P201-005` — old disposition: `needs-review`; new disposition: `restricted`.
  ASD evidence: Issue 9, revision `r0001`, physical PDF page 201 / printed page `2-1-C19`, exact locator `entry D-P201-005`, authenticated PDF SHA-256 `d1f4ea9e7cd6e46b47aa9057209f99e78c0e9cfc4e27a5b07895b05c1a166431`; visual review confirmed the distinct wrapped `CONTAMINATION (n)` row and its physical definition/example. The source interpretation remains mechanically extracted and unreviewed.
  External evidence, limits, fact/inference, and decision scope are the same bounded sources and limits recorded for `D-P201-004`; `restricted` is supported because the physical sense is relevant but the sources do not support unrestricted cloud-IT portability. Changed wording/rationale: “An unwanted physical change to a named material caused by a chemical or physical agent or another material, as recorded by an inspection or maintenance observation”; generic data, security-incident, configuration, malware, and ML uses remain excluded.

  Validation: affected batch-011 check; adaptation; corpus; all-batch vocabulary; document build/check; 118 unit tests with `ResourceWarning` treated as errors; authenticated source doctor; diagnostics (no errors/warnings); `git diff --check`; and canonical queue/count recomputation passed. Final commit hash is recorded in the completion report after commit.

Each subsequent change must add an entry here or in the linked per-slice research note with:

- canonical ID and previous/new disposition;
- ASD Issue/revision, physical PDF page, exact source locator and PDF hash;
- external sources actually inspected and their limitations;
- fact versus editorial inference;
- changed wording/examples/rationale;
- validation results and commit hash.

This register does not authorize vocabulary approval, release, publication, or SFT readiness.
