import http.client
import importlib.util
import json
import threading
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SERVER_PATH = ROOT / "scripts" / "serve_local_audit.py"
EXAMPLE_JSON = (
    ROOT
    / "skills"
    / "ieee-acm-paper-writing"
    / "examples"
    / "section-audit-map.json"
)
SPEC = importlib.util.spec_from_file_location("serve_local_audit", SERVER_PATH)
SERVER_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SERVER_MODULE)


class LocalAuditUiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.token = "test-session-token"
        cls.server = SERVER_MODULE.create_server(port=0, token=cls.token)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.port = cls.server.server_address[1]

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def request(self, method, path, body=None, headers=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=3)
        connection.request(method, path, body=body, headers=headers or {})
        response = connection.getresponse()
        payload = response.read()
        result = response.status, dict(response.getheaders()), payload
        connection.close()
        return result

    def test_workbench_is_local_self_contained_and_session_bound(self):
        status, headers, body = self.request("GET", "/")
        text = body.decode("utf-8")
        self.assertEqual(status, 200)
        self.assertIn(f'content="{self.token}"', text)
        self.assertIn('sandbox="allow-scripts"', text)
        self.assertIn('src="/local-audit-logo.png"', text)
        self.assertIn("Loopback only", text)
        self.assertIn("default-src 'self'", headers["Content-Security-Policy"])
        self.assertIn("frame-src blob:", headers["Content-Security-Policy"])
        self.assertNotIn("https://", text)
        self.assertNotIn("http://", text)

        logo_status, logo_headers, logo_body = self.request("GET", "/local-audit-logo.png")
        self.assertEqual(logo_status, 200)
        self.assertEqual(logo_headers["Content-Type"], "image/png")
        self.assertTrue(logo_body.startswith(b"\x89PNG\r\n\x1a\n"))

    def test_valid_json_is_rendered_by_canonical_renderer(self):
        raw = EXAMPLE_JSON.read_bytes()
        status, headers, body = self.request(
            "POST",
            "/render",
            raw,
            {"Content-Type": "application/json", "X-Audit-Session": self.token},
        )
        self.assertEqual(status, 200)
        self.assertEqual(headers["X-Audit-Finding-Count"], "12")
        self.assertIn(b"Section-Audit Map", body)
        self.assertEqual(
            body.decode("utf-8"),
            SERVER_MODULE.RENDERER.render_document(json.loads(raw.decode("utf-8"))),
        )

    def test_render_requires_session_and_json_content_type(self):
        raw = EXAMPLE_JSON.read_bytes()
        status, _, _ = self.request(
            "POST", "/render", raw, {"Content-Type": "application/json"}
        )
        self.assertEqual(status, 403)
        status, _, _ = self.request(
            "POST",
            "/render",
            raw,
            {"Content-Type": "text/plain", "X-Audit-Session": self.token},
        )
        self.assertEqual(status, 415)

    def test_invalid_schema_returns_bounded_error(self):
        status, headers, body = self.request(
            "POST",
            "/render",
            b'{"version": 1}',
            {"Content-Type": "application/json", "X-Audit-Session": self.token},
        )
        payload = json.loads(body)
        self.assertEqual(status, 422)
        self.assertEqual(headers["Content-Type"], "application/json; charset=utf-8")
        self.assertIn("missing top-level field", payload["error"])
        self.assertNotIn("Traceback", payload["error"])

    def test_non_loopback_binding_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "loopback"):
            SERVER_MODULE.create_server(host="0.0.0.0", port=0)

    def test_non_loopback_host_header_is_rejected(self):
        invalid_hosts = (
            "attacker.example",
            "127.0.0.1.evil.example",
            "attacker.example@127.0.0.1",
            "localhost/path",
            f"localhost:{self.port + 1}",
        )
        for host in invalid_hosts:
            with self.subTest(host=host):
                status, _, body = self.request("GET", "/", headers={"Host": host})
                self.assertEqual(status, 421)
                self.assertEqual(json.loads(body), {"error": "invalid local host"})

        status, _, body = self.request(
            "POST",
            "/render",
            EXAMPLE_JSON.read_bytes(),
            {
                "Host": "127.0.0.1.evil.example",
                "Content-Type": "application/json",
                "X-Audit-Session": self.token,
            },
        )
        self.assertEqual(status, 421)
        self.assertEqual(json.loads(body), {"error": "invalid local host"})

    def test_loopback_host_headers_are_accepted(self):
        for host in ("localhost", "127.0.0.1", f"localhost:{self.port}"):
            with self.subTest(host=host):
                status, _, _ = self.request("GET", "/health", headers={"Host": host})
                self.assertEqual(status, 200)

    def test_ui_sources_have_privacy_accessibility_and_theme_contracts(self):
        ui_root = ROOT / "scripts" / "local_audit_ui"
        html = (ui_root / "index.html").read_text(encoding="utf-8")
        css = (ui_root / "local-audit.css").read_text(encoding="utf-8")
        js = (ui_root / "local-audit.js").read_text(encoding="utf-8")
        self.assertIn('role="status" aria-live="polite"', html)
        self.assertIn('type="file"', html)
        self.assertIn("prefers-reduced-motion", css)
        self.assertIn('data-theme="dark"', css)
        self.assertIn(".theme-toggle { display: inline-flex; align-items: center; gap: 8px; min-height: 44px", css)
        self.assertIn(".text-action { min-height: 44px", css)
        self.assertIn('fetch("/render"', js)
        self.assertNotIn("https://", html + css + js)
        self.assertNotIn("http://", html + css + js)


if __name__ == "__main__":
    unittest.main()
