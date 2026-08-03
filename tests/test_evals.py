import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


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
        "artifact_hashes": RUNNER_MODULE.archived_artifact_hashes(output_file.parent, case),
        "must_pass": {criterion: True for criterion in case["must_pass"]},
        "must_not": {criterion: False for criterion in case.get("must_not", [])},
    }


class RunnerAuthorityTests(unittest.TestCase):
    def test_collection_preamble_pins_the_repository_skill_copy(self):
        self.assertIn(
            "skills/ieee-acm-paper-writing/SKILL.md",
            RUNNER_MODULE.SKILL_PREAMBLE,
        )
        self.assertIn("Do not use a user-level", RUNNER_MODULE.SKILL_PREAMBLE)

    def test_known_user_and_cache_copies_are_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            direct = home / ".codex" / "skills" / "ieee-acm-paper-writing"
            cached = (home / ".claude" / "plugins" / "cache" / "owner" / "plugin" /
                      "1.0.0" / "skills" / "ieee-acm-paper-writing")
            direct.mkdir(parents=True)
            cached.mkdir(parents=True)
            self.assertEqual(
                RUNNER_MODULE.authority_collisions(home),
                sorted([direct.absolute(), cached.absolute()], key=str),
            )

    def test_collection_refuses_collision_before_agent_invocation(self):
        with tempfile.TemporaryDirectory() as tmp:
            collision = Path(tmp) / "ieee-acm-paper-writing"
            args = SimpleNamespace(outdir=Path(tmp) / "out", case=CASES[0]["name"],
                                   agent_cmd="agent", timeout=1)
            with mock.patch.object(RUNNER_MODULE, "authority_collisions",
                                   return_value=[collision]), \
                    mock.patch.object(RUNNER_MODULE.subprocess, "run") as agent:
                with self.assertRaisesRegex(SystemExit, "collection refused"):
                    RUNNER_MODULE.cmd_collect(args)
                agent.assert_not_called()


class SkillHashTests(unittest.TestCase):
    def test_hash_covers_every_distributed_file_type(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp)
            files = (
                "SKILL.md",
                "scripts/render_audit_map.py",
                "examples/example.json",
                "examples/example.html",
                "references/integrity-audit.md",
            )
            for relative in files:
                path = skill / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(relative, encoding="utf-8")
            baseline = RUNNER_MODULE.skill_hash(skill)
            for relative in files:
                path = skill / relative
                original = path.read_text(encoding="utf-8")
                path.write_text(original + " changed", encoding="utf-8")
                self.assertNotEqual(RUNNER_MODULE.skill_hash(skill), baseline, relative)
                path.write_text(original, encoding="utf-8")

    def test_hash_ignores_generated_cache_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp)
            (skill / "SKILL.md").write_text("skill", encoding="utf-8")
            baseline = RUNNER_MODULE.skill_hash(skill)
            cache = skill / "scripts" / "__pycache__" / "renderer.pyc"
            cache.parent.mkdir(parents=True)
            cache.write_bytes(b"generated")
            self.assertEqual(RUNNER_MODULE.skill_hash(skill), baseline)

    def test_hash_rejects_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp)
            target = skill / "SKILL.md"
            target.write_text("skill", encoding="utf-8")
            (skill / "linked.md").symlink_to(target)
            with self.assertRaisesRegex(ValueError, "refuses symlink"):
                RUNNER_MODULE.skill_hash(skill)


class ReportTests(unittest.TestCase):
    def run_report(self, selected_cases, remove_outputs=False, replace_first=False,
                   empty_first=False, wrong_skill_hash=False):
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp)
            scores = {}
            for case in selected_cases:
                output_file = outdir / f"{case['name']}.md"
                output_file.write_text("test output", encoding="utf-8")
                for declared in case.get("artifacts", []):
                    artifact = RUNNER_MODULE.case_artifact_archive_path(
                        outdir, case["name"], declared
                    )
                    artifact.parent.mkdir(parents=True, exist_ok=True)
                    artifact.write_text(f"artifact for {declared}", encoding="utf-8")
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

    def test_missing_declared_artifact_is_stale(self):
        case = next(case for case in CASES if case.get("artifacts"))
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp)
            output_file = outdir / f"{case['name']}.md"
            output_file.write_text("test output", encoding="utf-8")
            for declared in case["artifacts"]:
                artifact = RUNNER_MODULE.case_artifact_archive_path(
                    outdir, case["name"], declared
                )
                artifact.parent.mkdir(parents=True, exist_ok=True)
                artifact.write_text("artifact", encoding="utf-8")
            scores = {case["name"]: passing_entry(case, output_file)}
            (outdir / "scores.json").write_text(json.dumps(scores), encoding="utf-8")
            first = RUNNER_MODULE.case_artifact_archive_path(
                outdir, case["name"], case["artifacts"][0]
            )
            first.unlink()
            result = subprocess.run(
                [sys.executable, str(RUNNER), "report", "--outdir", str(outdir), "--strict"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn(f"STALE     {case['name']}", result.stdout)

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

    def test_artifacts_must_stay_below_eval_tmp(self):
        base = {
            "name": "x", "prompt": "p", "must_pass": ["y"],
            "must_not": [], "expected_routing": [],
        }
        for artifact in ("../victim", "/tmp/victim", "tmp/other/file.json", "tmp\\evals\\x"):
            with self.subTest(artifact=artifact):
                case = dict(base, artifacts=[artifact])
                problems = RUNNER_MODULE.case_problems([case])
                self.assertTrue(any("artifact paths" in problem for problem in problems))

    def test_artifact_entries_must_be_strings(self):
        case = {
            "name": "x", "prompt": "p", "must_pass": ["y"],
            "must_not": [], "expected_routing": [], "artifacts": [{"path": "x"}],
        }
        problems = RUNNER_MODULE.case_problems([case])
        self.assertTrue(any("entries must be strings" in problem for problem in problems))

    def test_coverage_requires_every_mode_and_html_modifier(self):
        cases = [{"name": "only"}]
        problems = RUNNER_MODULE.coverage_problems(
            {"coverage": {"modes": {}, "modifiers": {}}}, cases
        )
        self.assertTrue(any("coverage.modes.expand" in problem for problem in problems))
        self.assertTrue(any("coverage.modifiers.html-map" in problem for problem in problems))


if __name__ == "__main__":
    unittest.main()
