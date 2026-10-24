# IT-STE evidence matrix for the remaining 11 records

State: completed bounded research run; canonical dispositions intentionally unchanged pending owner/schema decisions
Skill: `.agents/skills/it-ste-11-domain-evidence/SKILL.md`
Policy: `docs/it-ste-it-sense-policy.md`
Domain inventory: `docs/it-ste-it-domain-matrix.md`
Access date: 2026-10-24

## Scope and method

This register screens every target record against every domain in the project matrix. `A` means that the domain has a plausible, source-supported candidate sense; `U` means that a technically plausible sense remains unresolved because the source, object boundary, owner policy, or schema is insufficient; `N` means that the ASD sense has no justified use in that domain under the current policy. `A` does not change a canonical disposition by itself.

The study used authenticated ASD Issue 9 / revision `r0001` entry and page evidence, PDF SHA-256 `d1f4ea9e7cd6e46b47aa9057209f99e78c0e9cfc4e27a5b07895b05c1a166431`, the existing per-record research register, and the authoritative sources listed below. Source facts and editorial inference remain separate. No Reddit or Stack Overflow source was used.

### Domain columns

`GOV` governance/service management; `SW` software/applications; `LANG` programming languages/formal methods; `DATA` data/information; `NET` networking/protocols; `DIST` distributed systems/APIs; `CLOUD` cloud/infrastructure; `HW` hardware/datacenter/physical IT; `OT` operational technology; `SEC` cybersecurity/privacy; `CRYPTO` identity/access/cryptography; `OBS` monitoring/observability; `REL` reliability/recovery; `DEV` DevOps/configuration; `TEST` testing/quality; `PERF` performance/capacity; `UI` UI/accessibility/visual communication; `DOC` technical communication/support; `MAINT` maintenance/repair; `AI` AI/ML/data science; `RISK` safety/compliance/risk; `TIME` time/synchronization; `PHYS` physical geometry/measurement.

## Full domain screening

| ID / word | GOV | SW | LANG | DATA | NET | DIST | CLOUD | HW | OT | SEC | CRYPTO | OBS | REL | DEV | TEST | PERF | UI | DOC | MAINT | AI | RISK | TIME | PHYS |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `D-P349-003` RADIOACTIVE | N | N | N | N | N | N | U | U | U | N | N | N | U | N | N | N | N | U | U | U | U | N | U |
| `D-P351-001` real | U | U | N | U | N | U | U | U | N | U | N | U | U | U | U | N | N | U | U | N | U | U | N |
| `D-P368-010` scored | N | U | N | U | N | U | U | U | N | N | N | U | U | U | A | U | N | U | N | A | U | N | N |
| `D-P391-003` strain | N | N | N | N | N | N | N | U | U | N | N | N | N | N | U | N | N | U | U | N | U | N | U |
| `D-P391-005` stress | U | U | N | U | N | U | U | U | U | N | N | U | U | U | A | A | U | U | U | U | U | N | U |
| `D-P397-005` SYMBOL | U | U | U | U | U | U | U | N | N | U | U | U | N | U | U | N | A | A | N | U | N | N | N |
| `D-P397-006` SYMMETRICAL | N | U | U | U | N | U | U | U | N | N | U | N | N | U | U | N | A | U | N | N | N | N | U |
| `D-P397-007` SYMMETRICALLY | N | U | U | U | N | U | U | U | N | N | U | N | N | U | U | N | A | U | N | N | N | N | U |
| `D-P416-006` unobstructed | N | N | N | N | U | U | U | U | U | N | N | N | U | U | U | N | U | U | U | N | U | N | U |
| `D-P419-006` UPSTREAM | U | U | N | U | A | A | U | N | N | N | N | U | U | A | U | U | N | U | N | N | N | N | N |
| `D-P419-007` UPSTREAM OF | U | U | N | U | A | A | U | N | N | N | N | U | U | A | U | U | N | U | N | N | N | N | N |

## Record-level evidence and decisions

### `D-P349-003` — RADIOACTIVE

