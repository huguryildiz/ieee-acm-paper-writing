#!/usr/bin/env python3
"""Build the dependency-free Vercel showcase from tracked source artifacts."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_SOURCE = ROOT / "site"
SITE_OUTPUT = ROOT / "site-dist"
EXAMPLES = ROOT / "skills" / "ieee-acm-paper-writing" / "examples"


def build_site() -> None:
    if SITE_OUTPUT.exists():
        shutil.rmtree(SITE_OUTPUT)

    shutil.copytree(SITE_SOURCE, SITE_OUTPUT)
    shutil.copytree(ROOT / "assets", SITE_OUTPUT / "assets")

    output_examples = SITE_OUTPUT / "examples"
    output_examples.mkdir()
    for name in ("section-audit-map.html", "section-audit-map.json"):
        shutil.copy2(EXAMPLES / name, output_examples / name)


if __name__ == "__main__":
    build_site()
