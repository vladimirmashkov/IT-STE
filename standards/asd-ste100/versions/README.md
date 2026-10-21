# ASD-STE100 versions

[Русский](README.ru.md)

Create `<version>/revisions/<revision>/` directories here according to the [common storage structure](../../../docs/storage.md). No actual editions are registered yet. Do not insert an assumed “latest” edition number.

- `version` preserves the identity of the official edition. Also record the exact publisher designation in the source metadata.
- `revision` identifies a snapshot of this project's structured representation, metadata, and translations. It does not represent a new ASD-STE100 edition.
- `primary_language` is `en`. English source material remains authoritative; Russian is the preferred optional translation language.
- `sources/` contains source and rights metadata, not PDF files or standard text that are automatically cleared for publication.
- Populate `content/` only after verifying the rights required for that content and use. Until then, retain metadata only.
- Project record IDs do not replace official rule numbers. Keep official locators in `source_refs[].locator`.

A translation of ASD-STE100 belongs in the `asd-ste100` namespace. A rule changed for IT belongs in `it-ste`, has its own ID, and documents the reason for adaptation. The IT-STE project license does not by itself authorize either action with third-party text.