- Candidate domains: `HW`, `MAINT`, `RISK`, `OT`, facility `CLOUD`; all remain `U`, not `A`, because the inspected EPA source confirms americium-241 in some ionization smoke detectors, while AWS confirms data-center smoke detection and maintenance but does not identify radioactive equipment. The NRC page was inaccessible (HTTP 403) and was not evidence.
- Excluded domains: software, data, protocol, security, cryptography, UI, and generic service-management metaphors. `RADIOACTIVE` is not a synonym for dangerous, malicious, contaminated, or high-risk.
- Aggregate decision: `needs-review` → `needs-review`. Missing decision: whether radiological facility equipment belongs in IT-STE and which competent equipment/safety source identifies a qualifying IT object.

### `D-P351-001` — real

- Candidate domains: `DATA`, `OBS`, `SW`, `HW`, `REL`, `DEV`, `TIME`, `GOV`, `DIST`, `CLOUD`, `SEC`, `TEST`, `MAINT`; all remain `U` because measured, indicated, current, verified, production, and non-simulated contrasts are not interchangeable. VIM distinguishes measured quantity values and indications; Prometheus defines metric types; RFC 9110 distinguishes representations and validators.
- Excluded domains: `LANG` mathematical-real usage and unqualified claims that observed means true, current means verified, or cached means unreal.
- Aggregate decision: `needs-review` → `needs-review`; likely `split proposal`. Missing decision: select one controlled contrast and define time window, tolerance, reset, or verification method.

### `D-P368-010` — scored

- Applicable evidence: `AI` and `TEST` have `A` candidate senses because scikit-learn documents scoring functions/metrics and NIST AI RMF supports contextual evaluation; `HW`, `DATA`, `DIST`, `CLOUD`, `OBS`, `REL`, `DEV`, and `SEC` remain `U` where a named scoring function or physical inspection criterion would be required. NSK supports the physical bearing-damage sense but not IT equipment scope.
- Excluded domains: generic server rating, score as truth/correctness/readiness, and designed grooves treated as damage.
- Aggregate decision: `needs-review` → `needs-review`; `split proposal` is required for physical damage versus numerical/model/test scoring.

### `D-P391-003` — strain

- Candidate domains: `HW`, `MAINT`, `OT`, `PHYS`, and `TEST` remain `U`: the ASD row itself has distinct filtration and bellows-deformation references, but no single IT sense can safely combine them. Google Cloud performance guidance does not establish mechanical `strain` as software terminology.
- Excluded domains: generic log/data filtering, software-load metaphor, and unbounded durability claims.
- Aggregate decision: `needs-review` → `needs-review`; `split proposal` required for filtration versus mechanical deformation/measurement.

### `D-P391-005` — stress

- Applicable evidence: `TEST` and `PERF` have `A` candidate senses for an authorized software stress test with named workload, metrics, duration, stop and recovery criteria; `HW`, `PHYS`, `OT`, `DIST`, `CLOUD`, `REL`, `DEV`, `UI`, `DOC`, `MAINT`, `AI`, `DATA`, `GOV`, and `OBS` remain `U` where a named load/test contract is required. Google Cloud supports bounded workload/load testing; ITU-T L.301 provides telecommunications maintenance context but no universal threshold.
- Excluded domains: uncontrolled production failure, unbounded force, generic overload, and test result as a safety/capacity guarantee.
- Aggregate decision: `needs-review` → `needs-review`; `split proposal` required for mechanical load versus software stress testing.

### `D-P397-005` — SYMBOL

- Applicable evidence: `UI` and `DOC` have `A` candidate senses for a purpose-bearing visible/written mark in an identified representation; Unicode, SVG 2, and WCAG support distinct notation, graphical, and accessibility contexts. `LANG`, `SW`, `DATA`, `NET`, `DIST`, `CLOUD`, `SEC`, `CRYPTO`, `OBS`, `DEV`, `TEST`, and `AI` remain `U` because token, protocol, parser, key, or model meanings require separate representation rules.
- Excluded domains: hardware-only marks, unspecified protocol tokens, and one universal sense covering UI symbols, programming-language symbols, cryptographic notation, and SVG elements.
- Aggregate decision: `needs-review` → `needs-review`; likely `restricted` for a selected representation or `split proposal` for multiple representation types.

