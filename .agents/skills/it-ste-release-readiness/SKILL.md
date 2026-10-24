---
name: it-ste-release-readiness
description: Dispatch one bounded IT-STE release-readiness slice from compact repository state; never infer approval or publish.
disable-model-invocation: true
---

# IT-STE release-readiness dispatcher

Use only for the explicitly requested release-readiness workflow on branch `remediation/release-readiness`. This is orchestration, not vocabulary approval, release, publication, conformance, or SFT authorization.

## Invocation

```text
/it-ste-release-readiness bootstrap
/it-ste-release-readiness resume
/it-ste-release-readiness resume --iterations=N
/it-ste-release-readiness resume --phase=w2 --scope=<stable-theme-or-IDs>
/it-ste-release-readiness --phase=vocabulary --scope=<batch-or-IDs>
/it-ste-release-readiness --phase=gates --scope=rights|language|dataset
/it-ste-release-readiness --phase=candidate
```

`bootstrap` only validates the state/adapter registry and records a plan pointer; if an adapter is missing, create it only from the planned contract after a clean-baseline check. It never starts a slice. `resume` runs one slice unless a positive bounded `--iterations` is supplied. Never accept `run all`; convert it to sequential inputs. Candidate packaging requires an explicit request and recorded passing Phases 1–5.

## Compact dispatch contract

1. Read `AGENTS.md`, then run `python3 tools/it_ste_resume.py show --compact`. Read `docs/it-ste-state/README.md` only if the input/output contract is unclear.
2. Require the branch and baseline rules from `AGENTS.md`. Do not load the handoff, plan, history, or supporting skills before state selection.
3. If `current.json` has no exact scope/input, return `needs-scope` with the available phase and next action. Do not search large documents to guess a slice.
4. Select exactly one adapter: W2, vocabulary, gates, or candidate. Read only that one `SKILL.md`; never read all supporting skills or recurse into another full skill.
5. Create/validate one `runs/<run-id>.input.json`, run `begin`, execute the adapter, write one compact output, and run `finish`. Store full logs/diffs under `.local/it-ste-state/<run-id>/`.
6. For `--iterations=N`, repeat strictly from the new `current.json`; do not carry previous output or queue offsets in chat. Stop on the first blocker, failed check, ownership change, or failed commit.

## Phase map

- `w2` → `it-ste-w2-editorial-slice`; one theme and normally 2–5 rules/terms.
- `vocabulary` → `it-ste-vocabulary-gate-slice`; one batch or enumerated group.
- `gates` → `it-ste-release-gates`; exactly one of rights, language, dataset.
- `candidate` → `it-ste-release-candidate`; exact candidate manifest and passing gate references.
- `w3` is complete for the current plan; do not dispatch a W3 pair from this orchestrator unless a new explicit plan boundary is recorded.

## Safety boundary

The adapter owns the evidence, affected checks, allowlist, and commit policy for its slice. The dispatcher does not approve, publish, mutate the release catalog, or weaken draft status. Keep ASD ownership/permission, source limitations, `status: draft`, and `review_status: editorial-review-needed`. A passing structural check or empty queue is not approval.

## Output

Report in Russian from the compact output and referenced artifacts: run/phase/scope, decision, evidence refs and limitations, changed paths, validation statuses, Git inventory summary, commit metadata or blocker, next action, and reviewed changes left out. Do not paste full logs, diffs, source payloads, or generated documents.
