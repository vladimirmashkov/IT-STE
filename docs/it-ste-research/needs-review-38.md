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

No remediation result has been recorded yet. Each subsequent change must add an entry here or in the linked per-slice research note with:

- canonical ID and previous/new disposition;
- ASD Issue/revision, physical PDF page, exact source locator and PDF hash;
- external sources actually inspected and their limitations;
- fact versus editorial inference;
- changed wording/examples/rationale;
- validation results and commit hash.

This register does not authorize vocabulary approval, release, publication, or SFT readiness.
