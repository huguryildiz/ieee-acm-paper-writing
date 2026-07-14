#!/usr/bin/env python3
"""Repository validator for the ieee-acm-paper-writing skill.

Standard library only (no PyYAML). Checks:
  1. SKILL.md frontmatter: strict flat syntax, allowed keys, name and description limits.
  2. corpus-calibration.md excludes direct source identities and identifiers.
  3. Relative links and images in the selected repository Markdown files resolve.
  4. evals/cases.json parses, uses safe case names, and matches the v2 schema.
  5. agents/openai.yaml exists and is non-empty.

Usage:  python3 scripts/validate_skill.py [repo_root]
Exit status: 0 if all checks pass, 1 otherwise.
"""

import csv
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ALLOWED_FRONTMATTER_KEYS = {"name", "description"}
MAX_NAME = 64
MAX_DESCRIPTION = 1024
CASE_NAME_RE = re.compile(r"[a-z0-9][a-z0-9_-]*")

MD_FILES = [
    "CLAUDE.md",
    "README.md",
    "CHANGELOG.md",
    "docs/papers/README.md",
    "skills/ieee-acm-paper-writing/SKILL.md",
]
MD_GLOBS = [
    "docs/guides/*.md",
    "skills/ieee-acm-paper-writing/references/*.md",
    "skills/ieee-acm-paper-writing/examples/*.md",
    "evals/comparisons/*.md",
    "evals/results/*.md",
]

errors = []


def err(msg):
    errors.append(msg)


def check_frontmatter(skill_md: Path):
    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        err(f"{skill_md}: missing or malformed YAML frontmatter")
        return
    keys = {}
    for line_number, line in enumerate(m.group(1).splitlines(), start=2):
        if not line.strip():
            continue
        if line.startswith((" ", "\t")):
            err(f"{skill_md}:{line_number}: nested or indented frontmatter is unsupported")
            continue
        km = re.fullmatch(r"([A-Za-z-]+):[ ]*(.*)", line)
        if not km:
            err(f"{skill_md}:{line_number}: malformed frontmatter line")
            continue
        key = km.group(1)
        if key in keys:
            err(f"{skill_md}: duplicate frontmatter key '{key}'")
        keys[key] = km.group(2).strip()
    unexpected = set(keys) - ALLOWED_FRONTMATTER_KEYS
    if unexpected:
        err(f"{skill_md}: unexpected frontmatter keys: {sorted(unexpected)}")
    for required in ("name", "description"):
        if required not in keys or not keys[required]:
            err(f"{skill_md}: missing frontmatter key '{required}'")
    name = keys.get("name", "")
    if name:
        if not re.fullmatch(r"[a-z0-9-]+", name) or name.startswith("-") or name.endswith("-") or "--" in name:
            err(f"{skill_md}: name '{name}' is not valid hyphen-case")
        if len(name) > MAX_NAME:
            err(f"{skill_md}: name exceeds {MAX_NAME} characters")
    desc = keys.get("description", "")
    if desc:
        if len(desc) > MAX_DESCRIPTION:
            err(f"{skill_md}: description exceeds {MAX_DESCRIPTION} characters ({len(desc)})")
        if "<" in desc or ">" in desc:
            err(f"{skill_md}: description contains angle brackets")


