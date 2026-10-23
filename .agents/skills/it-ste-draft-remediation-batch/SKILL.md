---
name: it-ste-draft-remediation-batch
description: Run a parameterized sequential batch of IT-STE draft remediation slices, with fresh queue/checkpoint state, validation, review, and one safe automatic commit per completed iteration.
disable-model-invocation: true
---

# IT-STE draft remediation batch

Use this skill only when the user explicitly requests multiple sequential IT-STE remediation iterations. It is a batch wrapper around the single-slice contract in `../it-ste-draft-remediation/SKILL.md`; do not invoke the other skill as a nested slash command.

## Invocation and count

Accept exactly one positive integer iteration count from the user message:

```text
/it-ste-draft-remediation-batch 10
/it-ste-draft-remediation-batch --iterations=100
```

Interpret the count as the number of bounded research slices, not the number of records. Accept `1` through `100`; reject zero, negative, missing, non-integer, or larger values before changing files. If the count is missing or invalid, ask for a valid count and stop.

Run iterations strictly sequentially. Never start parallel iterations, and never begin iteration N+1 until iteration N has completed its evidence, checks, checkpoint update, final review, automatic commit, and post-commit clean-worktree check.

## Startup safety

Before iteration 1:

1. Read `AGENTS.md`, only the Current checkpoint in `docs/it-ste-draft-handoff.md`, `docs/it-ste-research-method.md`, and only the active note(s) linked by the checkpoint.
2. Capture the baseline worktree and index with the required Git status, diff, and name-status views.
3. Require a clean tracked/staged/untracked worktree before starting. Ignored `.local/` source PDFs and renderings are allowed; any nonignored pre-existing change is a safety stop. Do not hide, reset, stash, overwrite, or commit pre-existing work.
4. Run the authenticated source doctor and recompute canonical counts and the offset-0 queue. The checkpoint is a pointer, not authority over canonical data.

## One iteration

For each iteration:

1. Start from the just-written Current checkpoint and recompute the live queue from offset 0. Do not reuse stale IDs, offsets, counts, pages, batches, or cached context from the previous iteration.
2. Select exactly one bounded active-workstream slice: normally one authenticated physical PDF page and no more than two related canonical records. Do not expand the slice to fill the batch count.
3. Retrieve only the selected canonical records and exact ASD source entries. Verify the authenticated PDF page visually when layout matters; preserve Issue, revision, page, PDF hash, source pins, warnings, raw metadata, and historical ambiguity evidence.
4. For substantive IT meaning, inspect short targeted competent primary/expert sources. Compare alternatives and separate source facts from editorial inference. If evidence is insufficient, record `blocked` or `needs-review`; never force a disposition.
5. Create or update exactly one compact research note for the slice. Apply only justified draft changes to the selected canonical records. Preserve IDs, sequence, fixed retrieval locators, rights, `status: draft`, and `review_status: editorial-review-needed`; never hand-edit generated Markdown.
6. Run the affected batch check first, then the wider validation required by the handoff:

   ```sh
   python3 tools/it_ste_vocabulary.py check --batch <canonical-batch> --compact-json
   python3 tools/it_ste_adaptation.py check
   python3 tools/it_ste_corpus.py check
   python3 tools/it_ste_vocabulary.py check --compact-json
   python3 tools/it_ste_document.py build
   python3 tools/it_ste_document.py check
   python3 -W error::ResourceWarning -m unittest discover -s tests
   python3 tools/asd_ste100_local.py doctor
   ```

   Also run project diagnostics and `git diff --check`.
7. Recompute counts and queue after the edits. Update the Current checkpoint with the completed slice, note, actual validation, unresolved blockers, exact next action, and next live-queue slice.
8. Perform the complete required worktree/index review before any staging. Read all new/untracked content, inspect every diff, and distinguish this iteration from the iteration baseline.
9. If the slice is safely complete, automatically commit only the files changed by this iteration. Use explicit paths and one commit per iteration:

   ```sh
   git add -A -- <reviewed-iteration-paths>
   GIT_EDITOR=true git commit --only -m "<imperative message <=50 chars>" -- <reviewed-iteration-paths>
   ```

10. Verify the commit hash, exact committed paths, and a clean worktree/index before starting the next iteration.

A blocked or `needs-review` slice may count as a completed iteration only when its note/checkpoint and any justified canonical evidence changes are validated, reviewed, and safely committed. Do not create a cosmetic commit with no meaningful reviewed change.

## Stop conditions

Stop immediately and report the completed count and reason if any of these occurs:

- the starting worktree is not clean;
- a pre-existing or unrelated change overlaps a file needed by the current iteration;
- a validation, diagnostics, source authentication, or commit step fails and cannot be fixed safely;
- a source or PDF needed for the selected decision is unavailable and no bounded blocked result can be recorded;
- the queue has no eligible next slice;
- a user change appears between iterations;
- the requested count is reached.

Never continue past a failed commit, failed validation, unexpected diff, or ambiguous ownership boundary just to reach the requested count.

## Automatic commit boundaries

Automatic commits are authorized by this skill, but only after the full review of that iteration. Never include:

- pre-existing user changes;
- mixed files whose existing edits cannot be separated safely;
- ASD PDFs, PDF renderings, secrets, ignored local artifacts, unrelated staged paths, or accidental deletions/renames/binary/mode/submodule changes.

Use no blanket `git add .` or pathless `git add -A`. If a safety condition fails, do not stage or commit; preserve the worktree and report a copy-ready selective command instead. Do not release, publish, approve vocabulary, or claim SFT readiness.

## Final report

Report in Russian and include:

- requested iteration count and completed/committed count;
- each iteration's IDs/pages, disposition changes, note, validation result, commit hash, and paths;
- any blocked, skipped, or stopped iterations and exact reasons;
- final recomputed counts and offset-0 queue/next action;
- external sources actually inspected and limitations;
- complete final worktree/index inventory and ignored temporary artifacts;
- confirmation that no approval, release, publication, or SFT readiness was claimed.

Do not perform a release or a final aggregate commit. Each successful iteration must remain an independently reviewed commit.
