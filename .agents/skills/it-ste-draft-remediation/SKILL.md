---
name: it-ste-draft-remediation
description: Continue the IT-STE draft vocabulary remediation in one bounded W1/W2/W3 research slice, preserve canonical provenance, validate the authenticated ASD source, update the handoff, and automatically commit only the reviewed changes from this run.
---

# IT-STE draft remediation

When this skill is invoked in the IT-STE repository, continue the draft remediation workflow defined by `AGENTS.md` and the current checkpoint. Do not ask the user to repeat the standing assignment. This skill has explicit permission to create one safe commit at the end of a successful run, but never to include unrelated or pre-existing user work.

## Startup and scope

1. Read `AGENTS.md`.
2. Read only the **Current checkpoint** section of `docs/it-ste-draft-handoff.md`, `docs/it-ste-research-method.md`, and the research note(s) linked by the checkpoint. Do not read the historical handoff sections, generated Markdown, all vocabulary batches, or the complete source extraction merely to find the next task.
3. Recompute the canonical queue from offset 0 using the repository's canonical validation API. Treat the checkpoint, IDs, pages, batches, offsets, and counts as stale if they differ from canonical data; record any mismatch.
4. Execute exactly one bounded active-workstream slice, normally one authenticated physical PDF page and no more than two related records. Do not expand the slice without a demonstrated need. Leave unresolved questions `blocked` or `needs-review` rather than forcing a decision.

## Evidence and research

For the selected slice:

- Retrieve only the selected canonical record(s) and their exact ASD source entries.
- Run `python3 tools/asd_ste100_local.py doctor` before relying on the derivative source. Keep Issue, revision, physical PDF page, and authenticated PDF SHA-256 with the evidence.
- Verify row boundaries, spelling, POS, wrapping, columns, and layout against the authenticated PDF. Render only the cited page under ignored `.local/review-images/` when visual inspection is required; never publish or stage the PDF or rendering.
- For substantive IT meaning, use short targeted web searches and inspect competent primary or expert sources. Compare the current wording with reasonable alternatives, record limitations, and distinguish source facts from editorial inference.
- Do not cite search snippets, uninspected pages, AI summaries, or inaccessible sources as verified evidence.
- Do not claim vocabulary approval, release readiness, canonicalization, or SFT readiness.

## Changes

Create or update exactly one compact note in `docs/it-ste-research/`, following the format in `docs/it-ste-research-method.md`. Include state, scope, exact canonical paths/IDs, ASD evidence and visual findings, inspected external sources with URLs/access date/findings/limits, alternatives and decision, uncertainty, applied validation, and one exact next action.

Apply only justified draft changes to the selected canonical records. Preserve IDs, sequence, source pins, fixed retrieval commands, warnings, rights, raw metadata, historical ambiguity evidence, `status: draft`, and `review_status: editorial-review-needed`. Do not add schema fields, change fixed external retrieval locators, or edit generated Markdown by hand. Update affected test expectations and generated output only when required by canonical changes.

## Validation and checkpoint

After edits:

1. Run the affected batch check first:
   `python3 tools/it_ste_vocabulary.py check --batch <canonical-batch> --compact-json`
2. Run the wider validation required by the handoff:
   `python3 tools/it_ste_adaptation.py check`
   `python3 tools/it_ste_corpus.py check`
   `python3 tools/it_ste_vocabulary.py check --compact-json`
   `python3 tools/it_ste_document.py build`
   `python3 tools/it_ste_document.py check`
   `python3 -W error::ResourceWarning -m unittest discover -s tests`
3. Run authenticated source doctor, project diagnostics, and `git diff --check`.
4. Recompute the offset-0 queue and all disposition counts after changes.
5. Update the existing **Current checkpoint** in `docs/it-ste-draft-handoff.md` in place with the last completed ID/page, note, current counts, actual validations, unresolved blockers, exact next action, and next live-queue slice.

## Mandatory final review

Before reporting completion, inspect the complete worktree and index:

```sh
git --no-pager --no-optional-locks status --short --untracked-files=all
git --no-pager diff --find-renames
git --no-pager diff --cached --find-renames
git --no-pager diff --name-status --find-renames
git --no-pager diff --cached --name-status --find-renames
```

Review every modified, added, deleted, renamed, untracked, binary, mode, and submodule change. Read new/untracked content, inspect deleted content from Git, and distinguish pre-existing user work from changes made by this skill. Do not stage or commit until this review is complete. Never stage, commit, release, publish, or revert unrelated work.

## Automatic commit policy

After validation and the mandatory review, commit automatically only when all of these conditions hold:

1. The final change inventory can be separated from the baseline inventory captured at startup.
2. Every proposed commit path is wholly owned by this run; do not commit a file that mixes this run's edits with pre-existing user edits.
3. No PDF, PDF rendering, secret, ignored local artifact, unrelated staged change, deletion, rename, binary, mode, or submodule change is being included unintentionally.
4. The canonical, note, checkpoint, test, and generated files listed for this slice have passed all required checks.

Use explicit paths only, never a blanket add:

```sh
git add -A -- <reviewed-paths>
GIT_EDITOR=true git commit --only -m "<imperative message, <=50 chars>" -- <reviewed-paths>
```

Do not ask for confirmation: the user explicitly enabled automatic commits for this skill. If any safety condition fails, do not stage or commit; explain the exact blocker and provide a copy-ready selective command instead. If the commit command fails, report the failure and preserve existing user staging/work without resetting it. Report the resulting commit hash and exact paths when it succeeds.

## Final report

Report in Russian unless the user requests another language:

- what was recomputed and whether the checkpoint differed;
- the exact records changed and the evidence-based reason;
- sources actually inspected and their limitations;
- all validation results, including failures;
- the complete changed/new-file inventory and ignored temporary artifacts;
- unresolved questions and the exact next live-queue slice;
- the automatic commit result: commit hash, message, and exact paths, or the safety blocker and a copy-ready selective command if no commit was safe;
- reviewed changes left out of the commit and why.

Automatic committing is authorized by this skill. Never include unrelated or mixed user work merely to make the commit convenient.
