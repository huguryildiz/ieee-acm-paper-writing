#!/usr/bin/env python3
"""Repository validator for the ieee-acm-paper-writing skill.

Standard library only (no PyYAML). Checks:
  1. SKILL.md frontmatter: strict flat syntax, allowed keys, name and description limits.
  2. corpus-calibration.md excludes direct source identities and identifiers.
  3. Relative links and images resolve and do not depend on untracked local files.
  4. evals/cases.json parses, uses safe case names, and matches the v2 schema.
  5. Eval criteria share no distinctive 6-word phrase with any skill file (M5 guard).
  6. agents/openai.yaml exists and is non-empty.
  6b. Claude Code plugin and marketplace manifests are valid and version-aligned.
  7. The audit-map renderer accepts each example JSON and reproduces its checked-in HTML.
  8. The interactive showcase stays self-contained (no external asset fetch) and intact.

Usage:  python3 scripts/validate_skill.py [repo_root]
Exit status: 0 if all checks pass, 1 otherwise.
"""

import csv
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote

ALLOWED_FRONTMATTER_KEYS = {"name", "description"}
MAX_NAME = 64
MAX_DESCRIPTION = 1024
CASE_NAME_RE = re.compile(r"[a-z0-9][a-z0-9_-]*")
REQUIRED_EVAL_MODES = {
    "draft", "rewrite", "expand", "compress", "humanize", "outline",
    "audit", "section-audit", "venue-adapt",
}
REQUIRED_EVAL_MODIFIERS = {"html-map"}

