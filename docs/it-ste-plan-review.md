# Cross-target review of the Issue 9 adaptation plan

[Русское резюме](it-ste-plan-review.ru.md)

This English report is authoritative. It records an editorial review on 2026-10-22, not normative IT-STE requirements, an IT-STE release, or official ASD guidance.

## Scope and conclusion

Reviewed all 31 planned targets, their boundaries and exceptions, and the reciprocal mapping of all 61 source blocks: 53 rules and 8 general recommendations from ASD-STE100 Issue 9, representation revision `r0001`. The worktree was clean before this review.

**Conclusion:** retain all 31 stable IDs and their current source allocations. No merge, split, retirement, or renumbering is justified by this review. Three clarifications below resolve a cross-target contradiction and two source-facet disposition gaps. The plan is ready for canonical-schema design and controlled pilot authoring, **not** automatic bulk materialization, conformance claims, or publication as a finished standard.

The review has three complementary parts: a complete editorial boundary review, an independent cross-target exception review, and an independent source-traceability review. Structural authentication is reproducible; the editorial judgments are not a mechanical proof of semantic completeness.

## Reviewed artifact pins

Paths below are relative to the repository root. These hashes identify the corrected plan reviewed here; later edits require rechecking the affected conclusions, not silently treating this report as current.

| Artifact | Path / identity | SHA-256 |
| --- | --- | --- |
| Private source | `.local/sources/ASD-STE100-issue-9.pdf` | `d1f4ea9e7cd6e46b47aa9057209f99e78c0e9cfc4e27a5b07895b05c1a166431` |
| Published source representation | `standards/asd-ste100/versions/issue-9/revisions/r0001/reference/reference.sqlite3` | `4a1d2bc943d35f689599af564e5587e870d384552c25aaaeff9892effc87642b` |
| Plan manifest | `standards/it-ste/adaptation-plans/asd-ste100/issue-9/r0001/manifest.json` | `0f9d2636f8d5257b9ea71d97601b90c5caa44e661d9f1715a4da87a19314bc56` |
| Source map | `standards/it-ste/adaptation-plans/asd-ste100/issue-9/r0001/map.jsonl` | `83760ef899bab6839ae4be80543e3b03498b8e00b94c0881f0933f8e97897e16` |
| Target concepts | `standards/it-ste/adaptation-plans/asd-ste100/issue-9/r0001/targets.json` | `9925461987f41f1f948d7d4e1662eab19c76d9c15bc7bb3f036c6d580b5b97aa` |
| Domain registry | `standards/it-ste/domains/v1.0.0.json` | `b79f55d906bb669a4b2e326b7fedd912ec813586f788e2694837b47d7e603675` |

The source PDF remains private and ignored. The database is an authenticated but mechanically extracted representation. This review did not independently verify every PDF layout, diagram, or dictionary row.

## Corrections made

| Finding | Evidence | Disposition |
| --- | --- | --- |
| `0015` said an instruction must start with an imperative, conflicting with condition-first `0016`, `0021`, and `0029`. | Issue 9 rules 5.3–5.4, physical PDF pp. 89–91. | `ITSTE-R-0015` now controls the action's verb form, not the sentence's first word; a prerequisite or condition can precede it. Updated the 5.3 rationale. |
| `0014` changed the controlled unit from sentence to step without explicitly disposing of the sentence-level source requirement. | Issue 9 rule 5.2, physical PDF pp. 88–89: one instruction per sentence and potentially multiple sentences per work step. | Documented the IT adaptation as a step-level execution unit plus a preference for one principal instruction per sentence. Multiple sentences can retain coupled actions, results, limits, or verification. Updated the 5.2 rationale; existing atomic-action exceptions remain. |
| `0019` preserved early topic identification but did not explicitly retain the topic opening's bridging function. | Issue 9 rule 6.5, physical PDF p. 100. | Retained that function in `ITSTE-R-0019`, with a supporting cross-reference to `0013`. Updated the 6.5 rationale. |

The supporting cross-references above do not allocate additional source derivation edges or change source ownership. All target entries remain `planned`; all general recommendations remain source `kind: guidance`.

## Boundaries of all 31 targets

Every ID below has a distinct editorial decision to own. Related IDs cooperate; they do not automatically inherit each other's source allocations. Candidate domains remain editorial planning tags, not a complete conformance-scope taxonomy.

