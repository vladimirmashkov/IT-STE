---
name: it-ste-service-request-desk
description: Run one compact W3 pair profile for service request and service desk; delegate execution to the W3 cycle.
disable-model-invocation: true
---

# W3 pair profile: service request / service desk

Use only for this exact pair and one bounded run. Delegate the lifecycle to `it-ste-w3-cycle` by reference; do not load that skill or any history in full.

## Input profile

Require `phase: w3`, pair scope, excluded meanings, exact IDs if already allocated, evidence boundary, allowlist, and per-run authorization in `runs/<run-id>.input.json`. Candidate senses are hypotheses:

- `service request`: user request for information, access, or a predefined service action;
- `service desk`: support function that receives, coordinates, and communicates service requests/incidents.

Distinguish request from incident/problem/error/workaround/change; function from team, queue, tool, escalation/approval authority; receiving/communicating from fulfilling/approving. Do not research configuration item, IT asset, SLA/target, availability/resilience, release/deployment, API, protocol, cryptographic, runtime, UI, or physical meanings here. Candidate IDs `ITSTE-T-0007`/`0008` are hints only; never allocate duplicates.

## Evidence boundary

Use authenticated ASD exact-entry checks only for real lexical collisions, and direct current service-management evidence (official/primary/specialist). Record source metadata and limitations; do not copy formal definitions/examples or assign ASD provenance. Keep any new records original, draft, restricted, and project-rights-only under the existing schema.

Run the common W3 cycle, compact checks, output/finish, and explicit-path commit policy. If evidence or contract support is missing, output `blocked`/`needs-review`, preserve the active note/checkpoint, and do not create a cosmetic commit. Report exact IDs/POS/boundaries, refs, validations, next W3 action, and no-approval/no-release status.