MD_FILES = [
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


def tracked_files(root: Path):
    """Return resolved tracked file paths when root is a Git worktree."""
    if not (root / ".git").exists():
        return None
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return {
        (root / relative).resolve()
        for relative in result.stdout.split("\0")
        if relative
    }


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
    tracked = tracked_files(root)
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
            if tracked is not None and resolved.is_file() and resolved not in tracked:
                err(f"{md.relative_to(root)}: relative link targets untracked file -> {target}")
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
        artifacts = case.get("artifacts", [])
        if not isinstance(artifacts, list):
            err(f"evals/cases.json: {label}: 'artifacts' must be a list when present")
        elif not all(isinstance(artifact, str) for artifact in artifacts):
            err(f"evals/cases.json: {label}: 'artifacts' entries must be strings")
        elif len(set(artifacts)) != len(artifacts):
            err(f"evals/cases.json: {label}: 'artifacts' entries must be unique")
        else:
            for artifact in artifacts:
                valid = (
                    isinstance(artifact, str)
                    and artifact
                    and "\\" not in artifact
                    and not Path(artifact).is_absolute()
                    and ".." not in Path(artifact).parts
                    and Path(artifact).parts[:2] == ("tmp", "evals")
                    and len(Path(artifact).parts) > 2
                )
                if not valid:
                    err(
                        f"evals/cases.json: {label}: artifact paths must be safe relative "
                        f"paths below tmp/evals: {artifact!r}"
                    )
    if not cases:
        err("evals/cases.json: no cases defined")
        return

    coverage = data.get("coverage")
    if not isinstance(coverage, dict):
        err("evals/cases.json: 'coverage' must be an object")
        return
    for group, required in (("modes", REQUIRED_EVAL_MODES),
                            ("modifiers", REQUIRED_EVAL_MODIFIERS)):
        mapping = coverage.get(group)
        if not isinstance(mapping, dict):
            err(f"evals/cases.json: coverage.{group} must be an object")
            continue
        for surface in sorted(required):
            covered_by = mapping.get(surface)
            if not isinstance(covered_by, list) or not covered_by:
                err(
                    f"evals/cases.json: coverage.{group}.{surface} must name at least one case"
                )
                continue
            unknown = [case_name for case_name in covered_by if case_name not in names]
            if unknown:
                err(
                    f"evals/cases.json: coverage.{group}.{surface} references unknown cases: "
                    + ", ".join(unknown)
                )


def check_readme_case_count(root: Path):
    readme = root / "README.md"
    cases_path = root / "evals" / "cases.json"
    if not readme.exists() or not cases_path.exists():
        return
    try:
        count = len(json.loads(cases_path.read_text(encoding="utf-8")).get("cases", []))
    except (json.JSONDecodeError, AttributeError):
        return  # check_cases reports the underlying schema problem
    match = re.search(r"behavioral suite defines (\d+) self-contained", readme.read_text(encoding="utf-8"))
    if not match:
        err("README.md: missing behavioral-suite case count")
    elif int(match.group(1)) != count:
        err(f"README.md: behavioral-suite count is {match.group(1)}, but evals/cases.json has {count}")


def _criteria_ngrams(text, n=6):
    words = re.findall(r"[a-z0-9']+", text.lower())
    return {" ".join(words[i : i + n]) for i in range(len(words) - n + 1)}


def check_criteria_independence(root: Path):
    """Eval criteria must not share a distinctive 6-word phrase with any skill file.

    A criterion copied near-verbatim from a reference the agent loads lets a model
    pass by echoing skill text rather than demonstrating the behavior. This guards
    the M5 contamination invariant so it cannot silently regress when cases change.
    """
    cases_path = root / "evals" / "cases.json"
    if not cases_path.exists():
        return
    try:
        data = json.loads(cases_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return  # check_cases already reports the parse failure
    skill = root / "skills" / "ieee-acm-paper-writing"
    skill_grams = set()
    for md in skill.rglob("*.md"):
        skill_grams |= _criteria_ngrams(md.read_text(encoding="utf-8"))
    for case in data.get("cases", []):
        if not isinstance(case, dict):
            continue
        label = case.get("name", "?")
        for field in ("must_pass", "must_not"):
            for item in case.get(field, []) or []:
                if not isinstance(item, str):
                    continue
                overlap = _criteria_ngrams(item) & skill_grams
                if overlap:
                    sample = sorted(overlap)[0]
                    err(
                        f"evals/cases.json: {label}: '{field}' criterion shares a 6-word "
                        f"phrase with a skill file (e.g. {sample!r}); rephrase independently"
                    )


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
    if prompt and "@ieee-acm-paper-writing" not in prompt:
        err("skills/ieee-acm-paper-writing/agents/openai.yaml: default_prompt must mention @ieee-acm-paper-writing")


def check_claude_plugin_package(root: Path):
    """Validate the Claude Code plugin manifest, marketplace entry, and version agreement.

    The Claude Code install path is a session command, so no CI job can exercise it. This
    check gates the two manifests it depends on and keeps their version aligned with the
    Codex manifest and the release the README pins.
    """
    plugin_path = root / ".claude-plugin" / "plugin.json"
    market_path = root / ".claude-plugin" / "marketplace.json"
    codex_path = root / "plugins" / "ieee-acm-paper-writing" / ".codex-plugin" / "plugin.json"
    documents = {}
    for label, path in (
        ("plugin.json", plugin_path),
        ("marketplace.json", market_path),
        ("codex plugin.json", codex_path),
    ):
        if not path.is_file():
            err(f"{path.relative_to(root)}: missing plugin manifest")
            return
        try:
            documents[label] = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            err(f"{path.relative_to(root)}: invalid JSON: {exc}")
            return

    plugin = documents["plugin.json"]
    for field in ("name", "version", "description", "license", "repository"):
        if not isinstance(plugin.get(field), str) or not plugin[field].strip():
            err(f".claude-plugin/plugin.json: '{field}' must be a non-empty string")
    if plugin.get("name") != "ieee-acm-paper-writing":
        err(".claude-plugin/plugin.json: name must equal the skill directory name")

    market = documents["marketplace.json"]
    entries = market.get("plugins")
    if not isinstance(entries, list) or len(entries) != 1:
        err(".claude-plugin/marketplace.json: 'plugins' must list exactly one entry")
        return
    entry = entries[0]
    if not isinstance(entry, dict):
        err(".claude-plugin/marketplace.json: plugin entry must be an object")
        return
    if entry.get("name") != plugin.get("name"):
        err(".claude-plugin/marketplace.json: entry name must match plugin.json name")
    source = entry.get("source")
    if not isinstance(source, str) or not source.strip():
        err(".claude-plugin/marketplace.json: entry must declare a non-empty 'source'")
    elif not (root / source).is_dir():
        err(f".claude-plugin/marketplace.json: source does not resolve to a directory: {source}")
    elif not (root / source / "skills" / "ieee-acm-paper-writing" / "SKILL.md").is_file():
        err(f".claude-plugin/marketplace.json: source {source} contains no installable skill")
    owner = market.get("owner")
    if not isinstance(owner, dict) or not owner.get("name"):
        err(".claude-plugin/marketplace.json: 'owner.name' is required")

    versions = {
        ".claude-plugin/plugin.json": plugin.get("version"),
        ".claude-plugin/marketplace.json (metadata)": (market.get("metadata") or {}).get("version"),
        ".claude-plugin/marketplace.json (entry)": entry.get("version"),
        ".codex-plugin/plugin.json": documents["codex plugin.json"].get("version"),
    }
    distinct = {value for value in versions.values() if value is not None}
    if len(distinct) > 1:
        detail = ", ".join(f"{name}={value!r}" for name, value in versions.items())
        err(f"plugin manifests disagree on version: {detail}")
    declared = plugin.get("version")
    readme = (root / "README.md").read_text(encoding="utf-8")
    if isinstance(declared, str):
        prerelease = "-" in declared.partition("+")[0]
        if prerelease:
            if declared not in readme:
                err(f"README.md does not identify rolling plugin candidate {declared}")
            stable = r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
            stable_patterns = {
                "versioned skills installer and stable release URL": (
                    rf"npx\s+skills@\d+\.\d+\.\d+\s+add\s+"
                    rf"https://github\.com/huguryildiz/ieee-acm-paper-writing/tree/v({stable})"
                    r"(?![-+0-9A-Za-z.])"
                ),
                "manual stable release archive": (
                    rf"archive/refs/tags/v({stable})\.tar\.gz"
                ),
                "stable-pinned workbench clone": (
                    rf"git clone --branch v({stable})(?![-+0-9A-Za-z.]) --depth 1"
                ),
            }
            stable_versions = []
            for label, pattern in stable_patterns.items():
                match = re.search(pattern, readme)
                if not match:
                    err(f"README.md has no {label} while manifests declare {declared}")
                else:
                    stable_versions.append(match.group(1))
            if len(set(stable_versions)) > 1:
                err("README.md stable install channels disagree on release version")
        else:
            release = re.escape(declared)
            required_patterns = {
                "versioned skills installer and release URL": (
                    rf"npx\s+skills@\d+\.\d+\.\d+\s+add\s+"
                    rf"https://github\.com/huguryildiz/ieee-acm-paper-writing/tree/v{release}\b"
                ),
                "manual release archive": rf"archive/refs/tags/v{release}\.tar\.gz",
                "release-pinned workbench clone": rf"git clone --branch v{release} --depth 1",
            }
            for label, pattern in required_patterns.items():
                if not re.search(pattern, readme):
                    err(
                        f"README.md has no {label} for declared plugin version v{declared}; "
                        "tag the release and update every stable install channel"
                    )


def check_audit_map_renderer(root: Path):
    skill = root / "skills" / "ieee-acm-paper-writing"
    renderer = skill / "scripts" / "render_audit_map.py"
    template = skill / "assets" / "section-audit-map-template.html"
    example_pairs = (
        (
            skill / "examples" / "section-audit-map.json",
            skill / "examples" / "section-audit-map-rendered.html",
        ),
        (
            skill / "examples" / "method-reproducibility-audit-map.json",
            skill / "examples" / "method-reproducibility-audit-map.html",
        ),
        (
            skill / "examples" / "venue-adaptation-audit-map.json",
            skill / "examples" / "venue-adaptation-audit-map.html",
        ),
    )
    for path in (renderer, template, *(item for pair in example_pairs for item in pair)):
        if not path.is_file():
            err(f"{path.relative_to(root)}: missing audit-map renderer artifact")
            return
    with tempfile.TemporaryDirectory() as tmp:
        for example_json, example_html in example_pairs:
            output = Path(tmp) / example_html.name
            result = subprocess.run(
                [
                    sys.executable,
                    str(renderer),
                    str(example_json),
                    "--out",
                    str(output),
                    "--workspace-root",
                    tmp,
                ],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                detail = result.stderr.strip() or result.stdout.strip() or "unknown renderer failure"
                err(f"audit-map renderer rejected {example_json.name}: {detail}")
                continue
            if output.read_bytes() != example_html.read_bytes():
                err(f"{example_html.relative_to(root)}: stale renderer output")


# Tokens that only appear when an interactive page pulls an asset from a remote
# host at load time. The showcase embeds all fonts as data: URIs, so any of these
# would be a regression against the "self-contained, no external assets" guarantee.
EXTERNAL_ASSET_TOKENS = (
    "fonts.googleapis.com",
    "fonts.gstatic.com",
    'rel="preconnect"',
    'rel=\\"preconnect\\"',
    '@import',
)


def check_audit_map_showcase(root: Path):
    """The published showcase must be canonical renderer output and self-contained.

    The hosted page ships this file, so a hand-edited or re-exported copy would put
    content on the web that no renderer check covers. Pinning it to the deterministic
    fixture makes any divergence — including a stale copy carrying an outdated
    template — a validation failure, and the token scan still rejects a re-export
    that reintroduces a remote font fetch.
    """
    examples = root / "skills" / "ieee-acm-paper-writing" / "examples"
    showcase = examples / "section-audit-map.html"
    fixture = examples / "section-audit-map-rendered.html"
    rel = showcase.relative_to(root)
    if not showcase.is_file() or not showcase.read_text(encoding="utf-8").strip():
        err(f"{rel}: missing or empty interactive showcase")
        return
    text = showcase.read_text(encoding="utf-8")
    for token in EXTERNAL_ASSET_TOKENS:
        if token in text:
            err(f"{rel}: external asset dependency reintroduced ({token}); must stay self-contained")
    if not fixture.is_file():
        err(f"{fixture.relative_to(root)}: missing renderer fixture for the showcase")
        return
    if showcase.read_bytes() != fixture.read_bytes():
        err(f"{rel}: showcase differs from {fixture.name}; re-render it from section-audit-map.json")


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
        check_readme_case_count(root)
        check_criteria_independence(root)
        check_agent_interface(root)
        check_claude_plugin_package(root)
        check_audit_map_renderer(root)
        check_audit_map_showcase(root)
    if errors:
        print(f"FAIL: {len(errors)} problem(s)")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print(
        "OK: frontmatter, calibration policy, links, eval cases, criteria independence, "
        "agent interface, Claude plugin manifests, and audit map valid"
    )


if __name__ == "__main__":
    main()
