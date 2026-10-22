# Agent instructions

[Русский](AGENTS.ru.md)

These instructions apply to the entire repository. This English document is authoritative; the Russian version is an optional translation.

## Continuing IT-STE draft remediation

For draft vocabulary blockers, editorial review, or IT-only term coverage, read [the compact handoff](docs/it-ste-draft-handoff.md) first. It records completed work, the three open workstreams, bounded live-queue retrieval, and validation requirements. Do not bootstrap by reading the complete generated Markdown, all vocabulary batches, or the source extraction into context. Recompute current counts; handoff baseline numbers are historical, not approvals.

## ASD-STE100 Issue 9 derivative reference

Use the tracked derivative retrieval database instead of reading or converting the complete standard:

1. Run `python3 tools/asd_ste100_local.py doctor` to authenticate the published database and manifest. If the local source PDF is present, this also verifies its exact SHA-256.
2. Use progressive disclosure: `overview`; then `rules` or `search`; then `rule <ID>`, `excerpt <ID> <QUERY>`, `word <TERM>`, or `entry <ID>`. Prefer bounded `excerpt` and exact `entry` retrieval; add `--full` only when they are insufficient. Use `page <PDF_PAGE>` only to verify a cited page. Use `--compact-json` when machine-readable output saves context.
3. Never put the complete extraction into context. Keep the standard version and physical PDF page with every result. Treat mechanically extracted structure as unreviewed and verify ambiguous wording, table columns, typography, or diagrams against the PDF.
4. Publication permission covers the derivative database, not the source PDF. Keep the PDF under `.local/` and never stage, commit, or publish it. Regenerate published artifacts only through `build` and `publish`, retain ASD ownership and the IT-STE project link, and do not present an extraction or adaptation as official ASD guidance.

See [the derivative-reference guide](docs/asd-ste100-local-reference.md) and [permission record](docs/permissions/asd-ste100-issue-9-derivatives.md).

## Review all changes and propose terminal commands

After every change, before reporting completion:

1. Inspect the entire worktree and index with `git --no-pager --no-optional-locks status --short --untracked-files=all`. Review both unstaged and staged changes with `git --no-pager diff --find-renames`, `git --no-pager diff --cached --find-renames`, and the corresponding `--name-status` views.
2. Review every change, not only line diffs: added, modified, deleted, renamed or moved, and untracked files, plus file type/mode, binary, and submodule changes when present. Read added/untracked content, inspect deleted content from Git, and compare both paths of a rename, including deletion-plus-untracked pairs. If content cannot be inspected, explicitly report the limitation.
3. Analyze the complete pending change set for intended behavior, consistency, errors, and accidental or unrelated edits. Distinguish your changes from pre-existing user work. Do not overwrite or revert unrelated changes. Reviewing a change does not authorize modifying it or including it in a commit proposal.
4. Run relevant checks and briefly report the complete change inventory, analysis, and validation results. If a check cannot be run, say why.
5. At the end, propose one or more commits for independent logical changes. For each proposal, list the exact files it includes (both old and new paths for renames) and give a very short, one-line English imperative message, preferably no more than 50 characters. Identify reviewed changes left out of the proposals and explain why. Do not include unrelated pending work without the user's request.
6. Provide copy-ready terminal commands in fenced `sh` blocks, to be run from the repository root, not just commit messages. Follow the safety rules below.

### Safe command proposals

- Stage only explicit, reviewed paths with `git add -A -- ...`; include deletions and both paths of renames. Do not use blanket `git add .` or pathless `git add -A`.
- Prefix commit commands with `GIT_EDITOR=true` and supply the proposed message with `-m`.
- Check for unrelated staged changes before proposing a commit. Preserve them: use `git commit --only` with explicit paths only when each entire listed file belongs to the proposal. If a file mixes unrelated changes, explain the required selective staging instead of proposing unsafe whole-file staging or committing. Do not unstage someone else's work to make a command convenient.

A command proposal is not permission to execute it. Do not stage files, create commits, or rewrite Git history unless the user explicitly requests that action.
