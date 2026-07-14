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
          [--judge-cmd CMD]      With --judge-cmd, each criterion is judged
          [--case NAME]          automatically: the judge receives the
                                 criterion and the agent output on stdin and
                                 must answer PASS or FAIL as its first token.
                                 Without it, verdicts are left null for manual
                                 or LLM-assisted scoring.
  report  --outdir DIR           Aggregate scores.json: a case passes only if
          [--strict]             all must_pass are true and all must_not are
                                 false. Prints per-case results and the
                                 aggregate with its denominator. --strict exits
                                 non-zero on any failed or unscored case.

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

SKILL_PREAMBLE = (
    "You have the 'ieee-acm-paper-writing' agent skill installed. Read its "
    "SKILL.md first and follow it exactly, loading the reference files it "
    "routes to for this task. Then complete the task below and return the "
    "deliverable a user would see.\n\nTASK:\n"
)


def load_cases():
    data = json.loads(CASES.read_text(encoding="utf-8"))
    if data.get("version") != 2:
        sys.exit("cases.json: expected schema version 2")
    return data["cases"]


def cmd_validate(_args):
    cases = load_cases()
    problems = []
    names = set()
    for case in cases:
        name = case.get("name", "<unnamed>")
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
    if problems:
        print(f"FAIL: {len(problems)} problem(s)")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print(f"OK: {len(cases)} cases valid")


def cmd_list(_args):
    for case in load_cases():
        print(f"{case['name']}: {len(case['must_pass'])} must_pass, "
              f"{len(case.get('must_not', []))} must_not")


def selected(cases, only):
    if only:
        matches = [c for c in cases if c["name"] == only]
        if not matches:
            sys.exit(f"no case named '{only}'")
        return matches
    return cases


def cmd_collect(args):
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    for case in selected(load_cases(), args.case):
        prompt = SKILL_PREAMBLE + case["prompt"]
        print(f"collect: {case['name']} ...", flush=True)
        result = subprocess.run(args.agent_cmd, shell=True, input=prompt,
                                capture_output=True, text=True, timeout=args.timeout)
        (outdir / f"{case['name']}.md").write_text(result.stdout, encoding="utf-8")
        if result.returncode != 0:
            print(f"  warning: agent exited {result.returncode}; stderr head: "
                  f"{result.stderr[:200]}")
    print(f"outputs in {outdir}")


def judge(judge_cmd, criterion, polarity, output, timeout):
    prompt = (
        "You are scoring one binary criterion against an agent's output. "
        f"Criterion ({polarity}): {criterion}\n\n"
        "Answer with exactly PASS if the criterion holds true of the output, "
        "or FAIL if it does not. First token only.\n\n"
        f"--- AGENT OUTPUT ---\n{output}"
    )
    result = subprocess.run(judge_cmd, shell=True, input=prompt,
                            capture_output=True, text=True, timeout=timeout)
    token = (result.stdout.strip().split() or [""])[0].upper()
    if token in ("PASS", "FAIL"):
        return token == "PASS"
    return None


def cmd_score(args):
    outdir = Path(args.outdir)
    scores_path = outdir / "scores.json"
    scores = json.loads(scores_path.read_text()) if scores_path.exists() else {}
    for case in selected(load_cases(), args.case):
        output_file = outdir / f"{case['name']}.md"
        if not output_file.exists():
            print(f"skip {case['name']}: no output file")
            continue
        output = output_file.read_text(encoding="utf-8")
        entry = scores.setdefault(case["name"], {"must_pass": {}, "must_not": {}})
        for field in ("must_pass", "must_not"):
            for criterion in case.get(field, []):
                if entry[field].get(criterion) is not None:
                    continue
                verdict = None
                if args.judge_cmd:
                    verdict = judge(args.judge_cmd, criterion, field, output, args.timeout)
                entry[field][criterion] = verdict
        print(f"scored: {case['name']}")
    scores_path.write_text(json.dumps(scores, indent=2), encoding="utf-8")
    print(f"scores in {scores_path}; null verdicts need manual/judge scoring")


def cmd_report(args):
    scores_path = Path(args.outdir) / "scores.json"
    if not scores_path.exists():
        sys.exit(f"{scores_path} not found; run score first")
    scores = json.loads(scores_path.read_text(encoding="utf-8"))
    total = passed = unscored = 0
    failed_cases = []
    for name, entry in scores.items():
        verdicts_pass = list(entry.get("must_pass", {}).values())
        verdicts_not = list(entry.get("must_not", {}).values())
        total += 1
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
    print(f"\naggregate: {passed}/{total} cases passed "
          f"({unscored} unscored; rule: all must_pass true AND all must_not false)")
    if failed_cases:
        print(f"failed: {', '.join(failed_cases)}")
    if args.strict and (failed_cases or unscored):
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
    p_score.add_argument("--judge-cmd")
    p_score.add_argument("--case")
    p_score.add_argument("--timeout", type=int, default=300)
    p_report = sub.add_parser("report")
    p_report.add_argument("--outdir", required=True)
    p_report.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    {"validate": cmd_validate, "list": cmd_list, "collect": cmd_collect,
     "score": cmd_score, "report": cmd_report}[args.mode](args)


if __name__ == "__main__":
    main()
