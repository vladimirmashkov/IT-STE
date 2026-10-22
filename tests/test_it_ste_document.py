# SPDX-License-Identifier: GPL-3.0-only
"""Derived-document tests; all build writes use isolated temporary repositories."""

import contextlib
import copy
import hashlib
import io
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from tools import it_ste_document as document


class RenderingTests(unittest.TestCase):
    def test_real_snapshot_is_deterministic_and_complete(self):
        first = document.render()
        self.assertEqual(first, document.render())
        text = first.decode("utf-8")
        for number in range(1, 32):
            identifier = f"ITSTE-R-{number:04d}"
            self.assertIn(f"\n## {identifier}\n", text)
            self.assertIn(f"[{identifier}](#{identifier.lower()})", text)
        self.assertEqual(text.count("\n## ITSTE-R-"), 31)
        self.assertEqual(text.count("\n### D-P"), 40)
        for expected in ("DRAFT", "not a release", "NOT an approved", "2156 pending",
                         "needs-review", "physical_pdf_pages", "source_facet", "target_field",
                         "CC BY-SA 4.0", "downstream source license is unknown", "DO NOT EDIT"):
            self.assertIn(expected, text)
        batch = document.corpus.load_json(document.ROOT / document.DEFAULT_BATCH)
        self.assertEqual(sum(item["it_disposition"] == "needs-review"
                             for item in batch["decisions"]), 6)
        for item in batch["decisions"]:
            self.assertIn(item["entry_id"], text)
        manifest_path = document.ROOT / document.corpus.DEFAULT_MANIFEST
        manifest = document.corpus.load_json(manifest_path)
        for name in manifest["records"] + manifest["sources"]:
            path = manifest_path.parent / name
            self.assertIn(hashlib.sha256(path.read_bytes()).hexdigest(), text)

    def test_segments_join_without_invented_spaces(self):
        self.assertEqual(document.example([
            {"kind": "prose", "text": "Run "},
            {"kind": "literal", "text": "a_b"},
            {"kind": "prose", "text": "."},
        ]), "Run `a_b`\\.")

    def test_arbitrary_markdown_and_html_are_not_active(self):
        value = "[x](https://bad) <script> & *word* # title"
        shown = document.escaped(value)
        for punctuation in "[]()<>*&":
            self.assertIn("\\" + punctuation, shown)

    def test_multiline_backticks_are_lossless_and_cannot_close_fence(self):
        segments = [{"kind": "prose", "text": "Run "},
                    {"kind": "literal", "text": "```\nx`y\n````\n"},
                    {"kind": "prose", "text": " now."}]
        rendered = document.example(segments)
        self.assertEqual(rendered, "`````\nRun ```\nx`y\n````\n now.\n`````")
        self.assertEqual(document.example([{"kind": "literal", "text": " x "}]),
                         "```\n x \n```")

    def test_both_validators_gate_rendering(self):
        vocabulary = SimpleNamespace(check=mock.Mock(side_effect=RuntimeError("forged batch source")))
        with (
            mock.patch.object(document.importlib, "import_module", return_value=vocabulary),
            mock.patch.object(document.corpus, "check", return_value=31) as corpus_check,
            self.assertRaisesRegex(RuntimeError, "forged batch source"),
        ):
            document.render()
        corpus_check.assert_called_once_with()
        vocabulary.check.assert_called_once_with(path=document.DEFAULT_BATCH)
        with (
            mock.patch.object(document.importlib, "import_module", return_value=vocabulary),
            mock.patch.object(document.corpus, "check", side_effect=RuntimeError("forged rule source")),
            self.assertRaisesRegex(RuntimeError, "forged rule source"),
        ):
            document.render()

    def test_actual_forged_source_is_rejected(self):
        original = document.corpus.load_json

        def forged(path):
            data = copy.deepcopy(original(path))
            if Path(path).name == "ASDSTE-SOURCE-ISSUE9-R0001.json":
                data["artifact_sha256"] = "0" * 64
            return data

        with (
            mock.patch.object(document.corpus, "load_json", side_effect=forged),
            self.assertRaises(document.corpus.CorpusError),
        ):
            document.render()


class OutputTests(unittest.TestCase):
    def setUp(self):
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.root = Path(self.stack.enter_context(tempfile.TemporaryDirectory()))
        (self.root / "docs").mkdir()
        self.path = self.root / document.DEFAULT_OUTPUT
        self.stack.enter_context(mock.patch.object(document, "ROOT", self.root))
        self.data = (document.BANNER + "\nDRAFT fixture\n").encode("utf-8")
        self.render = self.stack.enter_context(mock.patch.object(document, "render", return_value=self.data))

    def test_build_and_exact_check(self):
        document.build()
        self.assertEqual(self.path.read_bytes(), self.data)
        with mock.patch.object(Path, "write_bytes", side_effect=AssertionError("check wrote bytes")):
            document.check()
            self.path.write_text("hand edit", encoding="utf-8")
            with self.assertRaisesRegex(document.DocumentError, "stale"):
                document.check()
        self.assertEqual(self.path.read_text(), "hand edit")
        with self.assertRaisesRegex(document.DocumentError, "unrelated"):
            document.build()

    def test_missing_check_does_not_create_output(self):
        with self.assertRaisesRegex(document.DocumentError, "missing"):
            document.check()
        self.assertFalse(self.path.exists())

    def test_newline_change_is_stale(self):
        document.build()
        changed = self.data.replace(b"\n", b"\r\n")
        self.path.write_bytes(changed)
        with self.assertRaises(document.DocumentError):
            document.check()
        self.assertEqual(self.path.read_bytes(), changed)

    def test_no_arbitrary_outputs_or_source_overwrites(self):
        for value in ("../escape.md", "docs/other.md", "tools/it_ste_document.py",
                      str(document.DEFAULT_BATCH), "docs/../docs/IT-STE-draft.md"):
            with self.subTest(value=value), self.assertRaises(document.DocumentError):
                document.build(value)
        self.assertFalse(self.path.exists())

    def test_symlink_file_and_parent_are_refused(self):
        other = self.root / "other.md"
        other.write_text("preserve", encoding="utf-8")
        self.path.symlink_to(other)
        with self.assertRaises(document.DocumentError):
            document.build()
        self.path.unlink()
        (self.root / "docs").rmdir()
        (self.root / "actual-docs").mkdir()
        (self.root / "docs").symlink_to(self.root / "actual-docs", target_is_directory=True)
        with self.assertRaises(document.DocumentError):
            document.check()
        self.assertEqual(other.read_text(), "preserve")

    def test_cli_errors_do_not_write(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(document.main(["check"]), 2)
            self.assertEqual(document.main(["build", "--output", "docs/unrelated.md"]), 2)
        self.assertFalse(self.path.exists())


if __name__ == "__main__":
    unittest.main()
