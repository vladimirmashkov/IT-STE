# IT-domain classification of the remaining 11 records

State: resolved research register; canonical dispositions intentionally unchanged pending owner/schema decisions
Run scope: 11 records, seven ASD pages, user-authorized domain-mapping study
Access date: 2026-10-24

## Purpose

This note applies `docs/it-ste-it-domain-matrix.md` to every record that remains in the frozen `needs-review` register. It separates ASD source facts, external IT facts, and editorial inference. It is not vocabulary approval, release authorization, publication, canonicalization, or SFT authorization.

ASD source facts were retrieved from the authenticated Issue 9 derivative with `python3 tools/asd_ste100_local.py doctor`, exact `entry` lookups, and the existing authenticated page/layout evidence. Source Issue: 9; revision: `r0001`; PDF SHA-256: `d1f4ea9e7cd6e46b47aa9057209f99e78c0e9cfc4e27a5b07895b05c1a166431`.

## Domain decisions

### `D-P349-003` — `RADIOACTIVE` (adj), page 349

- **ASD fact:** “Related to radioactivity”; physical contamination-check example; separate row, historical wrapped-headword warning preserved.
- **Potential IT domains:** `HW`, `MAINT`, `RISK`, facility infrastructure; only for a named physical equipment item, material, or safety register.
- **Bounded candidate sense:** having or containing a specified radioactive material/source, as established by controlling equipment or safety documentation.
- **Excluded:** software/log metaphors, generic danger, contamination, maliciousness, or claims that data-center smoke sensors are radioactive without equipment evidence.
- **Evidence:** EPA, *Americium in Ionization Smoke Detectors*, updated 2026-04-08, https://www.epa.gov/radtown/americium-ionization-smoke-detectors, confirms some ionization detectors use shielded americium-241. AWS, *Data Center Controls*, https://aws.amazon.com/compliance/data-center/controls/, confirms data-center smoke detection and equipment maintenance but not detector technology or radioactive material.
- **Decision:** retain `needs-review`.
- **Why alternatives are rejected:** `allowed` is unsupported and ambiguous; `restricted` is plausible only after identifying a qualifying IT facility item; `not-applicable` would prematurely exclude physical IT; `prohibited` would turn an evidence gap into a lexical ban; no split is currently needed.
- **Missing decision:** whether radioactive facility equipment belongs in IT-STE and which competent equipment/safety source identifies it.

### `D-P351-001` — `real` (adj), page 351

- **ASD fact:** `AGREE (v)` alternative; gauge/fuel agreement example; no tolerance, reference method, or comparison contract.
- **Potential IT domains:** `DATA`, `OBS`, `SW`, `HW`, `REL`.
- **Competing senses:** measured value; instrument indication; current state; verified value; production/non-simulated value.
- **Excluded:** treating observed as true, current as verified, a cache state as reality, or a mathematical real number as the ASD sense.
- **Evidence:** JCGM/BIPM VIM3 2.10, https://jcgm.bipm.org/vim/en/2.10.html, distinguishes measured quantity value from indication. VIM3 2.11, https://jcgm.bipm.org/vim/en/2.11.html, distinguishes true value from measured value. Prometheus, *Metric types*, https://prometheus.io/docs/concepts/metric_types/, distinguishes gauges and counters. RFC 9110, https://www.rfc-editor.org/rfc/rfc9110.html, distinguishes current representations and validators.
- **Decision:** retain `needs-review`; record a strong future `split proposal`.
- **Why alternatives are rejected:** `allowed` would hide the intended contrast; `restricted` is possible only after selecting one sense and contract; `not-applicable` is wrong because the domains are real IT domains; `prohibited` is too broad; split is likely but cannot be safely represented without owner selection/schema support.
- **Missing decision:** choose the contrast and contract: measured/indicated, current/cached, verified/unverified, or production/simulated, including time window, tolerance, reset, or verification method.

### `D-P368-010` — `scored` (adj), page 368

- **ASD fact:** physical score/groove damage on a bearing race; `SCORE (TN)`; not a numerical rating.
- **Potential IT domains:** `HW` physical-surface inspection; separately `AI`, `DATA`, `TEST` for numerical/model scoring.
- **Bounded senses:** a named hardware surface has a damage groove under an inspection criterion; separately, a model/data/test object has a value assigned by a named scoring function or rubric.
- **Excluded:** rating a server without a rubric; designed grooves treated as damage; score treated as truth, correctness, or production readiness.
- **Evidence:** NSK, *Scoring*, https://www.nsk.com/eu-en/tools-resources/troubleshooting/damage-by-type/scoring, supports physical bearing-surface scoring. scikit-learn, *Metrics and scoring*, https://scikit-learn.org/stable/modules/model_evaluation.html, supports defined model scoring functions and metrics. NIST AI RMF, https://www.nist.gov/itl/ai-risk-management-framework, supports contextual evaluation but not a universal `scored` definition. FOA connector inspection, https://www.thefoa.org/tech/ref/testing/test/scope.html, supports physical inspection context but not the word.
- **Decision:** `split proposal` is the recommended eventual classification; current canonical status remains `needs-review` because one record cannot safely express both senses.
- **Why alternatives are rejected:** `allowed` conflates damage and scoring; `restricted` is suitable only after a schema-supported sense choice; `not-applicable` is wrong globally; `prohibited` is too broad; retaining `needs-review` is required until split ownership is resolved.

