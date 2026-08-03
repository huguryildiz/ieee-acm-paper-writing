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


class ReviewLedgerEvidenceTests(unittest.TestCase):
    def test_retained_ledgers_have_explicit_evidence_for_every_verdict(self):
        manifest = json.loads(VALIDATOR_MODULE.MANIFEST.read_text(encoding="utf-8"))
        cases = VALIDATOR_MODULE.RUNNER.validated_cases()
        for campaign in manifest["campaigns"]:
            scores = VALIDATOR_MODULE.load_json(
                VALIDATOR_MODULE.BUNDLE / campaign["scores"]
            )
            ledger = VALIDATOR_MODULE.BUNDLE / campaign["review_ledger"]
            with self.subTest(campaign=campaign["id"]):
                VALIDATOR_MODULE.validate_ledger(ledger, cases, scores)

    def test_blank_evidence_is_rejected_even_when_rationale_remains(self):
        manifest = json.loads(VALIDATOR_MODULE.MANIFEST.read_text(encoding="utf-8"))
        campaign = manifest["campaigns"][0]
        cases = VALIDATOR_MODULE.RUNNER.validated_cases()
        scores = VALIDATOR_MODULE.load_json(
            VALIDATOR_MODULE.BUNDLE / campaign["scores"]
        )
        ledger = VALIDATOR_MODULE.load_json(
            VALIDATOR_MODULE.BUNDLE / campaign["review_ledger"]
        )
        ledger["cases"][0]["must_pass"][0]["evidence_quote"] = ""
        with tempfile.TemporaryDirectory(dir=ROOT, prefix=".evidence-test-") as tmp:
            path = Path(tmp) / "review-ledger.json"
            path.write_text(json.dumps(ledger), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "empty evidence"):
                VALIDATOR_MODULE.validate_ledger(path, cases, scores)


if __name__ == "__main__":
    unittest.main()
