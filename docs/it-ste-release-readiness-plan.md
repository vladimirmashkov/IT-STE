# IT-STE draft completion and release-readiness plan

This plan governs the branch `remediation/release-readiness`. It is an execution plan, not approval authority, a release declaration, ASD guidance, conformance evidence, or SFT authorization.

## Current checkpoint

- Base state: W3 ITIL/service-management inventory is bounded and complete through `ITSTE-T-0018`; the branch starts from commit `99c1091`.
- Canonical state: recomputed for the current W2 slice as 2,196 ASD records across 55 batches; `120 allowed`, `1,510 restricted`, `407 prohibited`, `159 not-applicable`, `0 needs-review`; offset-0 queue is empty. These are structural draft dispositions, not approval.
- Draft state: 31 canonical rules and 18 original IT-only terms remain `draft`; canonical English coverage is `partial`; external PeopleCert metadata is `reference-only`; the release catalog is unreleased.
- Active phase: Phase 2 vocabulary review gate after W2 editorial work completed as draft. Vocabulary validation is complete through batch `009`; each bounded slice remains draft-only and recorded in the release-readiness state, while W2 completion and the empty structural queue are not approval signals.
- Exact next action: run `it-ste-release-readiness resume` to select vocabulary batch `010` (selector cursor `9`). Batch `009` affected, exact-entry, authenticated source, adaptation, corpus, aggregate vocabulary, document, and full-suite checks pass; these remain structural draft checks only. Do not treat them or an empty offset-0 queue as vocabulary approval or release; do not begin a release candidate until Phases 1–5 have recorded passing gates.
- State source: `docs/it-ste-state/current.json`, `selector.json`, and the selected run input/output, plus only selectors named by that input. Do not reconstruct progress from chat history or scan the full plan/history.

## Objective

Finish the draft remediation in bounded, reviewable slices and produce a release candidate only when the independent gates below pass. Preserve the distinction between:

1. research and editorial draft work;
2. semantic vocabulary review;
3. rights, provenance, and translation gates;
4. release-candidate packaging; and
5. separately authorized publication or approval.

## Non-goals

- Do not silently approve vocabulary or change `status: draft` to an approved status.
- Do not present structural checks as semantic approval, conformance, publication, or SFT readiness.
- Do not alter ASD source rows, source extraction, fixed source sequence, private PDFs, or ignored renderings as part of release preparation.
- Do not add schema fields, relations, multi-sense structures, release fields, translations, or source-policy changes merely to make a gate pass. Stop and record an owner decision when the existing contract is insufficient.
- Do not update the release catalog or publish a release until the release-candidate gate and explicit release authorization are complete.

## Phased execution

### Phase 0 — Bootstrap and recovery

- Verify branch, clean worktree/index, current checkpoint, canonical counts, ASD authentication, and the skill set.
- Ensure the main orchestrator and its supporting skills exist without overwriting local work.
- Record the active phase and exact next bounded slice in this plan.
- Commit only plan/skill bootstrap changes in one explicit-path commit.

### Phase 1 — W2 editorial and technical review

Use `it-ste-w2-editorial-slice`. Process one coherent thematic slice per iteration, normally two to five rules or terms plus only their directly affected references. Select the slice from the manifest and current checkpoint, not from a guessed offset.

Review, as applicable:

- lexical admission, POS, alternatives, and rule/term consistency;
- grammar, modality, actors, conditions, sequencing, and executable units;
- safety/security consequences, protective context, literals, and measurable limits;
- examples, negative examples, domain scope, and cross-record contradictions;
- source-facet completeness, rights scope, and generated-document consistency.

Each completed slice gets one compact W2 note/checkpoint update, the affected validations, a complete review, and one logical commit. Keep unresolved editorial questions explicit.

### Phase 2 — Vocabulary review gate

Use `it-ste-vocabulary-gate-slice`. Review one explicit canonical batch/theme group at a time. Recompute the queue before each group and inspect exact ASD entries only for relevant collisions. Do not force a disposition to make the queue empty, and do not treat an empty queue as approval.

