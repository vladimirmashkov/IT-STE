---
name: it-ste-w2-editorial-slice
description: Run one bounded W2 editorial and technical review slice over selected IT-STE draft rules or terms, preserving evidence, updating the review note/checkpoint, validating generated output, and making one explicit-path automatic commit.
disable-model-invocation: true
---

# IT-STE W2 editorial slice

Use only under `it-ste-release-readiness` or when the user explicitly requests one bounded W2 slice. This is editorial/technical draft review, not vocabulary approval, release, publication, conformance, or SFT authorization.

## Scope

The caller must provide one explicit thematic slice, normally two to five manifest-listed rules or terms and only directly affected references. Do not review the entire draft in one run. Select records from the current manifest and checkpoint; record exact IDs and paths before editing.

Candidate themes include lexical admission/POS, actors and modality, conditions and sequencing, safety/security context, examples and negative examples, source-facet completeness, rights scope, or cross-record consistency. Do not change an ASD-derived row merely because an editorial slice finds a missing IT sense.

## Required method

1. Read `AGENTS.md`, the Current checkpoint in `docs/it-ste-draft-handoff.md`, the Current checkpoint in `docs/it-ste-release-readiness-plan.md`, the bounded sections of `docs/it-ste-research-method.md`, and only notes linked by the checkpoint.
2. Capture the full clean baseline with status, unstaged/staged diff, and name-status views. Stop for unrelated or mixed work.
3. Authenticate ASD and recompute canonical counts/queue before relying on source or checkpoint data.
4. Retrieve only selected canonical records and related rule/term references. Inspect competent primary/expert sources for substantive claims; directly fetch and record title, publisher, URL, date/version, section, finding, competence, and limitation.
5. Compare current wording with defensible alternatives, including leaving it unchanged. Separate source facts, editorial inference, unresolved owner decisions, and safety/security consequences.
6. Maintain one compact active note, normally `docs/it-ste-research/W2-editorial-review.md`, with state, exact slice, evidence, alternatives, decisions, uncertainty, validations, and one next action. Do not create duplicate history notes.
7. Apply only justified draft changes. Preserve schema, IDs, source pins, rights, `status: draft`, `review_status: editorial-review-needed`, and generated-output policy. Update affected tests/summaries only when necessary.
8. Build generated Markdown and run the affected check first when a vocabulary collision or batch was inspected, followed by adaptation, corpus, vocabulary, document check, unit tests, doctor, diagnostics, and `git diff --check`.
9. Recompute counts and queue; update the handoff and release-readiness plan with actual results.
10. Perform the complete final inventory review, read every new file, and commit exactly once with explicit paths if and only if all checks and ownership conditions pass.

## Allowed paths

Normal paths are the selected canonical rule/term records, one W2 note, handoff Current checkpoint, release-readiness plan checkpoint, manifest only when required, affected tests/summaries, and generated Markdown. Do not touch release catalog, private PDFs, renderings, source extraction, unrelated batches, or unrelated notes.

## Commit policy

Automatic commits require explicit user authorization. Use an imperative message of 50 characters or fewer, for example `Review rule actor boundaries`. Never use blanket staging. After commit verify hash, exact paths, and clean recovery state. A blocked editorial question may be recorded and committed as a meaningful state change; do not create cosmetic commits.

## Final report

Report in Russian with selected IDs, findings, sources/limits, changes, unresolved questions, validations, exact commit/path inventory, ignored artifacts, next W2 slice, and an explicit no-approval/no-release statement.
