#!/usr/bin/env python3
"""Validate the retained post-64cec1a behavioral evidence bundle."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "evals" / "results" / "post-64cec1a"
MANIFEST = BUNDLE / "manifest.json"
RUNNER_PATH = ROOT / "evals" / "run_evals.py"
CASES_PATH = ROOT / "evals" / "cases.json"
BASE_COMMIT = "64cec1afeb6d42a8bb1f2b0aec281f6f2bb91a32"

SPEC = importlib.util.spec_from_file_location("evidence_run_evals", RUNNER_PATH)
RUNNER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(RUNNER)


def fail(message: str) -> None:
    raise ValueError(message)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"cannot read JSON {path.relative_to(ROOT)}: {exc}")


def bundle_path(relative: str) -> Path:
    if not isinstance(relative, str) or not relative or "\\" in relative:
        fail(f"invalid evidence path: {relative!r}")
    candidate = (BUNDLE / relative).resolve()
    try:
        candidate.relative_to(BUNDLE.resolve())
    except ValueError:
        fail(f"evidence path escapes bundle: {relative!r}")
    if not candidate.is_file() or candidate.is_symlink():
        fail(f"missing or unsafe evidence file: {relative}")
    return candidate


def read_responses(path: Path, cases: list[dict]) -> dict[str, dict]:
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"{path.relative_to(ROOT)}:{number}: invalid JSON: {exc}")
        if not isinstance(row, dict):
            fail(f"{path.relative_to(ROOT)}:{number}: response row must be an object")
        rows.append(row)
    expected_names = [case["name"] for case in cases]
    if [row.get("name") for row in rows] != expected_names:
        fail(f"{path.relative_to(ROOT)}: response case set or order differs from cases.json")
    result = {}
    for row in rows:
        name = row["name"]
        response = row.get("response")
        if not isinstance(response, str) or not response.strip():
            fail(f"{path.relative_to(ROOT)}: {name} has no non-empty response")
        digest = sha256_bytes(response.encode("utf-8"))
        if row.get("sha256") != digest:
            fail(f"{path.relative_to(ROOT)}: {name} response hash mismatch")
        result[name] = row
    return result


def validate_ledger(path: Path, cases: list[dict], scores: dict) -> None:
    ledger = load_json(path)
    if ledger.get("scoring_method") != "agent-assisted criterion scoring":
        fail(f"{path.relative_to(ROOT)}: scoring method is not explicit")
    judge = ledger.get("judge")
    if not isinstance(judge, dict) or judge.get("independent_human_review") is not False:
        fail(f"{path.relative_to(ROOT)}: human-review boundary must be recorded as false")
    reviews = ledger.get("cases")
    if not isinstance(reviews, list) or [row.get("name") for row in reviews] != [
        case["name"] for case in cases
    ]:
        fail(f"{path.relative_to(ROOT)}: review case set or order differs from cases.json")
    for case, review in zip(cases, reviews):
        for field in ("must_pass", "must_not"):
            rows = review.get(field)
            if not isinstance(rows, list) or [row.get("criterion") for row in rows] != case[field]:
                fail(f"{path.relative_to(ROOT)}: {case['name']} {field} criteria differ")
            for row in rows:
                verdict = row.get("verdict")
                if type(verdict) is not bool:
                    fail(f"{path.relative_to(ROOT)}: {case['name']} has a non-binary verdict")
                if scores[case["name"]][field][row["criterion"]] is not verdict:
                    fail(f"{path.relative_to(ROOT)}: {case['name']} ledger and scores disagree")
                if (not isinstance(row.get("evidence_quote"), str)
                        or not row["evidence_quote"].strip()):
                    fail(f"{path.relative_to(ROOT)}: {case['name']} has empty evidence")
                if not isinstance(row.get("rationale"), str) or not row["rationale"].strip():
                    fail(f"{path.relative_to(ROOT)}: {case['name']} has an empty rationale")


def validate_campaign(campaign: dict, cases: list[dict], skill_hash: str) -> bool:
    campaign_id = campaign.get("id")
    if not isinstance(campaign_id, str) or not campaign_id:
        fail("campaign id must be a non-empty string")
    responses_path = bundle_path(campaign.get("responses"))
    scores_path = bundle_path(campaign.get("scores"))
    ledger_path = bundle_path(campaign.get("review_ledger"))
    responses = read_responses(responses_path, cases)
    scores = load_json(scores_path)
    if not isinstance(scores, dict) or list(scores) != [case["name"] for case in cases]:
        fail(f"{scores_path.relative_to(ROOT)}: score case set or order differs from cases.json")

    failed_cases = []
    for case in cases:
        name = case["name"]
        entry = scores[name]
        response = responses[name]["response"]
        if entry.get("case_hash") != RUNNER.case_hash(case):
            fail(f"{scores_path.relative_to(ROOT)}: {name} case hash mismatch")
        if entry.get("output_hash") != sha256_bytes(response.encode("utf-8")):
            fail(f"{scores_path.relative_to(ROOT)}: {name} output hash mismatch")
        if entry.get("skill_hash") != skill_hash:
            fail(f"{scores_path.relative_to(ROOT)}: {name} skill hash mismatch")

        artifact_hashes = entry.get("artifact_hashes")
        if not isinstance(artifact_hashes, dict) or list(artifact_hashes) != case.get("artifacts", []):
            fail(f"{scores_path.relative_to(ROOT)}: {name} artifact declarations differ")
        for declared, digest in artifact_hashes.items():
            relative = (
                f"{campaign['artifacts_dir']}/{name}/"
                + declared.replace("/", "__")
            )
            artifact = bundle_path(relative)
            if sha256_bytes(artifact.read_bytes()) != digest:
                fail(f"{artifact.relative_to(ROOT)}: artifact hash mismatch")

        for field in ("must_pass", "must_not"):
            verdicts = entry.get(field)
            if not isinstance(verdicts, dict) or list(verdicts) != case[field]:
                fail(f"{scores_path.relative_to(ROOT)}: {name} {field} criteria differ")
            if not all(type(value) is bool for value in verdicts.values()):
                fail(f"{scores_path.relative_to(ROOT)}: {name} has unscored criteria")
        if not all(entry["must_pass"].values()) or any(entry["must_not"].values()):
            failed_cases.append(name)

    validate_ledger(ledger_path, cases, scores)
    if campaign.get("failed_case_ids") != failed_cases:
        fail(f"campaign {campaign_id}: declared failed-case list differs from scores")
    if campaign.get("strict_pass") is not (not failed_cases):
        fail(f"campaign {campaign_id}: strict_pass differs from scores")
    return not failed_cases


def main() -> int:
    try:
        manifest = load_json(MANIFEST)
        if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
            fail("manifest.json: expected schema_version 1")
        if manifest.get("base_commit") != BASE_COMMIT:
            fail("manifest.json: base commit is not the audited 64cec1a commit")
        cases = RUNNER.validated_cases()
        skill_hash = RUNNER.skill_hash()
        candidate = manifest.get("candidate")
        if not isinstance(candidate, dict):
            fail("manifest.json: candidate must be an object")
        expected_candidate = {
            "skill_hash": skill_hash,
            "cases_sha256": sha256_bytes(CASES_PATH.read_bytes()),
            "case_count": len(cases),
            "must_pass_criteria": sum(len(case["must_pass"]) for case in cases),
            "must_not_criteria": sum(len(case["must_not"]) for case in cases),
        }
        if candidate != expected_candidate:
            fail("manifest.json: candidate hashes or declared denominator are stale")
        scoring = manifest.get("scoring")
        if not isinstance(scoring, dict) or scoring.get("independent_human_review") is not False:
            fail("manifest.json: independent human review must be recorded truthfully as false")
        collection = manifest.get("collection")
        if (not isinstance(collection, dict)
                or type(collection.get("mechanical_authority_isolation")) is not bool):
            fail("manifest.json: collection must record mechanical_authority_isolation as boolean")
        campaigns = manifest.get("campaigns")
        if not isinstance(campaigns, list) or len(campaigns) < 3:
            fail("manifest.json: at least three retained campaigns are required")
        ids = [campaign.get("id") for campaign in campaigns]
        if len(set(ids)) != len(ids):
            fail("manifest.json: campaign ids must be unique")
        clients = {campaign.get("client") for campaign in campaigns}
        if len(clients) < 2:
            fail("manifest.json: retained evidence must cover at least two clients")
        codex_reps = {
            campaign.get("replication") for campaign in campaigns
            if campaign.get("client") == "Codex CLI"
        }
        if not {1, 2}.issubset(codex_reps):
            fail("manifest.json: two distinct Codex replications are required")
        strict_passes = sum(
            validate_campaign(campaign, cases, skill_hash) for campaign in campaigns
        )
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL: {exc}")
        return 1
    print(
        f"OK: {len(campaigns)} retained campaigns, {len(cases)} cases each, "
        f"{strict_passes} strict pass(es); all hashes, verdicts, and failure lists valid; "
        "evidence validation is not release approval"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
