# SPDX-License-Identifier: GPL-3.0-only

import argparse
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from tools import asd_ste100_local as reference


def synthetic_record() -> dict[str, object]:
    return {
        "id": "D-SYNTHETIC-001",
        "headword": "ALPHA",
        "normalized_headword": "alpha",
        "pos": "n",
        "approval": "approved",
        "pdf_page": 1,
        "printed_page": "SYNTHETIC-1",
        "column_1": "ALPHA (n)",
        "column_2": "Project-authored synthetic meaning",
        "column_3": "SYNTHETIC EXAMPLE.",
        "column_4": "",
        "warnings": [],
        "text": "needle synthetic dictionary text",
    }


class PureFunctionTests(unittest.TestCase):
    def test_expected_public_structure(self) -> None:
        self.assertEqual(len(reference.EXPECTED_RULE_IDS), 53)
        self.assertEqual(len(reference.EXPECTED_GUIDANCE_IDS), 8)
        self.assertEqual(reference.EXPECTED_DICTIONARY_ENTRIES, 2_196)
        self.assertEqual(reference.approval_signal("ALPHA"), "approved")
        self.assertEqual(reference.approval_signal("alpha"), "not-approved")

    def test_page_split_removes_only_terminal_segment(self) -> None:
        self.assertEqual(reference.split_pdf_pages("one\ftwo\f"), ["one", "two"])
        self.assertEqual(reference.split_pdf_pages("one\f\ftwo\f"), ["one", "", "two"])

    def test_column_boundaries_keep_wide_cells(self) -> None:
        odd = reference.column_starts(149)
        self.assertEqual(reference.column_for_x(170.0, odd), 1)
        self.assertEqual(reference.column_for_x(175.0, odd), 2)
        self.assertEqual(reference.column_for_x(305.0, odd), 3)

    def test_title_repairs_layout_hyphen_wrap(self) -> None:
        text = "Rule 1.1 Use a line-\n             break safely.\n\nSynthetic detail."
        self.assertEqual(
            reference.derive_block_title("1.1", text),
            "Use a line-break safely.",
        )

    def test_limit_is_positive_and_bounded(self) -> None:
        self.assertEqual(reference.bounded_limit("1"), 1)
        self.assertEqual(reference.bounded_limit(str(reference.MAX_RESULTS)), reference.MAX_RESULTS)
        for value in ("0", "-1", str(reference.MAX_RESULTS + 1), "many"):
            with self.assertRaises(argparse.ArgumentTypeError):
                reference.bounded_limit(value)

    def test_private_path_rejects_public_output(self) -> None:
        accepted = reference.private_path(reference.LOCAL_ROOT / "test.db", "database")
        self.assertTrue(accepted.is_relative_to(reference.LOCAL_ROOT))
        with self.assertRaises(reference.ReferenceError):
            reference.private_path(reference.ROOT / "reference.db", "database")

    def test_rule_segmentation_with_project_authored_text(self) -> None:
        pages = [
            reference.Page(number, f"SYNTHETIC-{number}", reference.page_part(number), "")
            for number in range(1, 128)
        ]
        rule_ids = sorted(
            reference.EXPECTED_RULE_IDS,
            key=lambda value: tuple(int(part) for part in value.split(".")),
        )
        lines = []
        for block_id in rule_ids:
            lines.extend(
                [
                    f"Rule {block_id} Project-authored synthetic heading {block_id}.",
                    "",
                    f"Synthetic detail for {block_id}.",
                    "",
                ]
            )
        for block_id in sorted(reference.EXPECTED_GUIDANCE_IDS):
            lines.extend(
                [
                    f"{block_id} Project-authored synthetic recommendation.",
                    "",
                    f"Synthetic detail for {block_id}.",
                    "",
                ]
            )
        pages[44] = reference.Page(45, "SYNTHETIC-45", "part-1", "\n".join(lines))

        blocks = reference.extract_blocks(pages)
        self.assertEqual(len(blocks), 61)
        self.assertEqual({block["id"] for block in blocks if block["kind"] == "rule"}, reference.EXPECTED_RULE_IDS)
        self.assertEqual(
            {block["id"] for block in blocks if block["kind"] == "guidance"},
            reference.EXPECTED_GUIDANCE_IDS,
        )


