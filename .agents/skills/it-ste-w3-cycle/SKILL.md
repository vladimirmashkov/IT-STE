---
name: it-ste-w3-cycle
description: Execute exactly one bounded W3 pair from compact state through evidence, validation, review, and one authorized commit.
disable-model-invocation: true
---

# IT-STE W3 bounded-pair cycle

Use for exactly one coherent pair. The caller/input supplies pair scope, excluded meanings, evidence boundary, candidate-ID hints, allowlist, and authorization. This is not a vocabulary importer, approval workflow, release gate, publication workflow, or SFT authorization.

## State machine

Read `current.json` with `show --compact`, one input, and only its selectors. If no exact pair/input exists, return `needs-scope`; never recover by reading the full W3 note or history. Then run these stages once, in order:

`begin → baseline → ASD doctor → canonical counts/queue → bounded question → selected records/entries → direct competent sources → active note → justified draft records → checkpoint/manifest sync → generated build → affected+standard checks → complete Git review → output/finish → one commit if authorized`.

For the current ITIL pair inventory, maintain exactly `docs/it-ste-research/W3-itil-service-management.md` in place; keep all details in that active note and canonical records, with one exact next action and no duplicate history note. Keep stdout, full diffs, and inventory under `.local/it-ste-state/<run-id>/`. Do not read generated Markdown, all vocabulary batches, ASD extraction, SQLite payload, or private PDF merely to resume.

## Evidence/change rules

- Authenticate ASD and preserve Issue, revision, PDF hash, physical/printed page, locator, warnings, and no-ASD-provenance status for original IT terms. Inspect a PDF page only when layout matters.
- Use current official/primary/specialist sources; fetch them directly and record scope/version/competence/limits. Separate source facts from inference and compare alternatives.
- Materialize only distinct justified original terms under the existing contract, normally `status: draft`, `origin: original`, `usage: restricted`, project-only rights, and no copied protected text. Do not add schema fields, relations, multi-sense structures, ASD provenance, or duplicate IDs.
- Update only the active note, current checkpoint, W3 plan boundary, manifest/summaries/tests when required, justified source/term records, and generated output. Never edit generated Markdown by hand or touch private/ignored artifacts.
- A blocked pair may record a meaningful note/checkpoint result but must not be forced into a term or cosmetic commit. The next action must be exact.

Use the compact protocol for checks and output. Review all changes under `AGENTS.md`; commit explicit paths only when `input.authorization.auto_commit` is true. Report pair/IDs/boundaries, evidence refs/limits, counts/queue, validation statuses, changed paths, commit/blocker, next pair, and no-approval/no-release statement.
