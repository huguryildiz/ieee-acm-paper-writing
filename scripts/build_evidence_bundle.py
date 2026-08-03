#!/usr/bin/env python3
"""Assemble a retained behavioral evidence bundle from collected campaign outputs.

The retained bundle format (responses.jsonl, review-ledger.json, manifest.json, a
cases.json snapshot, and archived artifacts) used to be produced by hand, which is how a
relaxed criterion and paraphrased quotations entered the record. This builder derives
every mechanical field and refuses to emit a bundle whose review decisions are
incomplete, disagree with the scores, or quote text that is not in the retained response.

Workflow
  scaffold --outdir DIR          Write DIR/review.json and DIR/campaign.json templates
                                 for a collected, scored campaign.
  build --config FILE            Assemble the bundle named by the config into
       [--into DIR]              evals/results/<name>/ (or DIR).

Standard library only.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "evals" / "run_evals.py"
CASES_PATH = ROOT / "evals" / "cases.json"
RESULTS_ROOT = ROOT / "evals" / "results"
ABSENCE_EVIDENCE = "[absence verified by full-response inspection]"
SCORING_METHOD = "agent-assisted criterion scoring"
CAMPAIGN_FIELDS = (
    "client", "client_version", "model", "effort", "replication",
    "started_at", "completed_at", "authority_path",
)

SPEC = importlib.util.spec_from_file_location("bundle_run_evals", RUNNER_PATH)
RUNNER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(RUNNER)


def fail(message: str) -> None:
    raise SystemExit(f"bundle build refused: {message}")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"cannot read {path}: {exc}")


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def quote_fragments(quote: str) -> list[str]:
    return [part.strip() for part in re.split(r"\.\.\.|…", quote) if part.strip()]


def quote_is_supported(quote: str, response: str) -> bool:
    if quote.strip() == ABSENCE_EVIDENCE:
        return True
    fragments = quote_fragments(quote)
    return bool(fragments) and all(fragment in response for fragment in fragments)


def campaign_response(outdir: Path, name: str) -> str:
    path = RUNNER.case_output_path(outdir, name)
    if not path.is_file():
        fail(f"{outdir.name}: no collected response for {name}")
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        fail(f"{outdir.name}: empty collected response for {name}")
    return text


def cmd_scaffold(args) -> int:
    outdir = Path(args.outdir).resolve()
    cases = RUNNER.validated_cases()
    scores_path = outdir / "scores.json"
    if not scores_path.is_file():
        fail(f"{scores_path} not found; run 'run_evals.py score' first")
    scores = read_json(scores_path)

    review_path = outdir / "review.json"
    if review_path.exists():
        print(f"kept existing {review_path}")
    else:
        review = {
            "scoring_method": SCORING_METHOD,
            "judge": {"independent_human_review": None, "human_review_record": ""},
            "semantics": {
                "must_pass": "true only when the response unambiguously satisfies the whole criterion",
                "must_not": "true only when the prohibited behavior appears",
                "expected_routing_scored": False,
            },
            "cases": [
                {
                    "name": case["name"],
                    **{
                        field: [
                            {
                                "criterion": criterion,
                                "verdict": scores.get(case["name"], {}).get(field, {}).get(criterion),
                                "evidence_quote": "",
                                "rationale": "",
                            }
                            for criterion in case.get(field, [])
                        ]
                        for field in ("must_pass", "must_not")
                    },
                }
                for case in cases
            ],
        }
        write_json(review_path, review)
        print(f"wrote {review_path}")

    campaign_path = outdir / "campaign.json"
    if campaign_path.exists():
        print(f"kept existing {campaign_path}")
    else:
        write_json(campaign_path, {
            "client": "",
            "client_version": "",
            "model": "",
            "effort": "",
            "replication": 1,
            "started_at": "",
            "completed_at": "",
            "authority_path": "skills/ieee-acm-paper-writing/SKILL.md",
        })
        print(f"wrote {campaign_path}")
    print("fill every null verdict, quotation, and rationale before building the bundle")
    return 0


def build_campaign(entry: dict, cases: list[dict], into: Path, skill_hash: str) -> dict:
    campaign_id = entry.get("id")
    if not isinstance(campaign_id, str) or not campaign_id.strip():
        fail("every configured campaign needs a non-empty id")
    outdir = (ROOT / entry["outdir"]).resolve() if not Path(entry["outdir"]).is_absolute() \
        else Path(entry["outdir"]).resolve()
    if not outdir.is_dir():
        fail(f"{campaign_id}: {outdir} is not a directory")

    record = RUNNER.read_collection_record(outdir)
    if record is None:
        fail(f"{campaign_id}: {outdir}/collection.json is missing; this campaign carries no "
             "collection-time skill identity and cannot become release evidence")
    if record["skill_hash"] != skill_hash:
        fail(f"{campaign_id}: the installable skill changed after collection "
             f"({record['skill_hash']} at collection, {skill_hash} now)")

    metadata = read_json(outdir / "campaign.json")
    missing = [field for field in CAMPAIGN_FIELDS
               if not isinstance(metadata.get(field), (str, int)) or metadata.get(field) == ""]
    if missing:
        fail(f"{campaign_id}: campaign.json is incomplete: {', '.join(missing)}")

    scores = read_json(outdir / "scores.json")
    if list(scores) != [case["name"] for case in cases]:
        fail(f"{campaign_id}: scores.json case set or order differs from cases.json")
    review = read_json(outdir / "review.json")
    if review.get("scoring_method") != SCORING_METHOD:
        fail(f"{campaign_id}: review.json must state the scoring method explicitly")
    judge = review.get("judge")
    if not isinstance(judge, dict) or type(judge.get("independent_human_review")) is not bool:
        fail(f"{campaign_id}: review.json must record independent_human_review as a boolean")
    if judge["independent_human_review"] and not str(judge.get("human_review_record", "")).strip():
        fail(f"{campaign_id}: independent human review is claimed without a review record")
    reviews = {row["name"]: row for row in review.get("cases", [])}
    if list(reviews) != [case["name"] for case in cases]:
        fail(f"{campaign_id}: review.json case set or order differs from cases.json")

    target = into / campaign_id
    target.mkdir(parents=True, exist_ok=True)
    responses_lines = []
    failed_cases = []
    ledger_cases = []

    for case in cases:
        name = case["name"]
        response = campaign_response(outdir, name)
        digest = sha256_bytes(response.encode("utf-8"))
        responses_lines.append(json.dumps(
            {"name": name, "sha256": digest, "response": response}, ensure_ascii=False
        ))

        entry_scores = scores[name]
        if entry_scores.get("output_hash") != digest:
            fail(f"{campaign_id}: {name} scored output differs from the collected response")
        if entry_scores.get("case_hash") != RUNNER.case_hash(case):
            fail(f"{campaign_id}: {name} case hash is stale; rescore against current cases.json")
        if entry_scores.get("skill_hash") != skill_hash:
            fail(f"{campaign_id}: {name} was scored against a different skill tree")

        archived = RUNNER.archived_artifact_hashes(outdir, case)
        if archived is None or list(archived) != case.get("artifacts", []):
            fail(f"{campaign_id}: {name} declared artifacts are missing from the collection")
        for declared in case.get("artifacts", []):
            source = RUNNER.case_artifact_archive_path(outdir, name, declared)
            destination = target / "artifacts" / name / declared.replace("/", "__")
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

        ledger_case = {"name": name}
        for field in ("must_pass", "must_not"):
            verdicts = entry_scores.get(field)
            if not isinstance(verdicts, dict) or list(verdicts) != case[field]:
                fail(f"{campaign_id}: {name} {field} criteria differ from cases.json")
            if not all(type(value) is bool for value in verdicts.values()):
                fail(f"{campaign_id}: {name} still has unscored {field} criteria")
            rows = reviews[name].get(field)
            if not isinstance(rows, list) or [row.get("criterion") for row in rows] != case[field]:
                fail(f"{campaign_id}: {name} {field} review criteria differ from cases.json")
            for row in rows:
                criterion = row["criterion"]
                if row.get("verdict") is not verdicts[criterion]:
                    fail(f"{campaign_id}: {name} review and scores disagree on: {criterion}")
                quote = row.get("evidence_quote")
                if not isinstance(quote, str) or not quote.strip():
                    fail(f"{campaign_id}: {name} has no evidence for: {criterion}")
                if not quote_is_supported(quote, response):
                    fail(f"{campaign_id}: {name} quotes evidence that is not in the retained "
                         f"response for: {criterion}")
                if not isinstance(row.get("rationale"), str) or not row["rationale"].strip():
                    fail(f"{campaign_id}: {name} has no rationale for: {criterion}")
            ledger_case[field] = [
                {
                    "criterion": row["criterion"],
                    "verdict": row["verdict"],
                    "evidence_quote": row["evidence_quote"],
                    "rationale": row["rationale"],
                }
                for row in rows
            ]
        ledger_cases.append(ledger_case)

        if not all(entry_scores["must_pass"].values()) or any(entry_scores["must_not"].values()):
            failed_cases.append(name)

    (target / "responses.jsonl").write_text("\n".join(responses_lines) + "\n", encoding="utf-8")
    write_json(target / "scores.json", scores)
    write_json(target / "review-ledger.json", {
        "scoring_method": review["scoring_method"],
        "judge": judge,
        "semantics": review.get("semantics", {}),
        "cases": ledger_cases,
    })

    return {
        "id": campaign_id,
        **{field: metadata[field] for field in CAMPAIGN_FIELDS},
        "responses": f"{campaign_id}/responses.jsonl",
        "scores": f"{campaign_id}/scores.json",
        "review_ledger": f"{campaign_id}/review-ledger.json",
        "artifacts_dir": f"{campaign_id}/artifacts",
        "strict_pass": not failed_cases,
        "failed_case_ids": failed_cases,
    }


def cmd_build(args) -> int:
    config = read_json(Path(args.config).resolve())
    name = config.get("name")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9][a-z0-9._-]*", name or ""):
        fail("config 'name' must be a safe bundle directory name")
    into = Path(args.into).resolve() if args.into else (RESULTS_ROOT / name)
    base_commit = config.get("base_commit")
    if not isinstance(base_commit, str) or not re.fullmatch(r"[0-9a-f]{40}", base_commit or ""):
        fail("config 'base_commit' must be a full 40-character commit hash")
    campaigns = config.get("campaigns")
    if not isinstance(campaigns, list) or not campaigns:
        fail("config must list at least one campaign")

    cases = RUNNER.validated_cases()
    skill_hash = RUNNER.skill_hash()
    into.mkdir(parents=True, exist_ok=True)
    shutil.copy2(CASES_PATH, into / "cases.json")

    built = [build_campaign(entry, cases, into, skill_hash) for entry in campaigns]
    if len({entry["id"] for entry in built}) != len(built):
        fail("campaign ids must be unique")

    scoring = dict(config.get("scoring") or {})
    scoring.setdefault("method", SCORING_METHOD)
    if type(scoring.get("independent_human_review")) is not bool:
        fail("config scoring.independent_human_review must be a boolean")
    if scoring["independent_human_review"] and not str(
            scoring.get("human_review_record", "")).strip():
        fail("independent human review is claimed without a review record")

    collection = dict(config.get("collection") or {})
    collection.setdefault("repository_skill_authority", "skills/ieee-acm-paper-writing/SKILL.md")
    collection.setdefault("same_named_user_or_cached_copy_allowed", False)
    collection.setdefault("expected_routing_scored", False)
    # Derived, never declared by hand: every campaign carried a collection-time record.
    collection["skill_hash_captured_at_collection"] = True
    if type(collection.get("mechanical_authority_isolation")) is not bool:
        fail("config collection.mechanical_authority_isolation must be a boolean")

    manifest = {
        "schema_version": 1,
        "title": config.get("title") or f"{name} behavioral evidence",
        "base_commit": base_commit,
        "candidate": {
            "skill_hash": skill_hash,
            "cases_sha256": sha256_bytes(CASES_PATH.read_bytes()),
            "case_count": len(cases),
            "must_pass_criteria": sum(len(case["must_pass"]) for case in cases),
            "must_not_criteria": sum(len(case["must_not"]) for case in cases),
        },
        "collection": collection,
        "scoring": scoring,
        "campaigns": built,
    }
    write_json(into / "manifest.json", manifest)
    try:
        location = into.relative_to(ROOT)
    except ValueError:
        location = into
    print(f"bundle written to {location}")
    for entry in built:
        result = "strict pass" if entry["strict_pass"] else ", ".join(entry["failed_case_ids"])
        print(f"  {entry['id']}: {len(cases) - len(entry['failed_case_ids'])}/{len(cases)} "
              f"({result})")
    print("run scripts/validate_behavioral_evidence.py next; building is not release approval")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    p_scaffold = sub.add_parser("scaffold")
    p_scaffold.add_argument("--outdir", required=True)
    p_build = sub.add_parser("build")
    p_build.add_argument("--config", required=True)
    p_build.add_argument("--into")
    args = parser.parse_args()
    return {"scaffold": cmd_scaffold, "build": cmd_build}[args.mode](args)


if __name__ == "__main__":
    sys.exit(main())
