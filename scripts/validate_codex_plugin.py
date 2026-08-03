#!/usr/bin/env python3
"""Validate the repository's dependency-free Codex plugin package contract."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from sync_codex_plugin import PLUGIN_ROOT, ROOT, package_errors


PLUGIN_NAME = "ieee-acm-paper-writing"
MANIFEST = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
MANIFEST_FIELDS = {
    "author",
    "description",
    "homepage",
    "interface",
    "keywords",
    "license",
    "name",
    "repository",
    "skills",
    "version",
}
INTERFACE_FIELDS = {
    "brandColor",
    "capabilities",
    "category",
    "composerIcon",
    "defaultPrompt",
    "developerName",
    "displayName",
    "logo",
    "longDescription",
    "shortDescription",
    "websiteURL",
}


def _load_object(path: Path, errors: list[str]) -> dict[str, Any] | None:
    if not path.is_file():
        errors.append(f"missing {path.relative_to(ROOT)}")
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{path.relative_to(ROOT)} is invalid JSON: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)} must contain a JSON object")
        return None
    return value


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _check_asset(raw_path: Any, field: str, errors: list[str]) -> None:
    if not _non_empty_string(raw_path):
        errors.append(f"interface.{field} must be a non-empty relative path")
        return
    relative = Path(raw_path)
    if relative.is_absolute() or ".." in relative.parts:
        errors.append(f"interface.{field} must stay inside the plugin package")
        return
    candidate = (PLUGIN_ROOT / relative).resolve()
    if not candidate.is_relative_to(PLUGIN_ROOT.resolve()) or not candidate.is_file():
        errors.append(f"interface.{field} points to a missing plugin asset")


def validate_manifest(errors: list[str]) -> None:
    manifest = _load_object(MANIFEST, errors)
    if manifest is None:
        return
    unknown = sorted(set(manifest) - MANIFEST_FIELDS)
    if unknown:
        errors.append("plugin manifest has unsupported fields: " + ", ".join(unknown))
    if manifest.get("name") != PLUGIN_NAME:
        errors.append("plugin manifest name must match the plugin directory")
    version = manifest.get("version")
    if not _non_empty_string(version) or SEMVER_RE.fullmatch(version) is None:
        errors.append("plugin manifest version must use strict semver")
    for field in ("description", "homepage", "repository", "license"):
        if not _non_empty_string(manifest.get(field)):
            errors.append(f"plugin manifest {field} must be a non-empty string")
    if manifest.get("skills") != "./skills/":
        errors.append("plugin manifest skills must be ./skills/")
    author = manifest.get("author")
    if not isinstance(author, dict) or not _non_empty_string(author.get("name")):
        errors.append("plugin manifest author.name must be a non-empty string")
    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        errors.append("plugin manifest interface must be an object")
        return
    unknown_interface = sorted(set(interface) - INTERFACE_FIELDS)
    if unknown_interface:
        errors.append("plugin interface has unsupported fields: " + ", ".join(unknown_interface))
    for field in (
        "displayName",
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
        "websiteURL",
    ):
        if not _non_empty_string(interface.get(field)):
            errors.append(f"plugin interface {field} must be a non-empty string")
    capabilities = interface.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities or not all(
        _non_empty_string(item) for item in capabilities
    ):
        errors.append("plugin interface capabilities must be a non-empty string array")
    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3 or not all(
        _non_empty_string(item) and len(item) <= 128 for item in prompts
    ):
        errors.append(
            "plugin interface defaultPrompt must contain one to three prompts "
            "of at most 128 characters"
        )
    for field in ("composerIcon", "logo"):
        _check_asset(interface.get(field), field, errors)
    if "[TODO:" in json.dumps(manifest):
        errors.append("plugin manifest contains a TODO placeholder")


def validate_marketplace(errors: list[str]) -> None:
    marketplace = _load_object(MARKETPLACE, errors)
    if marketplace is None:
        return
    if marketplace.get("name") != PLUGIN_NAME:
        errors.append("marketplace name must match the plugin install selector")
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1 or not isinstance(plugins[0], dict):
        errors.append("marketplace must contain exactly one plugin entry")
        return
    entry = plugins[0]
    if entry.get("name") != PLUGIN_NAME:
        errors.append("marketplace plugin name must match the manifest")
    if entry.get("source") != {
        "source": "local",
        "path": "./plugins/ieee-acm-paper-writing",
    }:
        errors.append("marketplace source must point to ./plugins/ieee-acm-paper-writing")
    policy = entry.get("policy")
    if not isinstance(policy, dict):
        errors.append("marketplace entry must define policy")
    else:
        if policy.get("installation") not in {
            "AVAILABLE",
            "INSTALLED_BY_DEFAULT",
            "NOT_AVAILABLE",
        }:
            errors.append("marketplace installation policy is invalid")
        if policy.get("authentication") not in {"ON_INSTALL", "ON_USE"}:
            errors.append("marketplace authentication policy is invalid")
    if not _non_empty_string(entry.get("category")):
        errors.append("marketplace entry category must be a non-empty string")


def validation_errors() -> list[str]:
    errors = package_errors()
    validate_manifest(errors)
    validate_marketplace(errors)
    return errors


def main() -> None:
    errors = validation_errors()
    if errors:
        print("Codex plugin package validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"Codex plugin package validation passed: {PLUGIN_ROOT}")


if __name__ == "__main__":
    main()
