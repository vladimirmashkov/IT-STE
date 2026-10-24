---
name: it-ste-configuration-asset
description: Run one compact W3 pair profile for configuration item and IT asset; delegate execution to the W3 cycle.
disable-model-invocation: true
---

# W3 pair profile: configuration item / IT asset

Use only for this exact pair and one bounded run. Delegate the lifecycle to `it-ste-w3-cycle` by reference; do not load that skill or research history in full.

## Input profile

Require `phase: w3`, exact scope/IDs if any, excluded meanings, evidence boundary, allowlist, and per-run authorization in the input JSON. Candidate senses are hypotheses:

- `configuration item`: controlled component used to deliver/support a service, with recorded attributes and relationships;
- `IT asset`: item of organizational value managed to deliver/support IT services.

Distinguish a configuration item from an untracked component, service, register entry, implementation detail, or arbitrary object; attributes/relationships from ownership, value, procurement, inventory, and lifecycle; asset from configuration item; managed object from the tool/database/ticket/record/team; and service support from ownership/purchase/approval/accounting. Candidate IDs `ITSTE-T-0009`/`0010` are hints only; never allocate duplicates. Do not research SLA/target, availability/resilience, change authority, release/deployment, API, protocol, cryptographic, runtime, UI, physical, or unrelated ASD meanings.

## Evidence boundary

Authenticate ASD and retrieve exact entries only for real collisions. Inspect direct current configuration/asset-management sources, record scope/version/competence/limitations, and do not copy definitions/examples or assign ASD provenance. Any new records stay original, draft, restricted, project-rights-only, and within the existing schema.

Run the common W3 cycle, compact checks, output/finish, and explicit-path commit policy. Leave insufficient evidence as `blocked`/`needs-review`; never create a cosmetic commit. Report exact IDs/POS/boundaries, evidence refs, validation statuses, next pair, and no-approval/no-release status.
