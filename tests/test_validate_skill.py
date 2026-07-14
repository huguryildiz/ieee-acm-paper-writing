import importlib.util
import subprocess
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

    def test_existing_but_untracked_link_target_is_rejected_in_git_worktree(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("[local](local.md)\n", encoding="utf-8")
            (root / "local.md").write_text("local only\n", encoding="utf-8")
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "add", "README.md"], check=True)
            VALIDATOR_MODULE.check_links(root)
            self.assertTrue(any("targets untracked file" in error
                                for error in VALIDATOR_MODULE.errors))


class FrontmatterValidationTests(unittest.TestCase):
    def setUp(self):
        VALIDATOR_MODULE.errors.clear()

    def tearDown(self):
        VALIDATOR_MODULE.errors.clear()

    def check_frontmatter(self, frontmatter):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "SKILL.md"
            skill.write_text(f"---\n{frontmatter}\n---\n\n# Skill\n", encoding="utf-8")
            VALIDATOR_MODULE.check_frontmatter(skill)
            return list(VALIDATOR_MODULE.errors)

    def test_malformed_or_indented_frontmatter_is_rejected(self):
        errors = self.check_frontmatter(
            "name: valid-name\ndescription: valid description\n\tmalformed-yaml-indentation"
        )
        self.assertTrue(any("nested or indented frontmatter" in error for error in errors))

    def test_nonstandard_frontmatter_keys_are_rejected(self):
        errors = self.check_frontmatter(
            "name: valid-name\ndescription: valid description\nlicense: MIT\n"
            "allowed-tools: Read, Grep\nmetadata: version=1"
        )
        self.assertTrue(any("unexpected frontmatter keys" in error for error in errors))

    def test_unrecognized_frontmatter_content_is_rejected(self):
        errors = self.check_frontmatter(
            "name: valid-name\ndescription: valid description\nthis is not yaml"
        )
        self.assertTrue(any("malformed frontmatter line" in error for error in errors))


class CalibrationPolicyTests(unittest.TestCase):
    def setUp(self):
        VALIDATOR_MODULE.errors.clear()

    def tearDown(self):
        VALIDATOR_MODULE.errors.clear()

    def check_calibration(self, text):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            calibration = (root / "skills" / "ieee-acm-paper-writing" /
                           "references" / "corpus-calibration.md")
            calibration.parent.mkdir(parents=True)
            calibration.write_text(text, encoding="utf-8")
            catalog = root / "docs" / "papers" / "catalog.tsv"
            catalog.parent.mkdir(parents=True)
            catalog.write_text(
                "domain\tauthor_year\ttitle\tdoi\tlocal_file\tlocal_status\tnotes\n"
                "systems\tLamport 1978\tTime and events\t10.1000/example\tp.pdf\tavailable\t-\n",
                encoding="utf-8",
            )
            VALIDATOR_MODULE.check_calibration(root)
            return list(VALIDATOR_MODULE.errors)

    def test_direct_source_identifier_is_rejected(self):
        errors = self.check_calibration("Derived pattern, doi:10.1000/example\n")
        self.assertTrue(any("prohibited DOI" in error for error in errors))

    def test_catalog_author_is_rejected(self):
        errors = self.check_calibration("Pattern attributed to Lamport.\n")
        self.assertTrue(any("prohibited catalog author" in error for error in errors))

    def test_generic_derivative_pattern_passes(self):
        errors = self.check_calibration("Define the system boundary before the mechanism.\n")
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
