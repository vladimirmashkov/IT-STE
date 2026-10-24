# SPDX-License-Identifier: GPL-3.0-only
"""Derived-document tests; all build writes use isolated temporary repositories."""

import contextlib
import copy
import hashlib
import io
import json
import re
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from tools import it_ste_document as document
from tools import it_ste_vocabulary as vocabulary


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
        for identifier in ("ITSTE-T-0001", "ITSTE-T-0002", "ITSTE-T-0003", "ITSTE-T-0004"):
            self.assertIn(f"{identifier}", text)
        self.assertIn("Canonical draft terms", text)
        for example in (
            "The service provides status information for the payment queue.",
            "The monitoring alert identifies a queue depth above 500 jobs.",
            "The problem caused repeated timeouts in the payment service.",
            "The incident reduced payment-service response quality for new orders.",
        ):
            self.assertIn(document.escaped(example), text)
        batches, summary = vocabulary.checked_all()
        entries = [item["entry_id"] for batch in batches for item in batch["decisions"]]
        self.assertEqual(re.findall(r"^### (D-P\d+-\d+)$", text, re.MULTILINE), entries)
        self.assertIn(f"First {summary['candidates']} source rows across "
                      f"{summary['batch_count']} batches; {summary['remaining']} pending "
                      f"of {summary['total']} source rows.", text)
        self.assertIn(document.metadata(summary), text)
        for expected in ("DRAFT", "not a release", "NOT an approved",
                         "needs-review", "physical_pdf_pages", "source_facet", "target_field",
                         "CC BY-SA 4.0", "downstream source license is unknown", "DO NOT EDIT"):
            self.assertIn(expected, text)
        batch = document.corpus.load_json(document.ROOT / document.DEFAULT_BATCH)
        self.assertEqual(len(batch["decisions"]), 40)
        self.assertEqual(batch["decisions"][0]["entry_id"], "D-P149-001")
        self.assertEqual(sum(item["it_disposition"] == "needs-review"
                             for item in batch["decisions"]), 0)
        self.assertEqual(sum(item["evidence"]["pdf_layout_check"]["visual_verification_performed"]
                             for item in batch["decisions"]), 6)
        for item in batch["decisions"]:
            self.assertIn(item["entry_id"], text)
        for batch in batches:
            self.assertIn(document.metadata(batch["interpretation"]), text)
            self.assertIn(document.metadata({k: v for k, v in batch.items()
                                            if k not in ("decisions", "interpretation")}), text)
            path = document.ROOT / vocabulary.DEFAULT_BATCH.parent / f"batch-{batch['batch_id']}.json"
            self.assertIn(f"- `{path.relative_to(document.ROOT).as_posix()}` SHA-256: "
                          f"`{hashlib.sha256(path.read_bytes()).hexdigest()}`", text)
        manifest_path = document.ROOT / document.corpus.DEFAULT_MANIFEST
        manifest = document.corpus.load_json(manifest_path)
        for name in manifest["records"] + manifest["sources"]:
            path = manifest_path.parent / name
            self.assertIn(hashlib.sha256(path.read_bytes()).hexdigest(), text)

    def test_all_validated_entries_render_once_including_later_batches(self):
        batches, summary = copy.deepcopy(vocabulary.checked_all())
        batches = batches[:1]
        summary.update(candidates=40, remaining=summary["total"] - 40, batch_count=1,
                       dispositions=vocabulary.check()["dispositions"])
        later = copy.deepcopy(batches[-1])
        later["batch_id"] = f"{len(batches) + 1:03d}"
        decision = copy.deepcopy(later["decisions"][0])
        decision.update(entry_id="D-P999-001", sequence_number=summary["candidates"] + 1,
                        headword="later <term> *candidate*", it_disposition="needs-review")
        later["decisions"] = [decision]
        later["interpretation"]["examples"] = "Later batch examples are not blanket approvals."
        later["sequence"].update(first_entry_id=decision["entry_id"],
                                  last_entry_id=decision["entry_id"], entry_count=1,
                                  remaining=summary["remaining"] - 1)
        batches.append(later)
        summary.update(candidates=summary["candidates"] + 1,
                       remaining=summary["remaining"] - 1, batch_count=len(batches))
        summary["dispositions"]["needs-review"] = summary["dispositions"].get("needs-review", 0) + 1
        entries = [item["entry_id"] for batch in batches for item in batch["decisions"]]
        # Mock the validated API, not batch discovery: later editorial data need
        # not exist yet, and rendering must use the returned objects unchanged.
        with tempfile.TemporaryDirectory(dir=document.ROOT) as directory:
            paths = []
            for batch in batches:
                path = Path(directory) / f"batch-{batch['batch_id']}.json"
                path.write_text(json.dumps(batch, ensure_ascii=False) + "\n", encoding="utf-8")
                paths.append(path)
            with (
                mock.patch.object(vocabulary, "DEFAULT_BATCH", paths[0]),
                mock.patch.object(vocabulary, "checked_all", return_value=(batches, summary)) as checked,
            ):
                data = document.render()
                self.assertEqual(data, document.render())
            self.assertEqual(checked.call_count, 2)
            text = data.decode("utf-8")
            self.assertEqual(re.findall(r"^### (D-P\d+-\d+)$", text, re.MULTILINE), entries)
            self.assertIn(document.escaped(decision["headword"]), text)
            self.assertIn(document.metadata(summary), text)
            self.assertIn(f"{summary['remaining']} pending of {summary['total']} source rows.", text)
            self.assertIn("NOT an approved allowed/prohibited dictionary", text)
            self.assertIn(document.metadata(later["interpretation"]), text)
            for batch, path in zip(batches, paths):
                self.assertIn(document.metadata({k: v for k, v in batch.items()
                                                if k not in ("decisions", "interpretation")}), text)
                self.assertEqual(text.count(
                    f"- `{path.relative_to(document.ROOT).as_posix()}` SHA-256: "
                    f"`{hashlib.sha256(path.read_bytes()).hexdigest()}`"), 1)

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
        vocabulary = SimpleNamespace(checked_all=mock.Mock(side_effect=RuntimeError("forged batch source")))
        with (
            mock.patch.object(document.importlib, "import_module", return_value=vocabulary),
            mock.patch.object(document.corpus, "check", return_value=31) as corpus_check,
            self.assertRaisesRegex(RuntimeError, "forged batch source"),
        ):
            document.render()
        corpus_check.assert_called_once_with()
        vocabulary.checked_all.assert_called_once_with()
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
