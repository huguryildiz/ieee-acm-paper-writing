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
TOTAL = len(CASES)
SPEC = importlib.util.spec_from_file_location("run_evals", RUNNER)
RUNNER_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER_MODULE)


def passing_entry(case, output_file):
    return {
        "case_hash": RUNNER_MODULE.case_hash(case),
        "output_hash": RUNNER_MODULE.output_hash(output_file),
        "skill_hash": RUNNER_MODULE.skill_hash(),
        "must_pass": {criterion: True for criterion in case["must_pass"]},
        "must_not": {criterion: False for criterion in case.get("must_not", [])},
    }


class ReportTests(unittest.TestCase):
    def run_report(self, selected_cases, remove_outputs=False, replace_first=False,
                   empty_first=False, wrong_skill_hash=False):
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp)
            scores = {}
            for case in selected_cases:
                output_file = outdir / f"{case['name']}.md"
                output_file.write_text("test output", encoding="utf-8")
                scores[case["name"]] = passing_entry(case, output_file)
            (outdir / "scores.json").write_text(json.dumps(scores), encoding="utf-8")
            if replace_first and selected_cases:
                (outdir / f"{selected_cases[0]['name']}.md").write_text(
                    "replacement output", encoding="utf-8"
                )
            if empty_first and selected_cases:
                (outdir / f"{selected_cases[0]['name']}.md").write_text("", encoding="utf-8")
            if wrong_skill_hash and selected_cases:
                scores[selected_cases[0]["name"]]["skill_hash"] = "0" * 64
                (outdir / "scores.json").write_text(json.dumps(scores), encoding="utf-8")
            if remove_outputs:
                for case in selected_cases:
                    (outdir / f"{case['name']}.md").unlink()
            return subprocess.run(
                [sys.executable, str(RUNNER), "report", "--outdir", str(outdir), "--strict"],
                capture_output=True,
                text=True,
            )

    def test_missing_cases_remain_in_denominator_and_fail_strict(self):
        result = self.run_report(CASES[:2])
        self.assertEqual(result.returncode, 1)
        self.assertIn(f"aggregate: 2/{TOTAL} cases passed", result.stdout)
        self.assertEqual(result.stdout.count("MISSING   "), TOTAL - 2)

    def test_complete_passing_suite_passes_strict(self):
        result = self.run_report(CASES)
        self.assertEqual(result.returncode, 0)
        self.assertIn(f"aggregate: {TOTAL}/{TOTAL} cases passed", result.stdout)

    def test_missing_agent_outputs_fail_strict(self):
        result = self.run_report(CASES, remove_outputs=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout.count("MISSING   "), TOTAL)
        self.assertIn(f"aggregate: 0/{TOTAL} cases passed", result.stdout)

    def test_replaced_agent_output_is_stale(self):
        result = self.run_report(CASES, replace_first=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn(f"STALE     {CASES[0]['name']}", result.stdout)
        self.assertIn(f"aggregate: {TOTAL - 1}/{TOTAL} cases passed", result.stdout)

    def test_empty_agent_output_fails_strict(self):
        result = self.run_report(CASES, empty_first=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn(f"MISSING   {CASES[0]['name']} (empty agent output)", result.stdout)

    def test_changed_skill_snapshot_is_stale(self):
        result = self.run_report(CASES, wrong_skill_hash=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn(f"STALE     {CASES[0]['name']}", result.stdout)

    def test_score_resets_verdicts_after_output_change(self):
        case = CASES[0]
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp)
            output_file = outdir / f"{case['name']}.md"
            output_file.write_text("first output", encoding="utf-8")
            scores = {case["name"]: passing_entry(case, output_file)}
            (outdir / "scores.json").write_text(json.dumps(scores), encoding="utf-8")
            output_file.write_text("changed output", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(RUNNER), "score", "--outdir", str(outdir),
                 "--case", case["name"]],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0)
            rescored = json.loads((outdir / "scores.json").read_text(encoding="utf-8"))
            entry = rescored[case["name"]]
            self.assertTrue(all(value is None for value in entry["must_pass"].values()))
            self.assertTrue(all(value is None for value in entry["must_not"].values()))
            self.assertEqual(entry["output_hash"], RUNNER_MODULE.output_hash(output_file))

    def test_failed_collection_preserves_existing_output(self):
        case = CASES[0]
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp)
            output_file = outdir / f"{case['name']}.md"
            output_file.write_text("preserve me", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(RUNNER), "collect", "--outdir", str(outdir),
                 "--case", case["name"], "--agent-cmd",
                 f'{sys.executable} -c "import sys; sys.exit(7)"'],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertEqual(output_file.read_text(encoding="utf-8"), "preserve me")


class SchemaTests(unittest.TestCase):
    def test_name_is_required(self):
        problems = RUNNER_MODULE.case_problems([
            {"prompt": "x", "must_pass": ["y"], "must_not": [], "expected_routing": []}
        ])
        self.assertTrue(any("name must be a non-empty string" in problem for problem in problems))

    def test_prompt_must_be_a_string(self):
        problems = RUNNER_MODULE.case_problems([
            {"name": "x", "prompt": 1, "must_pass": ["y"], "must_not": [],
             "expected_routing": []}
        ])
        self.assertTrue(any("prompt must be a non-empty string" in problem for problem in problems))

    def test_must_not_and_expected_routing_are_required(self):
        problems = RUNNER_MODULE.case_problems([
            {"name": "x", "prompt": "p", "must_pass": ["y"]}
        ])
        self.assertIn("x: must_not is required", problems)
        self.assertIn("x: expected_routing is required", problems)

    def test_unsafe_case_names_are_rejected(self):
        for name in ("../victim", "/tmp/victim", "nested/name", "has space"):
            with self.subTest(name=name):
                problems = RUNNER_MODULE.case_problems([
                    {"name": name, "prompt": "p", "must_pass": ["y"],
                     "must_not": [], "expected_routing": []}
                ])
                self.assertTrue(any("name must match" in problem for problem in problems))

    def test_case_output_path_rejects_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                RUNNER_MODULE.case_output_path(tmp, "../victim")


if __name__ == "__main__":
    unittest.main()
