#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Create and validate a source-pinned IT-STE adaptation plan."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import sys
from collections.abc import Sequence
from contextlib import closing
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "standards/asd-ste100/versions/issue-9/revisions/r0001/reference"
SOURCE_DATABASE = SOURCE_ROOT / "reference.sqlite3"
SOURCE_MANIFEST = SOURCE_ROOT / "manifest.json"
DOMAINS = ROOT / "standards/it-ste/domains/v1.0.0.json"
PLAN_ROOT = ROOT / "standards/it-ste/adaptation-plans/asd-ste100/issue-9/r0001"
PLAN_MAP = PLAN_ROOT / "map.jsonl"
PLAN_TARGETS = PLAN_ROOT / "targets.json"
PLAN_MANIFEST = PLAN_ROOT / "manifest.json"
PROJECT_URL = "https://github.com/vladimirmashkov/IT-STE"
EXPECTED_DATABASE_SHA256 = "4a1d2bc943d35f689599af564e5587e870d384552c25aaaeff9892effc87642b"
EXPECTED_SOURCE_SHA256 = "d1f4ea9e7cd6e46b47aa9057209f99e78c0e9cfc4e27a5b07895b05c1a166431"
PERMISSION_RECORD_REFERENCE = "docs/permissions/asd-ste100-issue-9-derivatives.md"
PERMISSION_RECORD = ROOT / PERMISSION_RECORD_REFERENCE
EXPECTED_PERMISSION_SHA256 = "fa8bd26e2fae80e45607200c1635432feb7bfab9fb0f71173057a8db7f0576e3"
TARGET_RULE_ID_RE = re.compile(r"ITSTE-R-[0-9]{4}")
EXPECTED_RULE_IDS = {
    *(f"1.{number}" for number in range(1, 15)),
    *(f"2.{number}" for number in range(1, 3)),
    *(f"3.{number}" for number in range(1, 8)),
    *(f"4.{number}" for number in range(1, 6)),
    *(f"5.{number}" for number in range(1, 6)),
    *(f"6.{number}" for number in range(1, 7)),
    *(f"7.{number}" for number in range(1, 4)),
    *(f"8.{number}" for number in range(1, 8)),
    *(f"9.{number}" for number in range(1, 5)),
}
EXPECTED_GUIDANCE_IDS = {f"GR-{number}" for number in range(1, 9)}
ASSESSMENT_STATES = {"unreviewed", "in-review", "reviewed"}
APPLICABILITY_STATES = {
    "pending",
    "adopt",
    "adapt",
    "not-applicable",
}
ADAPTATION_ACTIONS = {
    "pending",
    "create-rule",
    "create-rules",
    "merge-into-rule",
    "record-rationale-only",
}


