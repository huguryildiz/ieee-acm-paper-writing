import importlib.util
import json
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


if __name__ == "__main__":
    unittest.main()
