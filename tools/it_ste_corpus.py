#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Validate the closed, draft-only IT-STE pilot profile, not prose conformance."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any

if __package__:
    from . import it_ste_adaptation as adaptation
else:
    import it_ste_adaptation as adaptation

ROOT = adaptation.ROOT
DEFAULT_MANIFEST = Path(
    "standards/it-ste/versions/0.1.0-draft.1/revisions/r0001/manifest.json"
)
OWNER = {
    "name": "Aerospace, Security and Defence Industries Association of Europe (ASD)",
    "url": "https://asd-ste100.org/",
}
PROJECT = {"name": "IT-STE contributors", "url": adaptation.PROJECT_URL}
SOURCE_ID = "ASDSTE-SOURCE-ISSUE9-R0001"
SCOPE = "original IT-STE wording and examples only; ASD source rights remain separate"
MARKER = re.compile(r"\b(?:TODO|TBD|FIXME|PLACEHOLDER)\b|\{\{|\}\}|<[^>\n]+>|\[(?:insert|replace)\b", re.IGNORECASE)
TERM_ID_RE = re.compile(r"ITSTE-T-[0-9]{4}")
EXTERNAL_SOURCE_ID_RE = re.compile(r"ITIL-SOURCE-[A-Z0-9-]+")
TERM_PARTS_OF_SPEECH = {"noun", "verb", "adjective", "adverb", "phrase"}
TERM_USAGES = {"allowed", "restricted", "prohibited"}
ORIGINAL_SCOPE = "original IT-STE wording and examples only; external source rights remain separate"


class CorpusError(RuntimeError):
    """A user-facing profile validation error."""


def require(condition, message):
    if not condition:
        raise CorpusError(message)


def fields(value, names, label):
    require(isinstance(value, dict), f"{label}: expected an object")
    expected = set(names.split())
    require(set(value) == expected, f"{label}: expected exactly fields {sorted(expected)}")


def text(value, label, *, authored=True, allow_blank=False):
    require(isinstance(value, str) and bool(value if allow_blank else value.strip()),
            f"{label}: expected nonempty text")
    if authored:
        require(not MARKER.search(value), f"{label}: template marker is forbidden")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise CorpusError(f"{label}: invalid Unicode text") from error


def strings(value, label, *, unique=False, nonempty=True):
    require(isinstance(value, list) and (bool(value) or not nonempty), f"{label}: expected an array")
    for item in value:
        text(item, label)
    if unique:
        require(len(value) == len(set(value)), f"{label}: duplicate values")
    return value


def confined(path, base):
    try:
        resolved = path.resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise CorpusError(f"Cannot resolve {path}: {error}") from error
    require(resolved.is_relative_to(base.resolve()), f"Path escapes {base}: {path}")
    return resolved


def relative_path(value, base):
    require(isinstance(value, str) and bool(value), "Expected a relative path")
    path = Path(value)
    require(
        not path.is_absolute() and "\\" not in value
        and all(part not in {"", ".", ".."} for part in value.split("/")),
        f"Unsafe relative path: {value!r}",
    )
    result = confined(base / path, base)
    confined(result, ROOT)
    require(result.is_file(), f"Expected a file: {value}")
    return result


def repo_name(path):
    path = Path(path)
    require(path.is_relative_to(ROOT), f"Artifact is outside repository: {path}")
    name = path.relative_to(ROOT).as_posix()
    relative_path(name, ROOT)
    return name


def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path, *, lines=False) -> Any:
    raw = path.read_bytes()
    require(not raw.startswith(b"\xef\xbb\xbf"), f"{path}: UTF-8 BOM is forbidden")
    require(raw.endswith(b"\n") and b"\r" not in raw, f"{path}: require LF and final newline")
    try:
        decoded = raw.decode("utf-8")
        def parse(part):
            return json.loads(part, object_pairs_hook=pairs, parse_constant=bad_constant)
        value = [parse(line) for line in decoded.splitlines()] if lines else parse(decoded)
    except (UnicodeError, ValueError) as error:
        raise CorpusError(f"{path}: invalid UTF-8 JSON: {error}") from error
    return value


def bad_constant(value):
    raise CorpusError(f"Non-JSON numeric constant: {value}")


