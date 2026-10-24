# IT-STE IT-domain and sense-boundary matrix

State: draft project reference for owner/editorial review

This matrix defines the IT coverage model used when adapting ASD-derived candidates. It is a scope and evidence framework, not an approval list and not a replacement for the canonical vocabulary. A word is not admitted merely because it can be imagined in a listed domain.

## Admission rule

A candidate sense must identify the domain, named object or actor, operation/state/relation, and an observable condition or acceptance boundary when applicable. The sense must be supported by a competent source appropriate to that domain. A source fact is not the same as the editorial decision to include the word.

When one spelling covers incompatible senses, keep the sense domain-bound and record a `split proposal` if the current schema cannot represent the distinction. Do not use ITIL to define protocol, software, hardware, mathematical, or security meanings outside ITIL's scope.

## Domain matrix

| ID | IT domain | Named objects or actors | Typical states, actions, relations, or properties | Required boundary/evidence | Common exclusions |
|---|---|---|---|---|---|
| GOV | Governance and service management | service, practice, policy, risk owner, change, configuration item, asset | decision, priority, risk, service level, availability, continuity, improvement | named service/practice, accountable actor, policy or measurement criterion; ITIL may provide the service-management frame | ordinary business meaning, undocumented authority, generic importance |
| SW | Software and applications | source code, function, process, job, API, application, dependency | execution, state, interface, failure, dependency, deployment | named software object and defined behavior or lifecycle event | physical-only meaning, vague quality claim |
| LANG | Programming languages and formal methods | token, symbol, expression, type, grammar, proof, model | notation, evaluation, equivalence, validity, transformation | named language/notation and formal or implementation rule | UI marks, mathematical claims without the relevant formal context |
| DATA | Data and information management | record, field, schema, database, object, message, dataset, storage medium | integrity, consistency, synchronization, retention, transformation, provenance | named data object, comparison/checkpoint, or lifecycle operation | physical cleanliness, authenticity, correctness without evidence |
| NET | Networking and protocols | endpoint, interface, route, packet, request, response, channel, proxy | flow, direction, upstream/downstream, delivery, reachability, protocol state | named flow/reference point and protocol or network specification | administrative hierarchy, authorization, physical obstruction by analogy |
| DIST | Distributed systems and APIs | service, node, broker, queue, controller, dependency, API | dependency, ordering, propagation, request/response, consistency | named graph/flow and reference component; specify direction | parent/child hierarchy, priority, unspecified topology |
| CLOUD | Cloud, infrastructure, and platforms | VM, container, node, cluster, resource, scheduler, platform service | allocation, capacity, placement, scaling, scheduling, health | named resource/platform and provider or platform semantics | aviation geometry transferred to cloud without a reference frame |
| HW | Hardware, datacenter, and physical IT | server, board, connector, cable, power unit, cooling system, facility area | installation, physical condition, contamination, damage, serviceability | named component/surface/facility system, inspection or documented procedure | generic machinery, software state, unrestricted physical claims |
| OT | Operational technology and cyber-physical systems | controller, sensor, actuator, industrial process, hydraulic/electrical subsystem | physical interaction, control, measurement, maintenance | named physical process/component and applicable procedure or safety boundary | treating all industrial terminology as ordinary cloud/software terminology |
| SEC | Cybersecurity and privacy | identity, credential, asset, vulnerability, threat, incident, evidence, control | authorization, confidentiality, integrity, availability, intent, exposure | named security object, control, evidence source, or incident process | unverified intent, generic danger, ordinary “real”/“critical” claims |
| CRYPTO | Identity, access control, and cryptography | key, certificate, principal, permission, policy, cryptographic operation | authentication, authorization, signing, encryption, symmetry/asymmetry | named protocol/algorithm/policy and its defined relation | visual symmetry, ordinary identity, generic access |
| OBS | Operations, monitoring, and observability | metric, log, trace, event, alert, dashboard, sample | measured value, score, threshold, state, correlation | named signal, collection method, time window, scale, threshold | “real” as true/correct, score without scale, intent inferred from logs |
| REL | Reliability, resilience, and recovery | service, component, replica, backup, restore point, failure mode | overload, failover, recovery, availability, continuity | named objective, failure condition, recovery point/time, or test | unqualified “healthy”, “serviceable”, or “available” |
| DEV | Automation, DevOps, and configuration | pipeline, stage, deployment, controller, configuration, release | dependency, rollout, rollback, drift, synchronization, trigger | named pipeline/configuration graph and checkpoint or execution rule | upstream as authority, synchronization without tolerance/checkpoint |
| TEST | Testing, quality, and verification | test case, requirement, build, artifact, acceptance result | scored, stress-tested, verified, satisfactory/unsatisfactory | named test object, scale, requirement, method, and result boundary | subjective quality, score without rubric, test result as guarantee |
| PERF | Performance and capacity | workload, request, resource, queue, latency, throughput | load, stress, saturation, capacity, response behavior | named workload/resource, metric, test method, and time window | mechanical stress by software analogy, generic pressure |
| UI | User interfaces, accessibility, and visual communication | control, label, icon, symbol, layout, coordinate system, user | symbol, alignment, symmetry, visibility, obstruction, affordance | named representation, reference frame, user impact, accessibility criterion | cryptographic/data symbol meanings, visual claim without frame |
| DOC | Technical communication and support content | procedure, instruction, warning, runbook, term, example | meaning, alternative, condition, escalation, diagnostic statement | named audience/task and verifiable procedure or condition | generic prose preference without technical consequence |
| MAINT | Support, maintenance, and repair | device, component, fastener, service action, technician | remove, clean, replace, inspect, serviceability | named equipment, authorized procedure, acceptance test, safety limit | logical remove/delete, generic repair claims |
| AI | AI/ML and data science | model, feature, label, score, dataset, inference | scoring, evaluation, confidence, training, drift | named model/task, metric or rubric, dataset/time boundary | “real” as truth, score as correctness, unqualified intelligence claim |
| RISK | Safety, compliance, and risk management | hazard, control, requirement, audit evidence, risk | severity, likelihood, compliance, acceptance, mitigation | named framework, criterion, evidence and responsible owner | universal safety guarantee, generic criticality |
| TIME | Time, synchronization, and real-time systems | clock, timestamp, event, process, deadline, control loop | synchronized, real-time, ordering, drift, tolerance | named clocks/events, tolerance, reference and observation window | ordinary agreement, vague currentness |
| PHYS | Physical/geometry/measurement support across IT | path, surface, axis, component, measured quantity | curvature, inboard, unobstructed, strain, stress, radioactive | named physical object/reference frame, measurement method, inspection or safety procedure | aviation-only geometry, software metaphor without technical object |

## Classification use

- `allowed`: a portable sense with low ambiguity and a controlling or broadly applicable IT definition.
- `restricted`: a useful sense requiring the named domain/object/relation/criterion above.
- `prohibited`: the proposed controlled-writing use would hide a necessary boundary or create a materially misleading claim; this is not a universal ban on the English word.
- `not-applicable`: the ASD sense has no justified use within this IT scope.
- `split proposal`: multiple incompatible domain senses are evidenced, but the current schema cannot safely represent them as separate canonical senses.
- `needs-review`: evidence or an owner policy choice is still insufficient.

For each candidate, record both the applicable domain(s) and the domains explicitly rejected. The final decision must distinguish ASD facts, external-source facts, and editorial inference.

## Relation to ITIL

ITIL is useful primarily for GOV, REL, OBS, RISK, MAINT, and service/support terminology. It can frame service value, practices, incidents, problems, changes, configuration, assets, service levels, availability, continuity, risk, and improvement. It does not define protocol direction, programming-language symbols, physical measurement, cryptographic symmetry, or UI geometry. Those senses require the relevant technical standard or official documentation.
