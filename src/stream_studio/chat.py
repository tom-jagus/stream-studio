"""Bounded, transient YouTube chat presentation state."""

import re
import threading
import time
from collections import deque
from datetime import datetime, timezone
from urllib.parse import parse_qs, urlsplit

MAX_MESSAGES = 50
MAX_TEXT = 1000
MAX_AUTHOR = 100
MAX_IDS = 1000
CLOCK_SKEW = 60
VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")


def video_id(value: str) -> str:
    """Accept an ID or a supported YouTube watch, live, shorts, or share URL."""
    if VIDEO_ID.fullmatch(value):
        return value
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"} or parsed.username or parsed.password:
        raise ValueError("Expected a YouTube video URL or ID.")
    host = (parsed.hostname or "").lower()
    parts = parsed.path.strip("/").split("/")
    if host in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        if parsed.path == "/watch":
            values = parse_qs(parsed.query).get("v", [])
            candidate = values[0] if len(values) == 1 else ""
        elif len(parts) == 2 and parts[0] in {"live", "shorts"}:
            candidate = parts[1]
        else:
            candidate = ""
    elif host == "youtu.be" and len(parts) == 1:
        candidate = parts[0]
    else:
        candidate = ""
    if not VIDEO_ID.fullmatch(candidate):
        raise ValueError("Expected a YouTube video URL or ID.")
    return candidate


def posting_time(value):
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            return None
        return parsed.astimezone(timezone.utc).timestamp()
    except (ValueError, OverflowError, OSError):
        return None


class Chat:
    def __init__(self, clock=time.time):
        self._clock = clock
        self._lock = threading.RLock()
        self._messages = deque(maxlen=MAX_MESSAGES)
        self._seen = set()
        self._seen_order = deque()
        self._expiry = None
        self._skipped = 0
        self._generation = 0
        self._state = "stopped"
        self._reason = "Not connected"

    def start(self):
        with self._lock:
            self._generation += 1
            self._messages.clear()
            self._seen.clear()
            self._seen_order.clear()
            self._skipped = 0
            self._state, self._reason = "connecting", "Connecting"
            return self._generation

    def stop(self):
        with self._lock:
            self._generation += 1
            self._messages.clear()
            self._seen.clear()
            self._seen_order.clear()
            self._state, self._reason = "stopped", "Stopped"

    def observe(self, generation, state, reason):
        with self._lock:
            if generation == self._generation and self._state != "stopped":
                self._state, self._reason = state, reason

    def set_expiry(self, minutes):
        if minutes is not None and (type(minutes) is not int or minutes < 1):
            raise ValueError("Expiry must be off or a positive whole number of minutes.")
        with self._lock:
            self._expiry = minutes
            self._expire()

    def _expire(self):
        if self._expiry is None:
            return
        now = self._clock()
        kept = deque(maxlen=MAX_MESSAGES)
        for message in self._messages:
            posted = message["posted"]
            if posted is None or posted > now + CLOCK_SKEW:
                self._skipped += 1
            elif now - posted < self._expiry * 60:
                kept.append(message)
        self._messages = kept

    def add(self, generation, message_id, author, text, timestamp):
        with self._lock:
            if (generation != self._generation or self._state == "stopped"
                    or not isinstance(message_id, str) or not message_id
                    or len(message_id) > 512 or message_id in self._seen
                    or not isinstance(author, str) or not isinstance(text, str)):
                return
            self._seen.add(message_id)
            self._seen_order.append(message_id)
            if len(self._seen_order) > MAX_IDS:
                self._seen.discard(self._seen_order.popleft())
            posted = posting_time(timestamp)
            now = self._clock()
            if self._expiry is not None:
                if posted is None or posted > now + CLOCK_SKEW:
                    self._skipped += 1
                    return
                if now - posted >= self._expiry * 60:
                    return
            self._messages.append({"author": author[:MAX_AUTHOR], "text": text[:MAX_TEXT],
                                   "posted": posted})
            self._expire()

    def status(self):
        with self._lock:
            self._expire()
            return {"state": self._state, "reason": self._reason,
                    "expiry": self._expiry, "skipped": self._skipped}

    def snapshot(self):
        with self._lock:
            self._expire()
            return {"state": self._state,
                    "messages": [{"author": item["author"], "text": item["text"]}
                                 for item in self._messages]}
