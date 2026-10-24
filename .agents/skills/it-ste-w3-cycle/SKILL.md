---
name: it-ste-w3-cycle
description: Run one interruption-safe IT-STE W3 bounded-pair cycle through resume, evidence, draft materialization, validation, final review, and one explicit-path automatic commit; use only for a user-authorized single pair.
disable-model-invocation: true
---

# IT-STE W3 bounded-pair cycle

Use this skill for exactly one coherent W3 pair in the IT-STE repository. The caller must provide the pair scope, excluded meanings, evidence boundary, and any candidate IDs only as hints. This is an execution protocol, not a vocabulary importer, approval workflow, release gate, publication workflow, or SFT authorization.

Keep research content in the repository's active note and canonical records. Do not put term definitions, web quotations, or source payloads into this skill. The repository is the resumable state store; the chat transcript is not required for recovery.

## Preconditions

- Read the repository `AGENTS.md` before editing.
- Read only the Current checkpoint in `docs/it-ste-draft-handoff.md`, the relevant bounded sections of `docs/it-ste-research-method.md`, the current W3 section of `docs/it-ste-draft-remediation-plan.md`, and the active W3 note linked by the checkpoint.
- Use one pair and one logical commit. Do not start another pair in the same run.
- The user must explicitly authorize automatic commits for this run. If authorization is absent, leave changes unstaged and provide the safe command instead.
- Treat a nonignored baseline change as a safety stop unless it is an unambiguous partial implementation of this exact pair and every affected file is wholly owned by this run.

## Fourteen-stage execution contract

Complete these stages in order. Record interruption-safe state in the existing active note and Current checkpoint; do not create a duplicate history note.

### 1. Resume from the repository

Read the bounded startup material only. Identify the exact pair, current checkpoint, previous slice, next action, and allowed paths. Do not read generated Markdown, all vocabulary batches, the complete ASD extraction, the SQLite payload, or the private PDF merely to resume.

### 2. Capture and classify the baseline

Run and inspect all required startup views:

```sh
git --no-pager --no-optional-locks status --short --untracked-files=all
git --no-pager diff --find-renames
git --no-pager diff --cached --find-renames
git --no-pager diff --name-status --find-renames
git --no-pager diff --cached --name-status --find-renames
```

Record whether the baseline differs from the checkpoint. Preserve unrelated, mixed, deleted, renamed, binary, mode, submodule, staged, and ambiguous changes; do not reset, stash, hide, overwrite, or commit them.

### 3. Authenticate ASD before using ASD evidence

Run:

```sh
python3 tools/asd_ste100_local.py doctor
```

Keep ASD Issue, revision, authenticated source PDF SHA-256, derivative database identity, and the fact that original IT-only terms receive no ASD provenance.

### 4. Recompute canonical state

Run the full canonical vocabulary check and recompute the offset-0 `needs-review` queue through the repository API. Use compact JSON where possible. Record total records, batches, all disposition counts, queue size, and next pointer. Treat checkpoint counts and offsets as historical pointers, not authority. An empty queue is not approval.

### 5. Freeze one bounded question

State one concrete question for the pair. Define included senses, POS candidates, named actors/objects, rejected meanings, and stop conditions. Do not promise materialization or allocate IDs before evidence supports separate bounded senses. Stop or record `blocked`/`needs-review` if a source, policy, schema, relation, multi-sense, or owner decision is missing.

### 6. Inspect only relevant canonical and ASD evidence

Retrieve only the existing canonical records needed for the boundary and exact ASD entries for real lexical collisions. Search canonical batches before retrieving entries. Use full canonical batch paths for affected checks later. Preserve exact IDs, POS, physical PDF pages, printed pages, warnings, fixed retrieval locators, and source hashes. Render an authenticated PDF page only when row boundaries, typography, wrapping, or columns matter. Never stage or publish the PDF or renderings.

### 7. Inspect competent external evidence

