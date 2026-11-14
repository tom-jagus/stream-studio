"""Read-only loopback HTTP server for the OBS browser source."""

import json
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
from urllib.parse import urlsplit

from .state import read_topic

HOST = "127.0.0.1"
PORT = 8766
BASE_URL = f"http://{HOST}:{PORT}"
ASSETS = {
    "/": ("topic.html", "text/html; charset=utf-8"),
    "/topic": ("topic.html", "text/html; charset=utf-8"),
    "/topic.css": ("topic.css", "text/css; charset=utf-8"),
    "/topic.js": ("topic.js", "text/javascript; charset=utf-8"),
    "/keys": ("keys.html", "text/html; charset=utf-8"),
    "/keys.css": ("keys.css", "text/css; charset=utf-8"),
    "/keys.js": ("keys.js", "text/javascript; charset=utf-8"),
    "/chat": ("chat.html", "text/html; charset=utf-8"),
    "/chat.css": ("chat.css", "text/css; charset=utf-8"),
    "/chat.js": ("chat.js", "text/javascript; charset=utf-8"),
    "/preview": ("preview.html", "text/html; charset=utf-8"),
    "/preview.css": ("preview.css", "text/css; charset=utf-8"),
    "/preview.js": ("preview.js", "text/javascript; charset=utf-8"),
}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        # Do not expose state to arbitrary Host headers or DNS rebinding.
        if self.headers.get("Host") not in {
            f"{HOST}:{PORT}", f"localhost:{PORT}"
        }:
            self.send_error(403, "Invalid Host")
            return
        path = urlsplit(self.path).path
        if path == "/api/topic":
            try:
                body = json.dumps({"topic": read_topic()}).encode("utf-8")
            except (OSError, ValueError):
                self.send_error(503, "Topic state is unavailable")
                return
            self.respond(body, "application/json; charset=utf-8")
        elif path == "/api/scene":
            try:
                state_path = Path.home() / ".local/share/stream-studio/scene.json"
                state = json.loads(state_path.read_text(encoding="utf-8"))
                if (not isinstance(state, dict)
                        or not all(state.get(key) is None or isinstance(state.get(key), str)
                                   for key in ("scene", "checked_at", "error"))):
                    raise ValueError("Invalid scene state")
                body = json.dumps({key: state.get(key) for key in
                                   ("scene", "checked_at", "error")}).encode("utf-8")
            except (OSError, UnicodeError, ValueError):
                self.send_error(503, "Scene state unavailable")
                return
            self.respond(body, "application/json; charset=utf-8")
        elif path == "/api/keys":
            keys = getattr(self.server, "keys", None)
            if keys is None:
                self.send_error(503, "Key presentation unavailable")
                return
            self.respond(json.dumps(keys.snapshot()).encode("utf-8"),
                         "application/json; charset=utf-8")
        elif path == "/api/chat":
            chat = getattr(self.server, "chat", None)
            if chat is None:
                self.send_error(503, "Chat unavailable")
                return
            self.respond(json.dumps(chat.snapshot()).encode("utf-8"),
                         "application/json; charset=utf-8")
        elif path in ASSETS:
            name, content_type = ASSETS[path]
            self.respond(
                files("stream_studio").joinpath("web", name).read_bytes(),
                content_type,
            )
        else:
            self.send_error(404)

    def respond(self, body: bytes, content_type: str) -> None:
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; style-src 'self'; "
            "connect-src 'self'; frame-ancestors 'none'",
        )
        self.end_headers()
        self.wfile.write(body)

    def log_request(self, code: int | str = "-", size: int | str = "-") -> None:
        # Routine polling need not fill the journal.
        if code != 200:
            super().log_request(code, size)


def serve() -> None:
    from .keys import Keys
    from .keys_control import Control
    from .chat_control import Control as ChatControl
    from .chat_service import ChatService

    keys = Keys()
    chat = ChatService()
    with ThreadingHTTPServer((HOST, PORT), Handler) as server:
        server.keys = keys
        server.chat = chat.chat
        control = Control(keys)
        chat_control = ChatControl(chat)
        from .keys_capture import Capture

        capture = Capture(keys)
        print(f"Topic overlay: {BASE_URL}/topic", flush=True)
        print(f"Keys overlay: {BASE_URL}/keys (disabled)", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            keys.command("off")
            capture.close()
            chat.close()
            chat_control.close()
            control.close()
