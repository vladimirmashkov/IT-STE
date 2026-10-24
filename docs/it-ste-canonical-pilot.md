# Canonical English draft rule contract

[Русское резюме](it-ste-canonical-pilot.ru.md)

This English document is authoritative. Profile `it-ste-pilot-v1`, data format `1.1.0`, is a narrow, executable contract for original English IT-STE draft rule records derived from the reviewed Issue 9 plan. It is not a released standard, a general corpus schema, an ASD translation, or an arbitrary-prose conformance checker.

## Scope and implementation

The read-only, standard-library validator is `tools/it_ste_corpus.py`. It validates this closed profile with explicit Python checks; there is no JSON Schema engine or dependency. Generic `1.0.0` templates remain scaffolds and are not accepted as pilot records. The additive pilot fields use `1.1.0`; no released format or snapshot is changed.

```sh
python3 tools/asd_ste100_local.py doctor
python3 tools/it_ste_adaptation.py check
python3 tools/it_ste_corpus.py check
python3 -W error::ResourceWarning -m unittest discover -s tests -v
```

`check --manifest <repository-relative-path>` selects a manifest explicitly. This first profile accepts only the namespace below. It never writes files, refreshes pins, approves rules, updates the catalog, or releases a snapshot. Its public Python entry point is `check(manifest=DEFAULT_MANIFEST)`; contract failures raise `CorpusError`, and CLI failures return exit code 2 with a diagnostic.

## Snapshot coordinates

```text
standards/it-ste/versions/0.1.0-draft.1/revisions/r0001/
  manifest.json
  sources/ASDSTE-SOURCE-ISSUE9-R0001.json
  content/en/rules/ITSTE-R-0001.json
  ...
  content/en/rules/ITSTE-R-0031.json
```

The initial three-rule pilot has been expanded to all 31 reviewed target IDs. Each rule now has original English draft text, exceptions, positive/negative examples, source-facet dispositions, and review criteria. Coverage deliberately remains partial because the controlled vocabulary is incomplete. Profile identity is retained because the rule record contract has not changed. Planned rule targets are not mutated into canonical records. The snapshot now also contains ten original IT-only draft term records, `ITSTE-T-0001` through `ITSTE-T-0010`; they use external ITIL reference metadata and never use ASD source provenance. `catalog.json` remains unchanged with empty release lists. English is authoritative; translations are outside this pilot profile, not prohibited by the project.

Each JSON object has exactly the fields specified below. Unknown fields and `template` markers are errors. Files are UTF-8 without BOM, LF-only, with a final newline. Duplicate JSON keys and non-JSON numeric constants are rejected. Member paths are relative to the snapshot, cannot contain traversal or escape through symlinks, and cannot alias another member. Language, ID, and filename must agree. Files under `content/` and `sources/` must be explicitly listed; unlisted files there are errors.

## Manifest

The manifest has these fields only:

| Fields | Required value or constraint |
| --- | --- |
| `schema_version`, `profile` | `1.1.0`, `it-ste-pilot-v1` |
| `standard`, `version`, `revision` | `it-ste`, `0.1.0-draft.1`, `r0001`, agreeing with the full repository path |
| `status`, `released_at` | `draft`, `null`; released manifests are rejected |
| `primary_language`, `languages`, `language_coverage` | `en`, `["en"]`, `{"en":"partial"}` |
| `records` | Nonempty, unique relative JSON paths `content/en/rules/ITSTE-R-NNNN.json` or `content/en/terms/ITSTE-T-NNNN.json` |
| `sources` | Exactly one canonical ASD source path plus zero or more `sources/ITIL-SOURCE-*.json` external-reference paths |
| `relations`, `supersedes` | Both `null`; no invented ASD canonical relation endpoints |
| `plan` | Object with `path`, `manifest_sha256`, `map_sha256`, `targets_sha256`, `domain_registry_sha256` |

The plan path is `standards/it-ste/adaptation-plans/asd-ste100/issue-9/r0001/manifest.json`. Its pins must match the authenticated current plan, not merely have a valid hash shape. The validator first runs the existing adaptation-plan checks, then compares all pins. A changed plan makes the ASD-derived rule portion of the pilot stale until the affected records are reviewed and their pins deliberately updated; there is no automatic resealing command for this profile. External ITIL reference metadata is validated separately and does not alter ASD plan pins.

These checks bind the pilot to one exact plan state, not an immutable historical plan archive. Before changing the plan, preserve the old state in Git and arrange any future historical-snapshot resolution explicitly. Never repin a released snapshot in place.

The canonical ASD source metadata remains required for the rule portion. External ITIL source metadata uses `standard: "itil"`, a publisher, URL, retrieval date, reference-only status, and explicit unknown downstream rights. It supports a draft IT-only term but is not ASD provenance, an ITIL glossary license, or an approval decision.

## Source metadata and rights boundary

The one source object contains exactly:

