# SPDX-License-Identifier: GPL-3.0-only
"""Synthetic closed-profile tests plus the repository pilot integration check."""

import contextlib
import copy
import hashlib
import io
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import it_ste_adaptation as adaptation
from tools import it_ste_corpus as corpus


def digest(value):
    return hashlib.sha256(value).hexdigest()


class PilotIntegrationTests(unittest.TestCase):
    def test_default_pilot(self):
        self.assertTrue((corpus.ROOT / corpus.DEFAULT_MANIFEST).is_file(),
                        "Default pilot manifest is required for integration")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(corpus.check(), 31)
        snapshot = corpus.ROOT / corpus.DEFAULT_MANIFEST.parent
        manifest = corpus.load_json(snapshot / "manifest.json")
        rule_names = [name for name in manifest["records"] if "/rules/" in name]
        term_names = [name for name in manifest["records"] if "/terms/" in name]
        rule_identifiers = {corpus.load_json(snapshot / name)["id"] for name in rule_names}
        term_records = [corpus.load_json(snapshot / name) for name in term_names]
        self.assertEqual(rule_identifiers, {f"ITSTE-R-{number:04d}" for number in range(1, 32)})
        self.assertEqual({record["id"] for record in term_records},
                         {f"ITSTE-T-{number:04d}" for number in range(1, 7)})
        self.assertTrue(all(record["status"] == "draft" and record["origin"] == "original"
                            for record in term_records))
        self.assertTrue(all(
            all(ref["source_id"].startswith("ITIL-SOURCE-") for ref in record["source_refs"])
            for record in term_records
        ))
        catalog = corpus.load_json(corpus.ROOT / "catalog.json")
        for standard in catalog["standards"]:
            if standard["id"] == manifest["standard"]:
                for release in standard["releases"]:
                    self.assertNotEqual((release["version"], release["revision"]),
                                        (manifest["version"], manifest["revision"]))
                    self.assertNotEqual(release["manifest"], corpus.DEFAULT_MANIFEST.as_posix())

    def test_complete_rule_draft_covers_every_planned_source_block(self):
        snapshot = corpus.ROOT / corpus.DEFAULT_MANIFEST.parent
        manifest = corpus.load_json(snapshot / "manifest.json")
        records = {rule["id"]: rule for rule in (
            corpus.load_json(snapshot / name) for name in manifest["records"] if "/rules/" in name
        )}
        locators = [ref["locator"] for rule in records.values() for ref in rule["source_refs"]]
        self.assertEqual(len(locators), 61)
        self.assertEqual(len({locator["block_id"] for locator in locators}), 61)
        self.assertEqual(sum(locator["kind"] == "rule" for locator in locators), 53)
        self.assertEqual(sum(locator["kind"] == "guidance" for locator in locators), 8)
        self.assertTrue(all(record["status"] == "draft" for record in records.values()))
        joined = lambda example: "".join(segment["text"] for segment in example["segments"])
        self.assertIn("Before the deployment starts, validate", joined(records["ITSTE-R-0009"]["examples"]["allowed"][0]))
        self.assertIn("In that failure case, contact", joined(records["ITSTE-R-0023"]["examples"]["allowed"][0]))
        self.assertIn("If validation has not succeeded, do not start", joined(records["ITSTE-R-0026"]["examples"]["allowed"][0]))
        self.assertIn("While the proxy is enabled, check", records["ITSTE-R-0029"]["examples"]["not_allowed"][0]["rationale"])

    def test_published_authentication_does_not_need_source_pdf(self):
        original_open = Path.open

        def no_private_source(path, *args, **kwargs):
            self.assertNotIn(".local", path.parts)
            self.assertNotEqual(path.suffix.lower(), ".pdf")
            return original_open(path, *args, **kwargs)

        with mock.patch.object(Path, "open", no_private_source):
            self.assertIn("manifest_sha256", corpus.authenticate_plan())