def authenticate_plan():
    # Preflight the exact files that the existing plan validator consumes. Its
    # parser is intentionally less strict than this new pilot profile's parser.
    for path in (adaptation.PLAN_MANIFEST, adaptation.PLAN_TARGETS,
                 adaptation.DOMAINS, adaptation.SOURCE_MANIFEST):
        load_json(relative_path(repo_name(path), ROOT))
    load_json(relative_path(repo_name(adaptation.PLAN_MAP), ROOT), lines=True)
    for path in (adaptation.SOURCE_DATABASE, adaptation.PERMISSION_RECORD):
        repo_name(path)
    with contextlib.redirect_stdout(io.StringIO()):
        adaptation.check()
    return {
        "path": repo_name(adaptation.PLAN_MANIFEST),
        "manifest_sha256": adaptation.sha256_file(adaptation.PLAN_MANIFEST),
        "map_sha256": adaptation.sha256_file(adaptation.PLAN_MAP),
        "targets_sha256": adaptation.sha256_file(adaptation.PLAN_TARGETS),
        "domain_registry_sha256": adaptation.sha256_file(adaptation.DOMAINS),
    }


def validate_source(source):
    permission = adaptation.PERMISSION_RECORD_REFERENCE
    relative_path(permission, ROOT)
    require(adaptation.sha256_file(ROOT / permission) == adaptation.EXPECTED_PERMISSION_SHA256,
            "Permission evidence hash mismatch")
    artifact = repo_name(adaptation.SOURCE_DATABASE)
    require(adaptation.sha256_file(ROOT / artifact) == adaptation.EXPECTED_DATABASE_SHA256,
            "Source artifact hash mismatch")
    expected = {
        "schema_version": "1.1.0", "id": SOURCE_ID, "standard": "asd-ste100",
        "version": "issue-9", "revision": "r0001", "title": "ASD-STE100 Issue 9",
        "url": "https://asd-ste100.org/", "retrieved_at": None,
        "artifact_path": artifact, "artifact_sha256": adaptation.EXPECTED_DATABASE_SHA256,
        "source_pdf_sha256": adaptation.EXPECTED_SOURCE_SHA256, "owner": OWNER,
        "permission": {
            "path": permission, "sha256": adaptation.EXPECTED_PERMISSION_SHA256,
            "scope": "authorized-derivatives-only", "source_pdf_redistribution": "forbidden",
            "downstream_license": "unknown",
        },
        "rights": {
            "license": None, "license_url": None, "redistribution": "unknown",
            "adaptation": "unknown", "attribution": [OWNER], "evidence": [permission],
        },
    }
    require(source == expected, "Source must exactly match authenticated Issue 9 provenance and rights")


def validate_rights(rights):
    fields(rights, "license license_url redistribution adaptation attribution evidence scope", "rights")
    expected = {
        "license": "CC-BY-SA-4.0", "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "redistribution": "allowed", "adaptation": "allowed", "scope": SCOPE,
    }
    for key, value in expected.items():
        require(rights[key] == value, f"rights: unexpected {key}")
    attribution = rights["attribution"]
    require(isinstance(attribution, list) and len(attribution) == 2
            and OWNER in attribution and PROJECT in attribution, "rights: require project and ASD attribution")
    evidence = strings(rights["evidence"], "rights.evidence", unique=True)
    require(set(evidence) == {"LICENSE-CONTENT.md", adaptation.PERMISSION_RECORD_REFERENCE},
            "rights: unexpected evidence paths")
    for path in evidence:
        relative_path(path, ROOT)


def validate_original_rights(rights):
    fields(rights, "license license_url redistribution adaptation attribution evidence scope", "term rights")
    expected = {
        "license": "CC-BY-SA-4.0", "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "redistribution": "allowed", "adaptation": "allowed", "scope": ORIGINAL_SCOPE,
    }
    for key, value in expected.items():
        require(rights[key] == value, f"term rights: unexpected {key}")
    require(rights["attribution"] == [PROJECT], "term rights: require IT-STE attribution only")
    evidence = strings(rights["evidence"], "term rights.evidence", unique=True)
    require(set(evidence) == {"LICENSE-CONTENT.md"}, "term rights: unexpected evidence paths")
    for path in evidence:
        relative_path(path, ROOT)


