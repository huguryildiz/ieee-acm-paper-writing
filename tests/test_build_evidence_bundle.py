import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BUILDER = load("build_evidence_bundle", "scripts/build_evidence_bundle.py")
VALIDATOR = load("validate_behavioral_evidence", "scripts/validate_behavioral_evidence.py")
RUNNER = BUILDER.RUNNER
CASES = RUNNER.validated_cases()


def synthetic_response(case):
    """A response that literally contains every criterion, so quotes are verbatim."""
    lines = [f"Audit for {case['name']}."]
    lines += [f"- {criterion}" for criterion in case["must_pass"]]
    lines += [f"- checked: {criterion}" for criterion in case.get("must_not", [])]
    for declared in case.get("artifacts", []):
        lines.append(f"artifact: {declared}")
    return "\n".join(lines) + "\n"


class EvidenceBundleBuildTests(unittest.TestCase):
    def make_campaign(self, outdir, *, replication, client, break_quote=False,
                      fail_first=False):
        outdir.mkdir(parents=True, exist_ok=True)
        RUNNER.write_collection_record(
            outdir,
            {"HOME": str(outdir), "PATH": ""},
            ["codex", "exec"],
        )
        scores = {}
        for case in CASES:
            response = synthetic_response(case)
            RUNNER.case_output_path(outdir, case["name"]).write_text(response, encoding="utf-8")
            for declared in case.get("artifacts", []):
                archived = RUNNER.case_artifact_archive_path(outdir, case["name"], declared)
                archived.parent.mkdir(parents=True, exist_ok=True)
                archived.write_text(f"artifact body for {declared}", encoding="utf-8")
            must_pass = {criterion: True for criterion in case["must_pass"]}
            if fail_first and case is CASES[0]:
                must_pass[case["must_pass"][0]] = False
            scores[case["name"]] = {
                "case_hash": RUNNER.case_hash(case),
                "output_hash": RUNNER.output_hash(RUNNER.case_output_path(outdir, case["name"])),
                "skill_hash": RUNNER.skill_hash(),
                "artifact_hashes": RUNNER.archived_artifact_hashes(outdir, case),
                "must_pass": must_pass,
                "must_not": {criterion: False for criterion in case.get("must_not", [])},
            }
        (outdir / "scores.json").write_text(json.dumps(scores), encoding="utf-8")

        BUILDER.cmd_scaffold(type("A", (), {"outdir": str(outdir)})())
        review = json.loads((outdir / "review.json").read_text(encoding="utf-8"))
        review["judge"] = {"independent_human_review": True,
                           "human_review_record": "reviewed by the maintainer"}
        for row in review["cases"]:
            for field in ("must_pass", "must_not"):
                for item in row[field]:
                    item["evidence_quote"] = item["criterion"]
                    item["rationale"] = "judged from the retained response"
        if break_quote:
            first = review["cases"][0]["must_pass"][0]
            first["evidence_quote"] = "a sentence the agent never wrote"
        (outdir / "review.json").write_text(json.dumps(review), encoding="utf-8")
        (outdir / "campaign.json").write_text(json.dumps({
            "client": client, "client_version": "0.0.1", "model": "test-model",
            "effort": "medium", "replication": replication,
            "started_at": "2026-08-04T10:00:00+03:00",
            "completed_at": "2026-08-04T10:30:00+03:00",
            "authority_path": "skills/ieee-acm-paper-writing/SKILL.md",
        }), encoding="utf-8")

    def build(self, root, *, config_overrides=None, **kwargs):
        # Replications on Claude Code, a single Codex run: the gate asks for two hosts
        # and two replications on one of them, not for Codex specifically.
        campaigns = [("claude-r1", 1, "Claude Code"), ("claude-r2", 2, "Claude Code"),
                     ("codex-r1", 1, "Codex CLI")]
        for name, replication, client in campaigns:
            self.make_campaign(root / "out" / name, replication=replication,
                               client=client, **kwargs)
        config = root / "bundle.json"
        payload = {
            "name": "synthetic",
            "title": "Synthetic bundle",
            "base_commit": "0" * 40,
            "scoring": {"independent_human_review": True,
                        "human_review_record": "reviewed by the maintainer"},
            "release_qualification": {
                "qualified": True,
                "review_record": "synthetic test review",
                "blocking_findings": [],
            },
            "campaigns": [{"id": name, "outdir": str(root / "out" / name)}
                          for name, _, _ in campaigns],
        }
        if config_overrides:
            payload.update(config_overrides)
        config.write_text(json.dumps(payload), encoding="utf-8")
        into = root / "bundle"
        BUILDER.cmd_build(type("A", (), {"config": str(config), "into": str(into)})())
        return into

    def test_built_bundle_passes_the_evidence_validator(self):
        with tempfile.TemporaryDirectory() as tmp:
            into = self.build(Path(tmp))
            manifest = json.loads((into / "manifest.json").read_text(encoding="utf-8"))
            self.assertTrue(manifest["collection"]["skill_hash_captured_at_collection"])
            self.assertTrue(manifest["collection"]["agent_command_captured_at_collection"])
            self.assertTrue(manifest["collection"]["collection_record_retained"])
            self.assertTrue(manifest["release_qualification"]["qualified"])
            self.assertEqual(manifest["candidate"]["skill_hash"], RUNNER.skill_hash())
            for campaign in manifest["campaigns"]:
                self.assertTrue((into / campaign["collection_record"]).is_file())
            self.assertTrue(all(c["strict_pass"] for c in manifest["campaigns"]))
            summary = VALIDATOR.validate_bundle(into)
            self.assertIn("3 strict pass(es)", summary)
            self.assertIn("collection record retained", summary)

    def test_a_single_run_on_every_host_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            into = self.build(Path(tmp))
            manifest = json.loads((into / "manifest.json").read_text(encoding="utf-8"))
            for campaign in manifest["campaigns"]:
                campaign["replication"] = 1
            (into / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "two distinct replications"):
                VALIDATOR.validate_bundle(into)

    def test_build_refuses_a_quotation_absent_from_the_response(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(SystemExit, "not in the retained response"):
                self.build(Path(tmp), break_quote=True)

    def test_build_refuses_a_campaign_without_a_collection_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outdir = root / "out" / "codex-r1"
            self.make_campaign(outdir, replication=1, client="Codex CLI")
            (outdir / "collection.json").unlink()
            with self.assertRaisesRegex(SystemExit, "collection.json is missing"):
                BUILDER.build_campaign({"id": "codex-r1", "outdir": str(outdir)},
                                       CASES, root / "bundle", RUNNER.skill_hash())

    def test_build_refuses_a_skill_edited_after_collection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outdir = root / "out" / "codex-r1"
            self.make_campaign(outdir, replication=1, client="Codex CLI")
            record = json.loads((outdir / "collection.json").read_text(encoding="utf-8"))
            record["skill_hash"] = "0" * 64
            (outdir / "collection.json").write_text(json.dumps(record), encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "changed after collection"):
                BUILDER.build_campaign({"id": "codex-r1", "outdir": str(outdir)},
                                       CASES, root / "bundle", RUNNER.skill_hash())

    def test_build_refuses_a_collection_record_without_the_agent_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outdir = root / "out" / "codex-r1"
            self.make_campaign(outdir, replication=1, client="Codex CLI")
            record_path = outdir / "collection.json"
            record = json.loads(record_path.read_text(encoding="utf-8"))
            record.pop("agent_command")
            record_path.write_text(json.dumps(record), encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "agent_command"):
                BUILDER.build_campaign({"id": "codex-r1", "outdir": str(outdir)},
                                       CASES, root / "bundle", RUNNER.skill_hash())

    def test_validator_rejects_a_tampered_retained_collection_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            into = self.build(Path(tmp))
            manifest = json.loads((into / "manifest.json").read_text(encoding="utf-8"))
            record_path = into / manifest["campaigns"][0]["collection_record"]
            record = json.loads(record_path.read_text(encoding="utf-8"))
            record["agent_command"] = ["claude", "--system-prompt", "injected", "-p"]
            record_path.write_text(json.dumps(record), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "collection record hash mismatch"):
                VALIDATOR.validate_bundle(into)

    def test_build_refuses_release_qualification_when_a_campaign_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(SystemExit, "every campaign to pass strictly"):
                self.build(Path(tmp), fail_first=True)

    def test_build_refuses_hand_declared_mechanical_isolation(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(SystemExit, "may not declare mechanical_authority"):
                self.build(Path(tmp), config_overrides={
                    "collection": {"mechanical_authority_isolation": True}
                })

    def test_validator_refuses_qualified_manifest_with_a_failed_campaign(self):
        with tempfile.TemporaryDirectory() as tmp:
            into = self.build(Path(tmp))
            manifest_path = into / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["campaigns"][0]["strict_pass"] = False
            manifest["campaigns"][0]["failed_case_ids"] = [CASES[0]["name"]]
            scores_path = into / manifest["campaigns"][0]["scores"]
            scores = json.loads(scores_path.read_text(encoding="utf-8"))
            scores[CASES[0]["name"]]["must_pass"][CASES[0]["must_pass"][0]] = False
            scores_path.write_text(json.dumps(scores), encoding="utf-8")
            ledger_path = into / manifest["campaigns"][0]["review_ledger"]
            ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
            ledger["cases"][0]["must_pass"][0]["verdict"] = False
            ledger_path.write_text(json.dumps(ledger), encoding="utf-8")
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "every campaign to pass strictly"):
                VALIDATOR.validate_bundle(into)


if __name__ == "__main__":
    unittest.main()
