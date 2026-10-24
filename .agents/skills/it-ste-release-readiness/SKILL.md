---
name: it-ste-release-readiness
description: Orchestrate the IT-STE draft-completion and release-readiness program through sequential bounded W2, vocabulary, rights, language, dataset, and release-candidate slices with explicit multi-commit boundaries; never infer approval or publish automatically.
disable-model-invocation: true
---

# IT-STE release-readiness orchestrator

Use this project-local skill only when the user explicitly asks to continue the IT-STE draft-completion or release-readiness program on `remediation/release-readiness`. The repository is the resumable state store. This skill coordinates the supporting skills in this directory; it does not replace their evidence rules and does not authorize publication, vocabulary approval, conformance, or SFT readiness.

## Invocation contract

Accept one explicit mode:

```text
/it-ste-release-readiness bootstrap
/it-ste-release-readiness resume
/it-ste-release-readiness resume --iterations=3
/it-ste-release-readiness --phase=w2 --iterations=3
/it-ste-release-readiness --phase=vocabulary --iterations=1
/it-ste-release-readiness --phase=gates --scope=rights
/it-ste-release-readiness --phase=candidate
```

- `bootstrap` validates/creates the supporting skills and records the plan state; it does not start a remediation slice.
- `resume` reads the plan and handoff checkpoints, skips only work explicitly recorded as completed, selects the next unfinished phase/slice, and runs one bounded slice by default. `--iterations=N` repeats that process strictly sequentially, stopping at the first blocker.
- `w2`, `vocabulary`, and `gates` require a positive bounded iteration count or one explicit bounded scope.
- `candidate` is refused unless the plan records passing Phases 1–5 and the user explicitly requests a release candidate.
- Do not accept an unbounded `run all` request without converting it into explicit sequential phases and iteration counts recorded in the plan.
- The current user authorization permits multiple automatic commits for the requested run, but every future run must still verify explicit authorization in the invocation/context.

Supporting skills:

- `../it-ste-w2-editorial-slice/SKILL.md`
- `../it-ste-vocabulary-gate-slice/SKILL.md`
- `../it-ste-release-gates/SKILL.md`
- `../it-ste-release-candidate/SKILL.md`

If a supporting skill is missing, create it from the repository's planned contract only after confirming the worktree is clean. Never overwrite an existing skill or silently change its scope. Report bootstrap creation as its own logical commit.

## Mandatory startup

1. Read `AGENTS.md`, only the current checkpoint in `docs/it-ste-draft-handoff.md`, the current checkpoint in `docs/it-ste-release-readiness-plan.md`, the relevant bounded sections of `docs/it-ste-draft-remediation-plan.md` and `docs/it-ste-research-method.md`, and only active notes linked by those checkpoints.
2. Require branch `remediation/release-readiness`; stop and report if the branch differs.
3. Capture and inspect the complete baseline:

   ```sh
   git --no-pager --no-optional-locks status --short --untracked-files=all
   git --no-pager diff --find-renames
   git --no-pager diff --cached --find-renames
   git --no-pager diff --name-status --find-renames
   git --no-pager diff --cached --name-status --find-renames
   ```

4. Require a clean nonignored worktree/index before the first slice and after every committed slice. Preserve any user work; do not reset, stash, hide, overwrite, or commit it.
5. Run `python3 tools/asd_ste100_local.py doctor` and `python3 tools/it_ste_vocabulary.py check --compact-json`. Record the final counts and offset-0 queue.
6. Validate that the supporting skills, plan, manifest, and checkpoints agree. A disagreement is a stop condition until recorded and resolved.

## Sequential stage loop

Run exactly one bounded stage at a time. Never begin stage N+1 before stage N has evidence, validation, full diff review, one explicit-path commit, and post-commit clean recovery.

### A. Select and delegate

- Read the relevant supporting skill in full before acting.
- In `resume` mode, inspect the plan/checkpoint and skip only phases/slices with an explicit completed result and commit; never infer completion from an empty queue or a passing structural check.
- Select one exact W2 theme, vocabulary batch/theme group, gate scope, or candidate scope. If the next slice cannot be selected without guessing, stop and ask for an explicit bounded scope.
- Record IDs/paths, excluded meanings, evidence boundary, expected allowed paths, and one next action in the plan/checkpoint before editing.
- Do not reuse stale queue offsets, counts, IDs, or cached chat context.

### B. Execute the bounded slice

Follow the supporting skill's evidence method. Inspect only selected canonical records, exact ASD entries, and directly relevant competent external sources. Distinguish source facts from editorial inference. Leave insufficient evidence blocked or unresolved.

### C. Validate and update state

Run the affected check first, then the required wider checks:

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

Refresh diagnostics, recompute the offset-0 queue/counts, and update the active note, `docs/it-ste-draft-handoff.md`, and `docs/it-ste-release-readiness-plan.md` with actual results. Never hand-edit generated Markdown.

### D. Review, commit, recover

Before staging, review the entire worktree/index and all name-status views. Read every new/untracked file and inspect generated/docs diffs, file type/mode, binary/submodule, rename/deletion, and ignored-local state. Stage only explicit paths wholly owned by this slice:

```sh
git add -A -- <explicit-reviewed-paths>
GIT_EDITOR=true git commit --only -m "<imperative message <=50 chars>" -- <explicit-reviewed-paths>
```

Use one logical commit per completed bounded slice. Do not create a final aggregate commit. Verify full commit hash, exact paths, clean worktree/index, diagnostics, document check, and counts before continuing.

## Phase boundaries

- Phase 1 may change draft rules/terms, notes, checkpoints, affected tests, summaries, and generated Markdown; it may not approve or release.
- Phase 2 may review vocabulary batches and record draft dispositions; it may not claim vocabulary approval without the separate human gate.
- Phase 3–5 may produce gate reports and justified metadata/checkpoint changes; unknown rights or missing language/quality decisions remain blockers.
- Phase 6 may create a release-candidate report only after all prior gates pass and the user explicitly requests it. It must not publish or mutate the catalog without separate authorization.

## Stop conditions

Stop without staging/committing if baseline ownership is ambiguous, evidence is unavailable, authentication/validation/diagnostics fail, a contract/schema/policy change is required, or any release gate is blocked. Preserve exact resume state and provide a safe selective command. Never weaken validation or claim that an empty queue is approval.

## Final report

Report in Russian: phase and bounded slices completed; records and evidence; sources/limitations; counts and queue; every validation result/failure; complete changed-file and ignored-artifact inventory; each commit hash/message/exact paths; blocked gates and next action; reviewed changes left out; and explicit confirmation that no approval, release, publication, conformance, or SFT readiness was claimed unless a separately authorized gate truly established it.
