#!/usr/bin/env python3
"""Validate every retained behavioral evidence bundle under evals/results/.

Each bundle carries its own cases.json snapshot, so a bundle stays checkable after the
skill or the case set moves on. A bundle whose declared identity still matches the working
tree is reported as current; one that no longer matches is reported as historical and is
checked for internal consistency only. Passing here is evidence integrity, not release
approval.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
RESULTS_ROOT = ROOT / "evals" / "results"
BUNDLE = RESULTS_ROOT / "post-64cec1a"
MANIFEST = BUNDLE / "manifest.json"
RUNNER_PATH = ROOT / "evals" / "run_evals.py"
CASES_PATH = ROOT / "evals" / "cases.json"

SPEC = importlib.util.spec_from_file_location("evidence_run_evals", RUNNER_PATH)
RUNNER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(RUNNER)


def fail(message: str) -> None:
    raise ValueError(message)


def shown(path: Path) -> Path:
    """Repo-relative path when possible; bundles under test may live outside the repo."""
    try:
        return path.relative_to(ROOT)
    except ValueError:
        return path


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"cannot read JSON {shown(path)}: {exc}")


def bundle_path(bundle: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or "\\" in relative:
        fail(f"invalid evidence path: {relative!r}")
    candidate = (bundle / relative).resolve()
    try:
        candidate.relative_to(Path(bundle).resolve())
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
            fail(f"{shown(path)}:{number}: invalid JSON: {exc}")
        if not isinstance(row, dict):
            fail(f"{shown(path)}:{number}: response row must be an object")
        rows.append(row)
    expected_names = [case["name"] for case in cases]
    if [row.get("name") for row in rows] != expected_names:
        fail(f"{shown(path)}: response case set or order differs from cases.json")
    result = {}
    for row in rows:
        name = row["name"]
        response = row.get("response")
        if not isinstance(response, str) or not response.strip():
            fail(f"{shown(path)}: {name} has no non-empty response")
        digest = sha256_bytes(response.encode("utf-8"))
        if row.get("sha256") != digest:
            fail(f"{shown(path)}: {name} response hash mismatch")
        result[name] = row
    return result


ABSENCE_EVIDENCE = "[absence verified by full-response inspection]"


def quote_fragments(quote: str) -> list[str]:
    return [part.strip() for part in re.split(r"\.\.\.|…", quote) if part.strip()]


def check_human_review(container: dict, label: str) -> None:
    """Require the human-review boundary as a truthful boolean, with a record when claimed."""
    reviewed = container.get("independent_human_review")
    if type(reviewed) is not bool:
        fail(f"{label}: independent_human_review must be recorded as a boolean")
    if reviewed:
        record = container.get("human_review_record")
        if not isinstance(record, str) or not record.strip():
            fail(f"{label}: independent human review is claimed without a review record")


def validate_ledger(path: Path, cases: list[dict], scores: dict,
                    responses: dict[str, dict] | None = None) -> None:
    ledger = load_json(path)
    if ledger.get("scoring_method") != "agent-assisted criterion scoring":
        fail(f"{shown(path)}: scoring method is not explicit")
    judge = ledger.get("judge")
    if not isinstance(judge, dict):
        fail(f"{shown(path)}: judge must be an object")
    check_human_review(judge, f"{shown(path)}: judge")
    reviews = ledger.get("cases")
    if not isinstance(reviews, list) or [row.get("name") for row in reviews] != [
        case["name"] for case in cases
    ]:
        fail(f"{shown(path)}: review case set or order differs from cases.json")
    for case, review in zip(cases, reviews):
        for field in ("must_pass", "must_not"):
            rows = review.get(field)
            if not isinstance(rows, list) or [row.get("criterion") for row in rows] != case[field]:
                fail(f"{shown(path)}: {case['name']} {field} criteria differ")
            for row in rows:
                verdict = row.get("verdict")
                if type(verdict) is not bool:
                    fail(f"{shown(path)}: {case['name']} has a non-binary verdict")
                if scores[case["name"]][field][row["criterion"]] is not verdict:
                    fail(f"{shown(path)}: {case['name']} ledger and scores disagree")
                quote = row.get("evidence_quote")
                if not isinstance(quote, str) or not quote.strip():
                    fail(f"{shown(path)}: {case['name']} has empty evidence")
                if responses is not None and quote.strip() != ABSENCE_EVIDENCE:
                    text = responses[case["name"]]["response"]
                    if not all(part in text for part in quote_fragments(quote)):
                        fail(
                            f"{shown(path)}: {case['name']} quotes evidence that is "
                            "not in the retained response"
                        )
                if not isinstance(row.get("rationale"), str) or not row["rationale"].strip():
                    fail(f"{shown(path)}: {case['name']} has an empty rationale")


def validate_campaign(campaign: dict, cases: list[dict], skill_hash: str,
                      bundle: Path = BUNDLE) -> bool:
    campaign_id = campaign.get("id")
    if not isinstance(campaign_id, str) or not campaign_id:
        fail("campaign id must be a non-empty string")
    responses_path = bundle_path(bundle, campaign.get("responses"))
    scores_path = bundle_path(bundle, campaign.get("scores"))
    ledger_path = bundle_path(bundle, campaign.get("review_ledger"))
    responses = read_responses(responses_path, cases)
    scores = load_json(scores_path)
    if not isinstance(scores, dict) or list(scores) != [case["name"] for case in cases]:
        fail(f"{scores_shown(path)}: score case set or order differs from cases.json")

    failed_cases = []
    for case in cases:
        name = case["name"]
        entry = scores[name]
        response = responses[name]["response"]
        if entry.get("case_hash") != RUNNER.case_hash(case):
            fail(f"{scores_shown(path)}: {name} case hash mismatch")
        if entry.get("output_hash") != sha256_bytes(response.encode("utf-8")):
            fail(f"{scores_shown(path)}: {name} output hash mismatch")
        if entry.get("skill_hash") != skill_hash:
            fail(f"{scores_shown(path)}: {name} skill hash mismatch")

        artifact_hashes = entry.get("artifact_hashes")
        if not isinstance(artifact_hashes, dict) or list(artifact_hashes) != case.get("artifacts", []):
            fail(f"{scores_shown(path)}: {name} artifact declarations differ")
        for declared, digest in artifact_hashes.items():
            relative = (
                f"{campaign['artifacts_dir']}/{name}/"
                + declared.replace("/", "__")
            )
            artifact = bundle_path(bundle, relative)
            if sha256_bytes(artifact.read_bytes()) != digest:
                fail(f"{shown(artifact)}: artifact hash mismatch")

        for field in ("must_pass", "must_not"):
            verdicts = entry.get(field)
            if not isinstance(verdicts, dict) or list(verdicts) != case[field]:
                fail(f"{scores_shown(path)}: {name} {field} criteria differ")
            if not all(type(value) is bool for value in verdicts.values()):
                fail(f"{scores_shown(path)}: {name} has unscored criteria")
        if not all(entry["must_pass"].values()) or any(entry["must_not"].values()):
            failed_cases.append(name)

    validate_ledger(ledger_path, cases, scores, responses)
    if campaign.get("failed_case_ids") != failed_cases:
        fail(f"campaign {campaign_id}: declared failed-case list differs from scores")
    if campaign.get("strict_pass") is not (not failed_cases):
        fail(f"campaign {campaign_id}: strict_pass differs from scores")
    return not failed_cases


def bundle_cases(bundle: Path) -> list[dict]:
    """Load the bundle's own case snapshot, so old evidence stays checkable."""
    snapshot = bundle / "cases.json"
    if not snapshot.is_file() or snapshot.is_symlink():
        fail(f"{bundle.name}: the bundle has no cases.json snapshot")
    document = load_json(snapshot)
    if not isinstance(document, dict) or document.get("version") != 2:
        fail(f"{bundle.name}/cases.json: expected schema version 2")
    cases = document.get("cases")
    if not isinstance(cases, list) or not cases:
        fail(f"{bundle.name}/cases.json: 'cases' must be a non-empty list")
    problems = RUNNER.case_problems(cases)
    if problems:
        fail(f"{bundle.name}/cases.json: {problems[0]}")
    return cases


