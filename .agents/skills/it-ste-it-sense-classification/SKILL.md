---
name: it-ste-it-sense-classification
description: Classify one bounded ASD-derived IT sense from compact input and direct evidence; never force needs-review out of the queue.
disable-model-invocation: true
---

# IT-STE independent IT-sense classification

Manual-only. The caller must supply one bounded ID/page/group and an iteration count when applicable. This is not vocabulary approval, canonicalization, release, publication, conformance, or SFT authorization.

## Compact input

Read `current.json` with `show --compact`, one classification input, and only its `read_set`. The frozen baseline is `docs/it-ste-research/needs-review-38.md`; maintain the aggregate `docs/it-ste-research/it-sense-classification-log.md` with one stable slice entry and old/new result per selected ID. The input must name exact IDs, batch/pages, IT question, excluded domains/meanings, baseline/log anchors, allowlist, and authorization. Do not read either aggregate file in full, nor all batches, generated Markdown, or source extraction. No exact slice means `needs-scope`.

## Evidence and outcomes

1. Run `begin`, then ASD `doctor`, exact `entry <ID> --compact-json`, and `page <PDF_PAGE>` only when layout matters. Preserve Issue/revision, physical/printed page, locator, PDF hash, spelling, POS, warnings, raw metadata, rights, ID, and sequence.
2. Research one concrete IT-sense question with direct applicable standards/specifications, official technology documentation, or competent specialist sources. Check version/status/scope/competence/limits. Forums, snippets, AI summaries, inaccessible pages, and uninspected URLs are discovery-only or unusable evidence.
3. Consider `retain/restricted`, `retain/allowed`, `exclude/prohibited`, `not-applicable`, `split/proposal`, unchanged, and `needs-review`; state why plausible alternatives were rejected. Never use `allowed` for unresolved polysemy or `prohibited` for an evidence gap.
4. Update one compact per-slice note and the aggregate log at a stable slice anchor; apply only justified draft JSON changes and never add schema/relations without owner approval. Keep `status: draft` and `review_status: editorial-review-needed`.

Run affected then standard checks from the compact protocol, diagnostics, full Git review, output/finish, and an explicit-path commit only when per-run authorization says so. Preserve blocked logs and exact next IDs/action. Report output refs and no-approval/no-release boundary, not history or source payloads.