def validate_external_source(source):
    fields(source, "schema_version id standard version revision title url retrieved_at publisher status rights notice",
           "external source")
    require(source["schema_version"] == "1.1.0", "external source: unexpected schema_version")
    require(EXTERNAL_SOURCE_ID_RE.fullmatch(source["id"]), "external source: invalid ID")
    require(source["standard"] == "itil", "external source: only ITIL references are accepted here")
    for key in ("version", "revision", "title", "url", "retrieved_at", "status", "notice"):
        text(source[key], f"external source.{key}")
    require(source["url"].startswith("https://"), "external source: URL must use HTTPS")
    require(re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", source["retrieved_at"]),
            "external source: retrieved_at must be an ISO date")
    fields(source["publisher"], "name url", "external source.publisher")
    text(source["publisher"]["name"], "external source.publisher.name")
    text(source["publisher"]["url"], "external source.publisher.url")
    fields(source["rights"], "license license_url redistribution adaptation attribution evidence",
           "external source.rights")
    require(source["rights"]["license"] is None and source["rights"]["license_url"] is None,
            "external source.rights: unknown license must remain explicit")
    require(source["rights"]["redistribution"] == "unknown" and source["rights"]["adaptation"] == "unknown",
            "external source.rights: unknown downstream rights must remain explicit")
    require(source["rights"]["attribution"] == [source["publisher"]],
            "external source.rights: publisher attribution is required")
    evidence = strings(source["rights"]["evidence"], "external source.rights.evidence", unique=True)
    for path in evidence:
        relative_path(path, ROOT)


def validate_term_examples(examples):
    fields(examples, "allowed not_allowed", "term examples")
    for category, items in examples.items():
        require(isinstance(items, list) and bool(items), f"term examples.{category}: require examples")
        for example in items:
            fields(example, "text rationale", "term example")
            text(example["text"], "term example.text")
            text(example["rationale"], "term example.rationale")


def validate_term_refs(refs, external_sources):
    require(isinstance(refs, list) and bool(refs), "term source_refs: require external references")
    seen = set()
    for ref in refs:
        fields(ref, "source_id locator", "term source_ref")
        source_id = ref["source_id"]
        require(source_id in external_sources, "term source_ref: ASD or unknown provenance is forbidden")
        locator = ref["locator"]
        fields(locator, "section", "term locator")
        text(locator["section"], "term locator.section")
        key = (source_id, locator["section"])
        require(key not in seen, "term source_refs: duplicate locator")
        seen.add(key)


def validate_term(term, domains, external_sources):
    fields(term, "schema_version id kind language status origin term part_of_speech definition domains usage "
           "rationale alternatives examples translation_of source_refs review rights", "term")
    for key, expected in {"schema_version": "1.1.0", "kind": "term", "language": "en",
                          "status": "draft", "origin": "original", "translation_of": None}.items():
        require(term[key] == expected, f"term: unexpected {key}")
    identifier = term["id"]
    require(isinstance(identifier, str) and TERM_ID_RE.fullmatch(identifier),
            "term: ID must use the ITSTE-T-NNNN namespace")
    for key in ("term", "definition", "rationale"):
        text(term[key], f"term.{key}")
    require(term["part_of_speech"] in TERM_PARTS_OF_SPEECH, "term: unsupported part of speech")
    applied = strings(term["domains"], "term.domains", unique=True)
    require(set(applied) <= domains, "term.domains: unknown domain IDs")
    require(term["usage"] in TERM_USAGES, "term: invalid usage")
    alternatives = strings(term["alternatives"], "term.alternatives", unique=True, nonempty=False)
    require(all(TERM_ID_RE.fullmatch(value) and value != identifier for value in alternatives),
            "term.alternatives: require other canonical term IDs")
    validate_term_examples(term["examples"])
    validate_term_refs(term["source_refs"], external_sources)
    fields(term["review"], "mode automation criteria", "term review")
    require(term["review"]["mode"] == "human" and term["review"]["automation"] == "structure-only",
            "term review: human, structure-only review is required")
    strings(term["review"]["criteria"], "term review.criteria")
    validate_original_rights(term["rights"])
    return identifier


def validate_examples(examples):
    fields(examples, "allowed not_allowed", "examples")
    for category, items in examples.items():
        require(isinstance(items, list) and bool(items), f"examples.{category}: require examples")
        for example in items:
            fields(example, "segments rationale", "example")
            text(example["rationale"], "example.rationale")
            segments = example["segments"]
            require(isinstance(segments, list) and bool(segments), "example: require segments")
            prose = []
            for segment in segments:
                require(isinstance(segment, dict), "segment: expected an object")
                kind = segment.get("kind")
                require(kind in ("prose", "literal"), "segment: unknown kind")
                fields(segment, "kind text" if kind == "prose" else "kind text literal_type sha256", "segment")
                text(segment["text"], "segment.text", authored=False, allow_blank=kind == "prose")
                if kind == "prose":
                    prose.append(segment["text"])
                else:
                    require(not MARKER.search("".join(prose)), "example prose: template marker is forbidden")
                    prose.clear()
                    require(segment["literal_type"] in ("command", "identifier", "interface", "quotation", "path", "value"),
                            "segment: unknown literal_type")
                    digest = hashlib.sha256(segment["text"].encode("utf-8")).hexdigest()
                    require(segment["sha256"] == digest, "segment: literal digest mismatch")
            require(not MARKER.search("".join(prose)), "example prose: template marker is forbidden")