- `schema_version`, `id`, `standard`, `version`, `revision`: `1.1.0`, `ASDSTE-SOURCE-ISSUE9-R0001`, `asd-ste100`, `issue-9`, `r0001`;
- `title`, `url`, `retrieved_at`: `ASD-STE100 Issue 9`, `https://asd-ste100.org/`, `null` (no retrieval date is invented);
- `artifact_path`, `artifact_sha256`: the tracked derivative database path and authenticated SHA-256;
- `source_pdf_sha256`: the authenticated source identity, not a dependency on reading the private PDF;
- `owner`: ASD's full name and URL, as recorded in the plan;
- `permission`: `path`, `sha256`, `scope: authorized-derivatives-only`, `source_pdf_redistribution: forbidden`, `downstream_license: unknown`;
- `rights`: `license: null`, `license_url: null`, `redistribution: unknown`, `adaptation: unknown`, ASD `attribution`, and the permission-record path in `evidence`.

The metadata must equal the trusted source profile, including hashes and permission evidence. Unknown broad source-license fields deliberately coexist with recorded permission for this derivative use: permission to publish derivatives does not establish an unrestricted downstream license for ASD text or permission to publish the PDF.

Each draft rule instead describes the rights to its **original IT-STE wording and examples**: CC BY-SA 4.0, redistribution/adaptation allowed for that original content, attribution to IT-STE contributors and ASD, and evidence paths `LICENSE-CONTENT.md` and `docs/permissions/asd-ste100-issue-9-derivatives.md`. Its mandatory `rights.scope` is `original IT-STE wording and examples only; ASD source rights remain separate`. No ASD examples or passages are copied into this pilot's rule text. A structural check is not legal approval for adding protected material later.

Mandatory project attribution: https://github.com/vladimirmashkov/IT-STE.

## Rule record

| Field | Contract |
| --- | --- |
| `schema_version`, `kind`, `language` | `1.1.0`, `rule`, `en` |
| `id` | Existing stable `ITSTE-R-NNNN` in the reviewed target registry; unique within snapshot |
| `status`, `origin`, `translation_of` | `draft`, `adaptation`, `null` |
| `title`, `text` | Nonempty original English title and draft normative statement |
| `applies_to` | Nonempty unique registered domain IDs; editorial applicability still requires review |
| `exceptions` | Nonempty list of explicit exception or scope statements |
| `examples` | Nonempty `allowed` and `not_allowed` arrays of structured examples |
| `source_refs` | One exact reference for every source block allocated to the target, with no extras or duplicates |
| `supporting_target_ids` | Unique other planned IDs, possibly not materialized in the pilot; these are planning cross-references, not canonical relation endpoints or extra derivations |
| `review` | `mode: human`, `automation: structure-only`, nonempty `criteria` strings |
| `rights` | The original-content rights object described above |

`text` is a normative formulation **inside a draft record**, not an approved requirement or proof of lexical completeness. This pilot does not provide the controlled vocabulary that it describes. A term used in an example is not thereby approved for all contexts.

### Source locator and facet dispositions

Each source reference has exactly `source_id`, `locator`, and `facets`. `source_id` resolves to the source metadata above. `locator` has exactly:

```json
{
  "block_id": "5.3",
  "kind": "rule",
  "physical_pdf_pages": [89, 90]
}
```

The source ID, metadata, and manifest's plan pins jointly supply the full source coordinates and hashes. The locator must match the authenticated database index and target allocation. A general recommendation keeps `kind: guidance`; there is no fake `ASDSTE-R-*` endpoint.

Every reference has at least one facet object:

- `source_facet`: original English summary of the relevant source aspect, not a copy of the source passage;
- `disposition`: `adopt`, `adapt`, or `not-applicable`;
- `rationale`: why the aspect is retained, changed, or excluded;
- `target_field`: `text` or `exceptions`, where the disposition is expressed in this rule.

A `not-applicable` facet does not remove the parent source allocation. The validator checks field structure and complete block coverage, not that an editor enumerated every semantic facet or correctly judged equivalence. Supporting target references do not imply delegated provenance. Actual facet delegation and cross-snapshot canonical relations are outside this first profile and need a later explicit contract, not inference from prose IDs.

## Original IT-only term record

An IT-only term is an original, sense- and part-of-speech-bound draft record. Its fields are closed and validated as follows:

| Field | Contract |
| --- | --- |
| `schema_version`, `kind`, `language` | `1.1.0`, `term`, `en` |
| `id`, `status`, `origin`, `translation_of` | `ITSTE-T-NNNN`, `draft`, `original`, `null` |
| `term`, `part_of_speech`, `definition` | Nonempty lexical form, supported POS, and one bounded English meaning |
| `domains`, `usage`, `rationale`, `alternatives` | Registered domain IDs; `allowed`, `restricted`, or `prohibited`; explicit boundary rationale; other canonical term IDs only |
| `examples` | Nonempty `allowed` and `not_allowed` arrays of prose `text`/`rationale` objects |
| `source_refs` | Nonempty `{source_id, locator}` references to validated external ITIL metadata only; ASD source IDs are forbidden |
| `review` | `mode: human`, `automation: structure-only`, nonempty criteria strings |
| `rights` | Original IT-STE wording/examples under CC BY-SA 4.0 with IT-STE attribution only; external source rights remain separate |

