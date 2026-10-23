# SPDX-License-Identifier: GPL-3.0-only
"""Sequential dictionary batches: provenance, order, and draft boundaries."""

import contextlib
import copy
import io
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import it_ste_vocabulary as vocabulary


class VocabularyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = vocabulary.ROOT / vocabulary.DEFAULT_BATCH
        cls.original = vocabulary.corpus.load_json(cls.path)

    def setUp(self):
        self.batch = copy.deepcopy(self.original)

    def checked(self):
        original_load = vocabulary.corpus.load_json

        def load(path, **kwargs):
            if Path(path) == self.path:
                return self.batch
            return original_load(path, **kwargs)

        with mock.patch.object(vocabulary.corpus, "load_json", side_effect=load):
            return vocabulary.check()

    def reject(self):
        with self.assertRaises(vocabulary.VocabularyError):
            self.checked()

    def test_exact_first_tranche_and_next_row(self):
        result = self.checked()
        self.assertEqual(result["total"], 2196)
        self.assertEqual(result["candidates"], 40)
        self.assertEqual(result["remaining"], 2156)
        self.assertEqual(result["next_entry_id"], "D-P154-007")
        self.assertEqual(result["dispositions"], {
            "allowed": 1, "restricted": 25, "prohibited": 10,
            "not-applicable": 4,
        })

    def test_complete_source_coverage_and_review_boundaries(self):
        batches, summary = vocabulary.checked_all()
        self.assertEqual(summary, {
            "total": 2196, "candidates": 2196, "remaining": 0,
            "next_entry_id": None, "batch_count": 55,
            "dispositions": {"allowed": 120, "restricted": 1483, "prohibited": 407,
                             "not-applicable": 148, "needs-review": 38},
        })
        decisions = [d for batch in batches for d in batch["decisions"]]
        self.assertEqual([d["sequence_number"] for d in decisions], list(range(1, 2197)))
        self.assertEqual(len({d["entry_id"] for d in decisions}), 2196)
        self.assertEqual(decisions[-1]["entry_id"], "D-P433-007")
        for decision in decisions:
            self.assertEqual(decision["status"], "draft")
            self.assertEqual(decision["review_status"], "editorial-review-needed")
        by_id = {d["entry_id"]: d for d in decisions}
        self.assertNotIn("may, for permission", by_id["D-P183-006"]["permitted_contextual_alternatives"])
        self.assertIn("Sanitization is a distinct operation", by_id["D-P212-003"]["rationale"])
        self.assertIn("test receiver", by_id["D-P252-011"]["examples"]["positive"]["text"])
        progress = by_id["D-P279-003"]
        self.assertEqual(progress["it_disposition"], "restricted")
        self.assertEqual(progress["evidence"]["extraction_warnings"], ["wrapped-headword"])
        self.assertTrue(progress["evidence"]["pdf_layout_check"]["visual_verification_performed"])
        self.assertIn("failure, or cancellation", progress["rationale"])
        self.assertIn("export job 42", progress["examples"]["positive"]["text"])
        precautionary = by_id["D-P336-009"]
        self.assertEqual(precautionary["it_disposition"], "prohibited")
        self.assertEqual(precautionary["evidence"]["extraction_warnings"], ["wrapped-headword"])
        self.assertTrue(precautionary["evidence"]["pdf_layout_check"]["visual_verification_performed"])
        self.assertIn("PRECAUTION (n)", precautionary["rationale"])
        self.assertNotIn("precautionary", precautionary["examples"]["positive"]["text"])
        temporal_phrase = by_id["D-P341-003"]
        self.assertEqual(temporal_phrase["it_disposition"], "prohibited")
        self.assertEqual(temporal_phrase["headword"], "process (in the process of )")
        self.assertEqual(temporal_phrase["evidence"]["extraction_warnings"], ["wrapped-headword"])
        self.assertTrue(temporal_phrase["evidence"]["pdf_layout_check"]["visual_verification_performed"])
        self.assertIn("not the technical noun process", temporal_phrase["rationale"])
        self.assertIn("While the service exports", temporal_phrase["examples"]["positive"]["text"])
        for identifier, disposition in (("D-P344-006", "restricted"), ("D-P344-007", "prohibited")):
            decision = by_id[identifier]
            self.assertEqual(decision["it_disposition"], disposition)
            self.assertTrue(decision["evidence"]["pdf_layout_check"]["visual_verification_performed"])
        self.assertTrue(by_id["D-P344-006"]["evidence"]["mechanical_ambiguities"])
        self.assertEqual(by_id["D-P344-007"]["evidence"]["extraction_warnings"], ["wrapped-headword"])
        self.assertIn("not an automatic substitute", by_id["D-P344-007"]["rationale"])
        radioactive = by_id["D-P349-003"]
        self.assertEqual(radioactive["it_disposition"], "needs-review")
        self.assertEqual(radioactive["evidence"]["extraction_warnings"], ["wrapped-headword"])
        self.assertTrue(radioactive["evidence"]["pdf_layout_check"]["visual_verification_performed"])
        self.assertIn("without identifying their sensing technology", radioactive["rationale"])
        real = by_id["D-P351-001"]
        self.assertEqual(real["it_disposition"], "needs-review")
        self.assertTrue(real["evidence"]["mechanical_ambiguities"])
        self.assertTrue(real["evidence"]["pdf_layout_check"]["visual_verification_performed"])
        self.assertIn("not automatically true or verified", real["rationale"])
        for identifier in ("D-P359-001", "D-P359-002"):
            decision = by_id[identifier]
            self.assertEqual(decision["it_disposition"], "restricted")
            self.assertIn("specified compatible type", decision["it_definition"])
            self.assertTrue(decision["evidence"]["pdf_layout_check"]["visual_verification_performed"])
        self.assertTrue(by_id["D-P359-001"]["evidence"]["mechanical_ambiguities"])
        self.assertEqual(by_id["D-P359-002"]["evidence"]["extraction_warnings"], ["wrapped-headword"])
        self.assertNotIn("new component", by_id["D-P359-002"]["permitted_contextual_alternatives"])
        rework = by_id["D-P363-009"]
        self.assertEqual(rework["it_disposition"], "restricted")
        self.assertIn("meets the specified requirements", rework["it_definition"])
        self.assertIn("not automatic substitutes", rework["rationale"])
        self.assertTrue(rework["evidence"]["mechanical_ambiguities"])
        self.assertTrue(rework["evidence"]["pdf_layout_check"]["visual_verification_performed"])
        self.assertNotIn("correct under the repair procedure", rework["permitted_contextual_alternatives"])
        self.assertNotIn("replace the faulty assembly", rework["permitted_contextual_alternatives"])
        self.assertIn("server cable harness", rework["examples"]["positive"]["text"])
        running = by_id["D-P365-011"]
        self.assertEqual(running["it_disposition"], "needs-review")
        self.assertEqual(running["part_of_speech_as_extracted"], "adj")
        self.assertTrue(running["evidence"]["mechanical_ambiguities"])
        self.assertTrue(running["evidence"]["pdf_layout_check"]["visual_verification_performed"])
        self.assertEqual(running["permitted_contextual_alternatives"], ["flowing water, in hardware cleaning"])
        self.assertIn("not a readiness or general health guarantee", running["rationale"])
        for identifier in ("D-P368-003", "D-P368-004"):
            decision = by_id[identifier]
            self.assertEqual(decision["it_disposition"], "restricted")
            self.assertTrue(decision["evidence"]["mechanical_ambiguities"])
            self.assertTrue(decision["evidence"]["pdf_layout_check"]["visual_verification_performed"])
        self.assertIn("specified sampling policy", by_id["D-P368-003"]["it_definition"])
        self.assertIn("no requests failed", by_id["D-P368-003"]["examples"]["problematic"]["text"])
        self.assertEqual(by_id["D-P368-004"]["evidence"]["extraction_warnings"], ["wrapped-headword"])
        self.assertIn("not a general recovery", by_id["D-P368-004"]["rationale"])
        self.assertIn("named test", by_id["D-P368-004"]["permitted_contextual_alternatives"][1])
        satisfactory = by_id["D-P368-005"]
        self.assertEqual(satisfactory["it_disposition"], "restricted")
        self.assertEqual(satisfactory["evidence"]["extraction_warnings"], ["wrapped-headword"])
        self.assertTrue(satisfactory["evidence"]["pdf_layout_check"]["visual_verification_performed"])
        self.assertIn("named IT service property", satisfactory["it_definition"])
        self.assertNotIn("passes the specified tests", satisfactory["permitted_contextual_alternatives"])
        self.assertIn("last 24 hours", satisfactory["examples"]["positive"]["text"])
        self.assertIn("measured at the gateway", satisfactory["examples"]["positive"]["text"])
        self.assertIn("not project measurements", satisfactory["examples"]["positive"]["explanation"])
        scored = by_id["D-P368-010"]
        self.assertEqual(scored["it_disposition"], "needs-review")
        self.assertTrue(scored["evidence"]["mechanical_ambiguities"])
        self.assertTrue(scored["evidence"]["pdf_layout_check"]["visual_verification_performed"])
        self.assertEqual(scored["permitted_contextual_alternatives"], ["damaged by a groove"])
        self.assertIn("does not define scored", scored["rationale"])
        self.assertIn("not a pass/fail rule", scored["examples"]["positive"]["explanation"])
        scratched = by_id["D-P369-002"]
        self.assertEqual(scratched["it_disposition"], "restricted")
        self.assertTrue(scratched["evidence"]["mechanical_ambiguities"])
        self.assertTrue(scratched["evidence"]["pdf_layout_check"]["visual_verification_performed"])
        self.assertIn("fiber-optic connector", scratched["it_definition"])
        self.assertNotIn("shallow", scratched["it_definition"])
        self.assertNotIn("surface-damaged", scratched["permitted_contextual_alternatives"])
        self.assertIn("inspection report", scratched["examples"]["positive"]["text"])
        self.assertIn("distinct scored entry remains unresolved", scratched["rationale"])
        security = by_id["D-P370-004"]
        self.assertEqual(security["it_disposition"], "prohibited")
        self.assertTrue(security["evidence"]["mechanical_ambiguities"])
        self.assertTrue(security["evidence"]["pdf_layout_check"]["visual_verification_performed"])
        self.assertIn("physical IT component", security["it_definition"])
        self.assertIn("does not prohibit independently scoped information-security", security["rationale"])
        self.assertIn("server rack latch", security["examples"]["positive"]["text"])
        self.assertIn("sentence rewrite", security["permitted_contextual_alternatives"][1])
        for identifier in ("D-P372-002", "D-P372-003"):
            decision = by_id[identifier]
            self.assertEqual(decision["it_disposition"], "restricted")
            self.assertTrue(decision["evidence"]["pdf_layout_check"]["visual_verification_performed"])
        self.assertTrue(by_id["D-P372-002"]["evidence"]["mechanical_ambiguities"])
        self.assertIn("UI's selected state", by_id["D-P372-002"]["it_definition"])
        self.assertIn("application-specific side effects", by_id["D-P372-002"]["rationale"])
        self.assertEqual(by_id["D-P372-003"]["evidence"]["extraction_warnings"], ["wrapped-headword"])
        self.assertIn("180-degree circular arc", by_id["D-P372-003"]["it_definition"])
        self.assertIn("not a filled half-disk", by_id["D-P372-003"]["rationale"])
        self.assertNotIn("cable guide", by_id["D-P372-003"]["examples"]["positive"]["text"])
        serve = by_id["D-P374-003"]
        self.assertEqual(serve["it_disposition"], "restricted")
        self.assertIn("configured URL-to-file mapping", serve["it_definition"])
        self.assertIn("HEAD, conditional responses and errors", serve["rationale"])
        serviceability = by_id["D-P374-005"]
        self.assertEqual(serviceability["it_disposition"], "needs-review")
        self.assertIn("not a complete operating-acceptance criterion", serviceability["rationale"])
        self.assertIn("not proof of every operating requirement", serviceability["examples"]["positive"]["explanation"])
        for decision in (serve, serviceability):
            self.assertTrue(decision["evidence"]["mechanical_ambiguities"])
            self.assertTrue(decision["evidence"]["pdf_layout_check"]["visual_verification_performed"])
        for identifier in ("D-P285-003", "D-P333-004", "D-P338-010", "D-P347-001", "D-P407-009"):
            self.assertIn("are permitted to", by_id[identifier]["examples"]["positive"]["text"])

    def test_batch_002_w1_resolutions_preserve_evidence(self):
        batches, _ = vocabulary.checked_all()
        batch = next(b for b in batches if b["batch_id"] == "002")
        by_id = {d["entry_id"]: d for d in batch["decisions"]}
        for identifier, disposition, page in (
            ("D-P156-005", "restricted", 156),
            ("D-P156-006", "restricted", 156),
            ("D-P157-003", "prohibited", 157),
        ):
            with self.subTest(entry=identifier):
                decision = by_id[identifier]
                self.assertEqual(decision["it_disposition"], disposition)
                evidence = decision["evidence"]
                self.assertEqual(evidence["physical_pdf_page"], page)
                self.assertTrue(evidence["mechanical_ambiguities"])
                self.assertEqual(evidence["source_interpretation_status"],
                                 "mechanically-extracted-unreviewed")
                layout = evidence["pdf_layout_check"]
                self.assertTrue(layout["performed"])
                self.assertTrue(layout["visual_verification_performed"])
                self.assertIn(vocabulary.adaptation.EXPECTED_SOURCE_SHA256, layout["method"])
                self.assertIn("Findings:", layout["method"])
                self.assertEqual(decision["status"], "draft")
                self.assertEqual(decision["review_status"], "editorial-review-needed")
        self.assertEqual(by_id["D-P156-006"]["evidence"]["extraction_warnings"],
                         ["wrapped-headword"])
        self.assertIn("--full", by_id["D-P157-003"]["evidence"]["pdf_layout_check"]["method"])
        self.assertEqual(by_id["D-P157-003"]["part_of_speech_as_extracted"], "n")
        self.assertIn("does not cover the verb", by_id["D-P157-003"]["rationale"])

    def test_no_skipped_reordered_or_duplicate_rows(self):
        for change in ("omit", "swap", "duplicate"):
            with self.subTest(change=change):
                self.batch = copy.deepcopy(self.original)
                decisions = self.batch["decisions"]
                if change == "omit":
                    decisions.pop()
                elif change == "swap":
                    decisions[0], decisions[1] = decisions[1], decisions[0]
                else:
                    decisions[1] = copy.deepcopy(decisions[0])
                self.reject()

    def test_forged_source_hashes_and_paths(self):
        for key in ("database_path", "database_sha256", "manifest_path", "manifest_sha256",
                    "permission_path", "permission_sha256", "pdf_sha256"):
            with self.subTest(key=key):
                self.batch = copy.deepcopy(self.original)
                self.batch["source"][key] = "untrusted"
                self.reject()

    def test_wrong_entry_locator_or_mechanical_approval(self):
        for key, value in (("entry_id", "D-P154-007"), ("headword", "changed"),
                           ("part_of_speech_as_extracted", "unknown"),
                           ("physical_pdf_page", 1), ("sequence_number", True)):
            with self.subTest(key=key):
                self.batch = copy.deepcopy(self.original)
                self.batch["decisions"][0][key] = value
                self.reject()
        self.batch = copy.deepcopy(self.original)
        self.batch["decisions"][0]["upstream_status_raw"]["value"] = "not-approved"
        self.reject()

    def test_cannot_claim_editorial_or_canonical_approval(self):
        for key in ("status", "review_status"):
            with self.subTest(key=key):
                self.batch = copy.deepcopy(self.original)
                self.batch[key] = "approved"
                self.reject()
                self.batch = copy.deepcopy(self.original)
                self.batch["decisions"][0][key] = "approved"
                self.reject()
        for key in ("human_editorial_approval", "canonical_terms_created", "rules_changed"):
            self.batch = copy.deepcopy(self.original)
            self.batch["evidence"][key] = True
            self.reject()

    def test_ambiguous_rows_cannot_be_treated_as_settled(self):
        for index, decision in enumerate(self.original["decisions"]):
            if decision["evidence"]["mechanical_ambiguities"]:
                with self.subTest(entry=decision["entry_id"]):
                    self.batch = copy.deepcopy(self.original)
                    changed = self.batch["decisions"][index]
                    changed["it_disposition"] = "allowed"
                    changed["evidence"]["pdf_layout_check"]["visual_verification_performed"] = False
                    self.reject()

    def test_cannot_discard_source_warnings_or_known_ambiguity(self):
        indices = [index for index, decision in enumerate(self.original["decisions"])
                   if decision["evidence"]["extraction_warnings"]]
        self.assertTrue(indices)
        for index in indices:
            self.batch = copy.deepcopy(self.original)
            self.batch["decisions"][index]["evidence"]["extraction_warnings"] = []
            self.reject()
        index = next(index for index, decision in enumerate(self.original["decisions"])
                     if decision["entry_id"] == "D-P153-004")
        self.batch = copy.deepcopy(self.original)
        self.batch["decisions"][index]["evidence"]["mechanical_ambiguities"] = []
        self.batch["decisions"][index]["it_disposition"] = "allowed"
        self.batch["decisions"][index]["evidence"]["pdf_layout_check"]["visual_verification_performed"] = False
        self.reject()

    def test_visual_resolution_requires_performed_check_source_pin_and_findings(self):
        for change in ("unperformed", "missing-pin", "missing-findings", "empty-method"):
            with self.subTest(change=change):
                self.batch = copy.deepcopy(self.original)
                decision = next(d for d in self.batch["decisions"] if d["entry_id"] == "D-P153-001")
                pdf = decision["evidence"]["pdf_layout_check"]
                if change == "unperformed":
                    pdf["performed"] = False
                elif change == "missing-pin":
                    pdf["method"] = "Findings: separate rows"
                elif change == "missing-findings":
                    pdf["method"] = vocabulary.adaptation.EXPECTED_SOURCE_SHA256
                else:
                    pdf["method"] = ""
                self.reject()

    def test_domains_definitions_examples_and_alternatives(self):
        for key, value in (("domains", ["unknown-domain"]), ("rationale", ""),
                           ("it_definition", ""), ("it_disposition", "approved"),
                           ("permitted_contextual_alternatives", ["ITSTE-T-9999"]),
                           ("examples", {})):
            with self.subTest(key=key):
                self.batch = copy.deepcopy(self.original)
                self.batch["decisions"][0][key] = value
                self.reject()

    def test_scope_and_rights_cannot_be_relicensed(self):
        self.batch["rights"]["project_link"] = "https://example.org"
        self.reject()
        self.batch = copy.deepcopy(self.original)
        self.batch["rights"]["asd_source"]["downstream_license"] = "CC-BY-SA-4.0"
        self.reject()
        self.batch = copy.deepcopy(self.original)
        self.batch["source"]["pdf_included"] = True
        self.reject()

    def test_counts_cannot_hide_remaining_rows(self):
        for key, value in (("remaining", 0), ("entry_count", 2196),
                           ("total_source_rows", 40), ("last_entry_id", "D-P154-007")):
            self.batch = copy.deepcopy(self.original)
            self.batch["sequence"][key] = value
            self.reject()

    def test_cli_entry_is_bounded_and_explicitly_draft(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(vocabulary.main(["entry", "D-P149-001", "--compact-json"]), 0)
        value = json.loads(output.getvalue())
        self.assertEqual(value["status"], "draft")
        self.assertEqual(value["review_status"], "editorial-review-needed")
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(vocabulary.main(["entry", "D-P154-007", "--batch", str(self.path)]), 2)
            self.assertEqual(vocabulary.main(["entry", "D-P999-999"]), 2)

    def test_duplicate_json_and_symlink_alias_are_rejected(self):
        with tempfile.TemporaryDirectory(dir=vocabulary.ROOT) as directory:
            path = Path(directory) / "batch.json"
            path.write_text('{"status":"draft","status":"approved"}\n', encoding="utf-8")
            with self.assertRaises(vocabulary.VocabularyError):
                vocabulary.check(path)
            path.unlink()
            path.symlink_to(self.path)
            with self.assertRaises(vocabulary.VocabularyError):
                vocabulary.check(path)

    def make_batch(self, number):
        """Build synthetic draft decisions from just the requested source chunk."""
        batch = copy.deepcopy(self.original)
        offset = (number - 1) * 40
        with contextlib.closing(sqlite3.connect(vocabulary.adaptation.SOURCE_DATABASE)) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                "SELECT id,headword,pos,approval,pdf_page,printed_page,warnings FROM dictionary_entries "
                "ORDER BY pdf_page,CAST(substr(id,-3) AS INTEGER) LIMIT 40 OFFSET ?",
                (offset,)).fetchall()
        batch["batch_id"] = f"{number:03d}"
        batch["sequence"].update(first_entry_id=rows[0]["id"], last_entry_id=rows[-1]["id"],
                                 entry_count=len(rows), remaining=2196 - offset - len(rows))
        batch["decisions"] = []
        for sequence, row in enumerate(rows, offset + 1):
            decision = copy.deepcopy(self.original["decisions"][0])
            decision.update(sequence_number=sequence, entry_id=row["id"], headword=row["headword"],
                            part_of_speech_as_extracted=row["pos"], physical_pdf_page=row["pdf_page"],
                            it_disposition="needs-review")
            decision["upstream_status_raw"]["value"] = row["approval"]
            decision["evidence"].update(
                source_entry_id=row["id"], physical_pdf_page=row["pdf_page"],
                printed_page=row["printed_page"], row_on_page=int(row["id"].rsplit("-", 1)[1]),
                extraction_warnings=json.loads(row["warnings"]))
            decision["evidence"]["retrieval"]["command"] = (
                f"python3 tools/asd_ste100_local.py entry {row['id']} --compact-json")
            batch["decisions"].append(decision)
        return batch

    def write_batch(self, directory, batch, name=None):
        path = Path(directory) / (name or f"batch-{batch['batch_id']}.json")
        path.write_text(json.dumps(batch) + "\n", encoding="utf-8")
        return path

    def test_multiple_batches_and_cli_defaults(self):
        with tempfile.TemporaryDirectory(dir=vocabulary.ROOT) as directory:
            first = self.write_batch(directory, self.original)
            second = self.make_batch(2)
            third = self.make_batch(3)
            second_path = self.write_batch(directory, second)
            self.write_batch(directory, third)
            with mock.patch.object(vocabulary, "DEFAULT_BATCH", first):
                batches, summary = vocabulary.checked_all()
                self.assertEqual([b["batch_id"] for b in batches], ["001", "002", "003"])
                self.assertEqual(summary, {
                    "total": 2196, "candidates": 120, "remaining": 2076,
                    "next_entry_id": self.make_batch(4)["decisions"][0]["entry_id"],
                    "dispositions": {**vocabulary.check()["dispositions"], "needs-review": 80},
                    "batch_count": 3,
                })
                self.assertEqual(vocabulary.check_all(), summary)
                individual = vocabulary.check(second_path)
                self.assertEqual(individual["candidates"], 40)
                self.assertEqual(individual["remaining"], 2116)
                self.assertEqual(individual["next_entry_id"], third["decisions"][0]["entry_id"])
                entry_id = third["decisions"][-1]["entry_id"]
                for args, expected in (
                    (["check"], {"candidates": 120, "batch_count": 3}),
                    (["check", "--batch", str(second_path)], {"candidates": 40, "remaining": 2116}),
                    (["entry", entry_id], {"entry_id": entry_id, "sequence_number": 120}),
                ):
                    with self.subTest(args=args), contextlib.redirect_stdout(io.StringIO()) as output:
                        self.assertEqual(vocabulary.main([*args, "--compact-json"]), 0)
                        result = json.loads(output.getvalue())
                        for key, value in expected.items():
                            self.assertEqual(result[key], value)
                with contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(vocabulary.main(["entry", entry_id, "--batch", str(first)]), 2)

    def test_later_batch_exact_offset_and_global_sequence(self):
        for change in ("omit", "extra", "swap", "duplicate", "previous", "local-number", "bool-number",
                       "remaining", "first", "last"):
            with self.subTest(change=change), tempfile.TemporaryDirectory(dir=vocabulary.ROOT) as directory:
                batch = self.make_batch(2)
                decisions = batch["decisions"]
                if change == "omit":
                    decisions.pop()
                elif change == "extra":
                    decisions.append(copy.deepcopy(decisions[-1]))
                elif change == "swap":
                    decisions[0], decisions[1] = decisions[1], decisions[0]
                elif change == "duplicate":
                    decisions[1] = copy.deepcopy(decisions[0])
                elif change == "previous":
                    batch["decisions"] = copy.deepcopy(self.original["decisions"])
                elif change in ("local-number", "bool-number"):
                    decisions[0]["sequence_number"] = 1 if change == "local-number" else True
                elif change == "remaining":
                    batch["sequence"]["remaining"] = 2156
                else:
                    batch["sequence"][change + "_entry_id"] = self.original["decisions"][0]["entry_id"]
                path = self.write_batch(directory, batch)
                with self.assertRaises(vocabulary.VocabularyError):
                    vocabulary.check(path)

    def test_canonical_batch_ids(self):
        for batch_id in (1, True, None, "", "000", "1", "01", "0001", "+01", " 01", "001\n", "٠٠١", "056"):
            with self.subTest(batch_id=batch_id):
                self.batch = copy.deepcopy(self.original)
                self.batch["batch_id"] = batch_id
                self.reject()

    def test_final_remainder(self):
        with tempfile.TemporaryDirectory(dir=vocabulary.ROOT) as directory:
            batch = self.make_batch(55)
            path = self.write_batch(directory, batch)
            summary = vocabulary.check(path)
            self.assertEqual(summary["candidates"], 36)
            self.assertEqual(summary["remaining"], 0)
            self.assertIsNone(summary["next_entry_id"])
            self.assertEqual(batch["decisions"][-1]["sequence_number"], 2196)
            batch["decisions"].pop()
            self.write_batch(directory, batch)
            with self.assertRaises(vocabulary.VocabularyError):
                vocabulary.check(path)

    def test_discovery_rejects_gaps_aliases_and_filename_id_mismatch(self):
        for change in ("empty", "missing-first", "gap", "duplicate", "reordered", "noncanonical",
                       "zero", "symlink", "directory-symlink", "outside"):
            with self.subTest(change=change), tempfile.TemporaryDirectory(dir=vocabulary.ROOT) as directory:
                first = Path(directory) / "batch-001.json"
                second = self.make_batch(2)
                if change != "empty":
                    self.write_batch(directory, self.original)
                if change == "missing-first":
                    first.unlink()
                    self.write_batch(directory, second)
                elif change == "gap":
                    self.write_batch(directory, self.make_batch(3))
                elif change in ("duplicate", "reordered"):
                    self.write_batch(directory, self.original if change == "duplicate" else self.make_batch(3),
                                     "batch-002.json")
                elif change in ("noncanonical", "zero"):
                    self.write_batch(directory, second, "batch-02.json" if change == "noncanonical" else "batch-000.json")
                elif change == "symlink":
                    (Path(directory) / "batch-002.json").symlink_to(self.path)
                elif change == "directory-symlink":
                    alias = Path(directory) / "alias"
                    alias.symlink_to(Path(directory), target_is_directory=True)
                    first = alias / "batch-001.json"
                elif change == "outside":
                    first = Path(directory).parent.parent / "batch-001.json"
                with (
                    mock.patch.object(vocabulary, "DEFAULT_BATCH", first),
                    self.assertRaises(vocabulary.VocabularyError),
                ):
                    vocabulary.check_all()

    def test_validation_never_opens_private_pdf(self):
        original_open = Path.open

        def open_without_pdf(path, *args, **kwargs):
            self.assertNotIn(".local", path.parts)
            self.assertNotEqual(path.suffix.lower(), ".pdf")
            return original_open(path, *args, **kwargs)

        with mock.patch.object(Path, "open", open_without_pdf):
            self.assertEqual(vocabulary.check()["candidates"], 40)


if __name__ == "__main__":
    unittest.main()
