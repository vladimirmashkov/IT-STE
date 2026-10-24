---
name: it-ste-11-domain-evidence
description: Systematically map the 11 remaining IT-STE needs-review records across the full IT domain matrix using authoritative evidence, explicit exclusions, bounded senses, and interruption-safe logs; never force a disposition.
disable-model-invocation: true
---

# IT-STE 11-record domain evidence study

Use this skill only when the user explicitly requests a full domain-evidence study of the remaining 11 records. This is a research and policy-validation workflow, not vocabulary approval, release, publication, canonicalization, or SFT authorization.

## Scope

The frozen target set is:

- `D-P349-003` `RADIOACTIVE`
- `D-P351-001` `real`
- `D-P368-010` `scored`
- `D-P391-003` `strain`
- `D-P391-005` `stress`
- `D-P397-005` `SYMBOL`
- `D-P397-006` `SYMMETRICAL`
- `D-P397-007` `SYMMETRICALLY`
- `D-P416-006` `unobstructed`
- `D-P419-006` `UPSTREAM`
- `D-P419-007` `UPSTREAM OF`

Use `docs/it-ste-it-domain-matrix.md` as the complete domain inventory and `docs/it-ste-it-sense-policy.md` as the admission policy. Do not silently add a domain. If a new domain is needed, record a policy proposal and stop before changing the matrix.

## Required evidence matrix

Maintain exactly one aggregate register:

`docs/it-ste-research/it-domain-11-evidence-matrix.md`

For every selected `word × domain` pair record:

- canonical ID, headword, POS, batch, ASD physical PDF page;
- candidate bounded sense and named object/actor;
- authoritative source actually inspected, URL, date, version/status, competence, finding, and limitation;
- source fact versus editorial inference;
- excluded meanings and why analogy is insufficient;
- result: `applicable`, `not-applicable`, or `unresolved`;
- proposed disposition: `restricted`, `split proposal`, `not-applicable`, or `needs-review`;
- exact missing owner/schema decision where unresolved.

Also record an aggregate result for each word, including old/new canonical disposition. The aggregate result may remain `needs-review`; do not change canonical JSON merely because a domain is plausible.

## Research groups

Run bounded groups sequentially, normally:

1. `UPSTREAM` / `UPSTREAM OF`;
2. `scored`;
3. `stress`;
4. `SYMBOL`;
5. `SYMMETRICAL` / `SYMMETRICALLY`;
6. `real`;
7. `strain`;
8. `unobstructed`;
9. `RADIOACTIVE`.

A user-provided iteration count means groups/slices, not records. Do not start the next group until the current group has evidence, register update, validation, checkpoint update, complete diff review, and (only if explicitly authorized) commit.

## Evidence method

1. Read `AGENTS.md`, the Current checkpoint in `docs/it-ste-draft-handoff.md`, this policy, the domain matrix, the frozen register, the aggregate classification log, and only the active domain-evidence note.
2. Capture the complete Git status/index/diff/name-status inventory. Existing changes from the same authorized study may be resumed only when ownership is explicit and no unrelated changes overlap; never reset, stash, hide, or overwrite them.
3. Recompute canonical counts and the offset-0 queue. Treat the queue as a pointer, not authority over evidence.
4. For each group, retrieve exact ASD entries with the authenticated derivative workflow and verify the cited physical PDF page when layout or row boundaries matter. Preserve Issue, revision, printed page, physical page, locator, PDF hash, warnings, raw metadata, and rights.
5. For each plausible domain, search for a concrete sense-domain question. Prefer controlling specifications, official documentation, specialist standards, and competent professional sources. ITIL is only a service-management reference; it cannot establish protocol, programming, geometry, cryptographic, or physical meanings outside its scope.
6. Inspect sources directly. Never rely on snippets, AI summaries, uncited claims, inaccessible pages, or forum answers. Reddit and Stack Overflow are discovery-only and must never support a decision; record their use if material.
7. Mark `applicable` only when a named IT object/actor, bounded operation/state/relation, and competent source support the sense. Mark `not-applicable` when the candidate is only aviation, metaphor, or unsupported analogy. Mark `unresolved` when a source or owner/schema decision is missing.
8. Compare `allowed`, `restricted`, `prohibited`, `not-applicable`, `split proposal`, and unchanged `needs-review`. Do not use `allowed` for polysemy, and do not use `prohibited` as a substitute for an evidence gap.
9. Update the matrix, one compact group note, `needs-review-38.md`, `it-sense-classification-log.md`, `external-sources.md`, and only the Current checkpoint in `it-ste-draft-handoff.md`. Never hand-edit generated Markdown. Do not add canonical records or schema fields without owner approval.

## Validation per group

Run the affected canonical batch check first when canonical records changed, then:

```sh
python3 tools/it_ste_adaptation.py check
python3 tools/it_ste_corpus.py check
python3 tools/it_ste_vocabulary.py check --compact-json
python3 tools/it_ste_document.py build
python3 tools/it_ste_document.py check
python3 -W error::ResourceWarning -m unittest discover -s tests
python3 tools/asd_ste100_local.py doctor
git diff --check
```

Run project diagnostics and recompute counts/queue after every group. Record actual outputs in the log. A passing check is not semantic approval.

## Commit and stop rules

Automatic commits are forbidden unless the user explicitly authorizes them for this run. Without that authorization, leave changes unstaged and provide explicit safe commands.

Stop immediately for an unrelated change, unavailable required source with no bounded unresolved result, failed authentication/validation/diagnostics, ambiguous ownership, or a proposed schema change. Preserve the log and report the exact resume pointer. Never force a record out of `needs-review`.

## Final report

Report in Russian:

- requested groups/iterations and completed groups;
- every target ID, domain results, old/new disposition, and unresolved blockers;
- authoritative sources actually inspected and limitations;
- any discovery-only forum use;
- changed files and validation results;
- Git inventory and ignored local artifacts;
- safe uncommitted commit commands if relevant;
- final counts and remaining queue;
- explicit confirmation that no vocabulary approval, release, publication, or SFT readiness was claimed.
