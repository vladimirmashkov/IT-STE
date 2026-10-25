# Release-readiness gates — rights, language, and dataset

This note records bounded release-readiness evidence. It is not vocabulary approval, a release decision, ASD guidance, publication authorization, conformance evidence, or SFT authorization.

## Rights gate — `rr-gates-001-20261025T004346Z`

State: **blocked / needs-owner-decision**

Question and scope: Can the current draft and its referenced source metadata satisfy the rights/provenance gate for a future release candidate without inferring rights that are not recorded? This slice covers ASD derivative permission and attribution, original IT-STE content rights, external PeopleCert metadata, copied-text boundaries, and manifest/source consistency. It does not approve vocabulary or package a candidate.

Canonical records and metadata inspected:

- `standards/it-ste/versions/0.1.0-draft.1/revisions/r0001/manifest.json`
- `standards/it-ste/versions/0.1.0-draft.1/revisions/r0001/sources/ASDSTE-SOURCE-ISSUE9-R0001.json`
- `standards/it-ste/versions/0.1.0-draft.1/revisions/r0001/sources/ITIL-SOURCE-PEOPLECERT-*.json`
- `standards/it-ste/vocabulary-reviews/asd-ste100/issue-9/r0001/batch-001.json` rights metadata as representative canonical batch provenance
- `docs/permissions/asd-ste100-issue-9-derivatives.md`
- `LICENSE-CONTENT.md`

Facts and evidence:

- The repository permission record states that written authorization was received for publication of authorized ASD-STE100 Issue 9 derivative files, including the structured retrieval database. It forbids source-PDF redistribution, says the derivative is not official ASD guidance, and records no broader downstream license terms.
- The canonical ASD source metadata preserves ASD ownership, Issue 9/revision `r0001`, the permission-record path and hash, the source PDF hash, `pdf_included: false`, and the separation between ASD source rights and IT-STE editorial rights. Batch rights metadata records `source_pdf_redistribution: forbidden` and `downstream_license: unknown`.
- Original IT-STE editorial content is marked CC BY-SA 4.0 with IT-STE contributor attribution and project link. `LICENSE-CONTENT.md` explicitly excludes ASD and other third-party material from that grant.
- The manifest is `status: draft`, lists only English with `language_coverage.en: partial`, records `released_at: null`, and includes ASD plus PeopleCert source metadata records.
- PeopleCert records are `status: reference-only`, have `license: null`, `redistribution: unknown`, and `adaptation: unknown`. Their notices state that no source text was copied and that the metadata is not an official ITIL glossary or ASD provenance. These notices do not grant downstream rights.
- Structural adaptation, corpus, vocabulary, document, and full-suite checks pass, but those checks do not establish legal permission or independent rights review.

Decision and limitation:

- The ASD derivative-permission and original-content attribution facts are recorded, but the gate cannot pass while broader downstream rights remain unknown for ASD-owned material and the external PeopleCert metadata has no recorded license or redistribution permission. A structural pass would incorrectly infer release rights.
- The rights gate note was missing when this bounded run was selected; this note records the blocker rather than treating the missing register as evidence of permission.
- No external rights corroboration was claimed or performed. The source-PDF prohibition remains in force, and no source PDF or rendering was staged.

Required owner decision / next action: a rights/provenance owner must either record competent permission and scope for every third-party artifact intended for a future candidate, or constrain/remove those materials and document the resulting release scope. Then retry this exact rights gate. Do not advance to language or dataset gates, update the release catalog, publish, or package a release candidate until the rights gate is independently resolved.

Applied changes and validation: added this compact blocker note; updated the release-readiness plan checkpoint only; ran authenticated ASD doctor, source-rights metadata audit, adaptation, corpus, aggregate vocabulary, document build/check, full test suite (`119 tests, OK`), and diagnostics with no structural errors or warnings. These results do not imply approval.
