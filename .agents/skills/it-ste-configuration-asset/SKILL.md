---
name: it-ste-configuration-asset
description: Continue exactly one resumable W3 IT-STE slice for configuration item and IT asset, using direct configuration/asset evidence, explicit ownership-versus-relationship boundaries, draft-only records when justified, full validation, and one safe automatic commit.
disable-model-invocation: true
---

# IT-STE configuration item and IT asset

Use this project-local skill only when the user explicitly requests the next W3 slice for `configuration item` and `IT asset`. It is a bounded pair workflow, not a bulk ITIL importer, an approval workflow, a release gate, publication permission, or SFT authorization. The current run is authorized to make one automatic commit only after the complete evidence, validation, and review cycle succeeds.

Read and execute `../it-ste-w3-cycle/SKILL.md` as the 14-stage orchestration contract. This file supplies the pair-specific scope and evidence boundary; it does not replace the repository `AGENTS.md` or the cycle's safety rules.

## Resume contract

The repository is the state store. At startup:

1. Read `AGENTS.md`.
2. Read only the Current checkpoint in `docs/it-ste-draft-handoff.md`, the relevant bounded sections of `docs/it-ste-research-method.md`, the current W3 section of `docs/it-ste-draft-remediation-plan.md`, and `docs/it-ste-research/W3-itil-service-management.md`.
3. Do not read the complete generated Markdown, all vocabulary batches, the complete ASD extraction, the SQLite payload, or the private PDF merely to resume.
4. Capture the full Git baseline required by the cycle skill before editing. Continue only when ownership is unambiguous. A nonignored unrelated, mixed, staged, deleted, renamed, binary, mode, or submodule change is a safety stop.
5. If a prior partial run created `ITSTE-T-0009` or `ITSTE-T-0010`, inspect and continue from the recorded state; never allocate duplicates. If the checkpoint already advances beyond this pair, do not repeat it without new evidence or an explicit user request.

## Exact bounded scope

The only active candidates are:

- `configuration item`: candidate bounded sense — a component controlled to deliver or support a service, with recorded attributes and relationships;
- `IT asset`: candidate bounded sense — an item of value that an organization manages to deliver or support IT services.

These are hypotheses until evidence supports them. The research must distinguish:

- a configuration item from an untracked component, service, asset register entry, implementation detail, or arbitrary system object;
- configuration attributes and relationships from asset ownership, financial value, procurement, inventory, and lifecycle management;
- an IT asset from a configuration item, while allowing that one real-world item can be represented in both management contexts;
- a managed object from the tool, database, ticket, record, queue, or team that stores or manages it;
- delivering/supporting a service from owning, purchasing, approving, or financially accounting for an item.

Likely next IDs are `ITSTE-T-0009` and `ITSTE-T-0010`, but allocate them only after separate bounded senses and POS choices are justified. A multi-word phrase is plausible, not predetermined. If evidence does not support distinct records, leave the pair unresolved or blocked and record the exact missing source or owner decision.

Do not research service-level agreement/target, availability, resilience, change authority, release, deployment, API, protocol, cryptographic, runtime, UI, physical meanings, or unrelated ASD vocabulary in this run.

## Required evidence

Run the authenticated ASD check before relying on ASD-derived data:

```sh
python3 tools/asd_ste100_local.py doctor
```

Search the canonical ASD batches for exact compounds and lexical components before retrieving entries. Retrieve exact entries only for actual collisions. Preserve ASD Issue, revision, physical PDF page, printed page, exact locator, warnings, raw metadata, and authenticated PDF SHA-256. Visually inspect a PDF page only if row layout or typography matters; no ASD row may be changed merely to add an ITIL sense.

For external evidence, directly inspect current, competent sources such as official PeopleCert/ITIL Service Configuration Management and IT Asset Management practice pages or an applicable primary service-management source. Discover URLs with targeted search if necessary, then fetch the actual page; do not cite snippets, guessed URLs, inaccessible pages, AI summaries, or copied glossary text. Record title, publisher, URL, access date, version/status, relevant section, finding, competence/applicability, and limitation. Keep downstream rights explicit/unknown.

The current canonical boundaries may require inspecting only the existing `service`, `service request`, and `service desk` draft records. Do not read unrelated terms or all generated output merely for context.

## Decision and change rules

Create separate original IT-STE draft phrases only if the evidence supports:

- a configuration-management sense centered on controlled identity, attributes, and relationships; and
- an asset-management sense centered on an item of organizational value and its managed ownership/lifecycle context.

Do not merge the terms, add relations, or introduce a multi-sense field without an existing contract field. Keep any new terms `status: draft`, `origin: original`, normally `usage: restricted`, with original IT-STE definitions/examples, project-only rights, and only external ITIL source references. Do not copy formal definitions or examples from the sources and do not assign ASD provenance.

Maintain exactly the active note `docs/it-ste-research/W3-itil-service-management.md` in place. It must state the pair scope, canonical paths/IDs actually inspected or created, ASD collision evidence or not-applicable visual statement, direct external evidence and limitations, alternatives/rejected boundaries, source facts versus inference, unresolved questions, actual validation results, and one exact next action. Update the Current checkpoint in place and advance the W3 plan only after the pair's actual outcome. If the canonical term count changes, update the manifest and both canonical contract summaries. Regenerate `docs/IT-STE-draft.md` with the document tool; never hand-edit it.

The successful allowlist is limited to the active note, Current checkpoint, W3 plan boundary, manifest, justified new term/source records, English/Russian canonical summaries, affected tests, and generated Markdown. Do not modify ASD batches, source extraction, catalog releases, private PDFs, renderings, secrets, or unrelated files.

## Cycle and commit

Execute all fourteen stages in `../it-ste-w3-cycle/SKILL.md` exactly once for this pair. Run affected full-path vocabulary checks for any inspected collision, then all wider checks, diagnostics, queue/count recomputation, complete final Git review, and one explicit-path automatic commit. Suggested imperative commit message when both terms are materialized: `Add configuration item and IT asset terms`.

If the slice is blocked, commit only justified note/checkpoint/plan/source evidence changes after validation and review; do not create a cosmetic no-op commit. If safety conditions fail, do not stage or commit.

The exact next W3 slice after a successful completed pair is `service level agreement` and `service level target`, unless the checkpoint records a different evidence-based next action.

## Final report

Report in Russian with the baseline/checkpoint comparison; whether either candidate was materialized or blocked, exact IDs/POS/boundaries; ASD and external sources actually inspected and limitations; queue/counts; every validation result including failures; complete changed/new-file inventory and ignored artifacts; unresolved questions; the exact next W3 slice; automatic commit hash/message/paths or the safety blocker; reviewed changes left out; and an explicit statement that no vocabulary approval, release, publication, conformance, or SFT readiness was claimed.
