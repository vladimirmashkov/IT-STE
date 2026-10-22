
# SPDX-License-Identifier: GPL-3.0-only
"""Check the first draft vocabulary review batch; never approve vocabulary."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from collections import Counter
from contextlib import closing
from pathlib import Path

if __package__:
    from . import it_ste_corpus as corpus
else:
    import it_ste_corpus as corpus

adaptation = corpus.adaptation
ROOT = corpus.ROOT
DEFAULT_BATCH = Path("standards/it-ste/vocabulary-reviews/asd-ste100/issue-9/r0001/batch-001.json")
VocabularyError = corpus.CorpusError
require, fields, text, strings = corpus.require, corpus.fields, corpus.text, corpus.strings
DISPOSITIONS = {"allowed", "restricted", "prohibited", "not-applicable", "needs-review"}
# These unflagged adjacent-row overlaps were recorded during the first semantic read.
KNOWN_AMBIGUITIES = {"D-P153-004", "D-P154-002"}


def safe_path(path):
    requested = Path(path)
    if not requested.is_absolute():
        requested = ROOT / requested
    name = corpus.repo_name(requested)
    resolved = corpus.relative_path(name, ROOT)
    require(resolved == requested, "Symlink aliases are forbidden")
    require(not any(p.is_symlink() for p in (requested, *requested.parents)),
            "Symlink paths are forbidden")
    return resolved


def expected(value, wanted, label):
    for key, item in wanted.items():
        require(type(value[key]) is type(item) and value[key] == item,
                f"{label}: unexpected {key}")


def draft(value):
    expected(value, {"status": "draft", "review_status": "editorial-review-needed"}, "review state")


def validate_source(batch):
    # Preflight aliases before the existing authentication routines open anything.
    artifacts = (adaptation.PLAN_MANIFEST, adaptation.PLAN_MAP, adaptation.PLAN_TARGETS,
                 adaptation.SOURCE_MANIFEST, adaptation.SOURCE_DATABASE,
                 adaptation.DOMAINS, adaptation.PERMISSION_RECORD)
    for path in artifacts:
        safe_path(path)
    corpus.authenticate_plan()
    source = batch["source"]
    fields(source, "standard issue issue_date revision revision_scope database_path database_sha256 "
           "manifest_path manifest_sha256 pdf_sha256 pdf_included permission_path permission_sha256 "
           "owner publisher review_state approval_field_interpretation", "source")
    expected(source, {"standard": "ASD-STE100", "issue": "9", "issue_date": "2025-01-15",
                     "revision": "r0001", "pdf_sha256": adaptation.EXPECTED_SOURCE_SHA256,
                     "pdf_included": False, "owner": "ASD", "publisher": "ASD",
                     "review_state": "mechanically-extracted-unreviewed"}, "source")
    for prefix, path in (("database", adaptation.SOURCE_DATABASE),
                         ("manifest", adaptation.SOURCE_MANIFEST),
                         ("permission", adaptation.PERMISSION_RECORD)):
        require(source[prefix + "_path"] == corpus.repo_name(path), f"Wrong {prefix} path")
        require(source[prefix + "_sha256"] == adaptation.sha256_file(path), f"Wrong {prefix} pin")
    interpretation = source["approval_field_interpretation"]
    fields(interpretation, "field algorithm limitation", "source status interpretation")
    require(interpretation["field"] == "dictionary_entries.approval", "Wrong source status field")
    for key in ("algorithm", "limitation"):
        text(interpretation[key], key)
    registry = batch["domain_registry"]
    fields(registry, "path sha256 registry_version status", "domain registry")
    expected(registry, {"path": corpus.repo_name(adaptation.DOMAINS),
                        "sha256": adaptation.sha256_file(adaptation.DOMAINS),
                        "registry_version": "1.0.0", "status": "draft"}, "domain registry")
    return adaptation.domain_ids()


def validate_decision(d, row, number, domains):
    fields(d, "sequence_number entry_id headword part_of_speech_as_extracted physical_pdf_page "
           "upstream_status_raw status review_status it_disposition it_definition domains rationale "
           "permitted_contextual_alternatives examples evidence", "decision")
    draft(d)
    expected(d, {"sequence_number": number, "entry_id": row["id"], "headword": row["headword"],
                 "part_of_speech_as_extracted": row["pos"], "physical_pdf_page": row["pdf_page"]}, "locator")
    raw = d["upstream_status_raw"]
    fields(raw, "field value provenance", "upstream status")
    expected(raw, {"field": "approval", "value": row["approval"]}, "upstream status")
    text(raw["provenance"], "source status provenance")
    require(isinstance(d["it_disposition"], str) and d["it_disposition"] in DISPOSITIONS,
            "Unknown disposition; allowed is only a draft candidate, never approval")
    for key in ("it_definition", "rationale"):
        text(d[key], key)
    require(set(strings(d["domains"], "domains", unique=True)) <= domains, "Unknown domain")
    alternatives = strings(d["permitted_contextual_alternatives"], "alternatives", unique=True)
    require(not any("ITSTE-" in item for item in alternatives), "Alternatives must be expressions, not term IDs")
    fields(d["examples"], "positive problematic", "examples")
    for example in d["examples"].values():
        fields(example, "text explanation", "example")
        text(example["text"], "example text")
        text(example["explanation"], "example explanation")
    ev = d["evidence"]
    fields(ev, "source_standard source_issue source_revision source_entry_id physical_pdf_page "
           "printed_page row_on_page retrieval extraction_warnings mechanical_ambiguities "
           "source_interpretation_status pdf_layout_check review_required", "decision evidence")
    expected(ev, {"source_standard": "ASD-STE100", "source_issue": "9", "source_revision": "r0001",
                  "source_entry_id": row["id"], "physical_pdf_page": row["pdf_page"],
                  "printed_page": row["printed_page"], "row_on_page": int(row["id"].rsplit("-", 1)[1]),
                  "source_interpretation_status": "mechanically-extracted-unreviewed"}, "evidence locator")
    warnings = json.loads(row["warnings"])
    require(ev["extraction_warnings"] == warnings, "Source warnings differ")
    ambiguities = strings(ev["mechanical_ambiguities"], "ambiguities", nonempty=False)
    if warnings or ambiguities or row["id"] in KNOWN_AMBIGUITIES:
        require(d["it_disposition"] == "needs-review", "Mechanical ambiguity requires needs-review")
    strings(ev["review_required"], "review requirements")
    fields(ev["retrieval"], "command scope", "retrieval")
    require(ev["retrieval"]["command"] ==
            f"python3 tools/asd_ste100_local.py entry {row['id']} --compact-json", "Forged retrieval locator")
    text(ev["retrieval"]["scope"], "retrieval scope")
    fields(ev["pdf_layout_check"], "performed method visual_verification_performed", "PDF check")
    require(type(ev["pdf_layout_check"]["performed"]) is bool and
            type(ev["pdf_layout_check"]["visual_verification_performed"]) is bool, "Invalid PDF check flags")


def validate_rights(rights):
    fields(rights, "original_editorial_content project_link asd_source", "rights")
    require(rights["project_link"] == adaptation.PROJECT_URL, "Wrong project attribution link")
    editorial = rights["original_editorial_content"]
    fields(editorial, "license license_url attribution scope", "editorial rights")
    expected(editorial, {"license": "CC-BY-SA-4.0",
                         "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
                         "attribution": "IT-STE contributors",
                         "scope": "Original IT sense definitions, rationales, contextual alternatives, examples, explanations, and editorial assessments only; does not relicense ASD source material."}, "editorial rights")
    source = rights["asd_source"]
    fields(source, "owner standard permission_record publication_basis source_pdf_redistribution "
           "downstream_license separation", "ASD rights")
    expected(source, {"owner": "ASD", "standard": "ASD-STE100 Issue 9",
                      "permission_record": adaptation.PERMISSION_RECORD_REFERENCE,
                      "source_pdf_redistribution": "forbidden",
                      "downstream_license": "unknown; no broader downstream license terms are recorded",
                      "separation": "Do not infer that the editorial CC-BY-SA license applies to ASD-owned source content or that ASD endorses these adaptations."}, "ASD rights")
    text(source["publication_basis"], "permission basis")


def _check(path):
    batch = corpus.load_json(safe_path(path))
    fields(batch, "schema_version kind status review_status batch_id primary_language purpose source "
           "sequence domain_registry interpretation decisions rights evidence", "batch")
    expected(batch, {"schema_version": "1.0.0", "kind": "vocabulary-adaptation-batch",
                     "batch_id": "001", "primary_language": "en"}, "batch")
    draft(batch)
    text(batch["purpose"], "purpose")
    domains = validate_source(batch)
    with closing(sqlite3.connect(adaptation.SOURCE_DATABASE.as_uri() + "?mode=ro", uri=True)) as connection:
        connection.row_factory = sqlite3.Row
        total = connection.execute("SELECT count(*) FROM dictionary_entries").fetchone()[0]
        rows = connection.execute(
            "SELECT id,headword,pos,approval,pdf_page,printed_page,warnings FROM dictionary_entries "
            "ORDER BY pdf_page,CAST(substr(id,-3) AS INTEGER) LIMIT 41").fetchall()
    require(total == 2196 and len(rows) == 41, "Unexpected source row count")
    seq = batch["sequence"]
    fields(seq, "first_entry_id last_entry_id order selection order_basis entry_count total_source_rows remaining", "sequence")
    expected(seq, {"first_entry_id": rows[0]["id"], "last_entry_id": rows[39]["id"],
                   "order": "physical-page-then-row", "entry_count": 40,
                   "total_source_rows": total, "remaining": total - 40}, "sequence")
    require(isinstance(batch["decisions"], list) and len(batch["decisions"]) == 40, "Require all first 40 rows")
    for number, (decision, row) in enumerate(zip(batch["decisions"], rows), 1):
        validate_decision(decision, row, number, domains)
    validate_rights(batch["rights"])
    ev = batch["evidence"]
    require(isinstance(ev, dict), "Invalid batch evidence")
    for key in ("human_editorial_approval", "canonical_terms_created", "rules_changed"):
        require(ev[key] is False, f"Batch cannot claim {key}")
    require(isinstance(batch["interpretation"], dict), "Invalid interpretation")
    for key in ("disposition_scope", *sorted(DISPOSITIONS), "alternatives", "examples",
                "literal_boundary", "source_content_limit"):
        text(batch["interpretation"][key], key)
    return batch, {"total": total, "candidates": 40, "remaining": total - 40,
                   "next_entry_id": rows[40]["id"],
                   "dispositions": dict(sorted(Counter(d["it_disposition"] for d in batch["decisions"]).items()))}


def checked(path):
    try:
        return _check(path)
    except VocabularyError:
        raise
    except (adaptation.PlanError, OSError, ValueError, TypeError, KeyError, IndexError,
            AttributeError, RecursionError, sqlite3.Error) as error:
        raise VocabularyError(f"Cannot validate vocabulary batch: {error}") from error


def check(path=DEFAULT_BATCH) -> dict:
    """Return verified source/candidate counts, not vocabulary approval."""
    return checked(path)[1]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("check", "entry"):
        command = commands.add_parser(name)
        command.add_argument("--batch", type=Path, default=DEFAULT_BATCH)
        if name == "entry":
            command.add_argument("id")
        command.add_argument("--compact-json", action="store_true")
    args = parser.parse_args(argv)
    try:
        batch, summary = checked(args.batch)
        if args.command == "entry":
            result = next((d for d in batch["decisions"] if d["entry_id"] == args.id), None)
            require(result is not None, "Entry is not declared in this draft batch")
        else:
            result = {"status": "draft", "review_status": "editorial-review-needed",
                      "validation": "structure-and-provenance-only; no vocabulary approval", **summary}
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":") if args.compact_json else None))
        return 0
    except VocabularyError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
