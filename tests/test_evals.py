import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "evals" / "run_evals.py"
CASES = json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))["cases"]


def passing_entry(case):
    return {
        "must_pass": {criterion: True for criterion in case["must_pass"]},
        "must_not": {criterion: False for criterion in case.get("must_not", [])},
    }


class ReportTests(unittest.TestCase):
    def run_report(self, selected_cases):
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp)
            scores = {}
            for case in selected_cases:
                (outdir / f"{case['name']}.md").write_text("test output", encoding="utf-8")
                scores[case["name"]] = passing_entry(case)
            (outdir / "scores.json").write_text(json.dumps(scores), encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(RUNNER), "report", "--outdir", str(outdir), "--strict"],
                capture_output=True,
                text=True,
            )

    def test_missing_cases_remain_in_denominator_and_fail_strict(self):
        result = self.run_report(CASES[:2])
        self.assertEqual(result.returncode, 1)
        self.assertIn("aggregate: 2/15 cases passed", result.stdout)
        self.assertEqual(result.stdout.count("MISSING   "), 13)

    def test_complete_passing_suite_passes_strict(self):
        result = self.run_report(CASES)
        self.assertEqual(result.returncode, 0)
        self.assertIn("aggregate: 15/15 cases passed", result.stdout)


class SchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("run_evals", RUNNER)
        cls.runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.runner)

    def test_name_is_required(self):
        problems = self.runner.case_problems([
            {"prompt": "x", "must_pass": ["y"], "must_not": [], "expected_routing": []}
        ])
        self.assertTrue(any("name must be a non-empty string" in problem for problem in problems))


if __name__ == "__main__":
    unittest.main()