### `D-P391-003` — `strain` (v), page 391

- **ASD fact:** two technical references: `FILTER (TN)` for liquid/oil filtration and `STRAIN (TN)` for bellows deformation.
- **Potential IT domains:** `HW`, `MAINT`, `PHYS`; not generic software performance.
- **Bounded senses:** filter a named coolant/liquid through a specified filter; separately deform or measure strain in a named component under a defined load/test method.
- **Excluded:** generic filtering of logs/data as the ASD sense; “strain” as an uncontrolled software-load instruction; durability or safety guarantees without limits.
- **Evidence:** Google Cloud, *Performance optimization pillar*, https://cloud.google.com/architecture/framework/performance-optimization, uses workload, load, overload, resources, metrics, and requirements rather than mechanical `strain`. NIST AI RMF, https://www.nist.gov/itl/ai-risk-management-framework, supports defined evaluation context but not the ASD verb. The ASD page itself proves the two distinct technical directions.
- **Decision:** `split proposal` recommended; retain canonical `needs-review` until owner chooses filtration versus mechanical sense and schema treatment.
- **Why alternatives are rejected:** `allowed` is unsafe for two meanings; `restricted` is suitable only per separate sense; `not-applicable` is too broad because physical IT is in scope; `prohibited` would reject legitimate maintenance; unchanged `needs-review` records the unresolved split.

### `D-P391-005` — `stress` (v), page 391

- **ASD fact:** `FORCE (TN)` and example warning against excessive force on ducting.
- **Potential IT domains:** `HW`, `PHYS`, `PERF`, `TEST`, `REL`.
- **Bounded senses:** apply specified mechanical force/load to a named component under a documented test; separately conduct an authorized software stress test with defined workload, metrics, duration, stop and recovery criteria.
- **Excluded:** uncontrolled production failure, unbounded force, generic overload, or treating test results as proof of safety/capacity.
- **Evidence:** Google Cloud performance guidance above supports bounded software workload/load terminology. NIST AI RMF supports context and evaluation but not the word. ITU-T L.301, https://www.itu.int/rec/T-REC-L.301, provides official telecommunications maintenance context but not a universal stress threshold.
- **Decision:** `split proposal` recommended; current canonical status remains `needs-review`.
- **Why alternatives are rejected:** `allowed` is too broad; `restricted` requires sense separation; `not-applicable` is wrong for hardware and performance testing; `prohibited` applies only to uncontrolled operational instructions, not the word globally.

### `D-P397-005` — `SYMBOL` (n), page 397

- **ASD fact:** written sign identifying a quantity, operation, item, or condition.
- **Potential IT domains:** `UI`, `DOC`, `LANG`, `SW`, protocol/representation contexts.
- **Bounded candidate:** a visible or written mark in an identified representation that denotes a specified object, operation, quantity, or state.
- **Excluded:** unspecified protocol token, parser symbol, cryptographic mark, or SVG-specific element treated as a universal sense.
- **Evidence:** Unicode Standard, https://www.unicode.org/versions/Unicode16.0.0/core-spec/chapter-6/, supports multiple symbol and notation contexts. W3C SVG 2, https://www.w3.org/TR/2026/CR-SVG2-20261006/, provides a concrete graphical `symbol` element and coordinate/rendering semantics. WCAG 2.2 non-text content, https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html, supports purpose-bearing accessible alternatives for visual content.
- **Decision:** retain `needs-review`; future `restricted` is plausible after selecting UI/notation scope, while a split may be needed for encoded/protocol meanings.
- **Why alternatives are rejected:** `allowed` is too broad; `not-applicable` is false; `prohibited` is false; `restricted` needs a selected representation; split requires owner/schema decision.

### `D-P397-006` — `SYMMETRICAL` (adj), page 397

- **ASD fact:** “That has or is with symmetry”; separate wrapped row.
- **Potential IT domains:** `UI`, graphics/layout, `PHYS`; cryptography only as a separate sense.
- **Bounded candidate:** corresponding shapes/positions about a named axis, center, coordinate system, or reference object.
- **Excluded:** cryptographic key symmetry, permission symmetry, data-model symmetry, or “balanced” without a reference frame.
- **Evidence:** W3C SVG coordinates, https://www.w3.org/TR/SVG2/coords.html, and CSS Transforms, https://www.w3.org/TR/css-transforms-1/, establish coordinate systems, transforms, origins, and reference boxes. NIST symmetric-key glossary, https://csrc.nist.gov/glossary/term/symmetric_key_algorithm, establishes the distinct cryptographic sense.
- **Decision:** retain `needs-review`; future `restricted` for UI/graphics is plausible; split is likely if cryptographic/formal senses are admitted.
- **Why alternatives are rejected:** `allowed` conflates incompatible senses; `not-applicable` and `prohibited` reject valid UI/graphics use; `restricted` needs an explicit frame; split requires schema/owner decision.

