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
    def make_campaign(self, outdir, *, replication, client, break_quote=False):
        outdir.mkdir(parents=True, exist_ok=True)
        RUNNER.write_collection_record(outdir, {"HOME": str(outdir)})
        scores = {}
        for case in CASES:
            response = synthetic_response(case)
            RUNNER.case_output_path(outdir, case["name"]).write_text(response, encoding="utf-8")
            for declared in case.get("artifacts", []):
                archived = RUNNER.case_artifact_archive_path(outdir, case["name"], declared)
                archived.parent.mkdir(parents=True, exist_ok=True)
                archived.write_text(f"artifact body for {declared}", encoding="utf-8")
            scores[case["name"]] = {
                "case_hash": RUNNER.case_hash(case),
                "output_hash": RUNNER.output_hash(RUNNER.case_output_path(outdir, case["name"])),
                "skill_hash": RUNNER.skill_hash(),
                "artifact_hashes": RUNNER.archived_artifact_hashes(outdir, case),
                "must_pass": {criterion: True for criterion in case["must_pass"]},
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

    def build(self, root, **kwargs):
        # Replications on Claude Code, a single Codex run: the gate asks for two hosts
        # and two replications on one of them, not for Codex specifically.
        campaigns = [("claude-r1", 1, "Claude Code"), ("claude-r2", 2, "Claude Code"),
                     ("codex-r1", 1, "Codex CLI")]
        for name, replication, client in campaigns:
            self.make_campaign(root / "out" / name, replication=replication,
                               client=client, **kwargs)
        config = root / "bundle.json"
        config.write_text(json.dumps({
            "name": "synthetic",
            "title": "Synthetic bundle",
            "base_commit": "0" * 40,
            "collection": {"mechanical_authority_isolation": True},
            "scoring": {"independent_human_review": True,
                        "human_review_record": "reviewed by the maintainer"},
            "campaigns": [{"id": name, "outdir": str(root / "out" / name)}
                          for name, _, _ in campaigns],
        }), encoding="utf-8")
        into = root / "bundle"
        BUILDER.cmd_build(type("A", (), {"config": str(config), "into": str(into)})())
        return into

    def test_built_bundle_passes_the_evidence_validator(self):
        with tempfile.TemporaryDirectory() as tmp:
            into = self.build(Path(tmp))
            manifest = json.loads((into / "manifest.json").read_text(encoding="utf-8"))
            self.assertTrue(manifest["collection"]["skill_hash_captured_at_collection"])
            self.assertEqual(manifest["candidate"]["skill_hash"], RUNNER.skill_hash())
            self.assertTrue(all(c["strict_pass"] for c in manifest["campaigns"]))
            summary = VALIDATOR.validate_bundle(into)
            self.assertIn("3 strict pass(es)", summary)
            self.assertIn("skill hash captured at collection", summary)

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


if __name__ == "__main__":
    unittest.main()
