---
name: it-ste-release-readiness
description: Dispatch sequential bounded IT-STE release-readiness slices from compact repository state; never infer approval or publish.
disable-model-invocation: true
---

# IT-STE release-readiness dispatcher

Use only for the explicitly requested release-readiness workflow on branch `remediation/release-readiness`. This is orchestration, not vocabulary approval, release, publication, conformance, or SFT authorization.

## Invocation

```text
/it-ste-release-readiness bootstrap
/it-ste-release-readiness resume
/it-ste-release-readiness resume --iterations=N
```

`bootstrap` only validates the state/adapter registry and records a plan pointer; if an adapter is missing, create it only from the planned contract after a clean-baseline check. It never starts a slice. Bare `resume` calls `python3 tools/it_ste_resume.py next`, executes the selected slice, and repeats the loop until the first blocker, owner decision, user change, failed validation/commit, or candidate authorization boundary; no phase/scope arguments are needed. `resume --iterations=N` is only an optional upper bound. Never accept `run all`; the selector already supplies sequential inputs. Candidate packaging remains an explicit authorization boundary after Phases 1–5 pass.

## Compact dispatch contract

1. Read `AGENTS.md`, then run `python3 tools/it_ste_resume.py show --compact` and `python3 tools/it_ste_resume.py next --compact`. Read `docs/it-ste-state/README.md` only if the contract is unclear.
2. Require the branch and baseline rules from `AGENTS.md`. Do not load the handoff, plan, history, or supporting skills before selector state chooses the slice.
3. If `next` returns an active run, continue that input; if it returns `needs-scope`, stop at the recorded candidate/owner boundary. Do not search large documents to guess a slice.
4. Select exactly one adapter named by the generated input: W2, vocabulary, gates, or candidate. Read only that one `SKILL.md`; never read all supporting skills or recurse into another full skill.
5. `next` has already created/activated the input. Execute one adapter, write one compact output, and run `finish`. Store full logs/diffs under `.local/it-ste-state/<run-id>/`.
6. After `status: done`, return to step 3 and call `next` again from the new `current.json`; do not carry previous output or queue offsets in chat. Without `--iterations`, continue until a stop condition. With `--iterations=N`, stop after N completed slices. Stop earlier on a blocker, failed check, ownership change, or failed commit.

## Phase map

- `w2` → `it-ste-w2-editorial-slice`; one theme and normally 2–5 rules/terms.
- `vocabulary` → `it-ste-vocabulary-gate-slice`; one batch or enumerated group.
- `gates` → `it-ste-release-gates`; exactly one of rights, language, dataset.
- `candidate` → `it-ste-release-candidate`; the selector stops here until the user explicitly requests packaging and passing gate references exist.
- `w3` is complete for the current plan; do not dispatch a W3 pair from this orchestrator unless a new explicit plan boundary is recorded.

## Safety boundary

The adapter owns the evidence, affected checks, allowlist, and commit policy for its slice. The dispatcher does not approve, publish, mutate the release catalog, or weaken draft status. Keep ASD ownership/permission, source limitations, `status: draft`, and `review_status: editorial-review-needed`. A passing structural check or empty queue is not approval.

## Output

Report in Russian from the compact output and referenced artifacts: run/phase/scope, decision, evidence refs and limitations, changed paths, validation statuses, Git inventory summary, commit metadata or blocker, next action, and reviewed changes left out. Do not paste full logs, diffs, source payloads, or generated documents.