def check_calibration(root: Path):
    calibration = root / "skills" / "ieee-acm-paper-writing" / "references" / "corpus-calibration.md"
    catalog = root / "docs" / "papers" / "catalog.tsv"
    if not calibration.exists():
        err("skills/ieee-acm-paper-writing/references/corpus-calibration.md: missing")
        return
    if not catalog.exists():
        err("docs/papers/catalog.tsv: missing; cannot enforce calibration identity policy")
        return

    text = calibration.read_text(encoding="utf-8")
    relative = calibration.relative_to(root)
    direct_patterns = {
        "DOI": r"\b10\.\d{4,9}/[^\s<>()]+",
        "arXiv identifier": r"\barXiv\s*:\s*\d{4}\.\d{4,5}\b",
        "source year": r"\b(?:19|20)\d{2}\b",
    }
    for label, pattern in direct_patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            err(f"{relative}: prohibited {label} in calibration -> {match.group(0)}")

    author_terms = set()
    title_terms = set()
    doi_terms = set()
    with catalog.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            author_year = (row.get("author_year") or "").strip()
            author_text = re.sub(r"\s+(?:19|20)\d{2}$", "", author_year)
            author_text = re.sub(r"\s+et al\.$", "", author_text)
            for term in re.split(r"\s+and\s+|,", author_text):
                if term.strip():
                    author_terms.add(term.strip())
            if (row.get("title") or "").strip():
                title_terms.add(row["title"].strip())
            if (row.get("doi") or "").strip():
                doi_terms.add(row["doi"].strip())

    for label, terms in (("catalog author", author_terms),
                         ("catalog title", title_terms),
                         ("catalog identifier", doi_terms)):
        for term in sorted(terms, key=len, reverse=True):
            if re.search(rf"(?<!\w){re.escape(term)}(?!\w)", text, re.IGNORECASE):
                err(f"{relative}: prohibited {label} in calibration -> {term}")
                break


def iter_md_files(root: Path):
    seen = set()
    for rel in MD_FILES:
        p = root / rel
        if p.exists():
            seen.add(p)
    for pattern in MD_GLOBS:
        for p in root.glob(pattern):
            seen.add(p)
    return sorted(seen)


def markdown_targets(text):
    targets = []
    patterns = (
        re.compile(r"!?\[[^\]]*\]\(([^)\n]+)\)"),
        re.compile(r"^\s*\[[^\]]+\]:\s*(?:<([^>]+)>|(\S+))", re.MULTILINE),
        re.compile(r"\b(?:href|src)\s*=\s*['\"]([^'\"]+)['\"]", re.IGNORECASE),
    )
    for pattern in patterns:
        for match in pattern.finditer(text):
            target = next((group for group in match.groups() if group), None)
            if target:
                target = target.strip()
                if target.startswith("<") and target.endswith(">"):
                    target = target[1:-1]
                elif " " in target:
                    target = target.split()[0]
                targets.append(target)
    return targets


def heading_anchors(text):
    anchors = set()
    counts = {}
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        heading = match.group(1)
        heading = re.sub(r"!?\[([^\]]+)\]\([^)]+\)", r"\1", heading)
        heading = re.sub(r"<[^>]+>", "", heading)
        heading = heading.replace("`", "").lower()
        slug = re.sub(r"[^\w\- ]", "", heading, flags=re.UNICODE)
        slug = re.sub(r"\s+", "-", slug.strip())
        if not slug:
            continue
        duplicate = counts.get(slug, 0)
        counts[slug] = duplicate + 1
        anchors.add(slug if duplicate == 0 else f"{slug}-{duplicate}")
    return anchors


def check_links(root: Path):
    for md in iter_md_files(root):
        text = md.read_text(encoding="utf-8")
        for target in markdown_targets(text):
            if not target or target.startswith(("http://", "https://", "mailto:", "//")):
                continue
            path_text, separator, fragment = target.partition("#")
            path_text = unquote(path_text.split("?", 1)[0])
            resolved = md if not path_text else (md.parent / path_text).resolve()
            if not resolved.exists():
                err(f"{md.relative_to(root)}: broken relative link -> {target}")
                continue
            if separator and fragment and resolved.suffix.lower() == ".md":
                anchors = heading_anchors(resolved.read_text(encoding="utf-8"))
                if unquote(fragment).lower() not in anchors:
                    err(f"{md.relative_to(root)}: broken Markdown anchor -> {target}")


