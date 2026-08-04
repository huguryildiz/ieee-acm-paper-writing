import importlib.util
import json
import os
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
            agents = home / ".agents" / "skills" / "ieee-acm-paper-writing"
            codex = home / ".codex" / "skills" / "ieee-acm-paper-writing"
            claude = home / ".claude" / "skills" / "ieee-acm-paper-writing"
            cached = (home / ".claude" / "plugins" / "cache" / "owner" / "plugin" /
                      "1.0.0" / "skills" / "ieee-acm-paper-writing")
            for path in (agents, codex, claude, cached):
                path.mkdir(parents=True)
            self.assertEqual(
                RUNNER_MODULE.authority_collisions(home),
                sorted([path.absolute() for path in (agents, codex, claude, cached)], key=str),
            )

    def test_alternate_codex_and_claude_roots_are_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            default = home / ".codex" / "skills" / "ieee-acm-paper-writing"
            codex = root / "codex" / "skills" / "ieee-acm-paper-writing"
            claude = (root / "claude" / "plugins" / "cache" / "owner" / "plugin" /
                      "1.0.0" / "skills" / "ieee-acm-paper-writing")
            for path in (default, codex, claude):
                path.mkdir(parents=True)
            env = {
                "HOME": str(home),
                "CODEX_HOME": str(root / "codex"),
                "CLAUDE_CONFIG_DIR": str(root / "claude"),
            }
            self.assertEqual(
                RUNNER_MODULE.authority_collisions(env=env),
                sorted([path.absolute() for path in (default, codex, claude)], key=str),
            )

    def test_agent_command_rejects_environment_and_config_overrides(self):
        for command in (
            "env HOME=/tmp/dirty codex exec",
            "sh -c 'HOME=/tmp/dirty codex exec'",
            "codex exec --config model=o3",
            "codex exec -c 'model_reasoning_effort=high'",
            "codex exec --config 'model_reasoning_effort=low'",
            "codex exec --config=model_reasoning_effort=medium",
            "codex exec -C/tmp/dirty",
            "claude -p --plugin-dir /tmp/dirty",
            "claude -p --append-system-prompt injected",
            "claude -p --append-system-prompt-file /tmp/injected.txt",
            "claude -p --system-prompt injected",
            "claude -p --system-prompt-file /tmp/injected.txt",
            "claude -p --permission-prompt-tool unsafe-tool",
            "/tmp/codex exec",
        ):
            with self.subTest(command=command), self.assertRaisesRegex(
                    ValueError, "not allowed|supported host|checked PATH"):
                RUNNER_MODULE.agent_command(command)
        self.assertEqual(RUNNER_MODULE.agent_command("codex exec"), ["codex", "exec"])
        self.assertEqual(
            RUNNER_MODULE.agent_command(
                "codex exec -m gpt-5.6-luna -c 'model_reasoning_effort=\"medium\"'"
            ),
            ["codex", "exec", "-m", "gpt-5.6-luna", "-c",
             'model_reasoning_effort="medium"'],
        )
        self.assertEqual(RUNNER_MODULE.agent_command("claude -p"), ["claude", "-p"])

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

    def test_collection_passes_the_checked_environment_without_a_shell(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = SimpleNamespace(outdir=Path(tmp) / "out", case=CASES[0]["name"],
                                   agent_cmd="codex exec", timeout=1)
            completed = SimpleNamespace(returncode=0, stdout="agent output", stderr="")
            with mock.patch.object(RUNNER_MODULE, "authority_collisions", return_value=[]), \
                    mock.patch.object(RUNNER_MODULE.subprocess, "run",
                                      return_value=completed) as agent:
                RUNNER_MODULE.cmd_collect(args)
            positional, keyword = agent.call_args
            self.assertEqual(positional[0], ["codex", "exec"])
            self.assertIs(keyword["shell"], False)
            self.assertEqual(keyword["env"]["HOME"], os.environ["HOME"])

    def test_collection_rejects_environment_override_before_agent_invocation(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = SimpleNamespace(outdir=Path(tmp) / "out", case=CASES[0]["name"],
                                   agent_cmd="env HOME=/tmp/dirty codex exec", timeout=1)
            with mock.patch.object(RUNNER_MODULE, "authority_collisions", return_value=[]), \
                    mock.patch.object(RUNNER_MODULE.subprocess, "run") as agent:
                with self.assertRaisesRegex(SystemExit, "collection refused"):
                    RUNNER_MODULE.cmd_collect(args)
                agent.assert_not_called()


class CollectionProvenanceTests(unittest.TestCase):
    """The recorded skill hash must attest the tree collection ran against."""

    def collect(self, outdir, agent_cmd="codex exec"):
        args = SimpleNamespace(outdir=outdir, case=CASES[0]["name"],
                               agent_cmd=agent_cmd, timeout=1)
        completed = SimpleNamespace(returncode=0, stdout="agent output", stderr="")
        with mock.patch.object(RUNNER_MODULE, "authority_collisions", return_value=[]), \
                mock.patch.object(RUNNER_MODULE.subprocess, "run", return_value=completed):
            RUNNER_MODULE.cmd_collect(args)

    def test_collection_records_the_skill_hash_it_ran_against(self):
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp) / "out"
            self.collect(outdir)
            record = json.loads((outdir / "collection.json").read_text(encoding="utf-8"))
            self.assertEqual(record["schema_version"], 2)
            self.assertEqual(record["skill_hash"], RUNNER_MODULE.skill_hash())
            self.assertEqual(record["agent_command"], ["codex", "exec"])
            self.assertEqual(record["authority_collisions"], [])
            self.assertTrue(record["mechanical_authority_isolation"])
            self.assertEqual(RUNNER_MODULE.release_collection_problems(record), [])
            self.assertIn("claude_effective", record["authority_roots"])

    def test_scoring_refuses_a_skill_edited_after_collection(self):
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp) / "out"
            self.collect(outdir)
            record_path = outdir / "collection.json"
            record = json.loads(record_path.read_text(encoding="utf-8"))
            record["skill_hash"] = "0" * 64
            record_path.write_text(json.dumps(record), encoding="utf-8")
            args = SimpleNamespace(outdir=outdir, case=CASES[0]["name"])
            with self.assertRaisesRegex(SystemExit, "changed after collection"):
                RUNNER_MODULE.cmd_score(args)

    def test_single_case_repair_retains_the_original_campaign_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp) / "out"
            self.collect(outdir)
            original = (outdir / "collection.json").read_text(encoding="utf-8")
            self.collect(outdir)
            self.assertEqual((outdir / "collection.json").read_text(encoding="utf-8"), original)

    def test_collection_refuses_an_outdir_recorded_under_a_different_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp) / "out"
            self.collect(outdir)
            original = (outdir / "collection.json").read_text(encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "agent_command"):
                self.collect(outdir, agent_cmd="claude -p")
            self.assertEqual((outdir / "collection.json").read_text(encoding="utf-8"), original)

    def test_collection_refuses_an_outdir_recorded_against_a_different_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp) / "out"
            self.collect(outdir)
            record_path = outdir / "collection.json"
            record = json.loads(record_path.read_text(encoding="utf-8"))
            record["skill_hash"] = "0" * 64
            record_path.write_text(json.dumps(record), encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "skill_hash"):
                self.collect(outdir)

    def collect_blind_to_an_existing_receipt(self, outdir, agent_cmd="codex exec"):
        """Collect as a process that lost the creation race: it saw no receipt, one exists."""
        real_read = RUNNER_MODULE.read_collection_record
        seen = []

        def blind_first(target):
            seen.append(target)
            return None if len(seen) == 1 else real_read(target)

        with mock.patch.object(RUNNER_MODULE, "read_collection_record", blind_first):
            self.collect(outdir, agent_cmd=agent_cmd)

    def test_losing_the_creation_race_keeps_the_winning_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp) / "out"
            self.collect(outdir)
            winner = (outdir / "collection.json").read_text(encoding="utf-8")
            self.collect_blind_to_an_existing_receipt(outdir)
            self.assertEqual((outdir / "collection.json").read_text(encoding="utf-8"), winner)
            self.assertEqual([path.name for path in outdir.glob("*.partial*")], [])

    def test_losing_the_creation_race_refuses_a_conflicting_campaign(self):
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp) / "out"
            self.collect(outdir)
            winner = (outdir / "collection.json").read_text(encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "agent_command"):
                self.collect_blind_to_an_existing_receipt(outdir, agent_cmd="claude -p")
            self.assertEqual((outdir / "collection.json").read_text(encoding="utf-8"), winner)

    def test_missing_record_falls_back_to_the_current_tree_with_a_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp)
            self.assertIsNone(RUNNER_MODULE.read_collection_record(outdir))
            self.assertEqual(RUNNER_MODULE.attested_skill_hash(outdir),
                             RUNNER_MODULE.skill_hash())


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
        for relative in ("linked.md", "linked.pyc", "__pycache__/linked.pyc"):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as tmp:
                skill = Path(tmp)
                target = skill / "SKILL.md"
                target.write_text("skill", encoding="utf-8")
                link = skill / relative
                link.parent.mkdir(parents=True, exist_ok=True)
                link.symlink_to(target)
                with self.assertRaisesRegex(ValueError, "refuses symlink"):
                    RUNNER_MODULE.skill_hash(skill)

    def test_hash_rejects_ignored_directory_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp)
            (skill / "SKILL.md").write_text("skill", encoding="utf-8")
            target = skill / "cache-target"
            target.mkdir()
            (skill / "__pycache__").symlink_to(target, target_is_directory=True)
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
