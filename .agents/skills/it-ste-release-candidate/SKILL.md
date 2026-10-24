---
name: it-ste-release-candidate
description: Package one explicitly requested IT-STE draft candidate from exact passing-gate inputs; never publish automatically.
disable-model-invocation: true
---

# IT-STE release-candidate packaging

Use only when the dispatcher supplies an exact candidate input, the branch is `remediation/release-readiness`, Phases 1–5 have recorded passing gates, and the user explicitly requests a candidate. A candidate is not an approved or published release and is not SFT authorization.

## Compact contract

1. Read `current.json` and one explicitly authorized input containing candidate scope/version, exact manifest/hash set, passing gate output references, read set, allowlist, clean baseline, and commit authorization. The automatic selector stops before this input; missing/stale gates are an immediate `blocked` output; do not scan all history.
2. Inspect only the exact candidate files/hashes and the specific release/catalog tooling commands identified by the input. Do not guess version semantics or read an entire tooling tree.
3. Re-run the affected and standard checks from the compact protocol, ASD doctor, diagnostics, and Git review. Generate artifacts only through repository tooling; keep draft notices, ASD ownership, source rights, language scope, and limitations. Never copy the private PDF, local renderings, or protected external text.
4. Write one compact output with candidate manifest/hash refs, validation statuses, exact changed paths, and `release-candidate` decision; run `finish`. Commit one explicit-path package only when all preconditions and input authorization pass.
5. Do not mutate the release catalog or publish. Stop on any missing gate, stale hash, rights/language/quality blocker, failed check, or ownership ambiguity.

Report in Russian from output/artifact refs: candidate scope/version, gate limitations, files/hashes, validations, ignored artifacts, commit or blocker, reviewed paths left out, and explicit no-publication/no-approval/no-SFT status.