def check_cases(root: Path):
    cases_path = root / "evals" / "cases.json"
    if not cases_path.exists():
        err("evals/cases.json: missing")
        return
    try:
        data = json.loads(cases_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        err(f"evals/cases.json: invalid JSON ({exc})")
        return
    if not isinstance(data, dict) or data.get("version") != 2:
        err("evals/cases.json: expected top-level object with version == 2")
        return
    references_dir = root / "skills" / "ieee-acm-paper-writing" / "references"
    names = set()
    cases = data.get("cases")
    if not isinstance(cases, list):
        err("evals/cases.json: 'cases' must be a list")
        return
    for i, case in enumerate(cases):
        if not isinstance(case, dict):
            err(f"evals/cases.json: case[{i}] must be an object")
            continue
        name = case.get("name")
        if not isinstance(name, str) or not name.strip():
            err(f"evals/cases.json: case[{i}]: 'name' must be a non-empty string")
            label = f"case[{i}]"
        else:
            label = name
            if not CASE_NAME_RE.fullmatch(name):
                err(f"evals/cases.json: {label}: name must match {CASE_NAME_RE.pattern!r}")
        if label in names:
            err(f"evals/cases.json: duplicate case name '{label}'")
        names.add(label)
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            err(f"evals/cases.json: {label}: missing or empty prompt")
        for field in ("must_pass", "must_not", "expected_routing"):
            value = case.get(field)
            if not isinstance(value, list) or (field == "must_pass" and not value):
                requirement = "a non-empty list" if field == "must_pass" else "a list"
                err(f"evals/cases.json: {label}: '{field}' must be {requirement}")
                continue
            if not all(isinstance(item, str) and item.strip() for item in value):
                err(f"evals/cases.json: {label}: '{field}' entries must be non-empty strings")
        routing = case.get("expected_routing")
        if isinstance(routing, list):
            for ref in routing:
                if isinstance(ref, str) and not (references_dir / ref).exists():
                    err(f"evals/cases.json: {label}: expected_routing references missing file '{ref}'")
    if not cases:
        err("evals/cases.json: no cases defined")


def check_agent_interface(root: Path):
    yaml_path = root / "skills" / "ieee-acm-paper-writing" / "agents" / "openai.yaml"
    if not yaml_path.exists() or not yaml_path.read_text(encoding="utf-8").strip():
        err("skills/ieee-acm-paper-writing/agents/openai.yaml: missing or empty")
        return
    text = yaml_path.read_text(encoding="utf-8")
    if not re.match(r"^interface:\s*$", text.splitlines()[0]):
        err("skills/ieee-acm-paper-writing/agents/openai.yaml: expected top-level interface mapping")
        return
    values = {}
    for line in text.splitlines()[1:]:
        match = re.match(r'^  ([a-z_]+):\s+"([^"\n]*)"\s*$', line)
        if not match:
            err(f"skills/ieee-acm-paper-writing/agents/openai.yaml: malformed line: {line}")
            continue
        key, value = match.groups()
        if key in values:
            err(f"skills/ieee-acm-paper-writing/agents/openai.yaml: duplicate key '{key}'")
        values[key] = value
    for required in ("display_name", "short_description", "default_prompt"):
        if not values.get(required):
            err(f"skills/ieee-acm-paper-writing/agents/openai.yaml: missing '{required}'")
    description = values.get("short_description", "")
    if description and not 25 <= len(description) <= 64:
        err("skills/ieee-acm-paper-writing/agents/openai.yaml: short_description must be 25-64 characters")
    prompt = values.get("default_prompt", "")
    if prompt and "$ieee-acm-paper-writing" not in prompt:
        err("skills/ieee-acm-paper-writing/agents/openai.yaml: default_prompt must mention $ieee-acm-paper-writing")


def main():
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    skill_md = root / "skills" / "ieee-acm-paper-writing" / "SKILL.md"
    if not skill_md.exists():
        err(f"{skill_md}: not found (is '{root}' the repo root?)")
    else:
        check_frontmatter(skill_md)
        check_calibration(root)
        check_links(root)
        check_cases(root)
        check_agent_interface(root)
    if errors:
        print(f"FAIL: {len(errors)} problem(s)")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("OK: frontmatter, calibration policy, links, eval cases, and agent interface all valid")


if __name__ == "__main__":
    main()
