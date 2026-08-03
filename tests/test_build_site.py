import json
import shutil
import unittest
from pathlib import Path

from scripts.build_site import EXAMPLE_ARTIFACTS, EXAMPLES, ROOT, SITE_OUTPUT, build_site


class SiteBuildTests(unittest.TestCase):
    def tearDown(self):
        shutil.rmtree(SITE_OUTPUT, ignore_errors=True)

    def test_build_copies_site_and_current_example_artifacts(self):
        build_site()

        for relative_path in (
            "index.html",
            "styles.css",
            "app.js",
            "assets/icon.svg",
            "examples/section-audit-map.html",
            "examples/section-audit-map.json",
            "examples/method-reproducibility-audit-map.html",
            "examples/method-reproducibility-audit-map.json",
            "examples/venue-adaptation-audit-map.html",
            "examples/venue-adaptation-audit-map.json",
        ):
            self.assertTrue((SITE_OUTPUT / relative_path).is_file(), relative_path)

        for name in EXAMPLE_ARTIFACTS:
            self.assertEqual(
                (SITE_OUTPUT / "examples" / name).read_bytes(),
                (EXAMPLES / name).read_bytes(),
            )

    def test_landing_page_links_to_built_artifacts(self):
        build_site()
        landing_page = (SITE_OUTPUT / "index.html").read_text(encoding="utf-8")

        self.assertIn('href="/examples/section-audit-map.html" download', landing_page)
        self.assertIn('href="/examples/section-audit-map.json" download', landing_page)
        self.assertIn('src="/examples/section-audit-map.html"', landing_page)
        self.assertIn('data-example-html="/examples/method-reproducibility-audit-map.html"', landing_page)
        self.assertIn('data-example-html="/examples/venue-adaptation-audit-map.html"', landing_page)
        self.assertIn('#local-audit-workbench', landing_page)
        self.assertIn('npx skills add', landing_page)
        self.assertIn('/tree/v0.6.0 -a codex -y', landing_page)
        self.assertIn('data-agent="codex"', landing_page)
        self.assertIn('data-agent="claude-code"', landing_page)
        self.assertIn('id="first-prompt"', landing_page)
        self.assertNotIn('id="workbench-command"', landing_page)
        self.assertNotIn('--agent codex claude-code', landing_page)
        self.assertNotIn("unpkg.com", landing_page)
        self.assertNotIn("cdn.jsdelivr.net", landing_page)

    def test_claude_code_install_uses_the_published_plugin_path(self):
        build_site()
        behavior = (SITE_OUTPUT / "app.js").read_text(encoding="utf-8")
        marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))

        self.assertIn("/plugin marketplace add huguryildiz/ieee-acm-paper-writing", behavior)
        self.assertIn("/plugin install ieee-acm-paper-writing", behavior)
        self.assertEqual(marketplace["name"], "ieee-acm-paper-writing")
        self.assertEqual([plugin["name"] for plugin in marketplace["plugins"]], ["ieee-acm-paper-writing"])


if __name__ == "__main__":
    unittest.main()
