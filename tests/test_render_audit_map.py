import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RENDERER = (
    ROOT
    / "skills"
    / "ieee-acm-paper-writing"
    / "scripts"
    / "render_audit_map.py"
)
EXAMPLE_JSON = (
    ROOT
    / "skills"
    / "ieee-acm-paper-writing"
    / "examples"
    / "section-audit-map.json"
)
RENDERED_EXAMPLE_HTML = EXAMPLE_JSON.with_name("section-audit-map-rendered.html")
SPEC = importlib.util.spec_from_file_location("render_audit_map", RENDERER)
RENDER_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RENDER_MODULE)


class AuditMapRendererTests(unittest.TestCase):
    def example(self):
        return json.loads(EXAMPLE_JSON.read_text(encoding="utf-8"))

    def test_checked_in_renderer_fixture_matches_renderer(self):
        rendered = RENDER_MODULE.render_document(self.example())
        self.assertEqual(RENDERED_EXAMPLE_HTML.read_text(encoding="utf-8"), rendered)

    def test_render_is_self_contained_and_not_a_bundler_artifact(self):
        rendered = RENDER_MODULE.render_document(self.example())
        self.assertIsNone(re.search(r'(?:src|href)=["\']https?://', rendered))
        self.assertNotIn("__bundler", rendered)
        self.assertIn('data-finding="12"', rendered)
        self.assertIn("1 finding · verified house rules", rendered)
        self.assertNotIn("0 · not exercised · verified house rules", rendered)

    def test_user_text_is_html_escaped(self):
        document = self.example()
        document["findings"][0]["source"] = '</blockquote><script>alert("x")</script>'
        rendered = RENDER_MODULE.render_document(document)
        self.assertNotIn('<script>alert("x")</script>', rendered)
        self.assertIn("&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;", rendered)

    def test_invalid_concern_layer_is_rejected(self):
        document = self.example()
        document["findings"][0]["layer"] = "editorial-vibes"
        with self.assertRaisesRegex(RENDER_MODULE.RenderError, "layer must be one of"):
            RENDER_MODULE.validate_document(document)

    def test_duplicate_finding_id_is_rejected(self):
        document = self.example()
        document["findings"][1]["id"] = document["findings"][0]["id"]
        with self.assertRaisesRegex(RENDER_MODULE.RenderError, "duplicate finding id"):
            RENDER_MODULE.validate_document(document)

    def test_empty_finding_set_does_not_imply_a_pass(self):
        document = self.example()
        document["findings"] = []
        rendered = RENDER_MODULE.render_document(document)
        self.assertEqual(rendered.count("0 · not exercised"), 3)
        self.assertIn("this does not imply that the manuscript passed", rendered)

    def test_existing_output_requires_explicit_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "audit.html"
            output.write_text("existing", encoding="utf-8")
            with self.assertRaisesRegex(RENDER_MODULE.RenderError, "output exists"):
                RENDER_MODULE.write_atomic(output, "replacement", force=False)
            self.assertEqual(output.read_text(encoding="utf-8"), "existing")
            RENDER_MODULE.write_atomic(output, "replacement", force=True)
            self.assertEqual(output.read_text(encoding="utf-8"), "replacement")


if __name__ == "__main__":
    unittest.main()