def validate_refs(refs, allocated, blocks):
    require(isinstance(refs, list) and bool(refs), "source_refs: require source references")
    seen = set()
    for ref in refs:
        fields(ref, "source_id locator facets", "source_ref")
        require(ref["source_id"] == SOURCE_ID, "source_ref: wrong source_id")
        locator = ref["locator"]
        fields(locator, "block_id kind physical_pdf_pages", "locator")
        block_id = locator["block_id"]
        require(isinstance(block_id, str) and block_id in allocated, "locator: unallocated source block")
        require(block_id not in seen, "source_refs: duplicate block")
        seen.add(block_id)
        block = blocks[block_id]
        pages = locator["physical_pdf_pages"]
        require(isinstance(pages, list) and all(type(page) is int for page in pages), "locator: invalid pages")
        require(locator == {"block_id": block_id, "kind": block["kind"],
                            "physical_pdf_pages": [block["start_pdf_page"], block["end_pdf_page"]]},
                "locator differs from authenticated source (guidance stays guidance)")
        facets = ref["facets"]
        require(isinstance(facets, list) and bool(facets), "source_ref: require facets")
        for facet in facets:
            fields(facet, "source_facet disposition rationale target_field", "facet")
            text(facet["source_facet"], "facet.source_facet")
            text(facet["rationale"], "facet.rationale")
            require(facet["disposition"] in ("adopt", "adapt", "not-applicable"), "facet: invalid disposition")
            require(facet["target_field"] in ("text", "exceptions"), "facet: invalid target_field")
    require(seen == allocated, "source_refs: missing allocated source blocks")


def validate_rule(rule, targets, blocks, domains):
    fields(rule, "schema_version id kind language status origin title text applies_to exceptions examples "
           "translation_of source_refs supporting_target_ids review rights", "rule")
    for key, expected in {"schema_version": "1.1.0", "kind": "rule", "language": "en",
                          "status": "draft", "origin": "adaptation", "translation_of": None}.items():
        require(rule[key] == expected, f"rule: unexpected {key}")
    identifier = rule["id"]
    require(isinstance(identifier, str) and adaptation.TARGET_RULE_ID_RE.fullmatch(identifier)
            and identifier in targets, "rule: ID must be a planned target")
    for key in ("title", "text"):
        text(rule[key], f"rule.{key}")
    applies = strings(rule["applies_to"], "applies_to", unique=True)
    require(set(applies) <= domains, "applies_to: unknown domain IDs")
    strings(rule["exceptions"], "exceptions")
    supporting = strings(rule["supporting_target_ids"], "supporting_target_ids", unique=True, nonempty=False)
    require(set(supporting) <= targets.keys() and identifier not in supporting,
            "supporting_target_ids: require other planned targets")
    fields(rule["review"], "mode automation criteria", "review")
    require(rule["review"]["mode"] == "human" and rule["review"]["automation"] == "structure-only",
            "review: human, structure-only review is required")
    strings(rule["review"]["criteria"], "review.criteria")
    validate_rights(rule["rights"])
    validate_examples(rule["examples"])
    validate_refs(rule["source_refs"], set(targets[identifier]["source_block_ids"]), blocks)
    return identifier


def check(manifest=DEFAULT_MANIFEST):
    """Validate draft rules and IT-only terms; return the materialized rule count."""
    try:
        return _check(manifest)
    except CorpusError:
        raise
    except (adaptation.PlanError, OSError, ValueError, TypeError, KeyError,
            AttributeError, RecursionError, sqlite3.Error) as error:
        raise CorpusError(f"Cannot validate pilot: {error}") from error


