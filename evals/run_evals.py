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
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
CASES = HERE / "cases.json"
REFERENCES = HERE.parent / "skills" / "ieee-acm-paper-writing" / "references"
SKILL_DIR = HERE.parent / "skills" / "ieee-acm-paper-writing"
CASE_NAME_RE = re.compile(r"[a-z0-9][a-z0-9_-]*")
REQUIRED_MODES = (
    "draft", "rewrite", "expand", "compress", "humanize", "outline",
    "audit", "section-audit", "venue-adapt",
)
REQUIRED_MODIFIERS = ("html-map",)

SKILL_PREAMBLE = (
    "For this evaluation, the sole authoritative skill copy is the repository-local "
    "'skills/ieee-acm-paper-writing/SKILL.md'. Do not use a user-level, global, cached, "
    "or otherwise installed copy with the same name. Read that exact SKILL.md first and "
    "follow it exactly, resolving every routed reference relative to its directory. Then "
    "complete the task below and return the deliverable a user would see.\n\nTASK:\n"
)


def load_document():
    data = json.loads(CASES.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("version") != 2:
        sys.exit("cases.json: expected schema version 2")
    if not isinstance(data.get("cases"), list):
        sys.exit("cases.json: 'cases' must be a list")
    return data


def load_cases():
    return load_document()["cases"]


def valid_artifact_path(value):
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return (
        not path.is_absolute()
        and ".." not in path.parts
        and len(path.parts) > 2
        and path.parts[:2] == ("tmp", "evals")
    )


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
        elif not CASE_NAME_RE.fullmatch(name):
            problems.append(
                f"{name}: name must match {CASE_NAME_RE.pattern!r}"
            )
        if name in names:
            problems.append(f"duplicate case name: {name}")
        names.add(name)
        prompt = case.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            problems.append(f"{name}: prompt must be a non-empty string")
        for field in ("must_pass", "must_not", "expected_routing"):
            if field not in case:
                problems.append(f"{name}: {field} is required")
            elif not isinstance(case[field], list):
                problems.append(f"{name}: {field} must be a list")
            elif field == "must_pass" and not case[field]:
                problems.append(f"{name}: must_pass must be a non-empty list")
            elif not all(
                    isinstance(item, str) and item.strip() for item in case[field]):
                problems.append(f"{name}: {field} entries must be non-empty strings")
        routing = case.get("expected_routing")
        if isinstance(routing, list):
            for ref in routing:
                if isinstance(ref, str) and not (REFERENCES / ref).exists():
                    problems.append(f"{name}: expected_routing references missing file: {ref}")
        artifacts = case.get("artifacts", [])
        if not isinstance(artifacts, list):
            problems.append(f"{name}: artifacts must be a list when present")
        elif not all(isinstance(artifact, str) for artifact in artifacts):
            problems.append(f"{name}: artifacts entries must be strings")
        elif len(set(artifacts)) != len(artifacts):
            problems.append(f"{name}: artifacts entries must be unique")
        else:
            for artifact in artifacts:
                if not valid_artifact_path(artifact):
                    problems.append(
                        f"{name}: artifact paths must be safe relative paths below tmp/evals: "
                        f"{artifact!r}"
                    )
    return problems


def coverage_problems(data, cases):
    problems = []
    coverage = data.get("coverage")
    if not isinstance(coverage, dict):
        return ["coverage must be an object"]
    known = {case.get("name") for case in cases if isinstance(case, dict)}
    for group, required in (("modes", REQUIRED_MODES),
                            ("modifiers", REQUIRED_MODIFIERS)):
        mapping = coverage.get(group)
        if not isinstance(mapping, dict):
            problems.append(f"coverage.{group} must be an object")
            continue
        for name in required:
            case_names = mapping.get(name)
            if not isinstance(case_names, list) or not case_names:
                problems.append(f"coverage.{group}.{name} must name at least one case")
                continue
            missing = [case_name for case_name in case_names if case_name not in known]
            if missing:
                problems.append(
                    f"coverage.{group}.{name} references unknown cases: "
                    + ", ".join(missing)
                )
    return problems


def validated_cases():
    data = load_document()
    cases = data["cases"]
    problems = case_problems(cases) + coverage_problems(data, cases)
    if problems:
        sys.exit("cases.json invalid:\n  - " + "\n  - ".join(problems))
    return cases


def cmd_validate(_args):
    data = load_document()
    cases = data["cases"]
    problems = case_problems(cases) + coverage_problems(data, cases)
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


def case_output_path(outdir, name):
    """Return a case output path contained directly within outdir."""
    root = Path(outdir).resolve()
    candidate = (root / f"{name}.md").resolve()
    if candidate.parent != root:
        raise ValueError(f"unsafe case output path for {name!r}")
    return candidate


def valid_verdict(value):
    return value is True or value is False or value is None


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def case_hash(case):
    scored_contract = {
        "name": case["name"],
        "prompt": case["prompt"],
        "must_pass": case["must_pass"],
        "must_not": case["must_not"],
        "artifacts": case.get("artifacts", []),
    }
    encoded = json.dumps(
        scored_contract, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(encoded)


def output_hash(path):
    return sha256_bytes(path.read_bytes())


def case_artifact_source_path(declared):
    root = HERE.parent.resolve()
    safe_root = (root / "tmp" / "evals").resolve()
    candidate = root.joinpath(*PurePosixPath(declared).parts)
    try:
        candidate.parent.resolve().relative_to(safe_root)
    except ValueError as exc:
        raise ValueError(f"unsafe declared artifact path: {declared!r}") from exc
    return candidate


def case_artifact_archive_path(outdir, case_name, declared):
    safe_name = declared.replace("/", "__")
    root = Path(outdir).resolve() / "artifacts" / case_name
    candidate = (root / safe_name).resolve()
    if candidate.parent != root.resolve():
        raise ValueError(f"unsafe artifact archive path: {declared!r}")
    return candidate


def archived_artifact_hashes(outdir, case):
    hashes = {}
    for declared in case.get("artifacts", []):
        archived = case_artifact_archive_path(outdir, case["name"], declared)
        if not archived.is_file():
            return None
        hashes[declared] = output_hash(archived)
    return hashes


def skill_hash():
    files = [SKILL_DIR / "SKILL.md", SKILL_DIR / "LICENSE",
             SKILL_DIR / "agents" / "openai.yaml"]
    files.extend(sorted((SKILL_DIR / "examples").glob("*.md")))
    files.extend(sorted((SKILL_DIR / "references").glob("*.md")))
    # Non-Markdown audit-map assets a section-audit case can depend on.
    files.extend(sorted((SKILL_DIR / "examples").glob("section-audit-map.*")))
    files.extend(sorted((SKILL_DIR / "assets").glob("*.html")))
    digest = hashlib.sha256()
    for path in files:
        if not path.is_file():
            continue
        digest.update(path.relative_to(SKILL_DIR).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def cmd_collect(args):
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    failures = []
    for case in selected(validated_cases(), args.case):
        prompt = SKILL_PREAMBLE + case["prompt"]
        print(f"collect: {case['name']} ...", flush=True)
        output_file = case_output_path(outdir, case["name"])
        declared_artifacts = case.get("artifacts", [])
        source_artifacts = [case_artifact_source_path(item) for item in declared_artifacts]
        existing = [str(path.relative_to(HERE.parent)) for path in source_artifacts if path.exists()]
        if existing:
            failures.append(case["name"])
            print("  error: declared artifact path already exists; remove before collection: "
                  + ", ".join(existing))
            continue
        try:
            result = subprocess.run(
                args.agent_cmd, shell=True, input=prompt, capture_output=True,
                text=True, timeout=args.timeout, cwd=HERE.parent,
            )
        except subprocess.TimeoutExpired:
            failures.append(case["name"])
            print(f"  error: agent timed out after {args.timeout} s")
            for source in source_artifacts:
                if source.is_file() and not source.is_symlink():
                    source.unlink()
            continue
        if result.returncode != 0:
            failures.append(case["name"])
            print(f"  error: agent exited {result.returncode}; stderr head: "
                  f"{result.stderr[:200]}")
            for source in source_artifacts:
                if source.is_file() and not source.is_symlink():
                    source.unlink()
            continue
        if not result.stdout.strip():
            failures.append(case["name"])
            print("  error: agent returned an empty response")
            for source in source_artifacts:
                if source.is_file() and not source.is_symlink():
                    source.unlink()
            continue
        artifact_problem = None
        for declared, source in zip(declared_artifacts, source_artifacts):
            if not source.is_file() or source.is_symlink():
                artifact_problem = f"missing or unsafe declared artifact: {declared}"
                break
            try:
                source.resolve().relative_to((HERE.parent / "tmp" / "evals").resolve())
            except ValueError:
                artifact_problem = f"declared artifact escaped tmp/evals: {declared}"
                break
        if artifact_problem:
            failures.append(case["name"])
            print(f"  error: {artifact_problem}")
            for source in source_artifacts:
                if source.is_file() and not source.is_symlink():
                    source.unlink()
            continue
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                    mode="w", encoding="utf-8", dir=outdir,
                    prefix=f".{case['name']}.", suffix=".tmp", delete=False) as handle:
                handle.write(result.stdout)
                temporary = Path(handle.name)
            for declared, source in zip(declared_artifacts, source_artifacts):
                archived = case_artifact_archive_path(outdir, case["name"], declared)
                archived.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, archived)
            temporary.replace(output_file)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
            for source in source_artifacts:
                if source.is_file() and not source.is_symlink():
                    source.unlink()
    print(f"outputs in {outdir}")
    if failures:
        print(f"failed collections: {', '.join(failures)}")
        sys.exit(1)


def cmd_score(args):
    outdir = Path(args.outdir)
    scores_path = outdir / "scores.json"
    scores = json.loads(scores_path.read_text()) if scores_path.exists() else {}
    if not isinstance(scores, dict):
        sys.exit(f"{scores_path}: expected a JSON object keyed by case name")
    cases = validated_cases()
    current_skill_hash = skill_hash()
    valid_names = {case["name"] for case in cases}
    scores = {name: entry for name, entry in scores.items() if name in valid_names}
    for case in selected(cases, args.case):
        output_file = case_output_path(outdir, case["name"])
        if not output_file.exists():
            print(f"skip {case['name']}: no output file")
            scores.pop(case["name"], None)
            continue
        if not output_file.read_bytes().strip():
            print(f"skip {case['name']}: empty output file")
            scores.pop(case["name"], None)
            continue
        current_artifact_hashes = archived_artifact_hashes(outdir, case)
        if current_artifact_hashes is None:
            print(f"skip {case['name']}: missing declared artifact")
            scores.pop(case["name"], None)
            continue
        old_entry = scores.get(case["name"], {})
        current_case_hash = case_hash(case)
        current_output_hash = output_hash(output_file)
        preserve = (
            isinstance(old_entry, dict)
            and old_entry.get("case_hash") == current_case_hash
            and old_entry.get("output_hash") == current_output_hash
            and old_entry.get("skill_hash") == current_skill_hash
            and old_entry.get("artifact_hashes", {}) == current_artifact_hashes
        )
        entry = {
            "case_hash": current_case_hash,
            "output_hash": current_output_hash,
            "skill_hash": current_skill_hash,
            "artifact_hashes": current_artifact_hashes,
            "must_pass": {},
            "must_not": {},
        }
        for field in ("must_pass", "must_not"):
            old_verdicts = old_entry.get(field, {}) if preserve else {}
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
    if not isinstance(scores, dict):
        sys.exit(f"{scores_path}: expected a JSON object keyed by case name")
    cases = validated_cases()
    current_skill_hash = skill_hash()
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
        output_file = case_output_path(args.outdir, name)
        if not output_file.exists():
            missing += 1
            print(f"MISSING   {name} (agent output)")
            continue
        if not output_file.read_bytes().strip():
            missing += 1
            print(f"MISSING   {name} (empty agent output)")
            continue
        if not isinstance(entry, dict):
            stale += 1
            print(f"STALE     {name}")
            continue
        if (entry.get("case_hash") != case_hash(case)
                or entry.get("output_hash") != output_hash(output_file)
                or entry.get("skill_hash") != current_skill_hash
                or entry.get("artifact_hashes", {}) != archived_artifact_hashes(args.outdir, case)):
            stale += 1
            print(f"STALE     {name}")
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
