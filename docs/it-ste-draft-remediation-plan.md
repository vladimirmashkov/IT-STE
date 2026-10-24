# IT-STE draft remediation execution plan

This is a bounded-work plan for the IT-STE draft. It records sequencing and stopping rules; it is not vocabulary approval, canonical release authority, or SFT authorization. English is authoritative.

## Current boundary

- Recovery Block 0 was closed in `b1fe909` (`Add draft IT-only term contract`) after reviewing the interrupted implementation of the first W3 term-contract slice.
- The current W3 slice adds only the draft-only original IT term records `ITSTE-T-0003` (`problem`, noun) and `ITSTE-T-0004` (`incident`, noun). It must not change the five inspected ASD-derived rows or the fixed 2,196-row source sequence.
- The canonical ASD queue must be recomputed before every slice. At this slice it is empty: 2,196 records / 55 batches, 120 allowed, 1,510 restricted, 407 prohibited, 159 not-applicable, 0 needs-review.
- If the queue becomes non-empty, W1 takes precedence over W2/W3. A queue offset is never a resume pointer; record exact IDs, pages, evidence notes, and the next action.

## Work blocks

### Block 0 — Recover and close the interrupted W3 implementation

Review the complete pending inventory, validate the term contract, canonical records, external reference metadata, generated document, tests, source authentication, diagnostics, and Git diff. Update the checkpoint with actual results and commit only files wholly owned by this slice. Do not add another term in this block.

### Block 1 — W1: explicit ASD blockers

Recompute the queue from offset 0. If unresolved rows exist, process one physical-page slice (normally one page and no more than two related rows): retrieve the existing proposal and exact ASD entry, visually inspect the authenticated PDF when layout matters, research substantive IT meaning when applicable, preserve raw warnings and source pins, and leave unresolved questions `needs-review`. Keep every disposition `draft` / `editorial-review-needed`.

### Block 2 — W3: ITIL/service-management terms

Use one related pair per iteration. Each pair is a research scope, not a promise to materialize records. Create a draft original term only when the inspected evidence supports a bounded sense/POS and the term remains distinct from existing ASD-derived meanings. Otherwise record the candidate as blocked or unresolved.

1. **Completed recovery slice:** `service` noun and `alert` noun — `ITSTE-T-0001` and `ITSTE-T-0002`.
2. **Completed bounded slice:** `problem` and `incident` — `ITSTE-T-0003` and `ITSTE-T-0004`, retained as restricted draft senses with explicit human-review criteria and no ASD provenance.
3. **Next slice:** `known error` and `workaround` — use Problem Management evidence; distinguish a recorded cause/workaround from a root-cause fix.
4. `service request` and `service desk` — use dedicated Service Request Management/Service Desk evidence; do not equate a desk with a queue, team, or escalation authority.
5. `configuration item` and `IT asset` — separate configuration relationships and attributes from ownership and financial lifecycle.
6. `service level agreement` and `service level target` — distinguish documented commitments/responsibilities from measurable targets and indicators.
7. `availability` and `resilience` — distinguish ability to perform an agreed function from continuation/recovery after disruption.
8. `continual improvement` and `change authority` — verify the practice boundary and the authority role before materialization.
9. `release` noun and `deployment` — distinguish the available version/set of components from placing it or a change into a target environment; preserve the ASD `release` verb.

The next term ID is allocated only after the preceding bounded slice has justified materialization. External ITIL metadata is reference evidence, never ASD provenance or a copied official glossary.

### Block 3 — W2: editorial and technical review of the whole draft

Review all 31 canonical rules and all 2,196 vocabulary decisions in bounded thematic slices, not only W1 flags:

- lexical admission, POS, alternatives, and rule/term consistency;
- grammar, modality, actors, conditions, sequencing, and execution units;
- safety/security consequences, protective context, literals, and measurable limits;
- examples, negative examples, domain scope, and cross-record contradictions;
- vocabulary batches in physical-page/order groups, preserving source boundaries and draft guards.

Record decisions and outstanding questions in compact notes. Do not treat research review as human approval, and do not convert an editorial candidate into approved vocabulary.

### Block 4 — W3 beyond the current ITIL inventory

After the service-management inventory is bounded, research missing concepts in the registered IT domains (including API, authentication/authorization, containers, transactions, distributed systems, and secret/key lifecycle). Check existing proposed senses first. Before accepting other origins or multi-sense relations, extend the contract deliberately for source/version policy, relations, and review—not by weakening the current validator.

### Block 5 — Release and dataset gates

Keep `status: draft`, `review_status: editorial-review-needed`, and the release catalog unreleased throughout remediation. Before any separately authorized release, require approved editorial/technical content, canonical vocabulary and release validation, rights/provenance review, reviewed translations, and an independent dataset/SFT quality gate. Successful structural checks, an empty W1 queue, or materialized draft terms never establish approval, publication, conformance, or SFT readiness.

## Required bounded-iteration loop

1. Read the current checkpoint, this plan, the active research note, and only the selected records.
2. Run the ASD source doctor; recompute canonical counts and the offset-0 queue.
3. Retrieve exact ASD entries and inspect the authenticated PDF page when layout is material; inspect competent, versioned external sources for substantive IT claims.
4. Compare the current wording with defensible alternatives and record facts, inference, limits, and one next action in one compact research note.
5. Apply only justified draft changes; preserve IDs, source pins, warnings, rights, and fixed source sequence.
6. Run the affected check first, then the handoff's wider validation, diagnostics, and `git diff --check`.
7. Update the current checkpoint with actual results and the next exact slice.
8. Review the entire worktree and index. Autocommit only explicit paths wholly owned by the iteration; leave mixed or unrelated work untouched.

Every iteration stops at its declared slice. It does not bulk-materialize the candidate inventory, read the complete generated Markdown or source extraction into context, or claim external corroboration without inspecting the cited source.
