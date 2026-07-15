#!/usr/bin/env python3
"""Render a self-contained section-audit HTML map from validated JSON.

The renderer performs presentation only. It does not infer findings, rewrite claims,
or fill missing evidence. Python 3 standard library only.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional


SCHEMA_VERSION = 1
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")
LAYERS = {
    "scientific-support": {
        "code": "S",
        "class": "s",
        "name": "Scientific support",
        "description": "claims vs. evidence",
    },
    "method-domain": {
        "code": "M",
        "class": "m",
        "name": "Method / domain reporting",
        "description": "reproducibility and disclosure",
    },
    "venue-compliance": {
        "code": "V",
        "class": "v",
        "name": "Venue compliance",
        "description": "verified house rules",
    },
}
SEVERITIES = {"Critical", "Major", "Minor", "Editorial"}
DISPOSITIONS = {
    "rewrite": "Evidence-scoped rewrite",
    "remove": "Remove unsupported statement",
    "author-query": "External author query",
    "retain": "Retain with verified scope",
    "verify": "Verification required",
}
TOP_LEVEL_DEFAULTS = {
    "eyebrow": "IEEE / ACM manuscript audit",
    "source_label": "Audited source",
    "revision_label": "Evidence-scoped response",
    "footer": (
        "Select a numbered finding to isolate its source sentence and bounded response. "
        "The HTML is a presentation of the canonical text audit and adds no scientific finding."
    ),
}
REQUIRED_TOP_LEVEL = ("title", "subject", "summary", "findings")
REQUIRED_FINDING_FIELDS = (
    "id",
    "layer",
    "severity",
    "title",
    "location",
    "source",
    "evidence",
    "consequence",
    "correction",
    "disposition",
)


class RenderError(ValueError):
    """Raised when an audit-map input violates the renderer contract."""


def require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RenderError(f"{label} must be a non-empty string")
    return value.strip()


def validate_document(raw: Any) -> Dict[str, Any]:
    if not isinstance(raw, dict):
        raise RenderError("top-level JSON value must be an object")
    if raw.get("version") != SCHEMA_VERSION:
        raise RenderError(f"version must equal {SCHEMA_VERSION}")

    document = dict(TOP_LEVEL_DEFAULTS)
    for field in REQUIRED_TOP_LEVEL:
        if field not in raw:
            raise RenderError(f"missing top-level field: {field}")
    for field in ("title", "subject", "summary"):
        document[field] = require_text(raw[field], field)
    for field in TOP_LEVEL_DEFAULTS:
        document[field] = require_text(raw.get(field, document[field]), field)

    findings = raw["findings"]
    if not isinstance(findings, list):
        raise RenderError("findings must be a list")

    normalized: List[Dict[str, str]] = []
    seen_ids = set()
    for index, item in enumerate(findings):
        label = f"findings[{index}]"
        if not isinstance(item, dict):
            raise RenderError(f"{label} must be an object")
        missing = [field for field in REQUIRED_FINDING_FIELDS if field not in item]
        if missing:
            raise RenderError(f"{label} missing fields: {', '.join(missing)}")
        finding = {
            field: require_text(item[field], f"{label}.{field}")
            for field in REQUIRED_FINDING_FIELDS
        }
        if not ID_RE.fullmatch(finding["id"]):
            raise RenderError(f"{label}.id must match {ID_RE.pattern!r}")
        if finding["id"] in seen_ids:
            raise RenderError(f"duplicate finding id: {finding['id']}")
        seen_ids.add(finding["id"])
        if finding["layer"] not in LAYERS:
            raise RenderError(
                f"{label}.layer must be one of: {', '.join(LAYERS)}"
            )
        if finding["severity"] not in SEVERITIES:
            raise RenderError(
                f"{label}.severity must be one of: {', '.join(sorted(SEVERITIES))}"
            )
        if finding["disposition"] not in DISPOSITIONS:
            raise RenderError(
                f"{label}.disposition must be one of: {', '.join(DISPOSITIONS)}"
            )
        normalized.append(finding)

    document["version"] = SCHEMA_VERSION
    document["findings"] = normalized
    return document


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def prose(value: str) -> str:
    return esc(value).replace("\n", "<br>\n")


def render_legend(findings: List[Dict[str, str]]) -> str:
    counts = {layer: 0 for layer in LAYERS}
    for finding in findings:
        counts[finding["layer"]] += 1
    chunks = []
    for layer_id, meta in LAYERS.items():
        count = counts[layer_id]
        count_text = f"{count} finding" if count == 1 else f"{count} findings"
        if count == 0:
            count_text = "0 · not exercised"
        chunks.append(
            f'<span class="layer-chip {meta["class"]}">'
            f'<span class="layer-code">{meta["code"]}</span>'
            f'<span class="layer-name">{esc(meta["name"])}</span>'
            f'<span class="layer-count">{esc(count_text)} · {esc(meta["description"])}</span>'
            "</span>"
        )
    return "\n    ".join(chunks)


def render_answer_key(findings: List[Dict[str, str]]) -> str:
    if not findings:
        return '<li class="key"><span class="key-title">No findings supplied</span></li>'
    chunks = []
    for finding in findings:
        meta = LAYERS[finding["layer"]]
        fid = finding["id"]
        chunks.append(
            f'<li><button class="key" type="button" data-finding="{esc(fid)}" '
            f'aria-controls="finding-{esc(fid)}">'
            f'<span class="finding-number {meta["class"]}">{esc(fid)}</span>'
            '<span>'
            f'<span class="key-title">{esc(finding["title"])}</span>'
            f'<span class="key-layer">{meta["code"]} · {esc(meta["name"])}</span>'
            "</span></button></li>"
        )
    return "\n        ".join(chunks)


def render_findings(findings: List[Dict[str, str]]) -> str:
    if not findings:
        return (
            '<div class="empty"><strong>No findings were supplied.</strong><br>'
            "Every concern layer remains not exercised; this does not imply that the manuscript passed.</div>"
        )
    chunks = []
    for finding in findings:
        meta = LAYERS[finding["layer"]]
        fid = finding["id"]
        chunks.append(
            f'<article class="finding-pair" id="finding-{esc(fid)}" data-finding="{esc(fid)}">\n'
            f'  <section class="panel" data-layer="{esc(finding["layer"])}" '
            f'aria-label="Finding {esc(fid)} source">\n'
            '    <div class="panel-head">\n'
            f'      <span class="badge {meta["class"]}">{esc(fid)}</span>\n'
            '      <div>\n'
            f'        <h2 class="finding-title">{esc(finding["title"])}</h2>\n'
            f'        <div class="location">{esc(finding["location"])}</div>\n'
            '      </div>\n'
            f'      <span class="severity">{esc(finding["severity"])}</span>\n'
            '    </div>\n'
            '    <div class="panel-body">\n'
            f'      <blockquote>{prose(finding["source"])}</blockquote>\n'
            '      <p class="analysis-label">Contradicted or missing evidence</p>\n'
            f'      <p class="analysis-text">{prose(finding["evidence"])}</p>\n'
            '      <p class="analysis-label">Scientific consequence</p>\n'
            f'      <p class="analysis-text">{prose(finding["consequence"])}</p>\n'
            '    </div>\n'
            '  </section>\n'
            f'  <section class="panel fix" data-layer="{esc(finding["layer"])}" '
            f'aria-label="Finding {esc(fid)} response">\n'
            '    <div class="panel-head">\n'
            f'      <span class="badge {meta["class"]}">{esc(fid)}</span>\n'
            '      <div>\n'
            '        <h2 class="finding-title">Bounded response</h2>\n'
            f'        <div class="location">{esc(meta["name"])}</div>\n'
            '      </div>\n'
            '    </div>\n'
            '    <div class="panel-body">\n'
            f'      <span class="disposition">{esc(DISPOSITIONS[finding["disposition"]])}</span>\n'
            f'      <p class="correction">{prose(finding["correction"])}</p>\n'
            '    </div>\n'
            '  </section>\n'
            '</article>'
        )
    return "\n      ".join(chunks)


def finding_data(findings: List[Dict[str, str]]) -> str:
    data = {
        finding["id"]: {
            "layer": LAYERS[finding["layer"]]["code"],
            "title": finding["title"],
        }
        for finding in findings
    }
    encoded = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return encoded.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")


def render_document(raw: Any, template_path: Optional[Path] = None) -> str:
    document = validate_document(raw)
    if template_path is None:
        template_path = Path(__file__).resolve().parent.parent / "assets" / "section-audit-map-template.html"
    try:
        template = template_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RenderError(f"cannot read template {template_path}: {exc}") from exc

    findings = document["findings"]
    replacements = {
        "@@DOCUMENT_TITLE@@": esc(f'{document["title"]} — {document["subject"]}'),
        "@@EYEBROW@@": esc(document["eyebrow"]),
        "@@TITLE@@": esc(document["title"]),
        "@@SUBJECT@@": esc(document["subject"]),
        "@@SUMMARY@@": prose(document["summary"]),
        "@@LAYER_LEGEND@@": render_legend(findings),
        "@@ANSWER_KEY@@": render_answer_key(findings),
        "@@FINDING_ROWS@@": render_findings(findings),
        "@@FINDING_COUNT@@": str(len(findings)),
        "@@SOURCE_LABEL@@": esc(document["source_label"]),
        "@@REVISION_LABEL@@": esc(document["revision_label"]),
        "@@FOOTER@@": prose(document["footer"]),
        "@@FINDING_DATA@@": finding_data(findings),
    }
    for token, value in replacements.items():
        template = template.replace(token, value)
    unresolved = sorted(set(re.findall(r"@@[A-Z_]+@@", template)))
    if unresolved:
        raise RenderError(f"template contains unresolved tokens: {', '.join(unresolved)}")
    return template.rstrip() + "\n"


def load_json(path_text: str) -> Any:
    try:
        if path_text == "-":
            return json.load(sys.stdin)
        return json.loads(Path(path_text).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, RecursionError) as exc:
        raise RenderError(f"cannot load JSON input: {exc}") from exc


def write_atomic(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise RenderError(f"output exists; pass --force only with explicit overwrite approval: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            handle.write(content)
            temp_name = handle.name
        os.replace(temp_name, path)
        path.chmod(0o644)
    finally:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render a self-contained HTML presentation of a canonical text audit."
    )
    parser.add_argument("input", help="audit-map JSON path, or - for stdin")
    parser.add_argument("--out", "-o", help="output HTML path; defaults to INPUT with .html suffix")
    parser.add_argument("--check", action="store_true", help="validate and render in memory without writing")
    parser.add_argument("--force", action="store_true", help="overwrite an existing output file")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        raw = load_json(args.input)
        rendered = render_document(raw)
        finding_count = len(validate_document(raw)["findings"])
        if args.check:
            print(f"OK: version {SCHEMA_VERSION}, {finding_count} findings, HTML renderable")
            return 0
        if args.out:
            output = Path(args.out)
        elif args.input == "-":
            raise RenderError("--out is required when input is read from stdin")
        else:
            output = Path(args.input).with_suffix(".html")
        write_atomic(output, rendered, args.force)
        print(f"Wrote {output} ({finding_count} findings)")
        return 0
    except RenderError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