### `D-P397-006` — SYMMETRICAL

- Applicable evidence: `UI` has an `A` candidate sense for corresponding shapes/positions about a named axis, center, coordinate system, or reference object; W3C SVG and CSS transforms establish the geometric frame. `SW`, `LANG`, `DATA`, `DIST`, `CLOUD`, `HW`, `CRYPTO`, `DEV`, and `TEST` remain `U` where a formal domain-specific sense may exist. NIST separately establishes symmetric-key cryptography, which must not be merged with geometric symmetry.
- Excluded domains: balanced, equal permissions, symmetric keys, and unspecified data/model symmetry.
- Aggregate decision: `needs-review` → `needs-review`; future `restricted` for UI/graphics or split if cryptographic/formal senses are admitted.

### `D-P397-007` — SYMMETRICALLY

- Candidate evidence and exclusions match `SYMMETRICAL`, but the adverb additionally requires a named placement/transformation action, identified objects, reference frame, and any applicable tolerance.
- Aggregate decision: `needs-review` → `needs-review`; future `restricted` for explicit geometric/UI action or split for formal domain senses.

### `D-P416-006` — unobstructed

- Candidate domains: `NET`, `DIST`, `CLOUD`, `HW`, `OT`, `REL`, `DEV`, `UI`, `DOC`, `MAINT`, `RISK`, and `PHYS` remain `U`; Kubernetes and RFC 1122/791 distinguish logical reachability/routes/interfaces from physical clearance, while Microsoft hardware requirements establish physical-host context without defining an obstruction criterion.
- Excluded domains: reachable, authorized, authenticated, secure, unrestricted network access, and generic availability.
- Aggregate decision: `needs-review` → `needs-review`; possible `restricted` only after direct physical IT/facilities evidence or an owner-approved runbook boundary.

### `D-P419-006` — UPSTREAM

- Applicable evidence: `NET`, `DIST`, and `DEV` have `A` candidate senses. RFC 9110 defines upstream/downstream relative to message flow; NGINX defines upstream server groups; Airflow defines upstream task dependency. `GOV`, `SW`, `DATA`, `CLOUD`, `OBS`, `REL`, `TEST`, `PERF`, and `DOC` remain `U` where the flow/reference boundary must be named.
- Excluded domains: authority, priority, parenthood, hierarchy, trust, and unspecified topology.
- Aggregate decision: `needs-review` → `needs-review`; likely future `restricted` after final general-IT wording and examples are owner-reviewed.

### `D-P419-007` — UPSTREAM OF

- The evidence and domain screening match `UPSTREAM`, with the additional requirement that the reference component and relation be explicit in the sentence.
- Aggregate decision: `needs-review` → `needs-review`; likely future `restricted` after schema/editorial treatment of the named relation.

## Sources actually inspected

- EPA, *Americium in Ionization Smoke Detectors*; AWS, *Data Center Controls*.
- JCGM/BIPM VIM 2.10 and 2.11; Prometheus, *Metric types*; RFC 9110 and RFC 3339.
- NSK, *Scoring*; scikit-learn, *Model evaluation*; NIST AI RMF; Google Cloud Performance Optimization; ITU-T L.301.
- Unicode Core Specification chapter 6; W3C SVG 2, CSS Transforms, and WCAG 2.2 non-text content.
- Kubernetes Service documentation; RFC 1122; RFC 791; Microsoft Windows Server hardware requirements.
- NGINX upstream module documentation; Apache Airflow task relationships.

The sources are indexed in `docs/it-ste-research/external-sources.md`. Limitations are recorded per record above. The source set supports bounded candidate senses and exclusions; it does not authorize vocabulary approval or force canonical dispositions.
