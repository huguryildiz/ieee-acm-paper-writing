import shutil
import unittest
from pathlib import Path

from scripts.build_site import EXAMPLES, ROOT, SITE_OUTPUT, build_site


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
        ):
            self.assertTrue((SITE_OUTPUT / relative_path).is_file(), relative_path)

        for name in ("section-audit-map.html", "section-audit-map.json"):
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
        self.assertNotIn("unpkg.com", landing_page)
        self.assertNotIn("cdn.jsdelivr.net", landing_page)


if __name__ == "__main__":
    unittest.main()
