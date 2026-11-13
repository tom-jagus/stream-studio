"""Private user-owned Unix socket; HTTP cannot enable keyboard capture."""

import fcntl
import json
import os
import socket
import socketserver
import stat
import threading
from pathlib import Path


def runtime_directory() -> Path:
    directory = Path(os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}")) / "stream-studio"
    directory.mkdir(mode=0o700, parents=False, exist_ok=True)
    info = directory.lstat()
    if (not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid()
            or stat.S_IMODE(info.st_mode) & 0o077):
        raise OSError("Unsafe stream-studio runtime directory.")
    return directory


class Control:
    def __init__(self, keys):
        self.keys = keys
        self.path = runtime_directory() / "keys.sock"
        self.lock = (self.path.parent / "keys.lock").open("a")
        try:
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            self.lock.close()
            raise OSError("Another key control service is already running.") from None
        self.path.unlink(missing_ok=True)
        owner = self

        class Handler(socketserver.StreamRequestHandler):
            def handle(self):
                self.connection.settimeout(1)
                try:
                    action = self.rfile.readline(128).decode("ascii").strip()
                    result = owner.keys.command(action)
                except (OSError, UnicodeError, ValueError):
                    result = {"error": "Invalid key control request"}
                try:
                    self.wfile.write(json.dumps(result).encode() + b"\n")
                except OSError:
                    pass

        class Server(socketserver.UnixStreamServer):

            def handle_error(self, request, client_address):
                # Do not log request bodies or capture state.
                pass

        try:
            self.server = Server(str(self.path), Handler)
            self.path.chmod(0o600)
        except BaseException:
            self.lock.close()
            raise
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def close(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.path.unlink(missing_ok=True)
        self.lock.close()


def request(action: str) -> dict:
    path = runtime_directory() / "keys.sock"
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
        connection.settimeout(2)
        connection.connect(str(path))
        connection.sendall(action.encode("ascii") + b"\n")
        with connection.makefile("rb") as response:
            payload = json.loads(response.readline(4096))
    if (not isinstance(payload, dict) or payload.get("state") not in {
        "disabled", "suspended", "presenting"
    } or not isinstance(payload.get("reason"), str)):
        raise ValueError("Invalid key control response.")
    return payload
