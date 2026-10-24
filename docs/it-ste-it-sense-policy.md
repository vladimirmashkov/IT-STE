# IT-STE independent IT-sense policy

State: draft policy for owner/editorial review

## Purpose

IT-STE is an IT terminology adaptation, not an aviation dictionary with IT labels. ASD-STE100 supplies source provenance, source wording, grammatical data, examples, and physical-page evidence. It does not determine whether a term belongs in IT-STE or what its IT meaning is.

This policy defines how to decide whether an ASD-derived candidate is useful across IT domains, how to constrain polysemy, and when to exclude a source sense. It applies to new classification work and to the remaining `needs-review` register.

This policy is itself a draft project decision. It does not approve vocabulary, release content, publish ASD material, or authorize SFT use.

## IT coverage model

The intended IT scope covers all of these domains, provided that the sense is evidenced and bounded:

1. **Governance and service management** — services, value, practices, risk, policies, incidents, problems, changes, configuration, assets, service levels, availability, continuity, and continual improvement.
2. **Software and applications** — source code, runtime behavior, APIs, interfaces, application state, jobs, workflows, testing, deployment, and dependencies.
3. **Data and information** — databases, schemas, records, storage, messages, consistency, integrity, retention, and data lifecycle.
4. **Networking and protocols** — endpoints, channels, routes, flows, requests, responses, transport, naming, and protocol state.
5. **Cloud, infrastructure, and platforms** — compute, virtualization, containers, orchestration, capacity, resources, scheduling, and platform services.
6. **Hardware, datacenter, and physical IT** — servers, components, cables, connectors, power, cooling, physical inspection, installation, maintenance, and equipment procedures.
7. **Cybersecurity and privacy** — identity, authorization, confidentiality, integrity, availability, vulnerability, threat, incident, evidence, and privacy controls.
8. **Operations, monitoring, and observability** — metrics, logs, traces, events, alerts, dashboards, thresholds, sampling, and measurement contracts.
9. **Reliability, resilience, and recovery** — failure modes, overload, redundancy, failover, backup, restore, continuity, disaster recovery, and service objectives.
10. **Automation, DevOps, and configuration** — pipelines, controllers, automation triggers, configuration state, drift, rollout, rollback, and change execution.
11. **User interfaces, accessibility, and technical communication** — controls, labels, layout, geometry, content, accessibility, procedures, runbooks, and support instructions.
12. **Support and maintenance** — troubleshooting, diagnosis, service actions, replacement, cleaning, repair boundaries, and escalation.

Physical IT is in scope, but only for a named component, surface, device, facility system, or documented procedure. A physical aviation sense must not be transferred to cloud, software, data, or networking by analogy alone. The detailed domain/object/boundary matrix is maintained in [`docs/it-ste-it-domain-matrix.md`](it-ste-it-domain-matrix.md).

## Sense profile

A canonical IT entry must represent a bounded sense profile, not an unqualified word. The working profile is:

```text
word and POS:
domain(s):
named object or actor:
action, state, relation, or property:
preconditions / measurement / acceptance criteria:
permitted context:
explicitly excluded meanings:
preferred alternatives:
authoritative evidence:
source facts versus editorial inference:
```

One spelling may have multiple domain-specific profiles. If those profiles cannot be represented without ambiguity in the current schema, record a `split proposal`; do not silently add records or schema fields.

## Classification mapping

The existing canonical dispositions map to this policy as follows:

- **Core / portable IT sense → `allowed`**: supported across more than one relevant IT context or by a controlling standard, with low ambiguity and no hidden guarantee.
- **Domain-restricted sense → `restricted`**: useful with a named domain, object, relation, operation, criterion, condition, or measurement contract.
- **Split proposal → normally `restricted` plus a documented split proposal**: do not merge distinct senses into one definition merely to avoid a new record.
- **Out of IT scope → `not-applicable`**: valid source/aviation terminology, but no justified use within the intended IT coverage. An explicit owner decision may also exclude a free, polysemous, or context-dependent word from the canonical IT-STE vocabulary layer even when the word remains valid in external technical documentation; this is not a universal English-word ban.
- **Misleading controlled-writing use → `prohibited`**: the considered IT wording hides a necessary condition, actor, object, evidence boundary, or safety consequence. This is not a universal ban on the English word.
- **Unresolved → `needs-review`**: evidence or project policy cannot select a safe bounded classification. This is temporary and must include one exact missing decision or evidence requirement.

Every decision must explain why the plausible alternative dispositions were rejected.

## ITIL alignment

