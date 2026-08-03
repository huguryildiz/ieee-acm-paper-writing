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
EXAMPLES = ROOT / "skills" / "ieee-acm-paper-writing" / "examples"
EXAMPLE_JSON = EXAMPLES / "section-audit-map.json"
RENDERED_EXAMPLE_HTML = EXAMPLE_JSON.with_name("section-audit-map-rendered.html")
FIXTURE_PAIRS = (
    (EXAMPLE_JSON, RENDERED_EXAMPLE_HTML),
    (
        EXAMPLES / "method-reproducibility-audit-map.json",
        EXAMPLES / "method-reproducibility-audit-map.html",
    ),
    (
        EXAMPLES / "venue-adaptation-audit-map.json",
        EXAMPLES / "venue-adaptation-audit-map.html",
    ),
)
SPEC = importlib.util.spec_from_file_location("render_audit_map", RENDERER)
RENDER_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RENDER_MODULE)


class AuditMapRendererTests(unittest.TestCase):
    def example(self):
        return json.loads(EXAMPLE_JSON.read_text(encoding="utf-8"))

    def test_checked_in_renderer_fixtures_match_renderer(self):
        for json_path, html_path in FIXTURE_PAIRS:
            with self.subTest(json_path=json_path.name):
                document = json.loads(json_path.read_text(encoding="utf-8"))
                rendered = RENDER_MODULE.render_document(document)
                self.assertEqual(html_path.read_text(encoding="utf-8"), rendered)

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

    def test_script_context_breakout_is_neutralized(self):
        document = self.example()
        document["findings"][0]["title"] = '</script><script>alert(1)</script>'
        rendered = RENDER_MODULE.render_document(document)
        self.assertNotIn("</script><script>alert(1)</script>", rendered)
        self.assertIn("\\u003c/script\\u003e", rendered)

    def test_invalid_utf8_input_fails_cleanly(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_bytes(b"\xff\xfe{")
            with self.assertRaises(RENDER_MODULE.RenderError):
                RENDER_MODULE.load_json(str(bad))

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

    def test_output_path_inside_workspace_is_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = RENDER_MODULE.output_within_workspace(root / "reports" / "audit.html", root)
            self.assertEqual(output, root / "reports" / "audit.html")

    def test_parent_traversal_outside_workspace_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "workspace"
            root.mkdir()
            with self.assertRaisesRegex(RENDER_MODULE.RenderError, "inside workspace root"):
                RENDER_MODULE.output_within_workspace(root / ".." / "outside.html", root)

    def test_absolute_output_outside_workspace_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            root = parent / "workspace"
            root.mkdir()
            with self.assertRaisesRegex(RENDER_MODULE.RenderError, "inside workspace root"):
                RENDER_MODULE.output_within_workspace(parent / "outside.html", root)

    def test_symlinked_parent_cannot_escape_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            root = parent / "workspace"
            outside = parent / "outside"
            root.mkdir()
            outside.mkdir()
            (root / "reports").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(RENDER_MODULE.RenderError, "inside workspace root"):
                RENDER_MODULE.output_within_workspace(root / "reports" / "audit.html", root)


if __name__ == "__main__":
    unittest.main()