The term contract intentionally separates lexical identity from source-row review. A term can reuse a spelling from an ASD row only as an independently authored IT sense or POS record. It does not change the fixed 2,196-row source sequence, inherit ASD approval, or approve the spelling outside its recorded domain and usage.

## Examples: prose versus literals

Each example has exactly `segments` and `rationale`. Segments concatenate **without inserted spaces** to form the example; spaces are included in segment text deliberately. Segment kinds:

- `{"kind":"prose","text":"..."}` — authored wording subject to editorial review;
- a literal object with `kind: literal`, nonempty `text`, `literal_type`, and `sha256` of the exact UTF-8 text, without an added newline.

Literal types are `command`, `identifier`, `interface`, `quotation`, `path`, and `value`. The digest detects unacknowledged edits; deliberately changing the text and recalculating its hash still requires editorial review. It does not prove that the text matches an external product or is safe to execute.

Known template-marker patterns are rejected in authored prose and metadata as a scaffold guard, not an English grammar test. Literal text bypasses that heuristic: real code can contain `TODO`, angle brackets, or HTML. Literal text still requires valid UTF-8 and a matching hash. This classification does not authorize secret disclosure or harmful execution.

Pilot commands and values are illustrative and are not instructions to run tools. `allowed` and `not_allowed` are editorial judgments for the named rule, not globally approved/disallowed corpora. A negative example can be grammatical English yet violate the particular rule. No example is executed by the validator.

## Shared precedence and conflict process

For this pilot's authors and reviewers:

1. Determine which spans are editable prose and which are exact external/literal text. Do not apply prose rewrites inside preserved spans; do not infer unrestricted lexical approval from preservation.
2. Preserve technical meaning, actors, modality, branch conditions, limits, and required safety/security context. Neither style nor a profile may silently change them.
3. Apply the specific rule within its stated scope, including its exceptions. An imperative is the action's form, not necessarily the sentence's first word.
4. Apply optional stylistic or local length policies only if the preceding constraints remain satisfied. This pilot defines no numeric word or token limit.
5. If a governing external requirement conflicts with these constraints, stop the proposed rewrite and record/escalate the conflict to the responsible editor or technical owner. Do not silently select a winner, alter a literal, omit a prerequisite, or claim conformance. A later general profile system must make such decisions explicit.

This order is an editorial contract, not a claim that the validator checks technical truth or resolves legal/security conflicts. Preserve necessary inline identifiers, but do not hide mandatory actions in skippable notes. Known pronouns and unambiguous referents must both be respected.

## Draft review criteria and validation limits

All 31 target rules are materialized. The original three pilot records still exercise complementary paths:

- `ITSTE-R-0002`: complete many-source allocation, a genuine guidance locator for GR-5, context-specific meanings, and a preserved identifier;
- `ITSTE-R-0015`: direct reader action, a preceding condition, and a named non-reader actor;
- `ITSTE-R-0021`: a protective action before the hazardous operation with a preserved illustrative command and a concrete consequence.

The records contain explicit human-review criteria. Before approval, review source-facet completeness, original wording, meaning preservation, examples and exceptions, rights scope, vocabulary dependencies, and supporting planned targets. A record can validate structurally and still need substantial editorial correction.

The validator checks paths, closed fields, encoding, source and plan authentication, full allocated-source coverage, domains, rights shape, literal digests, and presence of examples and review criteria. It does **not** check arbitrary prose, infer English language from strings, prove translations equivalent, execute commands, certify accessibility or legal rights, evaluate example correctness, approve a vocabulary, release a snapshot, or produce training data. Empty release catalogs and draft status are intentional. This profile rejects release fields but does not implement a general release workflow.

`python3 tools/it_ste_document.py build` generates [one Markdown draft](IT-STE-draft.md) from all manifest-listed rules and original IT-only draft terms plus all [vocabulary review batches](it-ste-vocabulary.md). Its `check` command detects stale output without writing. The document is a derived editorial view, not independently editable canonical content or a released corpus. Further work must define general release checks and record hashes, complete lexical dependencies, reviewed translations, released LLM views, and a separate SFT rights and quality gate. Do not train on these drafts or planning documents as if they were an approved standard.

Original project text: IT-STE contributors, [CC BY-SA 4.0](../LICENSE-CONTENT.md). ASD source ownership and [derivative-permission limits](permissions/asd-ste100-issue-9-derivatives.md) remain separate. This work is independent and not official ASD guidance.
