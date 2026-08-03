import importlib.util
import json
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


class CriteriaIndependenceTests(unittest.TestCase):
    def setUp(self):
        VALIDATOR_MODULE.errors.clear()

    def tearDown(self):
        VALIDATOR_MODULE.errors.clear()

    def check(self, criterion):
        import json

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            refs = root / "skills" / "ieee-acm-paper-writing" / "references"
            refs.mkdir(parents=True)
            (refs / "venue-guidance.md").write_text(
                "Replace ibid. with the explicit earlier reference number in the list.\n",
                encoding="utf-8",
            )
            (root / "evals").mkdir()
            (root / "evals" / "cases.json").write_text(
                json.dumps(
                    {
                        "version": 2,
                        "cases": [
                            {
                                "name": "sample",
                                "prompt": "p",
                                "must_pass": [criterion],
                                "must_not": [],
                                "expected_routing": [],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            VALIDATOR_MODULE.check_criteria_independence(root)
            return list(VALIDATOR_MODULE.errors)

    def test_criterion_echoing_skill_text_is_rejected(self):
        errors = self.check("Replace ibid. with the explicit earlier reference number shown.")
        self.assertTrue(any("shares a 6-word phrase" in error for error in errors))

    def test_independently_worded_criterion_passes(self):
        errors = self.check("Substitute the bracketed source number that the shorthand stands for.")
        self.assertEqual(errors, [])


class ReadmeCaseCountTests(unittest.TestCase):
    def setUp(self):
        VALIDATOR_MODULE.errors.clear()

    def tearDown(self):
        VALIDATOR_MODULE.errors.clear()

    def check(self, readme_count, case_count):
        import json

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                f"The behavioral suite defines {readme_count} self-contained cases.\n",
                encoding="utf-8",
            )
            (root / "evals").mkdir()
            (root / "evals" / "cases.json").write_text(
                json.dumps({"cases": [{} for _ in range(case_count)]}),
                encoding="utf-8",
            )
            VALIDATOR_MODULE.check_readme_case_count(root)
            return list(VALIDATOR_MODULE.errors)

    def test_matching_count_passes(self):
        self.assertEqual(self.check(27, 27), [])

    def test_stale_count_is_rejected(self):
        errors = self.check(26, 27)
        self.assertTrue(any("evals/cases.json has 27" in error for error in errors))


class EvalCoverageTests(unittest.TestCase):
    def setUp(self):
        VALIDATOR_MODULE.errors.clear()

    def tearDown(self):
        VALIDATOR_MODULE.errors.clear()

    def test_missing_mode_coverage_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "evals").mkdir()
            refs = root / "skills" / "ieee-acm-paper-writing" / "references"
            refs.mkdir(parents=True)
            case = {
                "name": "sample", "prompt": "p", "must_pass": ["observable result"],
                "must_not": [], "expected_routing": [],
            }
            modes = {
                mode: ["sample"]
                for mode in VALIDATOR_MODULE.REQUIRED_EVAL_MODES
                if mode != "compress"
            }
            document = {
                "version": 2,
                "coverage": {
                    "modes": modes,
                    "modifiers": {"html-map": ["sample"]},
                },
                "cases": [case],
            }
            (root / "evals" / "cases.json").write_text(
                json.dumps(document), encoding="utf-8"
            )
            VALIDATOR_MODULE.check_cases(root)
            self.assertTrue(
                any("coverage.modes.compress" in error for error in VALIDATOR_MODULE.errors)
            )

    def test_unsafe_artifact_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "evals").mkdir()
            refs = root / "skills" / "ieee-acm-paper-writing" / "references"
            refs.mkdir(parents=True)
            case = {
                "name": "sample", "prompt": "p", "must_pass": ["observable result"],
                "must_not": [], "expected_routing": [], "artifacts": ["../escape.html"],
            }
            document = {
                "version": 2,
                "coverage": {
                    "modes": {
                        mode: ["sample"] for mode in VALIDATOR_MODULE.REQUIRED_EVAL_MODES
                    },
                    "modifiers": {"html-map": ["sample"]},
                },
                "cases": [case],
            }
            (root / "evals" / "cases.json").write_text(
                json.dumps(document), encoding="utf-8"
            )
            VALIDATOR_MODULE.check_cases(root)
            self.assertTrue(any("artifact paths" in error for error in VALIDATOR_MODULE.errors))


class HtmlMapDocumentationTests(unittest.TestCase):
    def test_skill_requires_json_and_html_as_deliverables(self):
        skill = (
            ROOT / "skills" / "ieee-acm-paper-writing" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("The JSON is a user-deliverable artifact", skill)
        self.assertIn("plus the JSON path and HTML path", skill)
        self.assertIn("<source-stem>-section-audit-map.json", skill)
        self.assertIn("same path with `.json` substituted", skill)

    def test_skill_keeps_author_queries_after_claim_narrowing(self):
        skill = (
            ROOT / "skills" / "ieee-acm-paper-writing" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Omitting, narrowing, or qualifying an unsupported requested claim", skill)
        self.assertIn("A limitation sentence inside the\nmanuscript is not a substitute", skill)

    def test_readme_lists_every_mode_and_paired_artifacts(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for mode in (
            "draft",
            "rewrite",
            "expand",
            "compress",
            "humanize",
            "outline",
            "audit",
            "section-audit",
            "venue-adapt",
        ):
            self.assertIn(f"@ieee-acm-paper-writing {mode}", readme)
        self.assertIn("manuscript-section-audit-map.json", readme)
        self.assertIn("reports/results-audit.json", readme)

    def test_readme_documents_complete_modifier_surface(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("### Complete skill invocation reference", readme)
        self.assertIn("@ieee-acm-paper-writing audit --html-map manuscript.md", readme)
        self.assertIn(
            "@ieee-acm-paper-writing audit --html-map --out reports/manuscript-audit.html manuscript.md",
            readme,
        )
        self.assertIn("natural-language modifier", readme)
        self.assertIn("There are no mode-specific CLI flags beyond", readme)


class ModeDocumentationTests(unittest.TestCase):
    MODES = (
        "draft",
        "rewrite",
        "expand",
        "compress",
        "humanize",
        "outline",
        "audit",
        "section-audit",
        "venue-adapt",
    )

    def test_public_mode_inventory_matches_router(self):
        skill = (ROOT / "skills" / "ieee-acm-paper-writing" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for mode in self.MODES:
            self.assertIn(f"`{mode}`", skill)
            self.assertIn(f"@ieee-acm-paper-writing {mode}", readme)

    def test_release_pinned_install_and_workbench_scope_are_documented(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("npx skills@1.5.21 add https://github.com/huguryildiz/ieee-acm-paper-writing/tree/v0.6.2", readme)
        self.assertIn("is **not included**", readme)
        self.assertIn("git clone --branch v0.6.2 --depth 1", readme)

    def test_plugin_install_path_states_that_it_tracks_the_default_branch(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("/plugin marketplace add huguryildiz/ieee-acm-paper-writing", readme)
        self.assertIn("/plugin install ieee-acm-paper-writing", readme)
        self.assertIn("rather than a pinned release", readme)


class AuditMapShowcaseTests(unittest.TestCase):
    PAGE = '<!DOCTYPE html><html><head></head><body>{body}<div>audit map</div></body></html>'

    def setUp(self):
        VALIDATOR_MODULE.errors.clear()

    def tearDown(self):
        VALIDATOR_MODULE.errors.clear()

    def check(self, body="", fixture_body=None):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            examples = root / "skills" / "ieee-acm-paper-writing" / "examples"
            examples.mkdir(parents=True)
            (examples / "section-audit-map.html").write_text(
                self.PAGE.format(body=body), encoding="utf-8"
            )
            if fixture_body is not None:
                (examples / "section-audit-map-rendered.html").write_text(
                    self.PAGE.format(body=fixture_body), encoding="utf-8"
                )
            VALIDATOR_MODULE.check_audit_map_showcase(root)
            return list(VALIDATOR_MODULE.errors)

    def test_showcase_matching_the_renderer_fixture_passes(self):
        self.assertEqual(self.check(fixture_body=""), [])

    def test_showcase_diverging_from_the_renderer_fixture_is_rejected(self):
        errors = self.check(fixture_body="<p>re-rendered</p>")
        self.assertTrue(any("showcase differs from" in e for e in errors))

    def test_missing_renderer_fixture_is_rejected(self):
        errors = self.check()
        self.assertTrue(any("missing renderer fixture" in e for e in errors))

    def test_google_fonts_link_is_rejected(self):
        errors = self.check(
            '<link rel="preconnect" href="https://fonts.googleapis.com">',
            fixture_body='<link rel="preconnect" href="https://fonts.googleapis.com">',
        )
        self.assertTrue(any("external asset dependency" in e for e in errors))

    def test_missing_showcase_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            VALIDATOR_MODULE.check_audit_map_showcase(Path(tmp))
            self.assertTrue(any("missing or empty" in e for e in VALIDATOR_MODULE.errors))


if __name__ == "__main__":
    unittest.main()


class ClaudePluginPackageTests(unittest.TestCase):
    """Gate the Claude Code manifests, which no CI job can install and exercise."""

    def setUp(self):
        VALIDATOR_MODULE.errors.clear()

    def tearDown(self):
        VALIDATOR_MODULE.errors.clear()

    @staticmethod
    def build(root, *, plugin_version="1.2.3", market_version="1.2.3",
              entry_version="1.2.3", codex_version="1.2.3", source="./",
              readme=(
                  "npx skills@1.5.21 add "
                  "https://github.com/huguryildiz/ieee-acm-paper-writing/tree/v1.2.3\n"
                  "archive/refs/tags/v1.2.3.tar.gz\n"
                  "git clone --branch v1.2.3 --depth 1\n"
              )):
        (root / ".claude-plugin").mkdir(parents=True, exist_ok=True)
        (root / ".claude-plugin" / "plugin.json").write_text(json.dumps({
            "name": "ieee-acm-paper-writing",
            "version": plugin_version,
            "description": "d",
            "license": "MIT",
            "repository": "https://example.invalid/repo",
        }), encoding="utf-8")
        (root / ".claude-plugin" / "marketplace.json").write_text(json.dumps({
            "name": "ieee-acm-paper-writing",
            "owner": {"name": "owner"},
            "metadata": {"description": "m", "version": market_version},
            "plugins": [{
                "name": "ieee-acm-paper-writing",
                "source": source,
                "description": "d",
                "version": entry_version,
                "license": "MIT",
            }],
        }), encoding="utf-8")
        codex = root / "plugins" / "ieee-acm-paper-writing" / ".codex-plugin"
        codex.mkdir(parents=True, exist_ok=True)
        (codex / "plugin.json").write_text(
            json.dumps({"name": "ieee-acm-paper-writing", "version": codex_version}),
            encoding="utf-8",
        )
        skill = root / "skills" / "ieee-acm-paper-writing"
        skill.mkdir(parents=True, exist_ok=True)
        (skill / "SKILL.md").write_text("---\nname: x\ndescription: y\n---\n", encoding="utf-8")
        (root / "README.md").write_text(readme, encoding="utf-8")

    def run_check(self, **kwargs):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.build(root, **kwargs)
            VALIDATOR_MODULE.check_claude_plugin_package(root)
            return list(VALIDATOR_MODULE.errors)

    def test_aligned_manifests_pass(self):
        self.assertEqual(self.run_check(), [])

    def test_version_drift_between_manifests_is_rejected(self):
        errors = self.run_check(codex_version="9.9.9")
        self.assertTrue(any("disagree on version" in error for error in errors))

    def test_release_not_pinned_in_readme_is_rejected(self):
        errors = self.run_check(readme="Install from main\n")
        self.assertTrue(any("declared plugin version" in error for error in errors))

    def test_unversioned_installer_is_rejected(self):
        readme = (
            "npx skills add "
            "https://github.com/huguryildiz/ieee-acm-paper-writing/tree/v1.2.3\n"
            "archive/refs/tags/v1.2.3.tar.gz\n"
            "git clone --branch v1.2.3 --depth 1\n"
        )
        errors = self.run_check(readme=readme)
        self.assertTrue(any("versioned skills installer" in error for error in errors))

    def test_source_without_an_installable_skill_is_rejected(self):
        errors = self.run_check(source="./docs")
        self.assertTrue(any("source" in error for error in errors))

    def test_repository_manifests_are_aligned(self):
        VALIDATOR_MODULE.check_claude_plugin_package(ROOT)
        self.assertEqual(list(VALIDATOR_MODULE.errors), [])
