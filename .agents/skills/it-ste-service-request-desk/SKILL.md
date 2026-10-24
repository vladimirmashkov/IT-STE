---
name: it-ste-service-request-desk
description: Continue exactly one resumable W3 IT-STE slice for service request and service desk, using direct service-management evidence, draft-only term records when justified, checkpoint recovery, full validation, and one safe automatic commit.
disable-model-invocation: true
---

# IT-STE service request and service desk

Use this project-local skill only when the user explicitly asks to continue the next W3 slice for `service request` and `service desk`. This skill is intentionally limited to one related pair. It is not a bulk ITIL vocabulary importer, an approval workflow, a release gate, or SFT authorization. The current user authorization permits one automatic commit after a successful, fully reviewed run.

## Resume contract

The repository is the state store; do not require the new thread to reconstruct the chat transcript.

1. Read `AGENTS.md`.
2. Read only the **Current checkpoint** section of `docs/it-ste-draft-handoff.md`, the relevant bounded sections of `docs/it-ste-research-method.md`, the current W3 section of `docs/it-ste-draft-remediation-plan.md`, and the active note `docs/it-ste-research/W3-itil-service-management.md`.
3. Do not read the complete generated Markdown, all vocabulary batches, the complete ASD extraction, the SQLite payload, the private PDF, or historical handoff/research material merely to resume.
4. Capture the baseline before editing:

   ```sh
   git --no-pager --no-optional-locks status --short --untracked-files=all
   git --no-pager diff --find-renames
   git --no-pager diff --cached --find-renames
   git --no-pager diff --name-status --find-renames
   git --no-pager diff --cached --name-status --find-renames
   ```

5. If the baseline is clean, proceed. If nonignored changes exist, preserve them and classify ownership before editing:
   - resume only when every change, including any staged path, is clearly a partial implementation of this exact pair and belongs wholly to the allowed paths below;
   - preserve same-run staged changes without unstage/reset/overwrite; do not stage or commit them until the complete final review succeeds;
   - stop without resetting, stashing, hiding, overwriting, or committing when any unrelated, mixed, ambiguous, deleted, renamed, binary, mode, or submodule change is present;
   - distinguish the baseline inventory from changes created by this run.
6. If a prior partial run already created `ITSTE-T-0007` or `ITSTE-T-0008`, do not allocate duplicate IDs. Inspect the records, note, manifest, and checkpoint and continue from the recorded state. If the checkpoint already advances beyond this pair, do not repeat it without new evidence or an explicit user request.

## Bounded scope

The only active terms are:

- `service request`: candidate bounded sense — a user request for information, access, or a predefined service action;
- `service desk`: candidate bounded sense — a support function that receives, coordinates, and communicates service requests and incidents.

These are hypotheses, not decisions. The research must distinguish at least:

- a service request from an incident, problem, known error, workaround, or change;
- a service desk function from a team, ticket queue, tool, escalation authority, or approval authority;
- receiving/communicating a request from fulfilling or approving the requested action.

Likely next IDs are `ITSTE-T-0007` and `ITSTE-T-0008`, but allocate them only after the bounded evidence supports separate senses and POS choices. Do not promise materialization. If evidence is insufficient, leave the candidates unresolved or blocked and record the exact missing source or owner decision.

Do not research `configuration item`, `IT asset`, SLA/target, availability, resilience, change authority, release, deployment, API, protocol, cryptographic, runtime, UI, or physical meanings in this run.

## Evidence method

1. Run the authenticated source check before relying on ASD-derived data:

   ```sh
   python3 tools/asd_ste100_local.py doctor
   ```

   Preserve ASD Issue, revision, authenticated PDF SHA-256, and the fact that no ASD provenance is assigned to original IT-only terms.

2. Recompute canonical counts and the offset-0 `needs-review` queue from the canonical API. Treat checkpoint counts and pointers as stale if they differ. An empty queue does not mean vocabulary approval.
3. Retrieve only relevant current canonical terms, especially the existing `service`, `incident`, `problem`, `known error`, and `workaround` records when needed for boundaries. Search for lexical collisions in canonical ASD batches; retrieve exact ASD entries only for actual collisions. Do not modify ASD rows merely to add ITIL senses.
4. Inspect competent external evidence directly. Prefer an official ITIL/PeopleCert Service Request Management or Service Desk source, an applicable primary service-management source, or a competent specialist source with clear version/status and scope. Search snippets, AI summaries, guessed URLs, inaccessible pages, marketing claims outside their scope, and copied glossary text are not evidence. If a guessed URL returns 404, do not cite it as inspected evidence.
5. Record each inspected source with title, publisher, URL, access date, version/status, relevant section, finding, competence/applicability, and limitation. Separate source facts from editorial inference. Do not claim a complete official glossary definition when the public page is only a practice or course overview.
6. Reuse existing external source metadata only when its URL, version, scope, and inspected evidence actually support this pair. Add a new `reference-only` ITIL source metadata file only when a directly inspected source requires it. Keep downstream rights explicit/unknown where applicable. Never copy ASD source metadata or use an ASD source ID in a term record.
7. Use the existing term contract (`schema_version: 1.1.0`) without adding fields. Any required contract/schema, relation, multi-sense, or source-policy change is a stop condition, not a reason to weaken validation.

