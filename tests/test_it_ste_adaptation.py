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
        records = adaptation.initial_records()
        records[0] = copy.deepcopy(records[0])
        records[0]["assessment"]["status"] = "reviewed"
        records[0]["assessment"]["rationale"] = "Synthetic reviewed rationale."
        with self.assertRaises(adaptation.PlanError):
            adaptation.validate_records(records)

    def test_merge_can_share_one_target_id(self) -> None:
        records = adaptation.initial_records()
        for index in (0, 1):
            records[index] = copy.deepcopy(records[index])
            records[index]["assessment"].update(
                {
                    "status": "reviewed",
                    "applicability": "adapt",
                    "adaptation_action": "merge-into-rule",
                    "rationale": "Synthetic many-to-one merge rationale.",
                }
            )
            records[index]["target_rule_ids"] = ["ITSTE-R-0001"]
        counts = adaptation.validate_records(records)
        self.assertEqual(counts["assessment_reviewed"], 2)

    def test_unreviewed_decision_cannot_allocate_a_target(self) -> None:
        records = adaptation.initial_records()
        records[0] = copy.deepcopy(records[0])
        records[0]["assessment"].update(
            {
                "status": "unreviewed",
                "applicability": "adapt",
                "adaptation_action": "create-rule",
            }
        )
        records[0]["target_rule_ids"] = ["ITSTE-R-9999"]
        with self.assertRaises(adaptation.PlanError):
            adaptation.validate_records(records)

    def test_unrelated_target_domain_is_rejected(self) -> None:
        records = adaptation.load_jsonl(adaptation.PLAN_MAP)
        registry = adaptation.load_json(adaptation.PLAN_TARGETS)
        registry = copy.deepcopy(registry)
        registry["targets"][0]["candidate_domains"] = ["ai-automation"]
        original_load_json = adaptation.load_json

        def patched_load_json(path):
            if path == adaptation.PLAN_TARGETS:
                return registry
            return original_load_json(path)

        with (
            mock.patch.object(adaptation, "load_json", side_effect=patched_load_json),
            self.assertRaises(adaptation.PlanError),
        ):
            adaptation.validate_targets(records)

    def test_target_rule_id_format_is_exact(self) -> None:
        records = adaptation.initial_records()
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

    def test_section_one_decisions_map_to_five_targets(self) -> None:
        records = adaptation.load_jsonl(adaptation.PLAN_MAP)
        section = [
            record for record in records if record["source"]["block_id"].startswith("1.")
        ]
        self.assertEqual(len(section), 14)
        self.assertEqual(
            {record["assessment"]["status"] for record in section},
            {"reviewed"},
        )
        groups: dict[str, set[str]] = {}
        for record in section:
            for target in record["target_rule_ids"]:
                groups.setdefault(target, set()).add(record["source"]["block_id"])
        self.assertEqual(
            groups,
            {
                "ITSTE-R-0001": {"1.1", "1.5", "1.6", "1.12"},
                "ITSTE-R-0002": {"1.2", "1.3", "1.4", "1.7", "1.13"},
                "ITSTE-R-0003": {"1.8", "1.11"},
                "ITSTE-R-0004": {"1.9", "1.10"},
                "ITSTE-R-0005": {"1.14"},
            },
        )
        targets = adaptation.load_json(adaptation.PLAN_TARGETS)
        section_source_ids = {
            record["source"]["block_id"] for record in section
        }
        target_groups = {
            target["id"]: set(target["source_block_ids"]) & section_source_ids
            for target in targets["targets"]
            if target["id"] in groups
        }
        self.assertEqual(target_groups, groups)
        self.assertTrue(all("normative_record" not in target for target in targets["targets"]))

    def test_section_two_decisions_create_multi_word_term_target(self) -> None:
        records = adaptation.load_jsonl(adaptation.PLAN_MAP)
        section = [
            record for record in records if record["source"]["block_id"].startswith("2.")
        ]
        self.assertEqual(len(section), 2)
        self.assertEqual(
            {record["assessment"]["status"] for record in section},
            {"reviewed"},
        )
        self.assertEqual(
            {target for record in section for target in record["target_rule_ids"]},
            {"ITSTE-R-0006"},
        )
        targets = adaptation.load_json(adaptation.PLAN_TARGETS)["targets"]
        target = next(item for item in targets if item["id"] == "ITSTE-R-0006")
        self.assertEqual(target["source_block_ids"], ["2.1", "2.2"])
        self.assertEqual(target["working_title"], "Clarify multi-word technical terms")

    def test_section_three_decisions_create_verb_targets(self) -> None:
        records = adaptation.load_jsonl(adaptation.PLAN_MAP)
        section = [
            record for record in records if record["source"]["block_id"].startswith("3.")
        ]
        self.assertEqual(len(section), 7)
        self.assertEqual(
            {record["assessment"]["status"] for record in section},
            {"reviewed"},
        )
        groups: dict[str, set[str]] = {}
        for record in section:
            for target in record["target_rule_ids"]:
                groups.setdefault(target, set()).add(record["source"]["block_id"])
        self.assertEqual(
            groups,
            {
                "ITSTE-R-0002": {"3.1"},
                "ITSTE-R-0007": {"3.2", "3.3", "3.4", "3.5"},
                "ITSTE-R-0008": {"3.6"},
                "ITSTE-R-0009": {"3.7"},
            },
        )
        targets = {
            target["id"]: target
            for target in adaptation.load_json(adaptation.PLAN_TARGETS)["targets"]
        }
        self.assertIn("3.1", targets["ITSTE-R-0002"]["source_block_ids"])
        self.assertEqual(
            targets["ITSTE-R-0007"]["source_block_ids"],
            ["3.2", "3.3", "3.4", "3.5"],
        )
        self.assertEqual(
            targets["ITSTE-R-0008"]["working_title"],
            "Prefer active voice and name the actor",
        )
        self.assertEqual(
            targets["ITSTE-R-0009"]["working_title"],
            "Use direct verbs for actions",
        )

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
