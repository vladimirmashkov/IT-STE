# SPDX-License-Identifier: GPL-3.0-only
"""First sequential dictionary tranche: provenance, order, and draft boundaries."""

import contextlib
import copy
import io
import json
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
            "allowed": 1, "restricted": 20, "prohibited": 9,
            "not-applicable": 4, "needs-review": 6,
        })

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
            if decision["it_disposition"] == "needs-review":
                with self.subTest(entry=decision["entry_id"]):
                    self.batch = copy.deepcopy(self.original)
                    self.batch["decisions"][index]["it_disposition"] = "allowed"
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
            self.assertEqual(vocabulary.main(["entry", "D-P154-007"]), 2)

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
