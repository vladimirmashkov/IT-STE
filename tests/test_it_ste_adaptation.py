# SPDX-License-Identifier: GPL-3.0-only

import contextlib
import copy
import io
import unittest
from unittest import mock

from tools import it_ste_adaptation as adaptation


class AdaptationPlanTests(unittest.TestCase):
    def test_plan_authenticates_and_validates(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            adaptation.check()

    def test_map_covers_every_source_block_once(self) -> None:
        records = adaptation.load_jsonl(adaptation.PLAN_MAP)
        counts = adaptation.validate_records(records)
        self.assertEqual(counts["source_rules"], 53)
        self.assertEqual(counts["source_guidance"], 8)
        self.assertEqual(counts["source_blocks"], 61)

    def test_domain_registry_is_stable_and_attributed(self) -> None:
        registry = adaptation.load_json(adaptation.DOMAINS)
        identifiers = adaptation.domain_ids()
        self.assertEqual(len(identifiers), 18)
        self.assertEqual(registry["primary_language"], "en")
        self.assertEqual(
            registry["rights"]["attribution"]["url"],
            adaptation.PROJECT_URL,
        )

    def test_source_and_project_attribution_are_separate(self) -> None:
        manifest = adaptation.load_json(adaptation.PLAN_MANIFEST)
        self.assertEqual(
            manifest["source"]["owner"]["name"],
            "Aerospace, Security and Defence Industries Association of Europe (ASD)",
        )
        self.assertEqual(manifest["attribution"]["url"], adaptation.PROJECT_URL)
        self.assertIn("permission_record_sha256", manifest["source"])

    def test_init_never_overwrites_the_existing_plan(self) -> None:
        with self.assertRaises(adaptation.PlanError):
            adaptation.initialize()

    def test_forged_source_hash_is_rejected(self) -> None:
        forged = adaptation.load_json(adaptation.SOURCE_MANIFEST)
        forged["source_sha256"] = "0" * 64
        with (
            mock.patch.object(adaptation, "load_json", return_value=forged),
            self.assertRaises(adaptation.PlanError),
        ):
            adaptation.authenticate_source()

    def test_forged_permission_provenance_is_rejected(self) -> None:
        forged = adaptation.load_json(adaptation.SOURCE_MANIFEST)
        forged["permission_record"] = "forged.md"
        forged["permission_record_sha256"] = "0" * 64
        with (
            mock.patch.object(adaptation, "load_json", return_value=forged),
            self.assertRaises(adaptation.PlanError),
        ):
            adaptation.authenticate_source()

    def test_reviewed_decisions_must_be_coherent(self) -> None:
        records = adaptation.load_jsonl(adaptation.PLAN_MAP)
        records[0] = copy.deepcopy(records[0])
        records[0]["assessment"]["status"] = "reviewed"
        records[0]["assessment"]["rationale"] = "Synthetic reviewed rationale."
        with self.assertRaises(adaptation.PlanError):
            adaptation.validate_records(records)

    def test_merge_can_share_one_target_id(self) -> None:
        records = adaptation.load_jsonl(adaptation.PLAN_MAP)
        for index in (0, 1):
            records[index] = copy.deepcopy(records[index])
            records[index]["assessment"].update(
                {
                    "status": "reviewed",
                    "applicability": "merge",
                    "adaptation_action": "merge-into-rule",
                    "rationale": "Synthetic many-to-one merge rationale.",
                }
            )
            records[index]["target_rule_ids"] = ["ITSTE-R-0001"]
        counts = adaptation.validate_records(records)
        self.assertEqual(counts["assessment_reviewed"], 2)

    def test_target_rule_id_format_is_exact(self) -> None:
        records = adaptation.load_jsonl(adaptation.PLAN_MAP)
        records[0] = copy.deepcopy(records[0])
        records[0]["assessment"].update(
            {
                "status": "in-review",
                "applicability": "adapt",
                "adaptation_action": "create-rule",
            }
        )
        records[0]["target_rule_ids"] = ["ITSTE-R-invalid"]
        with self.assertRaises(adaptation.PlanError):
            adaptation.validate_records(records)

    def test_heading_only_candidates_are_non_normative(self) -> None:
        self.assertEqual(
            adaptation.candidate_domains("5.2"),
            ["general", "procedures-runbooks", "cli", "user-interface"],
        )
        manifest = adaptation.load_json(adaptation.PLAN_MANIFEST)
        self.assertFalse(manifest["method"]["candidate_domains_are_normative"])
        self.assertFalse(manifest["method"]["full_source_text_loaded"])


if __name__ == "__main__":
    unittest.main()
