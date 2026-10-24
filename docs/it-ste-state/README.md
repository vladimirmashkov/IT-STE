# Compact state protocol for IT-STE skills

This protocol keeps resumable work in small files. It is operational state, not vocabulary approval, release authority, or SFT authorization.

## Read budget

1. Read `AGENTS.md`.
2. Run `python3 tools/it_ste_resume.py show --compact` and keep only its JSON in context.
3. Read the one selected `SKILL.md` adapter and the current run `*.input.json`.
4. Read only paths and selectors in `input.read_set`. A missing exact scope is `needs-scope`; do not search history to guess it.
5. Retrieve only selected canonical records, ASD entries, and source sections. Never load generated Markdown, all batches, the complete ASD extraction, SQLite payload, PDF, or aggregate history merely to resume.

The orchestrator must load one adapter, never all supporting skills. An adapter must not recursively load another full skill; it may delegate to a named contract by reference.

## State files

- `docs/it-ste-state/current.json` is the single small resume pointer.
- `docs/it-ste-state/runs/<run-id>.input.json` freezes one bounded question, scope, read set, allowlist, baseline reference, and per-run authorization.
- `docs/it-ste-state/runs/<run-id>.output.json` stores status, decision, evidence/file references, compact validation statuses, next pointer, and commit metadata.
- Verbose command output and full Git inventories belong under `.local/it-ste-state/<run-id>/` and never in the input/output JSON or chat context.

Use `python3 tools/it_ste_resume.py begin --input <input.json>` before editing and `python3 tools/it_ste_resume.py finish --output <output.json>` after writing the output. The helper validates paths and advances `current.json` atomically.

## Input/output contract

Input must contain `schema: 1`, `run_id`, `workflow`, `skill`, `phase`, `question`, `scope`, `read_set`, `allowed_paths`, `baseline`, and `authorization`. `scope` contains exact IDs/paths/theme and excluded meanings; it must not be an offset-only pointer. `read_set` entries use `{path, selector}`. `authorization.auto_commit` is false unless the current invocation explicitly authorizes it.

Output must contain `schema: 1`, `run_id`, `status` (`done`, `blocked`, `needs-scope`, or `stopped`), `decision`, `evidence_refs`, `changed_paths`, `validations`, `next`, and `commit`. Store references, hashes, exit statuses, and short reasons only; do not store source payloads, quotations, full diffs, or stdout. `next` contains one `action` and, when known, the next phase/skill/scope.

## Bounded lifecycle

- `resume` reads `current.json`; if `active_run` is absent and `scope.theme` is null with empty `scope.ids`/`scope.paths`, return `needs-scope` without opening large documents.
- `begin` records the exact input before evidence or edits. Recompute canonical counts and queue from offset 0; checkpoint counts are hints, not authority.
- Work one slice only. Put research evidence in the active note and full validation/Git logs in `.local`; keep the output JSON compact.
- Run the affected check first, then the standard checks required by the repository/handoff, diagnostics, and `git diff --check`. Record pass/fail plus log references, not command transcripts.
- Review the complete worktree/index as required by `AGENTS.md`. Stage or commit only explicit paths wholly owned by the run and only when input authorization allows it.
- Write output, run `finish`, and continue only from the new `current.json`. Do not reread previous outputs or accumulate iteration reports in chat.

All evidence, provenance, ASD PDF restrictions, draft status, no-approval boundary, Git safety, and commit rules remain in force. This protocol reduces loading; it does not weaken validation or authorize publication.