class PlanError(RuntimeError):
    """A user-facing adaptation-plan error."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise PlanError(f"Cannot read JSON {path}: {error}") from error
    if not isinstance(value, dict):
        raise PlanError(f"Expected a JSON object: {path}")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise PlanError(f"Cannot read JSONL {path}: {error}") from error
    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            raise PlanError(f"Blank JSONL line at {path}:{line_number}")
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            raise PlanError(f"Invalid JSON at {path}:{line_number}: {error}") from error
        if not isinstance(value, dict):
            raise PlanError(f"Expected an object at {path}:{line_number}")
        records.append(value)
    return records


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_jsonl(path: Path, records: Sequence[dict[str, object]]) -> None:
    path.write_text(
        "".join(
            json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
            for record in records
        ),
        encoding="utf-8",
    )


def authenticate_source() -> dict[str, Any]:
    manifest = load_json(SOURCE_MANIFEST)
    required_manifest = {
        "standard": "ASD-STE100",
        "issue": "9",
        "database_sha256": EXPECTED_DATABASE_SHA256,
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "physical_pages": "434",
        "rules": "53",
        "guidance": "8",
        "dictionary_entries": "2196",
        "publication": "authorized-derivative",
        "source_pdf_included": False,
        "source_pdf_redistribution": "forbidden",
        "permission_record": PERMISSION_RECORD_REFERENCE,
        "permission_record_sha256": EXPECTED_PERMISSION_SHA256,
    }
    for key, expected in required_manifest.items():
        if manifest.get(key) != expected:
            raise PlanError(f"Published ASD manifest has unexpected {key}: {manifest.get(key)!r}")
    actual = sha256_file(SOURCE_DATABASE)
    if actual != EXPECTED_DATABASE_SHA256:
        raise PlanError("Published ASD reference database does not match the trusted r0001 hash")
    if sha256_file(PERMISSION_RECORD) != EXPECTED_PERMISSION_SHA256:
        raise PlanError("ASD derivative permission record does not match its trusted hash")
    with closing(sqlite3.connect(f"file:{SOURCE_DATABASE.resolve()}?mode=ro", uri=True)) as connection:
        integrity = connection.execute("PRAGMA integrity_check").fetchone()
        if not integrity or integrity[0] != "ok":
            raise PlanError(f"Published ASD reference failed integrity check: {integrity}")
        metadata = dict(connection.execute("SELECT key, value FROM metadata"))
        required_metadata = {
            "standard": "ASD-STE100",
            "issue": "9",
            "source_sha256": EXPECTED_SOURCE_SHA256,
            "physical_pages": "434",
            "rules": "53",
            "guidance": "8",
            "dictionary_entries": "2196",
            "review_state": "mechanically-extracted-unreviewed",
        }
        for key, expected in required_metadata.items():
            if metadata.get(key) != expected:
                raise PlanError(f"Published ASD database has unexpected {key}: {metadata.get(key)!r}")
        rows = connection.execute("SELECT id, kind FROM blocks").fetchall()
        rule_ids = {block_id for block_id, kind in rows if kind == "rule"}
        guidance_ids = {block_id for block_id, kind in rows if kind == "guidance"}
        if rule_ids != EXPECTED_RULE_IDS or guidance_ids != EXPECTED_GUIDANCE_IDS:
            raise PlanError("Published ASD block IDs do not match the trusted Issue 9 sets")
    return manifest


def source_blocks() -> list[dict[str, object]]:
    with closing(sqlite3.connect(f"file:{SOURCE_DATABASE.resolve()}?mode=ro", uri=True)) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            "SELECT id, kind, title, start_pdf_page, end_pdf_page FROM blocks"
        ).fetchall()
    return sorted(
        (dict(row) for row in rows),
        key=lambda row: (
            1 if str(row["id"]).startswith("GR-") else 0,
            tuple(
                int(part)
                for part in str(row["id"]).removeprefix("GR-").split(".")
            ),
        ),
    )


def candidate_domains(block_id: str) -> list[str]:
    if block_id.startswith("5."):
        return ["general", "procedures-runbooks", "cli", "user-interface"]
    if block_id.startswith("6."):
        return ["general", "software-documentation"]
    if block_id.startswith("7."):
        return ["general", "security", "monitoring-alerts", "procedures-runbooks"]
    if block_id == "GR-7":
        return ["general", "software-documentation", "user-interface"]
    return ["general"]


def initial_records() -> list[dict[str, object]]:
    records = []
    for block in source_blocks():
        records.append(
            {
                "schema_version": "1.0.0",
                "source": {
                    "standard": "asd-ste100",
                    "version": "issue-9",
                    "revision": "r0001",
                    "block_id": block["id"],
                    "kind": block["kind"],
                    "title": block["title"],
                    "physical_pdf_pages": [
                        block["start_pdf_page"],
                        block["end_pdf_page"],
                    ],
                },
                "assessment": {
                    "status": "unreviewed",
                    "applicability": "pending",
                    "adaptation_action": "pending",
                    "candidate_domains": candidate_domains(str(block["id"])),
                    "rationale": None,
                },
                "target_rule_ids": [],
            }
        )
    return records


def domain_ids() -> set[str]:
    registry = load_json(DOMAINS)
    if registry.get("registry_version") != "1.0.0":
        raise PlanError(f"Unsupported domain registry version: {registry.get('registry_version')!r}")
    domains = registry.get("domains")
    if not isinstance(domains, list) or not domains:
        raise PlanError("Domain registry must contain a non-empty domains array")
    identifiers = []
    for item in domains:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise PlanError("Every domain must be an object with a string id")
        identifiers.append(item["id"])
    if len(identifiers) != len(set(identifiers)):
        raise PlanError("Domain IDs must be unique")
    if "general" not in identifiers:
        raise PlanError("Domain registry must define general")
    for item in domains:
        parent = item.get("parent")
        if parent is not None and parent not in identifiers:
            raise PlanError(f"Unknown parent domain {parent!r} for {item['id']}")
    attribution = registry.get("rights", {}).get("attribution", {})
    if attribution.get("url") != PROJECT_URL:
        raise PlanError("Domain registry must retain the required IT-STE project link")
    return set(identifiers)


def validate_reviewed_decision(
    block_id: str, assessment: dict[str, Any], targets: list[str]
) -> None:
    applicability = assessment["applicability"]
    action = assessment["adaptation_action"]
    allowed_pairs = {
        "adopt": {"create-rule", "create-rules", "merge-into-rule"},
        "adapt": {"create-rule", "create-rules", "merge-into-rule"},
        "not-applicable": {"record-rationale-only"},
    }
    if applicability == "pending" or action == "pending":
        raise PlanError(f"A reviewed decision cannot remain pending: {block_id}")
    if action not in allowed_pairs[applicability]:
        raise PlanError(
            f"Incoherent reviewed applicability/action for {block_id}: "
            f"{applicability}/{action}"
        )
    if action in {"create-rule", "merge-into-rule"} and len(targets) != 1:
        raise PlanError(f"Reviewed {action} requires exactly one target ID: {block_id}")
    if action == "create-rules" and len(targets) < 2:
        raise PlanError(f"Reviewed create-rules requires at least two target IDs: {block_id}")
    if action == "record-rationale-only" and targets:
        raise PlanError(f"A rationale-only decision cannot have target IDs: {block_id}")


def validate_records(records: Sequence[dict[str, Any]]) -> dict[str, int]:
    domains = domain_ids()
    blocks = {str(block["id"]): block for block in source_blocks()}
    found_ids = []
    status_counts = {state: 0 for state in sorted(ASSESSMENT_STATES)}
    applicability_counts = {state: 0 for state in sorted(APPLICABILITY_STATES)}
    target_uses: dict[str, list[str]] = {}

    for record in records:
        if record.get("schema_version") != "1.0.0":
            raise PlanError(f"Unsupported map schema version: {record.get('schema_version')!r}")
        source = record.get("source")
        assessment = record.get("assessment")
        if not isinstance(source, dict) or not isinstance(assessment, dict):
            raise PlanError("Each map record requires source and assessment objects")
        block_id = source.get("block_id")
        if not isinstance(block_id, str) or block_id not in blocks:
            raise PlanError(f"Unknown source block ID: {block_id!r}")
        found_ids.append(block_id)
        block = blocks[block_id]
        expected_source = {
            "standard": "asd-ste100",
            "version": "issue-9",
            "revision": "r0001",
            "block_id": block_id,
            "kind": block["kind"],
            "title": block["title"],
            "physical_pdf_pages": [block["start_pdf_page"], block["end_pdf_page"]],
        }
        if source != expected_source:
            raise PlanError(f"Source coordinates differ from the authenticated index: {block_id}")

        status = assessment.get("status")
        applicability = assessment.get("applicability")
        action = assessment.get("adaptation_action")
        if status not in ASSESSMENT_STATES:
            raise PlanError(f"Invalid assessment status for {block_id}: {status!r}")
        if applicability not in APPLICABILITY_STATES:
            raise PlanError(f"Invalid applicability for {block_id}: {applicability!r}")
        if action not in ADAPTATION_ACTIONS:
            raise PlanError(f"Invalid adaptation action for {block_id}: {action!r}")
        candidates = assessment.get("candidate_domains")
        if not isinstance(candidates, list) or not candidates:
            raise PlanError(f"Candidate domains are required for {block_id}")
        unknown = set(candidates) - domains
        if unknown:
            raise PlanError(f"Unknown candidate domains for {block_id}: {sorted(unknown)}")
        rationale = assessment.get("rationale")
        if status == "reviewed" and (not isinstance(rationale, str) or not rationale.strip()):
            raise PlanError(f"A reviewed assessment requires a rationale: {block_id}")

        targets = record.get("target_rule_ids")
        if not isinstance(targets, list) or any(
            not isinstance(target, str) or TARGET_RULE_ID_RE.fullmatch(target) is None
            for target in targets
        ):
            raise PlanError(f"Invalid target_rule_ids for {block_id}")
        if len(targets) != len(set(targets)):
            raise PlanError(f"Duplicate target_rule_ids within source block {block_id}")
        if status == "unreviewed" and (
            applicability != "pending"
            or action != "pending"
            or rationale is not None
            or targets
        ):
            raise PlanError(f"An unreviewed assessment must remain empty and pending: {block_id}")
        if status != "reviewed" and targets:
            raise PlanError(f"Only reviewed assessments can allocate target IDs: {block_id}")
        if applicability in {"pending", "not-applicable"} and targets:
            raise PlanError(f"{applicability} assessment cannot have target IDs: {block_id}")
        if action == "pending" and targets:
            raise PlanError(f"Pending adaptation action cannot have target IDs: {block_id}")
        if status == "reviewed":
            validate_reviewed_decision(block_id, assessment, targets)
        for target in targets:
            target_uses.setdefault(target, []).append(str(action))
        status_counts[status] += 1
        applicability_counts[applicability] += 1

    if len(found_ids) != len(set(found_ids)):
        raise PlanError("Source block IDs must be unique in the adaptation map")
    expected_ids = EXPECTED_RULE_IDS | EXPECTED_GUIDANCE_IDS
    if set(found_ids) != expected_ids:
        missing = sorted(expected_ids - set(found_ids))
        extra = sorted(set(found_ids) - expected_ids)
        raise PlanError(f"Adaptation-map coverage mismatch; missing={missing}; extra={extra}")
    for target, uses in target_uses.items():
        if len(uses) > 1 and set(uses) != {"merge-into-rule"}:
            raise PlanError(
                f"Target {target} is shared without merge actions on all source blocks"
            )

    return {
        "source_blocks": len(found_ids),
        "source_rules": len(EXPECTED_RULE_IDS),
        "source_guidance": len(EXPECTED_GUIDANCE_IDS),
        **{f"assessment_{key}": value for key, value in status_counts.items()},
        **{f"applicability_{key}": value for key, value in applicability_counts.items()},
    }


def empty_targets() -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "status": "draft",
        "description": (
            "Planned IT-STE rule concepts produced by reviewed adaptation decisions. "
            "These entries are not normative rules."
        ),
        "targets": [],
        "rights": {
            "license": "CC-BY-SA-4.0",
            "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
            "attribution": {
                "name": "IT-STE contributors",
                "url": PROJECT_URL,
            },
        },
    }


def validate_targets(records: Sequence[dict[str, Any]]) -> int:
    registry = load_json(PLAN_TARGETS)
    if registry.get("schema_version") != "1.0.0" or registry.get("status") != "draft":
        raise PlanError("Target registry must use schema 1.0.0 and draft status")
    targets = registry.get("targets")
    if not isinstance(targets, list):
        raise PlanError("Target registry must contain a targets array")
    attribution = registry.get("rights", {}).get("attribution", {})
    if attribution.get("url") != PROJECT_URL:
        raise PlanError("Target registry must retain the required IT-STE project link")

    domains = domain_ids()
    domain_registry = load_json(DOMAINS)
    parents = {item["id"]: item["parent"] for item in domain_registry["domains"]}

    def ancestors(domain: str) -> set[str]:
        result = set()
        parent = parents[domain]
        while parent is not None:
            result.add(parent)
            parent = parents[parent]
        return result

    map_uses: dict[str, set[str]] = {}
    map_domains: dict[str, set[str]] = {}
    for record in records:
        block_id = record["source"]["block_id"]
        for target_id in record["target_rule_ids"]:
            map_uses.setdefault(target_id, set()).add(block_id)
            map_domains.setdefault(target_id, set()).update(
                record["assessment"]["candidate_domains"]
            )

    target_uses: dict[str, set[str]] = {}
    for target in targets:
        if not isinstance(target, dict):
            raise PlanError("Every planned target must be an object")
        target_id = target.get("id")
        if not isinstance(target_id, str) or TARGET_RULE_ID_RE.fullmatch(target_id) is None:
            raise PlanError(f"Invalid planned target ID: {target_id!r}")
        if target_id in target_uses:
            raise PlanError(f"Duplicate planned target ID: {target_id}")
        if target.get("status") != "planned" or "normative_record" in target:
            raise PlanError(f"Target {target_id} must remain planned and non-normative")
        for field in ("working_title", "design_intent"):
            value = target.get(field)
            if not isinstance(value, str) or not value.strip():
                raise PlanError(f"Target {target_id} requires a non-empty {field}")
        source_ids = target.get("source_block_ids")
        if not isinstance(source_ids, list) or not source_ids or any(
            not isinstance(source_id, str) for source_id in source_ids
        ):
            raise PlanError(f"Target {target_id} requires source_block_ids")
        if len(source_ids) != len(set(source_ids)):
            raise PlanError(f"Target {target_id} repeats a source block ID")
        candidates = target.get("candidate_domains")
        if not isinstance(candidates, list) or not candidates:
            raise PlanError(f"Target {target_id} requires candidate_domains")
        unknown = set(candidates) - domains
        if unknown:
            raise PlanError(f"Unknown target domains for {target_id}: {sorted(unknown)}")
        source_domains = map_domains.get(target_id, set())
        for candidate in candidates:
            if not any(
                candidate == source_domain or candidate in ancestors(source_domain)
                for source_domain in source_domains
            ):
                raise PlanError(
                    f"Target domain {candidate!r} is unsupported by source decisions for {target_id}"
                )
        for source_domain in source_domains:
            if not any(
                candidate == source_domain or candidate in ancestors(source_domain)
                for candidate in candidates
            ):
                raise PlanError(
                    f"Source domain {source_domain!r} is not covered by target {target_id}"
                )
        target_uses[target_id] = set(source_ids)

    if target_uses != map_uses:
        raise PlanError(
            "Target registry does not match map target/source relationships: "
            f"registry={target_uses}; map={map_uses}"
        )
    return len(targets)


def manifest(counts: dict[str, int]) -> dict[str, object]:
    source_manifest = authenticate_source()
    return {
        "schema_version": "1.0.0",
        "kind": "adaptation-plan",
        "status": "draft",
        "target": {
            "standard": "it-ste",
            "planned_version": "0.1.0-draft.1",
            "primary_language": "en",
        },
        "source": {
            "standard": "asd-ste100",
            "version": "issue-9",
            "revision": "r0001",
            "database": "standards/asd-ste100/versions/issue-9/revisions/r0001/reference/reference.sqlite3",
            "database_sha256": source_manifest["database_sha256"],
            "source_pdf_sha256": source_manifest["source_sha256"],
            "owner": {
                "name": "Aerospace, Security and Defence Industries Association of Europe (ASD)",
                "url": "https://asd-ste100.org/",
            },
            "permission_record": source_manifest["permission_record"],
            "permission_record_sha256": source_manifest["permission_record_sha256"],
        },
        "domain_registry": "standards/it-ste/domains/v1.0.0.json",
        "domain_registry_sha256": sha256_file(DOMAINS),
        "map": "standards/it-ste/adaptation-plans/asd-ste100/issue-9/r0001/map.jsonl",
        "map_sha256": sha256_file(PLAN_MAP),
        "targets": "standards/it-ste/adaptation-plans/asd-ste100/issue-9/r0001/targets.json",
        "targets_sha256": sha256_file(PLAN_TARGETS),
        "method": {
            "classification_basis": "authenticated compact source headings and physical page ranges",
            "initial_review_state": "unreviewed",
            "candidate_domains_are_normative": False,
            "full_source_text_loaded": False,
        },
        "counts": counts,
        "attribution": {
            "name": "IT-STE contributors",
            "url": PROJECT_URL,
        },
        "notice": "This planning artifact is not an IT-STE release and is not official ASD guidance.",
    }


def seal(accept_domain_change: bool = False) -> None:
    authenticate_source()
    records = load_jsonl(PLAN_MAP)
    counts = validate_records(records)
    counts["planned_targets"] = validate_targets(records)
    if PLAN_MANIFEST.exists():
        previous = load_json(PLAN_MANIFEST)
        previous_source = previous.get("source")
        if not isinstance(previous_source, dict):
            raise PlanError("Existing adaptation manifest has no source pin")
        if previous_source.get("database_sha256") != EXPECTED_DATABASE_SHA256:
            raise PlanError("Existing adaptation manifest is pinned to another source database")
        previous_domain_hash = previous.get("domain_registry_sha256")
        current_domain_hash = sha256_file(DOMAINS)
        if previous_domain_hash != current_domain_hash and not accept_domain_change:
            raise PlanError(
                "Domain registry changed; review classifications and rerun seal "
                "with --accept-domain-change"
            )
    write_json(PLAN_MANIFEST, manifest(counts))


def initialize() -> None:
    authenticate_source()
    domain_ids()
    PLAN_ROOT.mkdir(parents=True, exist_ok=True)
    if PLAN_MAP.exists() or PLAN_TARGETS.exists() or PLAN_MANIFEST.exists():
        raise PlanError("Adaptation plan already exists; init never overwrites manual work")
    write_jsonl(PLAN_MAP, initial_records())
    write_json(PLAN_TARGETS, empty_targets())
    seal()
    print(f"Created adaptation map: {PLAN_MAP}")
    print(f"Created adaptation manifest: {PLAN_MANIFEST}")


def check() -> None:
    source_manifest = authenticate_source()
    records = load_jsonl(PLAN_MAP)
    counts = validate_records(records)
    counts["planned_targets"] = validate_targets(records)
    plan_manifest = load_json(PLAN_MANIFEST)
    expected_manifest = manifest(counts)
    if plan_manifest != expected_manifest:
        raise PlanError("Adaptation manifest is stale; run seal after reviewed map changes")
    print("PASS")
    print(
        f"- authenticated source database: {source_manifest['database_sha256']}"
    )
    print(
        f"- coverage: {counts['source_rules']} rules; "
        f"{counts['source_guidance']} recommendations"
    )
    print(
        f"- assessments: {counts['assessment_unreviewed']} unreviewed; "
        f"{counts['assessment_in-review']} in review; {counts['assessment_reviewed']} reviewed"
    )
    print(f"- planned IT-STE targets: {counts['planned_targets']}")
    print(f"- required project link: {PROJECT_URL}")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        description="Create and validate the ASD-to-IT-STE adaptation plan."
    )
    commands = root.add_subparsers(dest="command", required=True)
    commands.add_parser("init", help="create the initial heading-based map once")
    seal_parser = commands.add_parser(
        "seal", help="refresh the manifest after reviewed map edits"
    )
    seal_parser.add_argument(
        "--accept-domain-change",
        action="store_true",
        help="repin the plan after explicitly reviewing a domain-registry change",
    )
    commands.add_parser("check", help="validate source pinning, coverage, domains, and hashes")
    return root


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "init":
            initialize()
        elif args.command == "seal":
            seal(args.accept_domain_change)
            print(f"Updated adaptation manifest: {PLAN_MANIFEST}")
        else:
            check()
        return 0
    except (PlanError, OSError, sqlite3.Error) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
