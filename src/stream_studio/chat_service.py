"""Read-only YouTube chat worker and private local configuration."""

import json
import os
import stat
import tempfile
import threading
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from .chat import Chat, video_id


def config_dir():
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "stream-studio"


def read_expiry():
    try:
        data = json.loads((config_dir() / "chat.json").read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    value = data.get("expiry") if isinstance(data, dict) else False
    if value is not None and (type(value) is not int or value < 1):
        raise ValueError("Invalid chat expiry configuration")
    return value


def save_expiry(value):
    directory = config_dir()
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, name = tempfile.mkstemp(prefix=".chat-", dir=directory)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as output:
            json.dump({"expiry": value}, output)
            output.flush()
            os.fsync(output.fileno())
        os.replace(name, directory / "chat.json")
    finally:
        Path(name).unlink(missing_ok=True)


def read_key():
    path = config_dir() / "youtube-api-key"
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
        raise ValueError("API key file must be owned by you and private (mode 600)")
    key = path.read_text(encoding="utf-8").strip()
    if not key or len(key) > 512 or any(c.isspace() for c in key):
        raise ValueError("Invalid API key file")
    return key


def resolve_chat(identifier, key):
    query = urllib.parse.urlencode({"part": "liveStreamingDetails", "id": identifier})
    request = urllib.request.Request("https://www.googleapis.com/youtube/v3/videos?" + query,
                                     headers={"X-Goog-Api-Key": key})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(request, timeout=10) as response:
        body = response.read(1_000_001)
    if len(body) > 1_000_000:
        raise ValueError("YouTube response too large")
    payload = json.loads(body)
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        raise ValueError("Invalid YouTube response")
    items = payload["items"]
    if not items:
        raise ValueError("Broadcast unavailable, not live, or chat disabled")
    if not isinstance(items[0], dict):
        raise ValueError("Invalid YouTube response")
    details = items[0].get("liveStreamingDetails", {})
    if not isinstance(details, dict):
        raise ValueError("Invalid YouTube response")
    chat = details.get("activeLiveChatId")
    if chat is None or chat == "":
        raise ValueError("Broadcast unavailable, not live, or chat disabled")
    if not isinstance(chat, str):
        raise ValueError("Invalid YouTube response")
    return chat


class ChatService:
    def __init__(self):
        self.chat = Chat()
        try:
            self.chat.set_expiry(read_expiry())
        except (OSError, ValueError, TypeError):
            # A broken optional chat configuration must not prevent topic/keys.
            self.chat.observe(self.chat.start(), "error", "Invalid chat expiry configuration")
        self._lock = threading.RLock()
        self._cancel = None
        self._thread = None
        self._call = None

    def command(self, action, argument=None):
        with self._lock:
            if action == "start":
                identifier = video_id(argument or "")
                self._stop()
                generation = self.chat.start()
                self._cancel = threading.Event()
                self._thread = threading.Thread(target=self._run, args=(identifier, generation, self._cancel), daemon=True)
                self._thread.start()
            elif action == "stop":
                self._stop()
            elif action == "expiry":
                if argument == "off":
                    minutes = None
                elif isinstance(argument, str) and argument.isascii() and argument.isdecimal() and 0 < len(argument) <= 9 and int(argument) > 0:
                    minutes = int(argument)
                else:
                    raise ValueError("Expiry must be off or a positive whole number of minutes")
                save_expiry(minutes)
                self.chat.set_expiry(minutes)
            elif action != "status":
                raise ValueError("Invalid chat command")
            return self.chat.status()

    def _stop(self):
        if self._cancel:
            self._cancel.set()
        if self._call:
            self._call.cancel()
        self.chat.stop()
        self._cancel = None
        self._call = None

    def close(self):
        with self._lock:
            self._stop()

    def _run(self, identifier, generation, cancelled):
        try:
            import grpc
            from .chat_proto import messages
            Request, Response = messages()
        except ImportError:
            self.chat.observe(generation, "error", "Install the chat extra and restart the service")
            return
        try:
            key = read_key()
        except (OSError, ValueError):
            self.chat.observe(generation, "error", "Missing or unsafe YouTube API key file")
            return
        token = ""
        delay = 1
        while not cancelled.is_set():
            try:
                chat_id = resolve_chat(identifier, key)
                with grpc.secure_channel("youtube.googleapis.com:443", grpc.ssl_channel_credentials()) as channel:
                    rpc = channel.unary_stream(
                        "/youtube.api.v3.V3DataLiveChatMessageService/StreamList",
                        request_serializer=lambda request: request.SerializeToString(),
                        response_deserializer=Response.FromString)
                    request = Request(live_chat_id=chat_id, part=["id", "snippet", "authorDetails"])
                    if token:
                        request.page_token = token
                    call = rpc(request, metadata=(("x-goog-api-key", key),))
                    with self._lock:
                        if cancelled.is_set():
                            call.cancel()
                            return
                        self._call = call
                    self.chat.observe(generation, "connecting", "Waiting for YouTube chat")
                    for response in call:
                        if cancelled.is_set():
                            return
                        self.chat.observe(generation, "connected", "Receiving chat")
                        for item in response.items:
                            if item.snippet.display_message:
                                self.chat.add(generation, item.id, item.author_details.display_name,
                                              item.snippet.display_message, item.snippet.published_at)
                        if response.next_page_token:
                            token = response.next_page_token
                        if response.offline_at:
                            self.chat.observe(generation, "ended", "Broadcast ended")
                            return
                        delay = 1
            except urllib.error.HTTPError as error:
                reason = "YouTube API access or quota error" if error.code in (403, 429) else "Broadcast lookup failed"
                self.chat.observe(generation, "error", reason)
            except ValueError as error:
                if str(error) == "Broadcast unavailable, not live, or chat disabled":
                    self.chat.observe(generation, "error", str(error))
                else:
                    self.chat.observe(generation, "error", "Invalid YouTube response")
            except (OSError, KeyError, TypeError):
                self.chat.observe(generation, "error", "Broadcast lookup or network failed")
            except grpc.RpcError:
                if cancelled.is_set():
                    return
                self.chat.observe(generation, "error", "YouTube chat connection failed; retrying")
            if cancelled.wait(delay):
                return
            delay = min(delay * 2, 60)
