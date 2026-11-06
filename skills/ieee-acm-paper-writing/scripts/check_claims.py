#!/usr/bin/env python3
"""Check a claim-ledger JSON against the artifacts it points to.

The agent writes the ledger; this tool alone assigns check levels. It verifies that
cited keys exist in the supplied .bib, that each quote occurs in the supplied source PDF,
and that each reported own-result value occurs in its artifact. It never judges whether a
quote supports a claim: the agent's judgment is carried through as model-judged, pending
human confirmation. No network access. Python 3 standard library; quote checks use the
external `pdftotext` (Poppler) when it is installed and report `not-checked` otherwise.

Exit status: 0 = no contradiction found, 1 = at least one key, quote, or value failed to
match, 2 = invalid ledger or usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


SCHEMA_VERSION = 1
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")
CLAIM_TYPES = {"literature", "own-result", "assumption"}
JUDGMENTS = {"supports", "partial", "contradicts", "not-found", "not-assessed"}
CLAIM_FIELDS = {"id", "text", "location", "type", "evidence", "judgment"}
LITERATURE_EVIDENCE_FIELDS = {"cite_key", "source_pdf", "page", "quote"}
RESULT_EVIDENCE_FIELDS = {"artifact", "value"}
MIN_QUOTE_WORDS = 6
FAILING = {"key-missing", "quote-mismatch", "value-mismatch"}


class LedgerError(ValueError):
    pass


def require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LedgerError(f"{label} must be a non-empty string")
    return value


def validate_ledger(raw: Any) -> Dict[str, Any]:
    if not isinstance(raw, dict):
        raise LedgerError("top-level JSON value must be an object")
    if raw.get("version") != SCHEMA_VERSION:
        raise LedgerError(f"version must equal {SCHEMA_VERSION}")
    unknown = set(raw) - {"version", "manuscript", "bib", "claims"}
    if unknown:
        raise LedgerError(f"unknown top-level fields: {', '.join(sorted(unknown))}")
    if "bib" in raw:
        require_text(raw["bib"], "bib")
    claims = raw.get("claims")
    if not isinstance(claims, list) or not claims:
        raise LedgerError("claims must be a non-empty list")
    seen = set()
    for index, claim in enumerate(claims, start=1):
        label = f"claims[{index}]"
        if not isinstance(claim, dict):
            raise LedgerError(f"{label} must be an object")
        extra = set(claim) - CLAIM_FIELDS
        if extra:
            # Check levels are computed here; a ledger must not pre-stamp them.
            raise LedgerError(f"{label} has fields the agent may not set: {', '.join(sorted(extra))}")
        missing = CLAIM_FIELDS - set(claim)
        if missing:
            raise LedgerError(f"{label} missing fields: {', '.join(sorted(missing))}")
        for field in ("id", "text", "location"):
            require_text(claim[field], f"{label}.{field}")
        if not ID_RE.fullmatch(claim["id"]) or claim["id"] in seen:
            raise LedgerError(f"{label}.id must be unique and match {ID_RE.pattern!r}")
        seen.add(claim["id"])
        if claim["type"] not in CLAIM_TYPES:
            raise LedgerError(f"{label}.type must be one of: {', '.join(sorted(CLAIM_TYPES))}")
        if claim["judgment"] not in JUDGMENTS:
            raise LedgerError(f"{label}.judgment must be one of: {', '.join(sorted(JUDGMENTS))}")
        if not isinstance(claim["evidence"], list):
            raise LedgerError(f"{label}.evidence must be a list (empty when none is supplied)")
        for e_index, item in enumerate(claim["evidence"], start=1):
            validate_evidence(item, claim["type"], f"{label}.evidence[{e_index}]")
    return raw


def validate_evidence(item: Any, claim_type: str, label: str) -> None:
    if not isinstance(item, dict):
        raise LedgerError(f"{label} must be an object")
    if claim_type == "literature":
        extra = set(item) - LITERATURE_EVIDENCE_FIELDS
        if extra or "cite_key" not in item:
            raise LedgerError(f"{label} needs cite_key and allows only: "
                              f"{', '.join(sorted(LITERATURE_EVIDENCE_FIELDS))}")
        require_text(item["cite_key"], f"{label}.cite_key")
        if "quote" in item:
            quote = require_text(item["quote"], f"{label}.quote")
            if "source_pdf" not in item:
                raise LedgerError(f"{label}.quote requires source_pdf")
            if len(quote.split()) < MIN_QUOTE_WORDS:
                raise LedgerError(f"{label}.quote must have at least {MIN_QUOTE_WORDS} words")
        if "source_pdf" in item:
            require_text(item["source_pdf"], f"{label}.source_pdf")
        if "page" in item and (not isinstance(item["page"], int) or item["page"] < 1):
            raise LedgerError(f"{label}.page must be a positive integer")
    elif claim_type == "own-result":
        if set(item) != RESULT_EVIDENCE_FIELDS:
            raise LedgerError(f"{label} needs exactly: artifact, value")
        require_text(item["artifact"], f"{label}.artifact")
        require_text(item["value"], f"{label}.value")
    else:
        raise LedgerError(f"{label}: assumption claims carry no evidence items")


def whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def normalized(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)
    for old, new in (("‘", "'"), ("’", "'"), ("“", '"'), ("”", '"')):
        text = text.replace(old, new)
    return whitespace(text).lower()


def alnum(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", normalized(text))


def match_level(quote: str, source: str) -> str:
    """Strongest textual match of quote in source: exact, normalized, weak, or none."""
    if whitespace(quote) in whitespace(source):
        return "exact"
    if normalized(quote) in normalized(source):
        return "normalized"
    if alnum(quote) in alnum(source):
        return "weak"
    return "none"


def bib_keys(path: Path) -> set:
    text = path.read_text(encoding="utf-8", errors="replace")
    return set(re.findall(r"@\w+\s*[{(]\s*([^,\s]+)\s*,", text))


def pdf_text(pdf: Path, page: Optional[int]) -> str:
    command = ["pdftotext", "-q"]
    if page is not None:
        command += ["-f", str(page), "-l", str(page)]
    result = subprocess.run(command + [str(pdf), "-"], capture_output=True, text=True)
    if result.returncode != 0:
        raise OSError(f"pdftotext failed on {pdf}")
    return result.stdout


def check_literature(item: Dict[str, Any], keys: Optional[set], base: Path,
                     have_pdftotext: bool) -> Tuple[str, str]:
    if keys is not None and item["cite_key"] not in keys:
        return "key-missing", f"{item['cite_key']} not in bib"
    if "quote" not in item:
        return "cited", "no quote supplied"
    pdf = base / item["source_pdf"]
    if not pdf.is_file():
        return "cited", f"source PDF not found: {item['source_pdf']}"
    if not have_pdftotext:
        return "cited", "quote not-checked: pdftotext unavailable"
    page = item.get("page")
    level = match_level(item["quote"], pdf_text(pdf, page))
    note = f"page {page}" if page else "whole document"
    if level == "none" and page is not None:
        if match_level(item["quote"], pdf_text(pdf, None)) in {"exact", "normalized"}:
            return "quote-mismatch", f"quote found, but not on stated page {page}"
    if level in {"exact", "normalized"}:
        return "quote-anchored", f"{level} match, {note}"
    if level == "weak":
        return "quote-weak", f"matches only after removing punctuation and symbols, {note}"
    return "quote-mismatch", f"quote not found, {note}"


def check_result(item: Dict[str, str], base: Path) -> Tuple[str, str]:
    artifact = base / item["artifact"]
    if not artifact.is_file():
        return "unresolved", f"artifact not found: {item['artifact']}"
    text = artifact.read_text(encoding="utf-8", errors="replace")
    pattern = r"(?<![\w.])" + re.escape(item["value"]) + r"(?![\w]|\.\d)"
    if re.search(pattern, text):
        return "value-matched", f"value {item['value']} present in {item['artifact']}"
    return "value-mismatch", f"value {item['value']} absent from {item['artifact']}"


RANK = {"key-missing": 0, "quote-mismatch": 0, "value-mismatch": 0, "unresolved": 1,
        "cited": 2, "quote-weak": 3, "quote-anchored": 4, "value-matched": 4}


def check_ledger(ledger: Dict[str, Any], base: Path,
                 have_pdftotext: Optional[bool] = None) -> List[Dict[str, Any]]:
    if have_pdftotext is None:
        have_pdftotext = shutil.which("pdftotext") is not None
    keys = None
    if "bib" in ledger:
        bib = base / ledger["bib"]
        if not bib.is_file():
            raise LedgerError(f"bib file not found: {ledger['bib']}")
        keys = bib_keys(bib)
    report = []
    for claim in ledger["claims"]:
        items = []
        for item in claim["evidence"]:
            if claim["type"] == "literature":
                level, note = check_literature(item, keys, base, have_pdftotext)
            else:
                level, note = check_result(item, base)
            items.append({"level": level, "note": note})
        if claim["type"] == "assumption":
            level = "assumption"
        elif not items:
            level = "unresolved"
        else:
            level = min((i["level"] for i in items), key=RANK.__getitem__)
        support = ("not applicable" if claim["type"] != "literature"
                   else f"model-judged: {claim['judgment']}; human confirmation pending")
        report.append({"id": claim["id"], "type": claim["type"], "level": level,
                       "support": support, "evidence": items})
    return report


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("ledger", help="claim-ledger JSON; relative paths resolve beside it")
    parser.add_argument("--out", help="write the checked report as JSON to this path")
    parser.add_argument("--force", action="store_true",
                        help="overwrite --out; pass only with explicit approval")
    args = parser.parse_args(argv)
    ledger_path = Path(args.ledger)
    try:
        ledger = validate_ledger(json.loads(ledger_path.read_text(encoding="utf-8")))
        report = check_ledger(ledger, ledger_path.resolve().parent)
    except (OSError, json.JSONDecodeError, LedgerError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if any("pdftotext unavailable" in i["note"] for row in report for i in row["evidence"]):
        print("NOTE: quotes were not checked because pdftotext (Poppler) is not installed. "
              "Install it, then rerun: macOS `brew install poppler`; Debian/Ubuntu "
              "`sudo apt-get install poppler-utils`; Fedora `sudo dnf install poppler-utils`; "
              "conda `conda install -c conda-forge poppler`.", file=sys.stderr)
    for row in report:
        notes = "; ".join(i["note"] for i in row["evidence"]) or "no evidence supplied"
        print(f"{row['id']}\t{row['level']}\t{row['support']}\t{notes}")
    if args.out:
        out = Path(args.out)
        if out.exists() and not args.force:
            print(f"ERROR: output exists; pass --force only with explicit approval: {out}",
                  file=sys.stderr)
            return 2
        out.write_text(json.dumps({"version": SCHEMA_VERSION, "claims": report},
                                  indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 1 if any(row["level"] in FAILING for row in report) else 0


if __name__ == "__main__":
    raise SystemExit(main())
