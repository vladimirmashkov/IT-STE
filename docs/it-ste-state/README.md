# Compact state protocol for IT-STE skills

This protocol keeps resumable work in small files. It is operational state, not vocabulary approval, release authority, or SFT authorization.

## Read budget

1. Read `AGENTS.md`.
2. Run `python3 tools/it_ste_resume.py show --compact`, then `python3 tools/it_ste_resume.py next --compact`; keep only their compact JSON in context.
3. Read the one selected `SKILL.md` adapter and the generated/current run `*.input.json`. `next` already activates the input; do not call `begin` again for that run.
4. Read only paths and selectors in `input.read_set`. `next` chooses the exact scope from `selector.json`; do not search history to guess it.
5. Retrieve only selected canonical records, ASD entries, and source sections. Never load generated Markdown, all batches, the complete ASD extraction, SQLite payload, PDF, or aggregate history merely to resume.

The orchestrator must load one adapter, never all supporting skills. An adapter must not recursively load another full skill; it may delegate to a named contract by reference.

## State files

- `docs/it-ste-state/current.json` is the single small resume pointer.
- `docs/it-ste-state/selector.json` contains only phase order and cursors; it is the deterministic automatic next-slice index.
- `docs/it-ste-state/runs/<run-id>.input.json` freezes one bounded question, scope, read set, allowlist, baseline reference, and per-run authorization.
- `docs/it-ste-state/runs/<run-id>.output.json` stores status, decision, evidence/file references, compact validation statuses, next pointer, and commit metadata.
- Verbose command output and full Git inventories belong under `.local/it-ste-state/<run-id>/` and never in the input/output JSON or chat context.

Normal `/it-ste-release-readiness resume` uses `next`, which creates and activates the input atomically. Use `begin --input <input.json>` only for manual recovery or a non-dispatcher skill. Always use `finish --output <output.json>` after writing the compact output; it advances the selector only after `status: done`.

## Input/output contract

Input must contain `schema: 1`, `run_id`, `workflow`, `skill`, `phase`, `question`, `scope`, `selection`, `read_set`, `allowed_paths`, `baseline`, `authorization`, and `output_path`. `scope` contains exact IDs/paths/theme and excluded meanings; it must not be an offset-only pointer. `selection` contains the phase cursor and next cursor. `read_set` entries use `{path, selector}`. `authorization.auto_commit` is false unless the current invocation explicitly authorizes it.

Output must contain `schema: 1`, `run_id`, `status` (`done`, `blocked`, `needs-scope`, or `stopped`), `decision`, `evidence_refs`, `changed_paths`, `validations`, `next`, and `commit`. Store references, hashes, exit statuses, and short reasons only; do not store source payloads, quotations, full diffs, or stdout. `next` contains one `action` and, when known, the next phase/skill/scope.

## Bounded lifecycle

- `resume` reads `current.json` and calls `next`; it automatically selects the next cursor from `selector.json` and repeats after every `done` output. It returns `needs-scope` only at an explicit human/candidate boundary or a selector error.
- `next` records the exact input before evidence/editing and activates it. Recompute canonical counts and queue from offset 0; checkpoint counts are hints, not authority.
- Work one slice per adapter invocation. The dispatcher may repeat slices without loading previous outputs; put research evidence in the active note and full validation/Git logs in `.local`, keeping each output JSON compact.
- Run the affected check first, then the standard checks required by the repository/handoff, diagnostics, and `git diff --check`. Record pass/fail plus log references, not command transcripts.
- Review the complete worktree/index as required by `AGENTS.md`. Stage or commit only explicit paths wholly owned by the run and only when input authorization allows it.
- Write output, run `finish`, and continue only from the new `current.json`. A `done` output advances one cursor; `blocked`/`stopped` preserves the exact point. Do not reread previous outputs or accumulate iteration reports in chat.

All evidence, provenance, ASD PDF restrictions, draft status, no-approval boundary, Git safety, and commit rules remain in force. This protocol reduces loading; it does not weaken validation or authorize publication.
