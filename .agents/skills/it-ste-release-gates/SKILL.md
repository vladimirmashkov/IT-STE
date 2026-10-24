---
name: it-ste-release-gates
description: Execute one bounded IT-STE release-readiness gate for rights/provenance, language coverage, or independent dataset quality, recording blockers and evidence with one logical explicit-path commit; never publish or infer approval.
disable-model-invocation: true
---

# IT-STE release-readiness gates

Use only under `it-ste-release-readiness` or for an explicitly requested single gate scope. Valid scopes are `rights`, `language`, and `dataset`. This skill records readiness evidence; it does not publish, approve vocabulary, mutate the release catalog, or authorize SFT.

## Preconditions

- Read `AGENTS.md`, the Current checkpoint in `docs/it-ste-draft-handoff.md`, the Current checkpoint in `docs/it-ste-release-readiness-plan.md`, and only the active gate note.
- Require a clean branch/worktree baseline and explicit user authorization for automatic commits.
- Run ASD `doctor`, canonical vocabulary check, and the relevant structural checks before making a gate decision.
- Stop if the gate needs a schema, relation, source-policy, language-policy, or owner decision that the current contract cannot express.

## Gate scopes

### Rights and provenance

Audit the manifest, all referenced source metadata, external URL/version/status/scope, downstream rights, ASD derivative permission, project-only rights, copied text, private PDF/rendering exclusion, generated output, and source-reference consistency. Unknown rights are blockers unless an owner records an explicit restriction or replacement decision.

### Language coverage

Record authoritative language, required release languages, translation inventory, review status, equivalence review, and the meaning of `partial` coverage. Do not invent translations or schema fields. If the proposed release is English-only, record that scope explicitly and obtain the required owner decision rather than treating it as implicit approval.

### Dataset/quality

Audit reproducibility, manifest/hash consistency, draft leakage, private material exclusion, license scope, generated-output consistency, evaluation split/quality requirements, and independent review. The correct result may be `not authorized` or `blocked`; never infer SFT readiness from passing tests.

## Execution stages

1. State one gate question, scope, criteria, evidence needed, and stop condition in one active note, normally `docs/it-ste-research/release-readiness-gates.md`.
2. Inspect only relevant files and directly fetched competent sources. Record facts versus inference and limitations.
3. Update the gate note and the release-readiness plan checkpoint with `pass`, `blocked`, or `needs-owner-decision`. Do not set an approved release status in canonical data.
4. Run affected checks, adaptation, corpus, vocabulary, document build/check, tests, ASD doctor, diagnostics, and `git diff --check`.
5. Review the complete inventory and commit only the gate note/plan/checkpoint and justified metadata/test changes with explicit paths. Do not create a cosmetic commit when no meaningful state changed.
6. Verify full hash, exact paths, clean worktree/index, counts, and queue before the next gate.

## Stop rules

A missing rights grant, incomplete translation review, unresolved vocabulary approval, failed independent quality criterion, unavailable source, failed validation, or ambiguous ownership stops the gate. Preserve the blocker and exact next action. Do not update `catalog.json`, publish, or create a release candidate from a blocked gate.

## Final report

Report in Russian: gate scope/result, inspected evidence and limitations, blockers/owner decisions, changed files, validations, commit hash/message/paths or safe uncommitted command, ignored artifacts, next gate, and explicit no-release/no-publication/no-SFT statement.
