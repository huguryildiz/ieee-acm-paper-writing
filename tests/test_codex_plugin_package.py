import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
SYNC_PATH = SCRIPTS / "sync_codex_plugin.py"
VALIDATOR_PATH = SCRIPTS / "validate_codex_plugin.py"

SYNC_SPEC = importlib.util.spec_from_file_location("sync_codex_plugin", SYNC_PATH)
SYNC = importlib.util.module_from_spec(SYNC_SPEC)
SYNC_SPEC.loader.exec_module(SYNC)
sys.modules["sync_codex_plugin"] = SYNC

VALIDATOR_SPEC = importlib.util.spec_from_file_location(
    "validate_codex_plugin", VALIDATOR_PATH
)
VALIDATOR = importlib.util.module_from_spec(VALIDATOR_SPEC)
VALIDATOR_SPEC.loader.exec_module(VALIDATOR)


class PluginSnapshotTests(unittest.TestCase):
    def test_packaged_snapshot_is_synchronized(self):
        self.assertEqual(SYNC.package_errors(), [])

    def test_changed_snapshot_file_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            packaged = root / "packaged"
            source.mkdir()
            packaged.mkdir()
            (source / "SKILL.md").write_text("canonical\n", encoding="utf-8")
            (packaged / "SKILL.md").write_text("stale\n", encoding="utf-8")
            self.assertEqual(
                SYNC.compare_trees(source, packaged),
                ["plugin snapshot differs at SKILL.md"],
            )

    def test_symlinked_snapshot_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            packaged = root / "packaged"
            source.mkdir()
            packaged.mkdir()
            (source / "SKILL.md").write_text("canonical\n", encoding="utf-8")
            (packaged / "SKILL.md").symlink_to(source / "SKILL.md")
            errors = SYNC.compare_trees(source, packaged)
            self.assertTrue(any("contains symlinks" in error for error in errors))


class PluginContractTests(unittest.TestCase):
    def test_manifest_marketplace_and_snapshot_validate(self):
        self.assertEqual(VALIDATOR.validation_errors(), [])

    def test_readme_documents_native_codex_install(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("### Install as a native Codex plugin", readme)
        self.assertIn("codex plugin marketplace add .", readme)
        self.assertIn(
            "codex plugin add ieee-acm-paper-writing@ieee-acm-paper-writing",
            readme,
        )
