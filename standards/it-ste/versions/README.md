# IT-STE versions

[Русский](README.ru.md)

Create `<version>/revisions/<revision>/` directories here according to the [common storage structure](../../../docs/storage.md). No versions or normative records have been released yet. All [31 English draft rules](../../../docs/it-ste-canonical-pilot.md) now exist at `0.1.0-draft.1/revisions/r0001/`. The [single-file draft](../../../docs/IT-STE-draft.md) generator includes them and all 55 [vocabulary review batches](../../../docs/it-ste-vocabulary.md), 001–055. All 2,196 source dictionary rows have draft proposals: 90 `allowed`, 1,359 `restricted`, 402 `prohibited`, 146 `not-applicable`, and 199 `needs-review`. There are no unprocessed source rows, but 199 unresolved sense/layout cases remain. The six initial first-batch ambiguity cases were resolved after visual inspection of physical PDF pages 153–154; other visual checks have not been done.

All vocabulary decisions remain `draft` / `editorial-review-needed`, not approvals or canonical term records. Source approval does not automatically transfer to IT-STE. Complete source-row draft coverage is not a complete approved IT vocabulary; IT-only terms still require a separate inventory. There is no approved lexicon, release readiness, or SFT readiness, and the release catalog remains empty.

Use SemVer for `version`:

- **MAJOR** — an incompatible change to normative requirements or to the meaning of permitted terms.
- **MINOR** — a compatible addition to the rules or vocabulary.
- **PATCH** — a correction to the primary normative text that does not change a requirement.
- Prereleases have an explicit suffix. `0.1.0-draft.1` currently identifies the draft snapshot, not a released version.

English (`en`) is the primary and authoritative language. A released normative snapshot must have complete approved English records. Russian (`ru`) is the preferred secondary language, but it and all other translations are optional. Translations, metadata, and packaging can be updated through `revision` without changing the normative version. Released snapshots are immutable.

Before authoring the first draft, record source applicability and rationale in the [adaptation plan](../../../docs/it-ste-adaptation.md). Carry the reviewed stable target IDs into the corresponding versioned draft records; planning concepts remain separate and do not replace those records.

For the current pilot, follow its [closed profile contract](../../../docs/it-ste-canonical-pilot.md), not unchanged generic [templates](../../../templates/). Add only original material or material for which the necessary rights have been verified. A relationship to ASD-STE100 must explain what was adapted and why; it must not imply official ASD endorsement.