def validate_bundle(bundle: Path) -> str:
    manifest = load_json(bundle / "manifest.json")
    label = bundle.name
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        fail(f"{label}/manifest.json: expected schema_version 1")
    base_commit = manifest.get("base_commit")
    if not isinstance(base_commit, str) or not re.fullmatch(r"[0-9a-f]{40}", base_commit):
        fail(f"{label}/manifest.json: base_commit must be a full 40-character commit hash")
    cases = bundle_cases(bundle)
    candidate = manifest.get("candidate")
    if not isinstance(candidate, dict):
        fail(f"{label}/manifest.json: candidate must be an object")
    expected_candidate = {
        "skill_hash": candidate.get("skill_hash"),
        "cases_sha256": sha256_bytes((bundle / "cases.json").read_bytes()),
        "case_count": len(cases),
        "must_pass_criteria": sum(len(case["must_pass"]) for case in cases),
        "must_not_criteria": sum(len(case["must_not"]) for case in cases),
    }
    if not isinstance(candidate.get("skill_hash"), str):
        fail(f"{label}/manifest.json: candidate.skill_hash must be a string")
    if candidate != expected_candidate:
        fail(f"{label}/manifest.json: declared denominator or case hash disagrees with the "
             "bundle's own cases.json snapshot")

    scoring = manifest.get("scoring")
    if not isinstance(scoring, dict):
        fail(f"{label}/manifest.json: scoring must be an object")
    check_human_review(scoring, f"{label}/manifest.json: scoring")
    collection = manifest.get("collection")
    if not isinstance(collection, dict):
        fail(f"{label}/manifest.json: collection must be an object")
    for flag in ("mechanical_authority_isolation", "skill_hash_captured_at_collection"):
        if type(collection.get(flag)) is not bool:
            fail(f"{label}/manifest.json: collection must record {flag} as a boolean")

    campaigns = manifest.get("campaigns")
    if not isinstance(campaigns, list) or len(campaigns) < 3:
        fail(f"{label}/manifest.json: at least three retained campaigns are required")
    ids = [campaign.get("id") for campaign in campaigns]
    if len(set(ids)) != len(ids):
        fail(f"{label}/manifest.json: campaign ids must be unique")
    if len({campaign.get("client") for campaign in campaigns}) < 2:
        fail(f"{label}/manifest.json: retained evidence must cover at least two clients")
    # Which host carries the replications is arbitrary; that one host does is not.
    replications: dict[str, set[int]] = {}
    for campaign in campaigns:
        replication = campaign.get("replication")
        if type(replication) is not int or replication < 1:
            fail(f"{label}/manifest.json: every campaign needs a positive integer replication")
        replications.setdefault(campaign.get("client"), set()).add(replication)
    if not any(len(seen) >= 2 for seen in replications.values()):
        fail(f"{label}/manifest.json: one client must carry at least two distinct replications")

    strict_passes = sum(
        validate_campaign(campaign, cases, candidate["skill_hash"], bundle)
        for campaign in campaigns
    )
    current = (candidate["skill_hash"] == RUNNER.skill_hash()
               and candidate["cases_sha256"] == sha256_bytes(CASES_PATH.read_bytes()))
    provenance = (
        "skill hash captured at collection"
        if collection["skill_hash_captured_at_collection"]
        else "skill hash recomputed after collection, so it does not attest the collected tree"
    )
    return (
        f"{label}: {len(campaigns)} campaigns, {len(cases)} cases each, "
        f"{strict_passes} strict pass(es); "
        f"{'describes the current tree' if current else 'historical: no longer describes the current tree'}; "
        f"{provenance}"
    )


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        bundles = [Path(name) if Path(name).is_absolute() else RESULTS_ROOT / name
                   for name in argv]
    else:
        bundles = sorted(path.parent for path in RESULTS_ROOT.glob("*/manifest.json"))
    if not bundles:
        print("FAIL: no evidence bundle found under evals/results/")
        return 1
    lines = []
    try:
        for bundle in bundles:
            if not (bundle / "manifest.json").is_file():
                fail(f"{bundle}: no manifest.json")
            lines.append(validate_bundle(bundle))
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL: {exc}")
        return 1
    for line in lines:
        print(f"OK: {line}")
    print("all hashes, verdicts, quotations, and failure lists valid; "
          "evidence validation is not release approval")
    return 0


if __name__ == "__main__":
    sys.exit(main())
