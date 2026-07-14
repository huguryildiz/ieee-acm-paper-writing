#!/usr/bin/env python3
"""Behavioral evaluation runner for the ieee-acm-paper-writing skill.

Standard library only. Cases live in cases.json (schema v2): each case has a
self-contained prompt, binary output-observable `must_pass` / `must_not`
criteria, and an informative `expected_routing` list (harness-level only,
never scored).

Modes
  validate                       Check cases.json against the v2 schema.
  list                           Print case names and criterion counts.
  collect --agent-cmd CMD        Run each case prompt through an agent command
          --outdir DIR           (prompt on stdin, output captured to
          [--case NAME]          DIR/<case>.md). CMD example:
                                 'claude -p' or 'codex exec'.
  score   --outdir DIR           Build DIR/scores.json listing every criterion.
          [--case NAME]          Verdicts are left null for manual scoring.
  report  --outdir DIR           Aggregate scores.json: a case passes only if
          [--strict]             all must_pass are true and all must_not are
                                 false. Prints per-case results and the
                                 aggregate with its denominator. --strict exits
                                 non-zero unless every defined case passes.

A single run per case is an existence check, not a statistical result; do not
report aggregate numbers without the denominator and the failed-case list.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CASES = HERE / "cases.json"
REFERENCES = HERE.parent / "skills" / "ieee-acm-paper-writing" / "references"

SKILL_PREAMBLE = (
    "You have the 'ieee-acm-paper-writing' agent skill installed. Read its "
    "SKILL.md first and follow it exactly, loading the reference files it "
    "routes to for this task. Then complete the task below and return the "
    "deliverable a user would see.\n\nTASK:\n"
)


def load_cases():
    data = json.loads(CASES.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("version") != 2:
        sys.exit("cases.json: expected schema version 2")
    if not isinstance(data.get("cases"), list):
        sys.exit("cases.json: 'cases' must be a list")
    return data["cases"]


def case_problems(cases):
    problems = []
    names = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            problems.append(f"case[{index}]: must be an object")
            continue
        name = case.get("name")
        if not isinstance(name, str) or not name.strip():
            problems.append(f"case[{index}]: name must be a non-empty string")
            name = f"case[{index}]"
        if name in names:
            problems.append(f"duplicate case name: {name}")
        names.add(name)
        if not str(case.get("prompt", "")).strip():
            problems.append(f"{name}: empty prompt")
        if not case.get("must_pass"):
            problems.append(f"{name}: must_pass is empty")
        for field in ("must_pass", "must_not", "expected_routing"):
            if field in case and not isinstance(case[field], list):
                problems.append(f"{name}: {field} must be a list")
            elif field in case and not all(
                    isinstance(item, str) and item.strip() for item in case[field]):
                problems.append(f"{name}: {field} entries must be non-empty strings")
        for ref in case.get("expected_routing", []):
            if isinstance(ref, str) and not (REFERENCES / ref).exists():
                problems.append(f"{name}: expected_routing references missing file: {ref}")
    return problems


def validated_cases():
    cases = load_cases()
    problems = case_problems(cases)
    if problems:
        sys.exit("cases.json invalid:\n  - " + "\n  - ".join(problems))
    return cases


def cmd_validate(_args):
    cases = load_cases()
    problems = case_problems(cases)
    if problems:
        print(f"FAIL: {len(problems)} problem(s)")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print(f"OK: {len(cases)} cases valid")


def cmd_list(_args):
    for case in validated_cases():
        print(f"{case['name']}: {len(case['must_pass'])} must_pass, "
              f"{len(case.get('must_not', []))} must_not")


def selected(cases, only):
    if only:
        matches = [c for c in cases if c["name"] == only]
        if not matches:
            sys.exit(f"no case named '{only}'")
        return matches
    return cases


def valid_verdict(value):
    return value is True or value is False or value is None


def cmd_collect(args):
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    failures = []
    for case in selected(validated_cases(), args.case):
        prompt = SKILL_PREAMBLE + case["prompt"]
        print(f"collect: {case['name']} ...", flush=True)
        output_file = outdir / f"{case['name']}.md"
        output_file.unlink(missing_ok=True)
        try:
            result = subprocess.run(args.agent_cmd, shell=True, input=prompt,
                                    capture_output=True, text=True, timeout=args.timeout)
        except subprocess.TimeoutExpired:
            failures.append(case["name"])
            print(f"  error: agent timed out after {args.timeout} s")
            continue
        if result.returncode != 0:
            failures.append(case["name"])
            print(f"  error: agent exited {result.returncode}; stderr head: "
                  f"{result.stderr[:200]}")
            continue
        output_file.write_text(result.stdout, encoding="utf-8")
    print(f"outputs in {outdir}")
    if failures:
        print(f"failed collections: {', '.join(failures)}")
        sys.exit(1)


def cmd_score(args):
    outdir = Path(args.outdir)
    scores_path = outdir / "scores.json"
    scores = json.loads(scores_path.read_text()) if scores_path.exists() else {}
    cases = validated_cases()
    valid_names = {case["name"] for case in cases}
    scores = {name: entry for name, entry in scores.items() if name in valid_names}
    for case in selected(cases, args.case):
        output_file = outdir / f"{case['name']}.md"
        if not output_file.exists():
            print(f"skip {case['name']}: no output file")
            scores.pop(case["name"], None)
            continue
        old_entry = scores.get(case["name"], {})
        entry = {"must_pass": {}, "must_not": {}}
        for field in ("must_pass", "must_not"):
            old_verdicts = old_entry.get(field, {})
            if not isinstance(old_verdicts, dict):
                old_verdicts = {}
            for criterion in case.get(field, []):
                verdict = old_verdicts.get(criterion)
                entry[field][criterion] = verdict if valid_verdict(verdict) else None
        scores[case["name"]] = entry
        print(f"scored: {case['name']}")
    scores_path.write_text(json.dumps(scores, indent=2), encoding="utf-8")
    print(f"scores in {scores_path}; replace null verdicts with true or false after manual review")


def cmd_report(args):
    scores_path = Path(args.outdir) / "scores.json"
    if not scores_path.exists():
        sys.exit(f"{scores_path} not found; run score first")
    scores = json.loads(scores_path.read_text(encoding="utf-8"))
    cases = validated_cases()
    total = len(cases)
    passed = unscored = missing = stale = 0
    failed_cases = []
    known_names = {case["name"] for case in cases}
    for case in cases:
        name = case["name"]
        entry = scores.get(name)
        if entry is None:
            missing += 1
            print(f"MISSING   {name}")
            continue
        expected = {field: set(case.get(field, [])) for field in ("must_pass", "must_not")}
        actual = {field: entry.get(field) for field in ("must_pass", "must_not")}
        if any(not isinstance(actual[field], dict) or set(actual[field]) != expected[field]
               for field in actual):
            stale += 1
            print(f"STALE     {name}")
            continue
        verdicts_pass = list(actual["must_pass"].values())
        verdicts_not = list(actual["must_not"].values())
        if any(not valid_verdict(value)
               for value in verdicts_pass + verdicts_not):
            stale += 1
            print(f"STALE     {name}")
            continue
        if None in verdicts_pass or None in verdicts_not:
            unscored += 1
            print(f"UNSCORED  {name}")
            continue
        ok = all(verdicts_pass) and not any(verdicts_not)
        if ok:
            passed += 1
            print(f"PASS      {name}")
        else:
            failed_cases.append(name)
            print(f"FAIL      {name}")
    unknown = sorted(set(scores) - known_names)
    for name in unknown:
        print(f"UNKNOWN   {name} (not counted)")
    print(f"\naggregate: {passed}/{total} cases passed "
          f"({len(failed_cases)} failed, {unscored} unscored, {missing} missing, "
          f"{stale} stale; rule: all must_pass true AND all must_not false)")
    if failed_cases:
        print(f"failed: {', '.join(failed_cases)}")
    if args.strict and passed != total:
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="mode", required=True)
    sub.add_parser("validate")
    sub.add_parser("list")
    p_collect = sub.add_parser("collect")
    p_collect.add_argument("--agent-cmd", required=True)
    p_collect.add_argument("--outdir", required=True)
    p_collect.add_argument("--case")
    p_collect.add_argument("--timeout", type=int, default=600)
    p_score = sub.add_parser("score")
    p_score.add_argument("--outdir", required=True)
    p_score.add_argument("--case")
    p_report = sub.add_parser("report")
    p_report.add_argument("--outdir", required=True)
    p_report.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    {"validate": cmd_validate, "list": cmd_list, "collect": cmd_collect,
     "score": cmd_score, "report": cmd_report}[args.mode](args)


if __name__ == "__main__":
    main()