### `D-P397-007` — `SYMMETRICALLY` (adv), page 397

- **ASD fact:** “In a symmetrical manner”; separate adverb row.
- **Potential IT domains:** `UI`, graphics/layout, geometry, `PHYS`.
- **Bounded candidate:** placing or transforming identified objects into corresponding positions about a named axis/reference frame.
- **Excluded:** cryptographic, data, mathematical, permission, or access-control uses without a formal domain statement.
- **Evidence:** same W3C SVG/CSS coordinate and transform sources; NIST symmetric-key source for exclusion of crypto conflation.
- **Decision:** retain `needs-review`; future `restricted` for an explicit geometric/UI action is plausible.
- **Why alternatives are rejected:** `allowed` does not identify action, objects, frame, or tolerance; `not-applicable`/`prohibited` are too broad; `restricted` awaits selected UI/geometry sense; split may be needed.

### `D-P416-006` — `unobstructed` (adj), page 416

- **ASD fact:** alternatives `CLOGGED` and `CLEAR`; drain opening and line-of-sight examples.
- **Potential IT domains:** `HW`, `MAINT`, `UI`, physical inspection; only explicitly physical paths in `NET`.
- **Bounded candidate:** free of a specified physical blockage along a named opening, airflow/cable/optical/inspection path or view.
- **Excluded:** reachable, authorized, authenticated, secure, or unrestricted network access.
- **Evidence:** Kubernetes Service docs, https://kubernetes.io/docs/concepts/services-networking/service/, distinguish endpoints/reachability from authorization. RFC 1122, https://www.rfc-editor.org/rfc/rfc1122.html, and RFC 791, https://www.rfc-editor.org/rfc/rfc791.html, distinguish interfaces/routes/reachability from physical clearance. Microsoft Windows Server hardware requirements, https://learn.microsoft.com/en-us/windows-server/get-started/hardware-requirements, distinguishes physical hosts and network adapters but does not define an obstruction criterion.
- **Decision:** retain `needs-review`; future `restricted` is plausible if a direct IT hardware/facilities source or owner runbook boundary is supplied.
- **Why alternatives are rejected:** `allowed` is too broad; `not-applicable` ignores physical IT; `prohibited` would ban a valid physical use; `restricted` currently lacks direct IT acceptance evidence.

### `D-P419-006` — `UPSTREAM` (adv), page 419

- **ASD fact:** “In a direction opposite to the flow”; separate adverb row.
- **Potential IT domains:** `NET`, `DIST`, `DEV`, workflow/service chains.
- **Bounded candidate:** toward the source of a named data/message flow or reverse direction of an explicit dependency path.
- **Excluded:** authority, priority, parenthood, hierarchy, trust, or unspecified topology.
- **Evidence:** RFC 9110 §3.7, https://www.rfc-editor.org/rfc/rfc9110.html#section-3.7, defines upstream/downstream relative to message flow. NGINX upstream module docs, https://nginx.org/en/docs/http/ngx_http_upstream_module.html, define upstream server groups. Apache Airflow task relationships, https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html#relationships, define upstream task dependency.
- **Decision:** retain `needs-review`; likely future `restricted` after editorial wording/flow boundary review.
- **Why alternatives are rejected:** `allowed` is too broad; `not-applicable`/`prohibited` reject established uses; `restricted` is plausible but current schema and examples need owner review.

### `D-P419-007` — `UPSTREAM OF` (prep), page 419

- **ASD fact:** “In a direction opposite to the flow”; separate prepositional row.
- **Potential IT domains:** `NET`, `DIST`, `DEV`, workflow/service chains.
- **Bounded candidate:** located before or toward the source side of a named component in an explicit data, processing, service, or dependency flow.
- **Excluded:** authority, priority, parenthood, seniority, or unspecified direction.
- **Evidence:** same RFC 9110, NGINX, and Airflow sources.
- **Decision:** retain `needs-review`; likely future `restricted` after naming the reference component and relation.
- **Why alternatives are rejected:** `allowed` hides the required relation; `not-applicable` and `prohibited` are too broad; `restricted` is plausible but needs schema/editorial decision.

## Aggregate result

All 11 records have at least one plausible IT domain. None can safely become unrestricted `allowed`. Recommended future outcomes are:

- `split proposal`: `scored`, `strain`, `stress`; likely also `real`, `SYMBOL`, and symmetry terms if multiple senses are admitted;
- future `restricted`: bounded flow terms `UPSTREAM` / `UPSTREAM OF`, geometric/UI symmetry, physical unobstructed path, and a named radioactive facility item if owner scope/evidence is supplied;
- remain `needs-review`: all 11 in the current canonical schema until the missing owner choices or direct evidence are supplied.

This is a completed research mapping, not a forced canonical disposition change.
