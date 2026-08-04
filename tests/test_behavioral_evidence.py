import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_behavioral_evidence.py"
SPEC = importlib.util.spec_from_file_location("validate_behavioral_evidence", VALIDATOR)
VALIDATOR_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR_MODULE)


def campaign_inputs(campaign):
    cases = VALIDATOR_MODULE.bundle_cases(VALIDATOR_MODULE.BUNDLE)
    scores = VALIDATOR_MODULE.load_json(VALIDATOR_MODULE.BUNDLE / campaign["scores"])
    responses = VALIDATOR_MODULE.read_responses(
        VALIDATOR_MODULE.BUNDLE / campaign["responses"], cases
    )
    return cases, scores, responses


class ReviewLedgerEvidenceTests(unittest.TestCase):
    def test_retained_ledgers_have_explicit_evidence_for_every_verdict(self):
        manifest = json.loads(VALIDATOR_MODULE.MANIFEST.read_text(encoding="utf-8"))
        for campaign in manifest["campaigns"]:
            cases, scores, responses = campaign_inputs(campaign)
            ledger = VALIDATOR_MODULE.BUNDLE / campaign["review_ledger"]
            with self.subTest(campaign=campaign["id"]):
                VALIDATOR_MODULE.validate_ledger(ledger, cases, scores, responses)

    def test_quoted_evidence_absent_from_the_response_is_rejected(self):
        manifest = json.loads(VALIDATOR_MODULE.MANIFEST.read_text(encoding="utf-8"))
        campaign = manifest["campaigns"][0]
        cases, scores, responses = campaign_inputs(campaign)
        ledger = VALIDATOR_MODULE.load_json(
            VALIDATOR_MODULE.BUNDLE / campaign["review_ledger"]
        )
        ledger["cases"][0]["must_pass"][0]["evidence_quote"] = (
            "the agent explicitly confirmed this criterion"
        )
        with tempfile.TemporaryDirectory(dir=ROOT, prefix=".evidence-test-") as tmp:
            path = Path(tmp) / "review-ledger.json"
            path.write_text(json.dumps(ledger), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "not in the retained response"):
                VALIDATOR_MODULE.validate_ledger(path, cases, scores, responses)

    def test_blank_evidence_is_rejected_even_when_rationale_remains(self):
        manifest = json.loads(VALIDATOR_MODULE.MANIFEST.read_text(encoding="utf-8"))
        campaign = manifest["campaigns"][0]
        cases, scores, responses = campaign_inputs(campaign)
        ledger = VALIDATOR_MODULE.load_json(
            VALIDATOR_MODULE.BUNDLE / campaign["review_ledger"]
        )
        ledger["cases"][0]["must_pass"][0]["evidence_quote"] = ""
        with tempfile.TemporaryDirectory(dir=ROOT, prefix=".evidence-test-") as tmp:
            path = Path(tmp) / "review-ledger.json"
            path.write_text(json.dumps(ledger), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "empty evidence"):
                VALIDATOR_MODULE.validate_ledger(path, cases, scores, responses)


class HumanReviewBoundaryTests(unittest.TestCase):
    def test_a_non_boolean_boundary_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "must be recorded as a boolean"):
            VALIDATOR_MODULE.check_human_review({"independent_human_review": "yes"}, "x")

    def test_claimed_review_without_a_record_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "without a review record"):
            VALIDATOR_MODULE.check_human_review({"independent_human_review": True}, "x")

    def test_claimed_review_with_a_record_is_accepted(self):
        VALIDATOR_MODULE.check_human_review(
            {"independent_human_review": True, "human_review_record": "reviewed 2026-08-04"}, "x"
        )
        VALIDATOR_MODULE.check_human_review({"independent_human_review": False}, "x")


class CampaignIntegrityFailureTests(unittest.TestCase):
    """Exercise every fail-closed identity/verdict branch in validate_campaign."""

    def copied_campaign(self, tmp):
        bundle = Path(tmp) / "bundle"
        shutil.copytree(VALIDATOR_MODULE.BUNDLE, bundle)
        manifest = VALIDATOR_MODULE.load_json(bundle / "manifest.json")
        campaign = manifest["campaigns"][0]
        cases = VALIDATOR_MODULE.bundle_cases(bundle)
        scores_path = bundle / campaign["scores"]
        return bundle, manifest, campaign, cases, scores_path

    def assert_score_mutation_rejected(self, mutate, message):
        with tempfile.TemporaryDirectory() as tmp:
            bundle, manifest, campaign, cases, scores_path = self.copied_campaign(tmp)
            scores = VALIDATOR_MODULE.load_json(scores_path)
            mutate(scores, cases)
            scores_path.write_text(json.dumps(scores), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, message):
                VALIDATOR_MODULE.validate_campaign(
                    campaign, cases, manifest["candidate"]["skill_hash"], bundle
                )

    def test_score_case_set_mismatch_is_a_clean_failure(self):
        self.assert_score_mutation_rejected(
            lambda scores, _cases: scores.pop(next(iter(scores))),
            "score case set or order differs",
        )

    def test_case_hash_mismatch_is_a_clean_failure(self):
        self.assert_score_mutation_rejected(
            lambda scores, cases: scores[cases[0]["name"]].update(case_hash="0" * 64),
            "case hash mismatch",
        )

    def test_output_hash_mismatch_is_a_clean_failure(self):
        self.assert_score_mutation_rejected(
            lambda scores, cases: scores[cases[0]["name"]].update(output_hash="0" * 64),
            "output hash mismatch",
        )

    def test_skill_hash_mismatch_is_a_clean_failure(self):
        self.assert_score_mutation_rejected(
            lambda scores, cases: scores[cases[0]["name"]].update(skill_hash="0" * 64),
            "skill hash mismatch",
        )

    def test_artifact_declaration_mismatch_is_a_clean_failure(self):
        self.assert_score_mutation_rejected(
            lambda scores, cases: scores[cases[0]["name"]].update(
                artifact_hashes={"tmp/evals/unexpected.txt": "0" * 64}
            ),
            "artifact declarations differ",
        )

    def test_artifact_hash_mismatch_is_a_clean_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle, manifest, campaign, cases, _scores_path = self.copied_campaign(tmp)
            case = next(item for item in cases if item.get("artifacts"))
            declared = case["artifacts"][0]
            artifact = (
                bundle
                / campaign["artifacts_dir"]
                / case["name"]
                / declared.replace("/", "__")
            )
            artifact.write_bytes(b"tampered artifact")
            with self.assertRaisesRegex(ValueError, "artifact hash mismatch"):
                VALIDATOR_MODULE.validate_campaign(
                    campaign, cases, manifest["candidate"]["skill_hash"], bundle
                )

    def test_criterion_set_mismatch_is_a_clean_failure(self):
        def mutate(scores, cases):
            scores[cases[0]["name"]]["must_pass"].pop(cases[0]["must_pass"][0])

        self.assert_score_mutation_rejected(mutate, "must_pass criteria differ")

    def test_unscored_criterion_is_a_clean_failure(self):
        def mutate(scores, cases):
            scores[cases[0]["name"]]["must_pass"][cases[0]["must_pass"][0]] = None

        self.assert_score_mutation_rejected(mutate, "has unscored criteria")


if __name__ == "__main__":
    unittest.main()