Use short targeted discovery and fetch the actual source pages. Prefer current official standards, official product/framework documentation, or competent specialist sources with clear version/status and scope. Record title, publisher, URL, access date, version/status, relevant section, finding, competence/applicability, and limitation. Search snippets, AI summaries, guessed URLs, inaccessible pages, copied glossary text, and marketing claims outside their scope are not evidence. Separate source facts from editorial inference and compare plausible alternatives, including keeping the candidate unresolved.

### 8. Update the active research note

Maintain exactly the active note `docs/it-ste-research/W3-itil-service-management.md`. Update it in place with state, exact pair scope, canonical paths/IDs, ASD collision evidence and visual findings or an explicit not-applicable statement, directly inspected sources, alternatives, rejected boundaries, facts versus inference, unresolved questions, actual validation results, and one exact next action. If interrupted, leave a precise `Last completed step` and resume action in the note rather than relying on chat history.

### 9. Materialize only justified draft records

When evidence supports distinct senses, create only the required original IT-STE term/source records under the existing `schema_version: 1.1.0` contract. Keep terms `status: draft`, `origin: original`, normally `usage: restricted`, with original wording/examples, project-only rights, and external ITIL metadata only. Do not add fields, relations, multi-sense structures, ASD provenance, source sequence numbers, or copied protected source text. If evidence is insufficient, record the bounded candidate as unresolved or blocked instead of forcing a term.

### 10. Synchronize canonical metadata and checkpoints

Update only what the bounded change requires:

- snapshot `manifest.json`;
- English/Russian canonical contract summaries when canonical term counts change;
- the current W3 boundary in `docs/it-ste-draft-remediation-plan.md`;
- the Current checkpoint in `docs/it-ste-draft-handoff.md`;
- affected test expectations.

Do not edit `docs/IT-STE-draft.md` manually. Preserve the fixed ASD plan pins and all unrelated records.

### 11. Regenerate derived output

Run the document tool's build command after canonical changes. Never hand-edit generated Markdown. The generated file is a derived editorial view, not an independently editable standard or release.

### 12. Validate the bounded slice and the repository

Run the affected full-path batch check first whenever a lexical collision or ASD batch was inspected, then run:

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

Refresh project diagnostics. Recompute the offset-0 queue and all disposition counts after edits. Record every result, including failures and corrected commands, in the note and checkpoint. Structural checks do not establish semantic approval, release readiness, publication, conformance, or SFT readiness.

### 13. Perform the complete final review

Before staging, repeat the complete status, unstaged/staged diff, and name-status inventory. Read every added/untracked file. Inspect generated and documentation diffs, file types/modes, binary and submodule state, deletions and renames, and compare the final inventory with the startup baseline. Verify that only explicit reviewed paths belong to this run and that no PDF, rendering, secret, ignored local artifact, unrelated staged path, or mixed file is included.

### 14. Commit exactly once and verify recovery state

Only after validation and review pass, stage explicit paths and create one commit:

```sh
git add -A -- <explicit-reviewed-paths>
GIT_EDITOR=true git commit --only -m "<imperative message <=50 chars>" -- <explicit-reviewed-paths>
```

Do not use `git add .` or pathless `git add -A`. After a successful commit, verify the hash, exact committed paths, clean worktree/index, final diagnostics, and document check. If any safety condition fails, do not stage or commit; preserve all work and report the exact blocker with a copy-ready selective command.

## Allowed and forbidden changes

The normal successful materialization allowlist is the active W3 note, Current checkpoint, W3 plan boundary, manifest, justified new term/source records, English/Russian canonical summaries, affected tests, and generated Markdown. Do not modify unrelated rules, ASD vocabulary batches, source extraction, catalog releases, private PDFs, renderings, secrets, or ignored local artifacts.

## Required final report

Report in Russian. Include the baseline and checkpoint comparison; exact pair/IDs/POS/boundaries; sources and limitations; ASD evidence; canonical counts and queue; every validation result including failures; complete changed/new-file inventory and ignored artifacts; unresolved questions and exact next pair; automatic commit hash/message/paths or safety blocker; reviewed changes left out; and an explicit statement that no vocabulary approval, release, publication, conformance, or SFT readiness was claimed.