Each group records:

- exact batch paths and entry IDs;
- source facts, external evidence, editorial inference, and limitations;
- old/new draft disposition where a justified change is made;
- unresolved owner or policy decisions;
- affected checks and one exact next group.

A vocabulary gate is complete only after all required groups have an explicit reviewed result and a separate human approval decision is recorded outside structural validation.

### Phase 3 — Rights and provenance gate

Use `it-ste-release-gates` for a bounded rights/provenance audit:

- ASD derivative permission and attribution boundaries;
- original IT-STE wording/example rights;
- every external source metadata record, URL, version/status, scope, and downstream rights;
- absence of copied protected source text;
- manifest/source-reference consistency;
- generated artifacts and private local material exclusion.

Unknown downstream rights remain blockers for public release unless the responsible owner records an accepted restriction or replaces the source with a permitted one.

### Phase 4 — Translation and language gate

Use `it-ste-release-gates` for language coverage. Confirm which languages are required for the proposed release, whether translations are reviewed, whether English is authoritative, and whether the existing contract can represent the result. Do not add translation records or schema fields without an explicit contract decision. `language_coverage: partial` is not a release approval.

### Phase 5 — Independent dataset and quality gate

Use `it-ste-release-gates` for reproducibility, dataset scope, license/rights, leakage of private material, generated-output consistency, and independent review of any proposed training/SFT view. This gate may conclude that no dataset or SFT artifact is authorized. It must never infer SFT readiness from passing repository checks.

### Phase 6 — Release-candidate packaging

Use `it-ste-release-candidate` only after Phases 1–5 have passing recorded gates and the user explicitly requests a candidate. First inspect the repository's release/catalog tooling and current contract; do not guess commands or mutate the catalog. Produce a separately labeled candidate with reproducible hashes, complete manifest/source inventory, rights/provenance report, reviewed language status, and explicit remaining limitations.

A release candidate is not a published release. Catalog mutation, publication, or approval requires a separate explicit authorization and a fresh final review.

## Commit policy

- Automatic commits are allowed only when the user explicitly authorizes them for the current run.
- The main skill runs phases strictly sequentially. Never parallelize slices that could edit the same note, manifest, generated document, tests, or checkpoint.
- One bounded editorial/vocabulary/gate slice equals at most one logical commit. Do not create cosmetic commits with no reviewed state change.
- Commit messages are short English imperatives, preferably 50 characters or fewer, and describe the actual work, for example `Review rule actor boundaries` or `Record source rights gate`.
- Stage only explicit reviewed paths with `git add -A -- ...`; commit with `git commit --only -m ... -- ...`.
- After every commit verify the full hash, exact paths, clean worktree/index, diagnostics, and current counts.
- Never include pre-existing, mixed, unrelated, staged, deleted, renamed, binary, mode, submodule, PDF, rendering, secret, or ignored-local changes.

## Stop conditions

Stop the current run without staging or committing when:

- the baseline is not clean or ownership is ambiguous;
- ASD authentication, source access, diagnostics, validation, or document generation fails;
- a decision requires a schema, relation, source-policy, language-policy, or owner change;
- evidence is insufficient and no bounded unresolved result can be recorded;
- a rights, translation, vocabulary, or dataset gate is blocked;
- the release catalog or publication tooling would need to be changed without explicit authorization.

Preserve the checkpoint and exact resume action. Do not reset, stash, hide, overwrite, or weaken the validator to continue.

## Completion criteria

The draft-remediation program is complete only when the repository contains:

- reviewed W2 results for all required rules and draft terms;
- explicit vocabulary review/approval records for the proposed release scope;
- passing rights/provenance and language gates;
- an independent dataset/quality decision;
- a reproducible release-candidate report;
- a separately authorized decision on publication/catalog status.

Until all criteria are met, report the state as draft or release-readiness-in-progress and do not claim approval, release, publication, conformance, or SFT readiness.