## Changes and interruption-safe state

Maintain exactly the active note `docs/it-ste-research/W3-itil-service-management.md`; do not create a duplicate history note. Update it in place with:

- state and exact pair scope;
- canonical paths/IDs actually inspected or created;
- ASD collision evidence and visual findings, or an explicit not-applicable statement;
- directly inspected external sources and limitations;
- alternatives, rejected boundaries, source facts versus inference, and the decision;
- unresolved questions;
- actual validation results;
- one exact next action.

If materialized, each new term must remain `status: draft`, `origin: original`, normally `usage: restricted`, use original IT-STE wording/examples and project-only rights, and reference only external ITIL metadata. Choose POS deliberately (`phrase` is plausible for a multi-word term, but evidence and grammar decide). Keep `service request` and `service desk` as separate records; do not merge them or add relations without an existing contract field.

Update the existing Current checkpoint in `docs/it-ste-draft-handoff.md` in place with the actual completed/blocked state, counts, validations, exact next action, and next W3 pair. Update the W3 plan boundary in `docs/it-ste-draft-remediation-plan.md` only as needed to mark this pair completed or blocked and identify the next exact slice. If the canonical term count changes, update the EN/RU canonical contract summaries and the manifest. Never edit `docs/IT-STE-draft.md` manually; regenerate it with the document tool.

Allowed paths for a successful materialization are limited to the active note, checkpoint, plan, manifest, new term/source records justified by this slice, canonical contract summaries, affected tests, and generated Markdown. Do not modify unrelated rules, ASD vocabulary batches, source extraction, catalog releases, or private/ignored artifacts.

## Validation

After edits, run the affected check first when an ASD batch was changed or a lexical collision was inspected; use the full canonical batch path, not a batch number:

```sh
python3 tools/it_ste_vocabulary.py check --batch <canonical-batch-path> --compact-json
```

Then run the wider checks:

```sh
python3 tools/it_ste_adaptation.py check
python3 tools/it_ste_corpus.py check
python3 tools/it_ste_vocabulary.py check --compact-json
python3 tools/it_ste_document.py build
python3 tools/it_ste_document.py check
python3 -W error::ResourceWarning -m unittest discover -s tests
python3 tools/asd_ste100_local.py doctor
git --no-pager diff --check
```

Refresh project diagnostics. Recompute the offset-0 queue and all disposition counts after edits. Record actual outputs, including failures and corrected command invocations, in the active note/checkpoint. Structural checks do not establish semantic approval, release readiness, publication, conformance, or SFT readiness.

## Mandatory final review and automatic commit

Before staging, run and inspect the complete inventory again:

```sh
git --no-pager --no-optional-locks status --short --untracked-files=all
git --no-pager diff --find-renames
git --no-pager diff --cached --find-renames
git --no-pager diff --name-status --find-renames
git --no-pager diff --cached --name-status --find-renames
```

Read every added/untracked file, inspect generated and documentation diffs, compare the final inventory with the startup baseline, and verify that no PDF, rendering, secret, unrelated staged path, deletion, rename, binary, mode, or submodule change is included. Do not stage until ownership is unambiguous.

When validation and review pass, automatically create exactly one commit for this bounded run. Use explicit paths only:

```sh
git add -A -- <explicit-reviewed-paths>
GIT_EDITOR=true git commit --only -m "<imperative message, <=50 chars>" -- <explicit-reviewed-paths>
```

Do not use `git add .` or pathless `git add -A`. If safety conditions fail, do not stage or commit; preserve all work and report the exact blocker with a copy-ready selective command. After a successful commit, verify the hash, exact committed paths, and a clean worktree/index.

## Final report

Report in Russian and include:

- baseline inventory and whether it differed from the checkpoint;
- whether `service request` and `service desk` were materialized or remain blocked, with exact IDs/POS/boundaries;
- external sources actually inspected and limitations;
- canonical queue/counts and every validation result, including failures;
- complete changed/new-file inventory and ignored temporary artifacts;
- unresolved questions and the exact next W3 slice;
- automatic commit hash, message, and exact paths, or the safety blocker and safe command;
- reviewed changes left out and why;
- explicit statement that no vocabulary approval, release, publication, or SFT readiness was claimed.