| Target ID | Primary responsibility | Boundary with related targets |
| --- | --- | --- |
| `ITSTE-R-0001` | Admission of general vocabulary and domain terms. | `0002` controls a particular admitted use; `0027` adds phrase-level admission requirements. |
| `ITSTE-R-0002` | Approved meaning, part of speech, form, and context; false friends. | Admission is `0001`; grammatical permission in `0007` is not lexical approval. |
| `ITSTE-R-0003` | Authoritative name for a concept in context. | `0004` selects a term when authority does not control it; `0028` controls recurring wording. |
| `ITSTE-R-0004` | Clear, internationally understandable term selection. | Do not override authoritative terms under `0003` or redefine them through shortening. |
| `ITSTE-R-0005` | American English prose baseline and governing-variety exceptions. | Does not normalize exact names, quotations, localized examples, or machine-significant text. |
| `ITSTE-R-0006` | Clarity of a selected multi-word term, aliases, and hyphenation. | Not vocabulary admission or term selection; no artificial hyphens to satisfy `0025`. |
| `ITSTE-R-0007` | Simple, precise tense, aspect, participles, and verb constructions. | Lexical forms remain subject to `0002`; voice and responsibility belong to `0008`. |
| `ITSTE-R-0008` | Active voice, justified passive voice, and truthful actors. | Reader-action form is `0015`; neither target permits an invented actor. |
| `ITSTE-R-0009` | Direct verbs instead of avoidable nominalizations. | Not an instruction-only rule; imperative form belongs to `0015`, phrase approval to `0027`. |
| `ITSTE-R-0010` | Concise, concrete sentences without universal word limits. | Execution units are `0014`; local measurement methods are `0025`. |
| `ITSTE-R-0011` | Necessary grammatical words, articles, clause markers, contractions, and clear fragments. | Referential cohesion is `0013`; modifier relationships are `0029`. |
| `ITSTE-R-0012` | Parallel lists, ordering, lead-ins, and consistent presentation. | Topic grouping is `0019`; execution-step boundaries are `0014`; literal syntax is preserved. |
| `ITSTE-R-0013` | Connections between ideas, canonical anchors, and unambiguous referents. | Information sequence is `0018`; topic openings are `0019`; no mechanical repetition. |
| `ITSTE-R-0014` | Independently executable steps and justified coupled actions. | Sentence focus remains `0010`; verb form is `0015`; required results remain with the action. |
| `ITSTE-R-0015` | Imperative reader actions versus explicitly named other actors. | `0016` can place a condition first; policy modality is not merely stylistic emphasis. |
| `ITSTE-R-0016` | Prerequisites and conditions before dependent actions. | `0021` applies this to protective instructions; this target is not limited to hazards. |
| `ITSTE-R-0017` | Supplemental notes versus required procedural content. | A necessary inline identifier in parentheses is not automatically a skippable note under `0024`. |
| `ITSTE-R-0018` | Reader-first sequence, gradual detail, and local retrieval context. | `0019` defines topic blocks; `0013` resolves references. Only optional detail can be deferred. |
| `ITSTE-R-0019` | One primary topic per paragraph or equivalent block and useful topic openings. | `0018` controls the larger information sequence; `0013` supplies general cohesion principles. |
| `ITSTE-R-0020` | Assessed risk labels and documented classification mappings. | Does not prescribe every protective action (`0021`) or invent consequences (`0022`). |
| `ITSTE-R-0021` | Specific protective action or condition before the hazardous operation. | Risk level is `0020`; explanation is `0022`; both travel with relevant retrieved content. |
| `ITSTE-R-0022` | Credible, appropriately disclosed consequences. | Explanation does not replace action; security sensitivity does not excuse an unusable precaution. |
| `ITSTE-R-0023` | Punctuation that clarifies prose structure. | Hyphenation is `0006`; parenthetical information is `0024`; executable punctuation is not edited. |
| `ITSTE-R-0024` | Clear parenthetical references, explanations, and alternatives. | Required conditions and choices stay explicit; parentheses in syntax are not prose asides. |
| `ITSTE-R-0025` | Reproducible local length metrics and tokenizer identity. | Not a universal limit or a readability proof; cannot override meaning or exact literals. |
| `ITSTE-R-0026` | Meaning-preserving rewriting and checks on related material. | Integrates other controls without turning dictionary replacements into unconditional rewrites. |
| `ITSTE-R-0027` | Explicit approval of multi-word verb meanings and patterns. | Extends `0001`/`0002`; neither a blanket phrasal-verb ban nor unrestricted admission. |
| `ITSTE-R-0028` | Reusable wording when meaning and context match. | `0003` controls names; real operational differences must not be flattened into one template. |
| `ITSTE-R-0029` | Explicit means, association, conditions, and possessive relationships. | `0016` controls condition placement; grammatical possessives are not banned. |
| `ITSTE-R-0030` | Clear English equivalents of Latin abbreviations without scope loss. | Not a general abbreviation ban; required sets cannot be replaced with an open-ended list. |
| `ITSTE-R-0031` | Neutral, respectful language with accurate references to people. | `0013` still requires clear referents; exact external terms need mappings, not silent renaming. |

## Shared constraints for canonical authoring

These are review decisions to carry into the schema and authoring checklist, not newly published normative rules.

