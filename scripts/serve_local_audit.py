#!/usr/bin/env python3
"""Serve the audit-map renderer behind a loopback-only local workbench.

The browser sends audit-map JSON only to this process on 127.0.0.1. The
existing renderer remains the sole implementation of validation and HTML
generation; this module only provides a local transport and static interface.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import secrets
import sys
import threading
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Optional, Tuple
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
UI_ROOT = ROOT / "scripts" / "local_audit_ui"
SKILL = ROOT / "skills" / "ieee-acm-paper-writing"
RENDERER_PATH = SKILL / "scripts" / "render_audit_map.py"
EXAMPLE_JSON = SKILL / "examples" / "section-audit-map.json"
MAX_REQUEST_BYTES = 2 * 1024 * 1024


def load_renderer() -> Any:
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("local_audit_renderer", RENDERER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load renderer: {RENDERER_PATH}")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


RENDERER = load_renderer()


class LocalAuditServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: Tuple[str, int], token: str):
        super().__init__(address, LocalAuditHandler)
        self.session_token = token


class LocalAuditHandler(BaseHTTPRequestHandler):
    server: LocalAuditServer

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _send(
        self,
        status: HTTPStatus,
        content_type: str,
        body: bytes,
        extra_headers: Optional[dict[str, str]] = None,
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        if extra_headers:
            for key, value in extra_headers.items():
                self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self._send(status, "application/json; charset=utf-8", body)

    def _valid_host_header(self) -> bool:
        """Reject DNS-rebinding hostnames before exposing the local session."""
        raw = self.headers.get("Host", "")
        try:
            parsed = urlsplit(f"//{raw}")
            hostname = (parsed.hostname or "").lower()
            port = parsed.port
        except ValueError:
            return False
        return (
            parsed.username is None
            and parsed.password is None
            and not parsed.path
            and not parsed.query
            and not parsed.fragment
            and hostname in {"127.0.0.1", "::1", "localhost"}
            and (
            port is None or port == self.server.server_port
            )
        )

    def _serve_workbench(self) -> None:
        template = (UI_ROOT / "index.html").read_text(encoding="utf-8")
        body = template.replace("@@SESSION_TOKEN@@", self.server.session_token).encode("utf-8")
        csp = (
            "default-src 'self'; script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; connect-src 'self'; frame-src blob:; "
            "object-src 'none'; base-uri 'none'; form-action 'none'; "
            "frame-ancestors 'none'"
        )
        self._send(
            HTTPStatus.OK,
            "text/html; charset=utf-8",
            body,
            {"Content-Security-Policy": csp},
        )

    def do_GET(self) -> None:
        if not self._valid_host_header():
            self._send_json(HTTPStatus.MISDIRECTED_REQUEST, {"error": "invalid local host"})
            return
        path = self.path.split("?", 1)[0]
        if path in ("/", "/local-audit.html"):
            self._serve_workbench()
            return
        if path == "/local-audit.css":
            self._send(
                HTTPStatus.OK,
                "text/css; charset=utf-8",
                (UI_ROOT / "local-audit.css").read_bytes(),
            )
            return
        if path == "/local-audit.js":
            self._send(
                HTTPStatus.OK,
                "text/javascript; charset=utf-8",
                (UI_ROOT / "local-audit.js").read_bytes(),
            )
            return
        if path in ("/local-audit-logo.png", "/favicon.ico"):
            self._send(
                HTTPStatus.OK,
                "image/png",
                (UI_ROOT / "local-audit-logo.png").read_bytes(),
            )
            return
        if path == "/example.json":
            self._send(
                HTTPStatus.OK,
                "application/json; charset=utf-8",
                EXAMPLE_JSON.read_bytes(),
            )
            return
        if path == "/health":
            self._send_json(HTTPStatus.OK, {"status": "ready", "renderer": "canonical"})
            return
        self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})

    def do_POST(self) -> None:
        if not self._valid_host_header():
            self._send_json(HTTPStatus.MISDIRECTED_REQUEST, {"error": "invalid local host"})
            return
        if self.path != "/render":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return
        supplied_token = self.headers.get("X-Audit-Session", "")
        if not secrets.compare_digest(supplied_token, self.server.session_token):
            self._send_json(HTTPStatus.FORBIDDEN, {"error": "invalid local session"})
            return
        content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
        if content_type != "application/json":
            self._send_json(
                HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                {"error": "Content-Type must be application/json"},
            )
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "invalid Content-Length"})
            return
        if length <= 0:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "empty JSON document"})
            return
        if length > MAX_REQUEST_BYTES:
            self._send_json(
                HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                {"error": "JSON document exceeds the 2 MiB local preview limit"},
            )
            return
        try:
            raw = json.loads(self.rfile.read(length).decode("utf-8"))
            normalized = RENDERER.validate_document(raw)
            rendered = RENDERER.render_document(raw).encode("utf-8")
        except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as exc:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": f"invalid JSON: {exc}"})
            return
        except RENDERER.RenderError as exc:
            self._send_json(HTTPStatus.UNPROCESSABLE_ENTITY, {"error": str(exc)})
            return
        self._send(
            HTTPStatus.OK,
            "text/html; charset=utf-8",
            rendered,
            {
                "X-Audit-Finding-Count": str(len(normalized["findings"])),
                "Content-Security-Policy": (
                    "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; "
                    "img-src data:; font-src data:; object-src 'none'; base-uri 'none'"
                ),
            },
        )


def create_server(host: str = "127.0.0.1", port: int = 0, token: Optional[str] = None) -> LocalAuditServer:
    if host not in ("127.0.0.1", "::1", "localhost"):
        raise ValueError("the local audit workbench may bind only to a loopback address")
    return LocalAuditServer((host, port), token or secrets.token_urlsafe(24))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Open a loopback-only workbench for local audit-map JSON."
    )
    parser.add_argument("--port", type=int, default=0, help="loopback port; 0 selects an available port")
    parser.add_argument("--no-open", action="store_true", help="do not open the default browser")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    server = create_server(port=args.port)
    host, port = server.server_address[:2]
    url = f"http://{host}:{port}/"
    print(f"Local audit workbench: {url}")
    print("Files stay on this computer. Press Ctrl+C to stop.")
    if not args.no_open:
        threading.Timer(0.15, webbrowser.open, args=(url,)).start()
    try:
        server.serve_forever(poll_interval=0.2)
    except KeyboardInterrupt:
        print("\nLocal audit workbench stopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