class SyntheticDatabaseTests(unittest.TestCase):
    def setUp(self) -> None:
        reference.LOCAL_ROOT.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=reference.LOCAL_ROOT)
        self.database = Path(self.temporary.name) / "synthetic.sqlite3"
        pages = [
            reference.Page(
                1,
                "SYNTHETIC-1",
                "front-matter",
                "Project-authored needle page text",
            )
        ]
        blocks = [
            {
                "id": "SYNTHETIC",
                "kind": "guidance",
                "title": "Project-authored needle heading",
                "start_pdf_page": 1,
                "end_pdf_page": 1,
                "text": "Project-authored needle block text",
                "segments": [
                    {
                        "pdf_page": 1,
                        "printed_page": "SYNTHETIC-1",
                        "text": "Project-authored needle block text",
                    }
                ],
            }
        ]
        metadata = {
            "standard": "SYNTHETIC",
            "issue": "0",
            "issue_date": "1970-01-01",
            "source_sha256": "synthetic",
            "physical_pages": "1",
            "rules": "0",
            "guidance": "1",
            "dictionary_entries": "1",
            "review_state": "synthetic",
            "redistribution": "allowed",
        }
        reference.create_database(self.database, pages, blocks, [synthetic_record()], metadata)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_database_and_fts_are_queryable(self) -> None:
        with reference.open_database(self.database) as connection:
            self.assertEqual(connection.execute("PRAGMA integrity_check").fetchone()[0], "ok")
            self.assertEqual(connection.execute("SELECT count(*) FROM pages_fts").fetchone()[0], 1)
            self.assertEqual(connection.execute("SELECT count(*) FROM blocks_fts").fetchone()[0], 1)
            self.assertEqual(connection.execute("SELECT count(*) FROM dictionary_fts").fetchone()[0], 1)

    def test_full_json_does_not_duplicate_payload(self) -> None:
        block_args = argparse.Namespace(
            id="SYNTHETIC", database=self.database, json=True, full=True
        )
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            self.assertEqual(reference.get_block(block_args), 0)
        block = json.loads(stream.getvalue())
        self.assertNotIn("text", block)
        self.assertEqual(len(block["segments"]), 1)

        word_args = argparse.Namespace(
            term="alpha", pos=None, limit=1, database=self.database, json=True, full=True
        )
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            self.assertEqual(reference.word(word_args), 0)
        item = json.loads(stream.getvalue())[0]
        self.assertNotIn("text", item)
        self.assertIn("column_1", item)
        self.assertIn("column_4", item)

    def test_search_limit_is_global_across_scopes(self) -> None:
        args = argparse.Namespace(
            query="needle", scope="all", limit=1, database=self.database, json=True
        )
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            self.assertEqual(reference.search(args), 0)
        self.assertEqual(len(json.loads(stream.getvalue())), 1)


@unittest.skipUnless(reference.DEFAULT_DATABASE.is_file(), "local reference is not built")
class LocalReferenceIntegrationTests(unittest.TestCase):
    def test_doctor_authenticates_local_artifacts(self) -> None:
        args = argparse.Namespace(
            source=reference.DEFAULT_SOURCE,
            database=reference.DEFAULT_DATABASE,
            manifest=reference.DEFAULT_MANIFEST,
        )
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(reference.doctor(args), 0)

    def test_expected_structural_counts(self) -> None:
        with reference.open_database(reference.DEFAULT_DATABASE) as connection:
            counts = dict(connection.execute("SELECT key, value FROM metadata"))
            self.assertEqual(counts["physical_pages"], str(reference.EXPECTED_PAGES))
            self.assertEqual(counts["rules"], str(len(reference.EXPECTED_RULE_IDS)))
            self.assertEqual(counts["guidance"], str(len(reference.EXPECTED_GUIDANCE_IDS)))
            self.assertEqual(
                counts["dictionary_entries"],
                str(reference.EXPECTED_DICTIONARY_ENTRIES),
            )

    def test_source_hash_matches_database_metadata(self) -> None:
        if not reference.DEFAULT_SOURCE.is_file():
            self.skipTest("local source PDF is absent")
        actual = reference.sha256_file(reference.DEFAULT_SOURCE)
        with reference.open_database(reference.DEFAULT_DATABASE) as connection:
            expected = connection.execute(
                "SELECT value FROM metadata WHERE key = 'source_sha256'"
            ).fetchone()[0]
        self.assertEqual(actual, expected)
        self.assertEqual(actual, reference.EXPECTED_SOURCE_SHA256)


if __name__ == "__main__":
    unittest.main()
