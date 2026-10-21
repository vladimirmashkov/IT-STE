# IT-STE versions

[Русский](README.ru.md)

Create `<version>/revisions/<revision>/` directories here according to the [common storage structure](../../../docs/storage.md). No versions or normative records have been released yet.

Use SemVer for `version`:

- **MAJOR** — an incompatible change to normative requirements or to the meaning of permitted terms.
- **MINOR** — a compatible addition to the rules or vocabulary.
- **PATCH** — a correction to the primary normative text that does not change a requirement.
- Prereleases have an explicit suffix, for example `0.1.0-draft.1`. This is an example, not a released version.

English (`en`) is the primary and authoritative language. A released normative snapshot must have complete approved English records. Russian (`ru`) is the preferred secondary language, but it and all other translations are optional. Translations, metadata, and packaging can be updated through `revision` without changing the normative version. Released snapshots are immutable.

For the first draft, use the [templates](../../../templates/). Add only original material or material for which the necessary rights have been verified. A relationship to ASD-STE100 must explain what was adapted and why; it must not imply official ASD endorsement.