ITIL is used as a **service-management reference model**, not as the sole dictionary authority. ITIL concepts are especially relevant for:

- service and value;
- governance and practices;
- incident, problem, and change management;
- configuration and asset management;
- availability, continuity, and resilience;
- service level and measurement;
- risk, improvement, and operational ownership.

An ITIL association does not by itself establish the meaning of a general English word. A term must still be checked against the applicable ITIL concept, current official material where available, and the technical domain in which the proposed wording will be used.

Use other controlling sources for other domains:

- IETF and applicable RFCs for Internet protocols;
- W3C/WHATWG for web platform and UI semantics;
- NIST, ISO/IEC, and applicable security standards for security and governance claims;
- official product or manufacturer documentation for product behavior and hardware procedures;
- specialist engineering standards for physical, electrical, mechanical, or measurement claims.

Do not use ITIL to manufacture software, protocol, hardware, or mathematical meanings that ITIL does not define.

## Admission criteria

A proposed IT sense may leave `needs-review` only when all applicable conditions are satisfied:

1. The sense has a real, relevant IT use within one or more listed domains.
2. The object, actor, operation, state, relation, or property is named.
3. The scope and excluded meanings are explicit.
4. At least one competent primary, official, or specialist source supports the factual claim.
5. The source is applicable in version, domain, status, and terminology.
6. The proposed wording does not imply unsupported delivery, success, safety, correctness, durability, readiness, intent, or completeness.
7. The term is not merely an aviation borrowing whose IT use is inferred from a superficial resemblance.
8. The proposed examples can be evaluated against the source and the stated IT contract.
9. If the term is polysemous, the entry either names the domain or records a split proposal.
10. The rationale distinguishes source fact from editorial adaptation.

## Eleven-record domain-evidence workflow

The remaining 11 records require a separate evidence matrix because the question is not merely whether each word has an IT use, but which combinations of word, sense, and IT domain are defensible. Use `docs/it-ste-research/it-domain-11-evidence-matrix.md` and the project-local skill `.agents/skills/it-ste-11-domain-evidence/SKILL.md`.

For each `word × domain` pair, record:

1. a concrete candidate sense;
2. the named IT object or actor;
3. the operation, state, relation, or property;
4. the observable condition, measurement, tolerance, procedure, or acceptance boundary;
5. an authoritative source actually inspected;
6. source facts, limitations, and editorial inference separately;
7. excluded aviation, metaphorical, and unrelated IT meanings;
8. one result: `applicable`, `not-applicable`, or `unresolved`.

A domain is not applicable merely because a sentence can be imagined with the word. An `applicable` result requires a competent source and a bounded sense. An `unresolved` result is correct when the source, owner policy, or schema cannot select a safe sense. The aggregate word disposition must remain `needs-review` when any unresolved split or policy boundary prevents a safe canonical entry.

For polysemous words, investigate the most plausible domains and explicitly close the remaining domains with evidence-based `not-applicable` or `unresolved` findings. Do not claim exhaustive coverage from a synonym search or search snippet. `allowed` is unavailable for a word whose domains or senses remain materially ambiguous. `split proposal` is required when multiple applicable senses cannot be represented independently in the current schema.

Physical IT is admissible only when the object belongs to an IT-operated system or documented facility process and the source establishes the relevant physical condition. Network reachability, authorization, security, logical availability, or software behavior must not be described with physical-clearance words by analogy. ITIL may frame governance, service management, operations, reliability, assets, incidents, changes, and service levels; it does not define meanings for protocols, programming languages, geometry, cryptography, or physical measurement.

Reddit and Stack Overflow may assist discovery of terminology or candidate primary sources only. They are never evidence for `applicable`, `restricted`, `not-applicable`, or any other disposition.

## Decision workflow for the 36-record register

For each record:

1. Verify the ASD entry and authenticated PDF layout.
2. State the intended IT question and list aviation-only and unrelated IT meanings that are out of scope.
3. Check the relevant ITIL practice/concept if the term concerns service management or operations.
4. Select the strongest applicable technical authority for the actual domain.
5. Compare `allowed`, `restricted`, `prohibited`, `not-applicable`, `split proposal`, and retaining `needs-review`.
6. Record the old/new disposition and evidence in `needs-review-38.md` and `it-sense-classification-log.md`.
7. Change canonical wording only when the sense profile is justified.
8. Preserve unresolved records when the missing issue is a project policy choice rather than a research gap.

The goal is not zero `needs-review` at any cost. The goal is a defensible IT vocabulary in which every retained word has an explicit domain and sense boundary.