1. **Editable prose versus preserved text.** Classify spans or blocks before applying lexical or style checks. Exact external strings and literals remain exact. Preservation does not approve their words for unrestricted explanatory prose and does not authorize unsafe execution or disclosure of secrets. Quoting unsafe text is not endorsing it.
2. **Lexical versus grammatical permission.** An allowed tense, participle, possessive, pronoun construction, or multi-word pattern is not blanket approval of every word or sense. Define entry-level forms and contexts, admission authority, and the treatment of unlisted terms before making conformance claims.
3. **Truth before surface uniformity.** Rewrites, templates, active voice, brevity, and local metrics cannot invent actors, alter modality or limits, erase branches, or change technical effects. Unclear source meaning requires clarification.
4. **Executable units.** Define the relationship between a sentence, step, transaction, and example. Coupling actions requires a technical reason, not convenience; it does not make dense instruction chains acceptable.
5. **Required versus optional context.** Define the independently consumable unit. Prerequisites, decision-relevant referents, protective actions, and necessary consequences must remain available with the action. A retrieval boundary cannot make required context optional. Necessary inline identifiers may be parenthetical; protective instructions and branch selection must not be hidden as asides.
6. **Respect and reference clarity together.** Use known pronouns correctly. If a referent is ambiguous, use a name or role instead of substituting an inaccurate pronoun. Do not recreate the ASD pronoun inventory as an IT policy.
7. **Profiles and exceptions.** Define applicable profiles and a conflict/exception process. A local length limit that cannot accommodate a literal, atomic action, or prerequisite needs an explicit exception or escalation path, not corrupted content. Choose a reproducible metric; token counts are tokenizer-specific.

## Traceability and materialization gate

The current validator authenticates source pins, source objects, domain IDs, counts, and exact map-to-target relationships. It does **not** establish facet-level semantic completeness, verify the declared reading method, or reconcile canonical records that do not exist yet. Required-clause tests are planning regressions, not an executable prose-conformance test.

Before creating a versioned canonical snapshot, establish and validate a source locator contract that can address the published retrieval database without inventing canonical ASD record endpoints. It must retain, directly or through immutable authenticated references:

- source standard, issue, representation revision, database SHA-256, and source PDF SHA-256;
- source block ID, original `rule` or `guidance` kind, and physical PDF page range;
- the exact adaptation-plan path and manifest/map/targets hashes;
- the target ID, rationale, and disposition of each relevant source facet;
- source ownership, permission evidence, project attribution, and applicable rights without silently replacing third-party terms with project-license defaults.

Distinguish **primary derivation** from a **supporting cross-reference** and from a **facet delegated to another target**. The current `target_rule_ids` describe primary allocations; references inside rationale or intent are not additional graph edges. For example:

- `6.1 → 0018` retains the one-principal-subject facet locally and references `0010` for consistency;
- `6.5 → 0019` retains the topic-opening bridge locally and references `0013` for consistency;
- `9.4 → 0028` includes authoritative terms locally and references `0003` for terminology policy.

Do not infer extra `adapted_from` edges by scraping every mentioned target ID. If a future rule really delegates a retained facet elsewhere, record that decision and its destination explicitly in the materialization model.

Templates are scaffolds, not adaptation-ready records: complete origin, source references, rights, evidence, and attribution deliberately. Never publish a source-derived rule with an unchanged `origin: original` default. Guidance must not be relabeled as a source rule just to fit a relation schema.

## Next authoring gate and limits

Proceed in this order:

1. Define canonical source/facet locators, prose/literal boundaries, profile precedence, and the record-validation contract.
2. Pilot a small set that exercises the difficult boundaries: lexical use, condition-led imperative, and risk instruction with a preserved literal. Keep the existing stable IDs.
3. Give each pilot English normative text, applicability, exceptions, positive/negative IT examples, source-facet dispositions, and a testable review criterion. Keep Russian optional and subordinate to English.
4. Validate records and provenance before generating Markdown or LLM exports. Reconcile pilot records with the pinned plan; do not mutate targets into canonical records.
5. Expand to the remaining targets only after the pilot contract works. Define separately whether a criterion is mechanically checkable, requires human judgment, or is outside automated scope.

The review does not adapt the full ASD dictionary, guarantee every IT domain is covered, verify all PDF typography, settle all future profile conflicts, or establish SFT dataset readiness. Do not use `reviewed` map status as an automatic normative-release or training-data approval.

## Reproduction and attribution

```sh
python3 tools/asd_ste100_local.py doctor
python3 tools/it_ste_adaptation.py check
python3 -W error::ResourceWarning -m unittest discover -s tests -v
```

Source ownership remains with the Aerospace, Security and Defence Industries Association of Europe (ASD). Permission evidence is recorded in [the derivative permission record](permissions/asd-ste100-issue-9-derivatives.md); do not infer broader source rights from it. The private PDF is not published.

Original review text: IT-STE contributors, [CC BY-SA 4.0](../LICENSE-CONTENT.md). Required project attribution: https://github.com/vladimirmashkov/IT-STE.
