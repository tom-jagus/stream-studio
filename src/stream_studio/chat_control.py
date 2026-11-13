"""Private local control socket for chat; browser access is read-only."""

import json
import socket
import socketserver
import threading

from .keys_control import runtime_directory


class Control:
    def __init__(self, service):
        self.path = runtime_directory() / "chat.sock"
        self.path.unlink(missing_ok=True)

        class Handler(socketserver.StreamRequestHandler):
            def handle(self):
                self.connection.settimeout(2)
                try:
                    request = json.loads(self.rfile.readline(4096))
                    result = service.command(request["action"], request.get("argument"))
                except (ValueError, KeyError, TypeError, OSError):
                    result = {"error": "Invalid request or chat configuration unavailable"}
                try:
                    self.wfile.write(json.dumps(result).encode() + b"\n")
                except OSError:
                    pass

        class Server(socketserver.UnixStreamServer):
            def handle_error(self, request, client_address):
                pass

        self.server = Server(str(self.path), Handler)
        self.path.chmod(0o600)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def close(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.path.unlink(missing_ok=True)


def request(action, argument=None):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
        connection.settimeout(3)
        connection.connect(str(runtime_directory() / "chat.sock"))
        connection.sendall(json.dumps({"action": action, "argument": argument}).encode() + b"\n")
        with connection.makefile("rb") as response:
            result = json.loads(response.readline(4096))
    if not isinstance(result, dict) or "error" in result:
        raise ValueError(result.get("error", "Invalid chat control response"))
    return result
