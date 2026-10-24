---
name: it-ste-release-candidate
description: Package an explicitly requested IT-STE release candidate only after recorded W2, vocabulary, rights, language, and dataset gates pass; inspect release tooling first, preserve draft safeguards, and never publish automatically.
disable-model-invocation: true
---

# IT-STE release-candidate packaging

Use only when `it-ste-release-readiness` explicitly delegates a release-candidate phase and the plan records passing Phases 1–5. This skill packages a candidate; it is not publication, approval, conformance evidence, or SFT authorization.

## Hard preconditions

- Require branch `remediation/release-readiness`, clean worktree/index, explicit user request for a candidate, and recorded passing gate results.
- Read `AGENTS.md`, the release-readiness plan/checkpoint, handoff Current checkpoint, active gate notes, canonical manifest, catalog/release tooling documentation, and only relevant release scripts. Do not guess commands or version semantics.
- Re-run ASD doctor, canonical counts/queue, corpus/adaptation/vocabulary/document checks, tests, diagnostics, rights/language/dataset reports, and `git diff --check` before packaging.
- Stop if any gate is missing, stale, blocked, or represented only by a structural check.

## Packaging rules

1. Inspect current version/revision/catalog contract and identify the exact candidate files and hashes. Do not change the contract or catalog merely to make packaging possible.
2. Keep canonical draft safeguards and explicit notices until a separately authorized approval process changes them.
3. Preserve ASD ownership, derivative-permission notices, original IT-STE rights, external source limitations, language coverage, and dataset restrictions.
4. Generate candidate artifacts only through repository tooling. Never hand-edit generated Markdown, copy the private ASD PDF, include local renderings, or copy protected external text.
5. Perform a complete final inventory review: status/index/diffs/name-status, new/deleted/renamed/binary/mode/submodule files, exact candidate manifest, hashes, and ignored artifacts.
6. Use one explicit-path commit for the candidate packaging only if every precondition passes. Do not include unrelated gate notes or user work. Do not publish or mutate release catalog unless the user separately authorizes that exact action.
7. Verify the candidate commit and clean recovery state. Report the candidate as `release-candidate`, not released.

## Commit policy

Automatic commit requires explicit authorization for this candidate run. Use a short imperative message such as `Package draft release candidate`, explicit paths only, and `git commit --only`. If any gate fails, leave changes preserved and unstaged and provide a safe selective command instead.

## Final report

Report in Russian: candidate scope/version, gate evidence and limitations, exact files/hashes, all validations, ignored artifacts, commit hash/message/paths or blocker, reviewed changes left out, and an explicit statement that no publication, approval, conformance, or SFT readiness was claimed.
