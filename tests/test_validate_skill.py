import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_skill.py"
SPEC = importlib.util.spec_from_file_location("validate_skill", VALIDATOR)
VALIDATOR_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR_MODULE)


class LinkValidationTests(unittest.TestCase):
    def setUp(self):
        VALIDATOR_MODULE.errors.clear()
        self.old_md_files = VALIDATOR_MODULE.MD_FILES
        self.old_md_globs = VALIDATOR_MODULE.MD_GLOBS
        VALIDATOR_MODULE.MD_FILES = ["README.md"]
        VALIDATOR_MODULE.MD_GLOBS = []

    def tearDown(self):
        VALIDATOR_MODULE.MD_FILES = self.old_md_files
        VALIDATOR_MODULE.MD_GLOBS = self.old_md_globs
        VALIDATOR_MODULE.errors.clear()

    def check_readme(self, text):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(text, encoding="utf-8")
            VALIDATOR_MODULE.check_links(root)
            return list(VALIDATOR_MODULE.errors)

    def test_html_href_anchor_is_validated(self):
        errors = self.check_readme('<a href="#missing">Missing</a>\n\n## Present\n')
        self.assertTrue(any("broken Markdown anchor" in error for error in errors))

    def test_reference_style_link_is_validated(self):
        errors = self.check_readme("[guide][g]\n\n[g]: missing.md\n")
        self.assertTrue(any("broken relative link" in error for error in errors))

    def test_existing_html_anchor_passes(self):
        errors = self.check_readme('<a href="#present">Present</a>\n\n## Present\n')
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
