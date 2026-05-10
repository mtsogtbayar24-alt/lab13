from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .repository import JsonLinkRepository
from .service import ExpiredLinkError, LinkNotFoundError, ShortLinkService, ValidationError


ROOT = Path(__file__).resolve().parents[2]
STATIC_DIR = ROOT / "static"
DATA_DIR = ROOT / "data"


def build_service() -> ShortLinkService:
    return ShortLinkService(JsonLinkRepository(DATA_DIR / "links.json"))


class RequestHandler(BaseHTTPRequestHandler):
    service = build_service()

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._serve_static("index.html", "text/html; charset=utf-8")
            return
        if parsed.path == "/app.js":
            self._serve_static("app.js", "application/javascript; charset=utf-8")
            return
        if parsed.path == "/style.css":
            self._serve_static("style.css", "text/css; charset=utf-8")
            return
        if parsed.path == "/api/links":
            status = parse_qs(parsed.query).get("status", ["all"])[0]
            self._json_response({"items": self.service.list_links(status)})
            return
        if parsed.path.startswith("/api/links/"):
            code = parsed.path.rsplit("/", 1)[-1]
            try:
                self._json_response(self.service.get_link(code))
            except LinkNotFoundError:
                self._json_response({"error": "Link not found"}, HTTPStatus.NOT_FOUND)
            return
        if parsed.path.startswith("/r/"):
            code = parsed.path.rsplit("/", 1)[-1]
            try:
                target_url = self.service.resolve_link(code)
            except LinkNotFoundError:
                self._json_response({"error": "Link not found"}, HTTPStatus.NOT_FOUND)
                return
            except ExpiredLinkError:
                self._json_response({"error": "Link expired"}, HTTPStatus.GONE)
                return
            self.send_response(HTTPStatus.FOUND)
            self.send_header("Location", target_url)
            self.end_headers()
            return
        self._json_response({"error": "Not found"}, HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/links":
            self._json_response({"error": "Not found"}, HTTPStatus.NOT_FOUND)
            return
        payload = self._read_json()
        try:
            link = self.service.create_link(
                target_url=str(payload.get("target_url", "")),
                expires_at=payload.get("expires_at") or None,
            )
        except ValidationError as exc:
            self._json_response({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            return
        self._json_response(link.to_dict(), HTTPStatus.CREATED)

    def do_DELETE(self) -> None:  # noqa: N802
        if not self.path.startswith("/api/links/"):
            self._json_response({"error": "Not found"}, HTTPStatus.NOT_FOUND)
            return
        code = self.path.rsplit("/", 1)[-1]
        try:
            self.service.delete_link(code)
        except LinkNotFoundError:
            self._json_response({"error": "Link not found"}, HTTPStatus.NOT_FOUND)
            return
        self._json_response({"deleted": code})

    def log_message(self, format: str, *args: object) -> None:
        return

    def _read_json(self) -> dict[str, object]:
        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length) if content_length else b"{}"
        return json.loads(raw_body.decode("utf-8"))

    def _serve_static(self, filename: str, content_type: str) -> None:
        path = STATIC_DIR / filename
        body = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json_response(self, payload: dict[str, object], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), RequestHandler)
    print(f"Serving ClipLink at http://{host}:{port}")
    server.serve_forever()