class CorpusTests(unittest.TestCase):
    def setUp(self):
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.root = Path(self.stack.enter_context(tempfile.TemporaryDirectory()))
        self.stack.enter_context(mock.patch.object(corpus, "ROOT", self.root))
        self.stack.enter_context(mock.patch.object(adaptation, "ROOT", self.root))
        artifacts = {
            "PLAN_MANIFEST": "plan/manifest.json", "PLAN_TARGETS": "plan/targets.json",
            "PLAN_MAP": "plan/map.jsonl", "DOMAINS": "domains.json",
            "SOURCE_MANIFEST": "reference/manifest.json", "SOURCE_DATABASE": "reference/reference.sqlite3",
            "PERMISSION_RECORD": adaptation.PERMISSION_RECORD_REFERENCE,
        }
        for name, relative in artifacts.items():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"{}\n")
            self.stack.enter_context(mock.patch.object(adaptation, name, path))
        self.stack.enter_context(mock.patch.object(adaptation, "EXPECTED_DATABASE_SHA256", digest(b"{}\n")))
        self.stack.enter_context(mock.patch.object(adaptation, "EXPECTED_PERMISSION_SHA256", digest(b"{}\n")))
        self.auth = self.stack.enter_context(mock.patch.object(adaptation, "check"))
        self.blocks = [
            {"id": "1.1", "kind": "rule", "start_pdf_page": 10, "end_pdf_page": 11},
            {"id": "GR-1", "kind": "guidance", "start_pdf_page": 12, "end_pdf_page": 12},
        ]
        self.stack.enter_context(mock.patch.object(adaptation, "source_blocks", return_value=self.blocks))
        self.stack.enter_context(mock.patch.object(adaptation, "domain_ids", return_value={"general", "cli"}))
        self.write(adaptation.PLAN_TARGETS, {"targets": [
            {"id": "ITSTE-R-0001", "source_block_ids": ["1.1", "GR-1"]},
            {"id": "ITSTE-R-0002", "source_block_ids": ["1.1"]},
        ]})
        (self.root / "LICENSE-CONTENT.md").write_text("Content license\n", encoding="utf-8")
        self.path = self.root / corpus.DEFAULT_MANIFEST
        self.path.parent.mkdir(parents=True)
        self.source = {
            "schema_version": "1.1.0", "id": corpus.SOURCE_ID, "standard": "asd-ste100",
            "version": "issue-9", "revision": "r0001", "title": "ASD-STE100 Issue 9",
            "url": "https://asd-ste100.org/", "retrieved_at": None,
            "artifact_path": "reference/reference.sqlite3",
            "artifact_sha256": adaptation.EXPECTED_DATABASE_SHA256,
            "source_pdf_sha256": adaptation.EXPECTED_SOURCE_SHA256,
            "owner": copy.deepcopy(corpus.OWNER),
            "permission": {
                "path": adaptation.PERMISSION_RECORD_REFERENCE,
                "sha256": adaptation.EXPECTED_PERMISSION_SHA256,
                "scope": "authorized-derivatives-only", "source_pdf_redistribution": "forbidden",
                "downstream_license": "unknown",
            },
            "rights": {
                "license": None, "license_url": None, "redistribution": "unknown",
                "adaptation": "unknown", "attribution": [copy.deepcopy(corpus.OWNER)],
                "evidence": [adaptation.PERMISSION_RECORD_REFERENCE],
            },
        }
        literal = "service restart"
        example = {"segments": [
            {"kind": "prose", "text": "Run this command:"},
            {"kind": "literal", "literal_type": "command", "text": literal,
             "sha256": digest(literal.encode())},
        ], "rationale": "The literal command is preserved."}
        self.rule = {
            "schema_version": "1.1.0", "id": "ITSTE-R-0001", "kind": "rule",
            "language": "en", "status": "draft", "origin": "adaptation",
            "title": "Preserve command syntax", "text": "Keep command syntax unchanged.",
            "applies_to": ["general"], "exceptions": ["Quoted source text can retain its wording."],
            "examples": {"allowed": [copy.deepcopy(example)], "not_allowed": [copy.deepcopy(example)]},
            "translation_of": None, "supporting_target_ids": ["ITSTE-R-0002"],
            "source_refs": [{
                "source_id": corpus.SOURCE_ID,
                "locator": {"block_id": block["id"], "kind": block["kind"],
                            "physical_pdf_pages": [block["start_pdf_page"], block["end_pdf_page"]]},
                "facets": [{"source_facet": "Keep technical text precise.", "disposition": "adapt",
                            "rationale": "Command syntax is literal.", "target_field": "text"}],
            } for block in self.blocks],
            "review": {"mode": "human", "automation": "structure-only",
                       "criteria": ["Review applicability to the stated domain."]},
            "rights": {
                "license": "CC-BY-SA-4.0", "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
                "redistribution": "allowed", "adaptation": "allowed",
                "attribution": [copy.deepcopy(corpus.PROJECT), copy.deepcopy(corpus.OWNER)],
                "evidence": ["LICENSE-CONTENT.md", adaptation.PERMISSION_RECORD_REFERENCE],
                "scope": corpus.SCOPE,
            },
        }
        self.manifest = {
            "schema_version": "1.1.0", "profile": "it-ste-pilot-v1", "standard": "it-ste",
            "version": "0.1.0-draft.1", "revision": "r0001", "status": "draft",
            "primary_language": "en", "languages": ["en"], "language_coverage": {"en": "partial"},
            "records": ["content/en/rules/ITSTE-R-0001.json"],
            "sources": [f"sources/{corpus.SOURCE_ID}.json"],
            "relations": None, "supersedes": None, "released_at": None,
            "plan": corpus.authenticate_plan(),
        }
        self.save()

    def write(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False) + "\n", encoding="utf-8")

    def save(self):
        self.write(self.path, self.manifest)
        self.write(self.path.parent / "content/en/rules/ITSTE-R-0001.json", self.rule)
        self.write(self.path.parent / f"sources/{corpus.SOURCE_ID}.json", self.source)

    def add_valid_term(self):
        source_id = "ITIL-SOURCE-TEST-2026"
        source = {
            "schema_version": "1.1.0", "id": source_id, "standard": "itil",
            "version": "ITIL 4", "revision": "web-2026-10-24", "title": "Test reference",
            "url": "https://example.test/itil", "retrieved_at": "2026-10-24",
            "publisher": {"name": "Test publisher", "url": "https://example.test"},
            "status": "reference-only",
            "rights": {
                "license": None, "license_url": None, "redistribution": "unknown",
                "adaptation": "unknown", "attribution": [{"name": "Test publisher", "url": "https://example.test"}],
                "evidence": ["LICENSE-CONTENT.md"],
            },
            "notice": "Reference metadata only; no source text copied.",
        }
        term = {
            "schema_version": "1.1.0", "id": "ITSTE-T-0001", "kind": "term", "language": "en",
            "status": "draft", "origin": "original", "term": "service", "part_of_speech": "noun",
            "definition": "A managed IT capability with a stated outcome.", "domains": ["general"],
            "usage": "restricted", "rationale": "Keep the named service boundary.", "alternatives": [],
            "examples": {
                "allowed": [{"text": "The service provides status information.", "rationale": "Names an outcome."}],
                "not_allowed": [{"text": "The service is good.", "rationale": "The claim is unbounded."}],
            },
            "translation_of": None,
            "source_refs": [{"source_id": source_id, "locator": {"section": "Test section"}}],
            "review": {"mode": "human", "automation": "structure-only",
                       "criteria": ["Review the named service and outcome."]},
            "rights": {
                "license": "CC-BY-SA-4.0", "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
                "redistribution": "allowed", "adaptation": "allowed", "attribution": [copy.deepcopy(corpus.PROJECT)],
                "evidence": ["LICENSE-CONTENT.md"], "scope": corpus.ORIGINAL_SCOPE,
            },
        }
        self.manifest["records"].append("content/en/terms/ITSTE-T-0001.json")
        self.manifest["sources"].append(f"sources/{source_id}.json")
        self.write(self.path.parent / f"sources/{source_id}.json", source)
        self.write(self.path.parent / "content/en/terms/ITSTE-T-0001.json", term)
        self.save()
        return term, self.path.parent / "content/en/terms/ITSTE-T-0001.json"

    def reject(self):
        self.save()
        with self.assertRaises(corpus.CorpusError):
            corpus.check(self.path)

    def test_valid_partial_pilot_and_planning_only_support(self):
        self.assertEqual(corpus.check(self.path), 1)
        self.auth.assert_called()
        self.rule["rights"]["attribution"].reverse()
        self.rule["source_refs"][0]["facets"][0]["disposition"] = "not-applicable"
        self.save()
        self.assertEqual(corpus.check(self.path), 1)

    def test_original_term_requires_external_provenance_and_project_rights(self):
        term, path = self.add_valid_term()
        self.assertEqual(corpus.check(self.path), 1)
        for mutation in (
            lambda value: value["source_refs"][0].update(source_id=corpus.SOURCE_ID),
            lambda value: value["rights"].update(attribution=[copy.deepcopy(corpus.PROJECT), copy.deepcopy(corpus.OWNER)]),
            lambda value: value.update(origin="adaptation"),
        ):
            with self.subTest(mutation=mutation):
                mutated = copy.deepcopy(term)
                mutation(mutated)
                self.write(path, mutated)
                self.reject()

    def test_manifest_closed_identity_language_and_draft_constraints(self):
        original = copy.deepcopy(self.manifest)
        for key, value in {
            "unknown": True, "schema_version": "1.0.0", "profile": "generic",
            "standard": "other", "version": "1.0.0", "revision": "r0002", "status": "released",
            "primary_language": "ru", "languages": ["en", "ru"],
            "language_coverage": {"en": "complete"}, "relations": [],
            "supersedes": "previous", "released_at": "2026-01-01",
        }.items():
            with self.subTest(key=key):
                self.manifest = copy.deepcopy(original)
                self.manifest[key] = value
                self.reject()

    def test_forged_plan_pins_and_path(self):
        original = copy.deepcopy(self.manifest["plan"])
        for key in original:
            with self.subTest(key=key):
                self.manifest["plan"] = dict(original, **{key: "0" * 64})
                self.reject()

    def test_plan_json_is_strict_before_authentication(self):
        adaptation.PLAN_MANIFEST.write_bytes(b'{"status":"draft","status":"released"}\n')
        with self.assertRaisesRegex(corpus.CorpusError, "Duplicate JSON key"):
            corpus.check(self.path)

    def test_plan_authentication_failure_is_corpus_error_with_cause(self):
        error = adaptation.PlanError("unauthenticated plan")
        self.auth.side_effect = error
        with self.assertRaisesRegex(corpus.CorpusError, "unauthenticated plan") as caught:
            corpus.check(self.path)
        self.assertIs(caught.exception.__cause__, error)

    def test_public_api_wraps_authentication_and_validation_io_data_errors(self):
        errors = [OSError("unreadable artifact"), ValueError("invalid data"),
                  json.JSONDecodeError("invalid JSON", "{", 0),
                  sqlite3.DatabaseError("invalid database"), KeyError("missing field"),
                  TypeError("wrong field type"), AttributeError("wrong object type")]
        for stage in ("authenticate_plan", "validate_rule"):
            for error in errors:
                with self.subTest(stage=stage, error=type(error).__name__):
                    with (
                        mock.patch.object(corpus, stage, side_effect=error),
                        self.assertRaises(corpus.CorpusError) as caught,
                    ):
                        corpus.check(self.path)
                    self.assertIs(caught.exception.__cause__, error)

    def test_public_api_does_not_swallow_interrupts(self):
        with (
            mock.patch.object(corpus, "authenticate_plan", side_effect=KeyboardInterrupt),
            self.assertRaises(KeyboardInterrupt),
        ):
            corpus.check(self.path)

    def test_source_metadata_hashes_paths_and_rights(self):
        original = copy.deepcopy(self.source)
        changes = [
            ("artifact_sha256", "0" * 64), ("source_pdf_sha256", "0" * 64),
            ("artifact_path", "elsewhere.sqlite3"), ("retrieved_at", "today"),
            ("unknown", None), ("owner", {}), ("rights", {}),
            ("permission", dict(original["permission"], sha256="0" * 64)),
        ]
        for key, value in changes:
            with self.subTest(key=key):
                self.source = copy.deepcopy(original)
                self.source[key] = value
                self.reject()

    def test_changed_source_or_permission_bytes(self):
        for path in (adaptation.SOURCE_DATABASE, adaptation.PERMISSION_RECORD):
            with self.subTest(path=path):
                path.write_bytes(b"changed\n")
                with self.assertRaises(corpus.CorpusError):
                    corpus.check(self.path)
                path.write_bytes(b"{}\n")

    def test_rule_constraints_and_domains(self):
        original = copy.deepcopy(self.rule)
        for key, value in {
            "unknown": None, "id": "ITSTE-R-9999", "origin": "original", "status": "released",
            "language": "ru", "translation_of": "other", "title": "TODO: write title",
            "text": "{{template}}", "exceptions": [], "examples": {},
            "applies_to": ["unknown-domain"], "supporting_target_ids": ["ITSTE-R-0001"],
            "source_refs": [], "review": {"mode": "machine"}, "rights": {},
        }.items():
            with self.subTest(key=key):
                self.rule = copy.deepcopy(original)
                self.rule[key] = value
                self.reject()

    def test_template_origin_and_nested_closed_fields(self):
        self.rule["origin"] = "template"
        self.reject()
        self.rule["origin"] = "adaptation"
        objects = [self.rule["review"], self.rule["rights"],
                   self.rule["source_refs"][0]["locator"],
                   self.rule["source_refs"][0]["facets"][0],
                   self.rule["examples"], self.rule["examples"]["allowed"][0],
                   self.rule["examples"]["allowed"][0]["segments"][0]]
        for item in objects:
            with self.subTest(fields=list(item)):
                item["unknown"] = True
                self.reject()
                del item["unknown"]

    def test_duplicate_and_unknown_supporting_ids_and_domains(self):
        for key, value in [("applies_to", ["general", "general"]),
                           ("supporting_target_ids", ["ITSTE-R-9999"]),
                           ("supporting_target_ids", ["ITSTE-R-0002"] * 2)]:
            with self.subTest(key=key, value=value):
                self.rule[key] = value
                self.reject()
                self.rule[key] = ["general"] if key == "applies_to" else []

    def test_missing_duplicate_and_wrong_source_locators(self):
        original = copy.deepcopy(self.rule["source_refs"])
        cases = [original[:1], original + [original[0]],
                 [dict(original[0], locator=dict(original[0]["locator"], physical_pdf_pages=[1, 2])), original[1]],
                 [original[0], dict(original[1], locator=dict(original[1]["locator"], kind="rule"))],
                 [dict(original[0], facets=[]), original[1]],
                 [dict(original[0], unknown=True), original[1]]]
        for refs in cases:
            with self.subTest(refs=refs):
                self.rule["source_refs"] = copy.deepcopy(refs)
                self.reject()

    def test_literal_and_example_structure(self):
        original = copy.deepcopy(self.rule["examples"])
        for field, value in [("sha256", "0" * 64), ("text", "mutated command"),
                             ("literal_type", "executable"), ("kind", "unknown"), ("extra", True)]:
            with self.subTest(field=field):
                self.rule["examples"] = copy.deepcopy(original)
                self.rule["examples"]["allowed"][0]["segments"][1][field] = value
                self.reject()
        for value in ([], [{}], [{"segments": [], "rationale": "Reason"}]):
            self.rule["examples"] = copy.deepcopy(original)
            self.rule["examples"]["allowed"] = value
            self.reject()

    def test_literal_html_todo_and_template_syntax_are_preserved(self):
        literal = self.rule["examples"]["allowed"][0]["segments"][1]
        for value in ("<div>TODO: render café</div>", "echo <...>", "{{value}}"):
            with self.subTest(literal=value):
                literal["text"] = value
                literal["sha256"] = digest(value.encode("utf-8"))
                self.save()
                self.assertEqual(corpus.check(self.path), 1)

    def test_literal_requires_nonempty_utf8_even_with_marker_bypass(self):
        examples = self.rule["examples"]
        literal = examples["allowed"][0]["segments"][1]
        for value in ("", "   ", "\ud800"):
            with self.subTest(literal=repr(value)):
                literal["text"] = value
                with self.assertRaises(corpus.CorpusError):
                    corpus.validate_examples(examples)

    def test_split_markers_in_adjacent_prose_are_rejected(self):
        example = self.rule["examples"]["allowed"][0]
        literal = copy.deepcopy(example["segments"][1])
        for parts in (("TO", "DO: finish this"), ("<place", "holder>"), ("{", "{value}", "}")):
            for at_end in (False, True):
                with self.subTest(parts=parts, at_end=at_end):
                    prose = [{"kind": "prose", "text": part} for part in parts]
                    example["segments"] = [literal] + prose if at_end else prose + [literal]
                    self.reject()

    def test_prose_runs_stop_at_literals(self):
        literal = {"kind": "literal", "literal_type": "quotation", "text": "TODO <placeholder> {{value}}"}
        literal["sha256"] = digest(literal["text"].encode("utf-8"))
        example = self.rule["examples"]["allowed"][0]
        example["segments"] = [{"kind": "prose", "text": "TO"}, literal,
                               {"kind": "prose", "text": "DO: finish this"}]
        self.save()
        self.assertEqual(corpus.check(self.path), 1)

    def test_nonempty_whitespace_prose_separator_is_preserved(self):
        example = self.rule["examples"]["allowed"][0]
        literal = example["segments"][1]
        example["segments"] = [{"kind": "prose", "text": "Run"},
                               {"kind": "prose", "text": " "}, literal,
                               {"kind": "prose", "text": " "},
                               {"kind": "prose", "text": "now."}]
        self.save()
        self.assertEqual(corpus.check(self.path), 1)
        self.assertEqual("".join(segment["text"] for segment in example["segments"]),
                         "Run service restart now.")

    def test_empty_or_invalid_utf8_prose_and_blank_metadata_are_rejected(self):
        example = self.rule["examples"]["allowed"][0]
        for value in ("", "\ud800"):
            example["segments"][0]["text"] = value
            with self.subTest(prose=repr(value)), self.assertRaises(corpus.CorpusError):
                corpus.validate_examples(self.rule["examples"])
        example["segments"][0]["text"] = "Run this command:"
        for target, key in ((example, "rationale"), (self.rule, "title")):
            original = target[key]
            target[key] = " "
            self.reject()
            target[key] = original

    def test_authored_prose_and_metadata_still_reject_template_markers(self):
        example = self.rule["examples"]["allowed"][0]
        for target, key in ((example["segments"][0], "text"), (example, "rationale"),
                            (self.rule, "title")):
            original = target[key]
            for marker in ("TODO: finish this", "<placeholder>", "{{value}}"):
                with self.subTest(field=key, marker=marker):
                    target[key] = marker
                    self.reject()
            target[key] = original

    def test_noncanonical_record_language_directory_and_filename(self):
        canonical = "content/en/rules/ITSTE-R-0001.json"
        for wrong in ("content/rule.json", "content/ru/rules/ITSTE-R-0001.json",
                      "content/en/guidance/ITSTE-R-0001.json", "content/en/rules/other.json",
                      "content/en/rules/ITSTE-R-0002.json"):
            with self.subTest(path=wrong):
                self.manifest["records"] = [wrong]
                self.save()
                (self.path.parent / canonical).unlink()
                self.write(self.path.parent / wrong, self.rule)
                with self.assertRaises(corpus.CorpusError):
                    corpus.check(self.path)
                (self.path.parent / wrong).unlink()

    def test_noncanonical_source_filename_and_directory(self):
        canonical = f"sources/{corpus.SOURCE_ID}.json"
        for wrong in ("sources/source.json", f"sources/en/{corpus.SOURCE_ID}.json",
                      f"content/{corpus.SOURCE_ID}.json"):
            with self.subTest(path=wrong):
                self.manifest["sources"] = [wrong]
                self.save()
                (self.path.parent / canonical).unlink()
                self.write(self.path.parent / wrong, self.source)
                with self.assertRaisesRegex(corpus.CorpusError, "canonical source path"):
                    corpus.check(self.path)
                (self.path.parent / wrong).unlink()

    def test_manifest_requires_full_namespace_not_only_suffix(self):
        suffix = "versions/0.1.0-draft.1/revisions/r0001/manifest.json"
        for prefix in ("", "standards/other", "fixtures/standards/it-ste"):
            wrong = self.root / prefix / suffix
            with self.subTest(path=wrong):
                self.write(wrong, self.manifest)
                with self.assertRaisesRegex(corpus.CorpusError, "canonical repository namespace"):
                    corpus.check(wrong)
        alias = self.root / "manifest.json"
        alias.symlink_to(self.path)
        with self.assertRaisesRegex(corpus.CorpusError, "canonical repository namespace"):
            corpus.check(alias)

    def test_duplicate_ids(self):
        self.manifest["records"].append("content/en/rules/ITSTE-R-0002.json")
        self.write(self.path.parent / "content/en/rules/ITSTE-R-0002.json", self.rule)
        self.reject()

    def test_unsafe_member_paths(self):
        for value in ("/etc/passwd", "../rule.json", "content/../content/rule.json", "content\\rule.json"):
            with self.subTest(path=value):
                self.manifest["records"] = [value]
                self.reject()

    def test_missing_unlisted_and_duplicate_members(self):
        original = copy.deepcopy(self.manifest)
        for records in (["content/en/rules/ITSTE-R-0003.json"],
                        ["content/en/rules/ITSTE-R-0001.json"] * 2):
            self.manifest["records"] = records
            self.reject()
        self.manifest = original
        for name in ("content/unlisted.json", "sources/extra.txt"):
            path = self.path.parent / name
            path.write_bytes(b"{}\n")
            self.reject()
            path.unlink()

    def test_symlink_escape_and_resolved_alias(self):
        link = self.path.parent / "content/en/rules/ITSTE-R-0002.json"
        outside_snapshot = self.root / "other.json"
        self.write(outside_snapshot, self.rule)
        link.symlink_to(outside_snapshot)
        self.manifest["records"].append("content/en/rules/ITSTE-R-0002.json")
        self.reject()
        link.unlink()
        link.symlink_to(self.path.parent / "content/en/rules/ITSTE-R-0001.json")
        self.reject()
        link.unlink()
        with tempfile.TemporaryDirectory() as directory:
            external = Path(directory) / "external.json"
            self.write(external, self.rule)
            link.symlink_to(external)
            self.reject()

    def test_unlisted_symlink_alias_is_not_hidden(self):
        link = self.path.parent / "content/unlisted.json"
        link.symlink_to(self.path.parent / "content/en/rules/ITSTE-R-0001.json")
        self.reject()

    def test_bad_member_encoding_is_rejected(self):
        for relative in ("content/en/rules/ITSTE-R-0001.json", f"sources/{corpus.SOURCE_ID}.json"):
            with self.subTest(member=relative):
                self.save()
                (self.path.parent / relative).write_bytes(b'\xef\xbb\xbf{}\n')
                with self.assertRaises(corpus.CorpusError):
                    corpus.check(self.path)

    def test_manifest_identity_path(self):
        wrong = self.root / "versions/0.1.0-draft.1/revisions/r0002/manifest.json"
        self.write(wrong, self.manifest)
        with self.assertRaisesRegex(corpus.CorpusError, "identity"):
            corpus.check(wrong)

    def test_json_encoding_duplicates_and_non_json_numbers(self):
        for raw in (b'{"a": 1, "a": 2}\n', b'{"nested":{"x":1,"x":2}}\n',
                    b'{}', b'{}\r\n', b'\xef\xbb\xbf{}\n', b'{"x":"\xff"}\n',
                    b'{"x":NaN}\n', b'[]\n'):
            with self.subTest(raw=raw):
                self.path.write_bytes(raw)
                with self.assertRaises(corpus.CorpusError):
                    corpus.check(self.path)

    def test_cli_errors_have_no_tracebacks_or_false_pass(self):
        self.rule["status"] = "released"
        self.save()
        output, error = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            result = corpus.main(["check", "--manifest", str(self.path)])
        self.assertEqual(result, 2)
        self.assertIn("ERROR:", error.getvalue())
        self.assertNotIn("Traceback", error.getvalue())
        self.assertNotIn("PASS", output.getvalue())

    def test_cli_success_limits_its_claims(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(corpus.main(["check", "--manifest", str(self.path)]), 0)
        self.assertIn("structure and provenance only", output.getvalue())


if __name__ == "__main__":
    unittest.main()
