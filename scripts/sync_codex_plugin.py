#!/usr/bin/env python3
"""Build or check the install-safe Codex plugin snapshot."""

from __future__ import annotations

import argparse
import shutil
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SKILL = ROOT / "skills" / "ieee-acm-paper-writing"
PLUGIN_ROOT = ROOT / "plugins" / "ieee-acm-paper-writing"
PACKAGED_SKILL = PLUGIN_ROOT / "skills" / "ieee-acm-paper-writing"
SOURCE_ICON = ROOT / "assets" / "icon.svg"
PACKAGED_ICON = PLUGIN_ROOT / "assets" / "icon.svg"
IGNORED_NAMES = {".DS_Store", ".pytest_cache", "__pycache__"}


def _ignored(path: Path, root: Path) -> bool:
    return any(part in IGNORED_NAMES for part in path.relative_to(root).parts)


def tree_files(root: Path) -> tuple[dict[Path, bytes], list[Path]]:
    """Return regular-file content and symlinks, excluding local cache artifacts."""
    files: dict[Path, bytes] = {}
    symlinks: list[Path] = []
    if not root.is_dir():
        return files, symlinks
    for path in sorted(root.rglob("*")):
        if _ignored(path, root):
            continue
        relative = path.relative_to(root)
        if path.is_symlink():
            symlinks.append(relative)
        elif path.is_file():
            files[relative] = path.read_bytes()
    return files, symlinks


def compare_trees(source: Path, packaged: Path) -> list[str]:
    source_files, source_links = tree_files(source)
    packaged_files, packaged_links = tree_files(packaged)
    errors: list[str] = []
    if source_links:
        errors.append("canonical skill contains symlinks: " + ", ".join(map(str, source_links)))
    if packaged_links:
        errors.append("plugin snapshot contains symlinks: " + ", ".join(map(str, packaged_links)))
    for relative in sorted(source_files.keys() - packaged_files.keys()):
        errors.append(f"plugin snapshot is missing {relative}")
    for relative in sorted(packaged_files.keys() - source_files.keys()):
        errors.append(f"plugin snapshot has stale file {relative}")
    for relative in sorted(source_files.keys() & packaged_files.keys()):
        if source_files[relative] != packaged_files[relative]:
            errors.append(f"plugin snapshot differs at {relative}")
    return errors


def package_errors() -> list[str]:
    errors = compare_trees(SOURCE_SKILL, PACKAGED_SKILL)
    if not SOURCE_ICON.is_file():
        errors.append("assets/icon.svg is missing")
    elif not PACKAGED_ICON.is_file():
        errors.append("plugin package is missing assets/icon.svg")
    elif SOURCE_ICON.read_bytes() != PACKAGED_ICON.read_bytes():
        errors.append("plugin package icon differs from assets/icon.svg")
    return errors


def _copy_ignore(_directory: str, names: list[str]) -> set[str]:
    return set(names) & IGNORED_NAMES


def write_snapshot() -> None:
    if not SOURCE_SKILL.is_dir():
        raise SystemExit(f"canonical skill is missing: {SOURCE_SKILL}")
    PLUGIN_ROOT.mkdir(parents=True, exist_ok=True)
    (PLUGIN_ROOT / "skills").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="codex-plugin-snapshot-", dir=PLUGIN_ROOT.parent) as tmp:
        staged = Path(tmp) / "ieee-acm-paper-writing"
        shutil.copytree(SOURCE_SKILL, staged, ignore=_copy_ignore)
        if PACKAGED_SKILL.exists():
            backup = Path(tmp) / "previous-snapshot"
            PACKAGED_SKILL.rename(backup)
            try:
                staged.rename(PACKAGED_SKILL)
            except Exception:
                backup.rename(PACKAGED_SKILL)
                raise
        else:
            staged.rename(PACKAGED_SKILL)
    PACKAGED_ICON.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE_ICON, PACKAGED_ICON)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="replace the packaged snapshot with the canonical skill and icon",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.write:
        write_snapshot()
    errors = package_errors()
    if errors:
        print("Codex plugin snapshot check failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"Codex plugin snapshot is synchronized: {PLUGIN_ROOT}")


if __name__ == "__main__":
    main()
