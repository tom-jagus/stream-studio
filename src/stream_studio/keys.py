"""Transient key presentation state. This module never opens input devices."""

import threading
import time
import uuid
from collections import deque

MAX_KEYS = 11
KEY_LIFETIME = 4.0
OBSERVATION_LIFETIME = 0.5


def suspension_reason(workspace: int | None, *, special: bool,
                      locked: bool | None, prompt: bool | None,
                      ipc_connected: bool) -> str | None:
    if not ipc_connected:
        return "Hyprland IPC unavailable"
    if locked is None or prompt is None or workspace is None:
        return "Desktop state uncertain"
    if locked:
        return "Screen locked"
    if prompt:
        return "Authentication prompt active"
    if special or workspace not in range(1, 6):
        return "Workspace not permitted"
    return None


class Keys:
    def __init__(self, clock=time.monotonic):
        self._clock = clock
        self._lock = threading.RLock()
        self._enabled = False
        self._reason = "Capture backend unavailable"
        self._observed = float("-inf")
        self._generation = uuid.uuid4().hex
        self._keys = deque(maxlen=MAX_KEYS)
        self._close_capture = None

    def attach(self, close_capture):
        """Register a synchronous, idempotent device-closure callback."""
        with self._lock:
            self._close_capture = close_capture

    def _clear(self):
        self._keys.clear()
        self._generation = uuid.uuid4().hex

    def _expire(self):
        if (self._observed != float("-inf")
                and self._clock() - self._observed > OBSERVATION_LIFETIME):
            if self._reason != "Desktop observation stale":
                self._reason = "Desktop observation stale"
                self._clear()
        while self._keys and self._clock() - self._keys[0][0] >= KEY_LIFETIME:
            self._keys.popleft()

    def command(self, action: str) -> dict:
        close_capture = None
        with self._lock:
            if action not in {"on", "off", "toggle", "status"}:
                raise ValueError("Expected keys on, off, toggle, or status.")
            if action == "toggle":
                action = "off" if self._enabled else "on"
            if action == "on" and not self._enabled:
                self._enabled = True
                self._observed = float("-inf")
                self._reason = "Awaiting capture and desktop state"
                self._clear()
            elif action == "off":
                self._enabled = False
                self._observed = float("-inf")
                self._reason = "Awaiting capture and desktop state"
                self._clear()
                close_capture = self._close_capture
        # The adapter may need the state lock while finishing an input batch.
        if close_capture is not None:
            close_capture()
        return self.status()

    def observe(self, reason: str | None):
        """The adapter supplies None only after both capture and gates are ready."""
        with self._lock:
            # Detect an observation gap even when no HTTP request intervened.
            self._expire()
            if reason != self._reason:
                self._clear()
            self._reason = reason
            self._observed = self._clock()

    def status(self) -> dict:
        with self._lock:
            self._expire()
            if not self._enabled:
                state, reason = "disabled", "Manually disabled"
            elif self._reason is not None:
                state, reason = "suspended", self._reason
            else:
                state, reason = "presenting", "Workspace and capture ready"
            return {"state": state, "reason": reason}

    def ticket(self) -> str | None:
        """Capture must obtain a ticket before processing each input batch."""
        with self._lock:
            return self._generation if self.status()["state"] == "presenting" else None

    def publish(self, text: str, ticket: str | None, parts=None):
        with self._lock:
            if (ticket is None or ticket != self.ticket()
                    or not isinstance(text, str) or not text or len(text) > 64
                    or any(ord(character) < 32 for character in text)):
                return
            parts = list(parts) if parts is not None else [text]
            if (not parts or len(parts) > 5
                    or any(not isinstance(part, str) or not part or len(part) > 64
                           or any(ord(char) < 32 for char in part) for part in parts)):
                return
            now = self._clock()
            entry = {"text": text, "parts": parts, "count": 1}
            if self._keys and self._keys[-1][1]["parts"] == parts:
                _, previous = self._keys[-1]
                if previous["count"] >= 3:
                    self._keys.pop()
                    entry["count"] = min(previous["count"] + 1, 999999)
                elif (len(self._keys) >= 2
                      and self._keys[-2][1]["parts"] == parts):
                    self._keys.pop()
                    self._keys.pop()
                    entry["count"] = 3
                else:
                    # Keep the first two presses separate, refreshing both.
                    self._keys[-1] = (now, previous)
            self._keys.append((now, entry))

    def snapshot(self) -> dict:
        with self._lock:
            status = self.status()
            return {
                **status,
                "generation": self._generation,
                "keys": [dict(entry, parts=list(entry["parts"])) for _, entry in self._keys]
                if status["state"] == "presenting" else [],
            }