def _check(manifest):
    path = Path(manifest)
    requested = path if path.is_absolute() else ROOT / path
    path = confined(requested, ROOT)
    require(path.name == "manifest.json", "Expected manifest.json")
    data = load_json(path)
    fields(data, "schema_version profile standard version revision status primary_language languages "
           "language_coverage records sources relations supersedes released_at plan", "manifest")
    expected = {
        "schema_version": "1.1.0", "profile": "it-ste-pilot-v1", "standard": "it-ste",
        "version": "0.1.0-draft.1", "revision": "r0001", "status": "draft",
        "primary_language": "en", "languages": ["en"], "language_coverage": {"en": "partial"},
        "relations": None, "supersedes": None, "released_at": None,
    }
    for key, value in expected.items():
        require(data[key] == value, f"manifest: unexpected {key}")
    namespace = Path("standards/it-ste/versions") / data["version"] / "revisions" / data["revision"] / "manifest.json"
    require(requested == ROOT / namespace and path == ROOT.resolve() / namespace,
            "Manifest identity does not match its canonical repository namespace")
    pins = authenticate_plan()
    require(data["plan"] == pins, "manifest: plan paths or authenticated pins differ")
    snapshot = path.parent
    members = []
    declared = set()
    groups = []
    for group in ("records", "sources"):
        names = strings(data[group], group, unique=True)
        if group == "sources":
            require(f"sources/{SOURCE_ID}.json" in names, "Require the canonical source path")
            require(all(
                name == f"sources/{SOURCE_ID}.json"
                or re.fullmatch(r"sources/ITIL-SOURCE-[A-Z0-9-]+\.json", name)
                for name in names
            ), "Sources require canonical ASD or ITIL reference paths")
        else:
            require(all(
                re.fullmatch(r"content/en/rules/ITSTE-R-[0-9]{4}\.json", name)
                or re.fullmatch(r"content/en/terms/ITSTE-T-[0-9]{4}\.json", name)
                for name in names
            ), "Records require canonical rule or term paths")
        declared.update(snapshot / name for name in names)
        resolved = [relative_path(name, snapshot) for name in names]
        require(all(member == snapshot / name for name, member in zip(names, resolved)),
                "Members must resolve to their canonical snapshot paths")
        members.extend(resolved)
        groups.append(resolved)
    require(len(set(members + [path])) == len(members) + 1, "Duplicate/resolved member aliases")
    for directory in (snapshot / "content", snapshot / "sources"):
        if directory.exists() or directory.is_symlink():
            confined(directory, snapshot)
            require(not directory.is_symlink(), "Symlink directory aliases are forbidden")
            pending = [directory]
            while pending:
                current = pending.pop()
                for child in current.iterdir():
                    confined(child, snapshot)
                    if child.is_dir():
                        require(not child.is_symlink(), "Symlink directory aliases are forbidden")
                        pending.append(child)
                    else:
                        require(child in declared, f"Unlisted snapshot file: {child}")
    source_records = {}
    external_sources = {}
    for name, member in zip(data["sources"], groups[1]):
        source = load_json(member)
        source_id = source.get("id")
        require(isinstance(source_id, str) and source_id not in source_records,
                "Sources require unique IDs")
        require(name == f"sources/{source_id}.json", "Source filename must match its ID")
        if source_id == SOURCE_ID:
            validate_source(source)
        else:
            validate_external_source(source)
            external_sources[source_id] = source
        source_records[source_id] = source
    require(SOURCE_ID in source_records, "Canonical ASD source metadata is missing")
    targets = {item["id"]: item for item in load_json(adaptation.PLAN_TARGETS)["targets"]}
    blocks = {item["id"]: item for item in adaptation.source_blocks()}
    domains = adaptation.domain_ids()
    rule_identifiers = []
    term_identifiers = []
    for name, member in zip(data["records"], groups[0]):
        record = load_json(member)
        if "/rules/" in name:
            identifier = validate_rule(record, targets, blocks, domains)
            require(name == f"content/en/rules/{identifier}.json", "Rule filename must match its ID")
            rule_identifiers.append(identifier)
        else:
            identifier = validate_term(record, domains, external_sources)
            require(name == f"content/en/terms/{identifier}.json", "Term filename must match its ID")
            term_identifiers.append(identifier)
    require(len(rule_identifiers) == len(set(rule_identifiers)), "Duplicate rule IDs")
    require(len(term_identifiers) == len(set(term_identifiers)), "Duplicate term IDs")
    return len(rule_identifiers)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    command = commands.add_parser("check", help="check draft pilot structure and provenance only")
    command.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args(argv)
    try:
        count = check(args.manifest)
    except CorpusError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print(f"PASS: {count} draft pilot rules and canonical draft terms; structure and provenance only. "
          "No prose conformance, editorial correctness, or tool-command verification.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
