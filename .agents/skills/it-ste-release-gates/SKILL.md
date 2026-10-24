---
name: it-ste-release-gates
description: Execute one bounded rights, language, or dataset gate using compact state; record blockers and never infer approval.
disable-model-invocation: true
---

# IT-STE release-readiness gate

Use under `it-ste-release-readiness` or for one explicit scope: `rights`, `language`, or `dataset`. This records readiness evidence; it does not approve vocabulary, publish, mutate the catalog, or authorize SFT.

## Compact execution

1. Read `current.json` and the dispatcher-created input with exact `phase`, gate scope, question, criteria, read set, allowlist, baseline, and per-run commit authorization. `next` already activated it; if the selector stops, return the recorded `needs-scope` without reading the full plan or source registry.
2. Require branch/clean ownership rules and inspect only the relevant manifest, source metadata, gate note, generated artifact/hash, and directly fetched competent sources named in the input.
3. Evaluate exactly one gate:
   - `rights`: ASD derivative permission/attribution, original IT-STE rights, external URL/version/scope/downstream rights, copied-text exclusion, and manifest/source consistency;
   - `language`: required release languages, translation inventory/review/equivalence, English authority, and representability of `partial` coverage;
   - `dataset`: reproducibility/hashes, scope, draft/private leakage, license, generated consistency, evaluation quality, and independent review.
4. Record facts versus inference, limitations, and `pass`, `blocked`, or `needs-owner-decision` in the active gate note (normally `docs/it-ste-research/release-readiness-gates.md`) and plan checkpoint. Unknown rights, incomplete translation review, unresolved vocabulary approval, or missing independent quality evidence remain blockers.
5. Run affected and standard checks from the compact protocol, diagnostics, Git review, then write/finish one compact output. Commit only explicit wholly owned state/metadata paths when authorized. Never update `catalog.json` or publish.

Report compact evidence refs, blockers/owner decisions, changed paths, validation statuses, commit metadata or safe blocker, ignored artifacts, next gate, and an explicit no-release/no-publication/no-SFT statement.
