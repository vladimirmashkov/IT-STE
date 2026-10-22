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
        self.assertEqual(
            [source_id for source_id in target["source_block_ids"] if source_id.startswith("2.")],
            ["2.1", "2.2"],
        )
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

    def test_section_four_decisions_create_sentence_targets(self) -> None:
        records = adaptation.load_jsonl(adaptation.PLAN_MAP)
        section = [
            record for record in records if record["source"]["block_id"].startswith("4.")
        ]
        self.assertEqual(len(section), 5)
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
                "ITSTE-R-0010": {"4.1"},
                "ITSTE-R-0011": {"4.2", "4.5"},
                "ITSTE-R-0012": {"4.3"},
                "ITSTE-R-0013": {"4.4"},
            },
        )
        targets = {
            target["id"]: target
            for target in adaptation.load_json(adaptation.PLAN_TARGETS)["targets"]
        }
        self.assertEqual(
            targets["ITSTE-R-0011"]["source_block_ids"],
            ["4.2", "4.5"],
        )
        clarity_intent = targets["ITSTE-R-0011"]["design_intent"]
        for required_clause in (
            "An imperative can keep its understood reader subject",
            "a sentence does not need an object when its verb or meaning does not require one",
            "Use articles and demonstratives where standard English and the intended specificity require them",
            "Spell out contractions",
            "Permit conventional fragments",
            "Preserve quotations, externally controlled strings, and machine-significant text exactly",
        ):
            self.assertIn(required_clause, clarity_intent)
        self.assertEqual(
            targets["ITSTE-R-0012"]["working_title"],
            "Use parallel lists for complex content",
        )
        list_intent = targets["ITSTE-R-0012"]["design_intent"]
        for required_clause in (
            "make every item connect grammatically to its lead-in",
            "keep items parallel",
            "use an ordered list only when sequence or priority matters",
            "Follow the governing output format or style guide",
        ):
            self.assertIn(required_clause, list_intent)
        self.assertTrue(
            all(targets[target_id]["status"] == "planned" for target_id in groups)
        )

    def test_section_five_decisions_create_procedure_targets(self) -> None:
        records = adaptation.load_jsonl(adaptation.PLAN_MAP)
        section = [
            record for record in records if record["source"]["block_id"].startswith("5.")
        ]
        self.assertEqual(len(section), 5)
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
                "ITSTE-R-0010": {"5.1"},
                "ITSTE-R-0014": {"5.2"},
                "ITSTE-R-0015": {"5.3"},
                "ITSTE-R-0016": {"5.4"},
                "ITSTE-R-0017": {"5.5"},
            },
        )
        targets = {
            target["id"]: target
            for target in adaptation.load_json(adaptation.PLAN_TARGETS)["targets"]
        }
        self.assertTrue(
            {"4.1", "5.1"}.issubset(
                set(targets["ITSTE-R-0010"]["source_block_ids"])
            )
        )
        sentence_intent = targets["ITSTE-R-0010"]["design_intent"]
        self.assertIn("Do not impose one universal word limit", sentence_intent)
        self.assertIn(
            "a content profile can define and validate a local limit",
            sentence_intent,
        )
        required_clauses = {
            "ITSTE-R-0014": (
                "each independently executable action in a separate procedural step",
                "simultaneous, atomic, conventionally inseparable, or immediately coupled to a required result or verification",
                "Preserve an intentional transaction boundary",
            ),
            "ITSTE-R-0015": (
                "reader as the understood subject",
                "Name the actor explicitly when a system",
                "Do not add must to an imperative only for emphasis",
            ),
            "ITSTE-R-0016": (
                "before the action that depends on it",
                "make the condition's scope unambiguous",
                "use separate sentences, a list, or an explicit control-flow structure",
            ),
            "ITSTE-R-0017": (
                "Use a note only for supplemental information",
                "required actions, prerequisites, limits, acceptance criteria, expected results",
                "safety- or security-critical information in the main flow",
                "warnings, cautions, requirements, and other semantic blocks their correct labels",
                "complete and executable when its notes are hidden or skipped",
            ),
        }
        for target_id, clauses in required_clauses.items():
            intent = targets[target_id]["design_intent"]
            for clause in clauses:
                self.assertIn(clause, intent)

    def test_section_six_decisions_create_description_targets(self) -> None:
        records = adaptation.load_jsonl(adaptation.PLAN_MAP)
        section = [
            record for record in records if record["source"]["block_id"].startswith("6.")
        ]
        self.assertEqual(len(section), 6)
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
                "ITSTE-R-0018": {"6.1"},
                "ITSTE-R-0013": {"6.2"},
                "ITSTE-R-0010": {"6.3"},
                "ITSTE-R-0019": {"6.4", "6.5", "6.6"},
            },
        )
        targets = {
            target["id"]: target
            for target in adaptation.load_json(adaptation.PLAN_TARGETS)["targets"]
        }
        self.assertEqual(
            targets["ITSTE-R-0010"]["source_block_ids"],
            ["4.1", "5.1", "6.3"],
        )
        self.assertEqual(
            targets["ITSTE-R-0013"]["source_block_ids"],
            ["4.4", "6.2"],
        )
        self.assertEqual(
            targets["ITSTE-R-0019"]["source_block_ids"],
            ["6.4", "6.5", "6.6"],
        )
        required_clauses = {
            "ITSTE-R-0010": (
                "Do not impose one universal word limit across procedural or descriptive IT content",
                "a content profile can define and validate a local limit",
            ),
            "ITSTE-R-0013": (
                "Reuse the same canonical key terms as anchors",
                "Do not replace a term with a synonym merely for variety",
                "do not add a connector or mechanical repetition",
            ),
            "ITSTE-R-0018": (
                "Present purpose, scope, prerequisites, and core concepts before details",
                "expose optional detail progressively",
                "each independently retrievable section, help topic, or LLM chunk enough local context",
                "Keep one principal subject in each sentence when possible",
                "when multiple subjects are necessary, state their relationship explicitly",
                "consistently with ITSTE-R-0010",
            ),
            "ITSTE-R-0019": (
                "keep one primary topic in that block",
                "when the topic, reader task, retrieval boundary, or level of detail changes",
                "Do not impose a universal six-sentence maximum",
                "constrained formats can provide equivalent topic boundaries without conventional paragraphs",
            ),
        }
        for target_id, clauses in required_clauses.items():
            intent = targets[target_id]["design_intent"]
            for clause in clauses:
                self.assertIn(clause, intent)

    def test_section_seven_decisions_create_risk_targets(self) -> None:
        records = adaptation.load_jsonl(adaptation.PLAN_MAP)
        section = [
            record for record in records if record["source"]["block_id"].startswith("7.")
        ]
        expected = {
            "7.1": "ITSTE-R-0020",
            "7.2": "ITSTE-R-0021",
            "7.3": "ITSTE-R-0022",
        }
        self.assertEqual(len(section), 3)
        targets = {
            target["id"]: target
            for target in adaptation.load_json(adaptation.PLAN_TARGETS)["targets"]
        }
        for record in section:
            source_id = record["source"]["block_id"]
            target_id = expected[source_id]
            self.assertEqual(record["assessment"]["status"], "reviewed")
            self.assertEqual(record["assessment"]["applicability"], "adapt")
            self.assertEqual(record["assessment"]["adaptation_action"], "create-rule")
            self.assertEqual(record["target_rule_ids"], [target_id])
            self.assertEqual(targets[target_id]["source_block_ids"], [source_id])
            self.assertEqual(targets[target_id]["status"], "planned")
        required_clauses = {
            "ITSTE-R-0020": (
                "actual risk assessment and the governing classification policy",
                "physical harm, data loss, security compromise, and service disruption",
                "do not downgrade a more serious risk",
                "Do not impose the aviation warning/caution distinction as a universal IT scale",
                "without a documented mapping",
                "rather than relying only on color or a symbol",
            ),
            "ITSTE-R-0021": (
                "After the risk label",
                "condition that the reader must evaluate first",
                "State the required action explicitly",
                "Place the instruction before the hazardous operation",
                "independently retrieved procedural content",
                "do not hide required precautions in notes",
            ),
            "ITSTE-R-0022": (
                "When a credible consequence is known and can be disclosed",
                "Distinguish possible consequences from certain outcomes",
                "do not invent causes, probabilities, or guarantees",
                "without exposing secrets or unnecessary exploit details",
                "An explanation does not replace the protective action",
            ),
        }
        for target_id, clauses in required_clauses.items():
            for clause in clauses:
                self.assertIn(clause, targets[target_id]["design_intent"])

    def test_section_eight_decisions_create_punctuation_and_metric_targets(self) -> None:
        records = adaptation.load_jsonl(adaptation.PLAN_MAP)
        section = [
            record for record in records if record["source"]["block_id"].startswith("8.")
        ]
        self.assertEqual(len(section), 7)
        self.assertEqual(
            {record["assessment"]["status"] for record in section}, {"reviewed"}
        )
        self.assertEqual(
            {record["assessment"]["applicability"] for record in section}, {"adapt"}
        )
        groups: dict[str, set[str]] = {}
        for record in section:
            for target_id in record["target_rule_ids"]:
                groups.setdefault(target_id, set()).add(record["source"]["block_id"])
        self.assertEqual(
            groups,
            {
                "ITSTE-R-0023": {"8.1"},
                "ITSTE-R-0006": {"8.2"},
                "ITSTE-R-0024": {"8.3"},
                "ITSTE-R-0025": {"8.4", "8.5", "8.6", "8.7"},
            },
        )
        targets = {
            target["id"]: target
            for target in adaptation.load_json(adaptation.PLAN_TARGETS)["targets"]
        }
        self.assertEqual(
            targets["ITSTE-R-0006"]["source_block_ids"], ["2.1", "2.2", "8.2"]
        )
        self.assertEqual(
            targets["ITSTE-R-0025"]["source_block_ids"], ["8.4", "8.5", "8.6", "8.7"]
        )
        self.assertTrue(all(targets[target_id]["status"] == "planned" for target_id in groups))
        required_clauses = {
            "ITSTE-R-0006": (
                "distinguish hyphens from dashes",
                "never substitute typographic dashes for syntax-controlled characters",
                "Do not impose an absolute three-word limit or add hyphens to evade a length limit",
            ),
            "ITSTE-R-0023": (
                "Prefer separate sentences or steps to complex semicolon constructions",
                "do not impose a universal ban on semicolons",
                "prose guidance must not change executable meaning",
            ),
            "ITSTE-R-0024": (
                "State required conditions, limits, and branch-selection criteria explicitly in the main instruction",
                "expand ambiguous parenthetical alternatives into explicit choices",
                "Preserve parentheses and other delimiters in literal commands",
            ),
            "ITSTE-R-0025": (
                "If a content profile applies length limits",
                "define a reproducible measurement method, its version, and its scope",
                "a colon in IT syntax is not automatically a sentence boundary",
                "Do not automatically count arbitrary parenthetical or quoted passages as one word",
                "Distinguish words, characters, and LLM tokens",
                "token budgets must identify the tokenizer and its version",
                "do not alter spelling, hyphenation, or document structure merely to game the metric",
                "No universal ASD counting convention or 20/25-word limit is imposed",
            ),
        }
        for target_id, clauses in required_clauses.items():
            for clause in clauses:
                self.assertIn(clause, targets[target_id]["design_intent"])

    def test_heading_only_candidates_are_non_normative(self) -> None:
        self.assertEqual(
            adaptation.candidate_domains("5.2"),
            ["general", "procedures-runbooks", "cli", "user-interface"],
        )
        manifest = adaptation.load_json(adaptation.PLAN_MANIFEST)
        self.assertFalse(manifest["method"]["candidate_domains_are_normative"])
        self.assertFalse(manifest["method"]["full_source_text_loaded"])
        self.assertEqual(
            manifest["method"]["classification_basis"],
            "initial candidates from authenticated source headings and physical page ranges; reviewed decisions from bounded source-text retrieval and editorial IT applicability assessment",
        )


if __name__ == "__main__":
    unittest.main()
