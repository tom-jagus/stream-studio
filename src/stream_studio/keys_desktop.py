"""Bounded desktop observations and IPC invalidation, without window titles."""

import json
import os
import socket
import subprocess
import threading
import time

from .keys import suspension_reason


class Desktop:
    def __init__(self):
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._connected = False
        self._revision = 0
        self._keyboard_revision = 0
        self._reason = "Desktop state unavailable"
        self._updated = float("-inf")
        self._mapping = None
        self._threads = [threading.Thread(target=target, daemon=True)
                         for target in (self._events, self._poll)]
        for thread in self._threads:
            thread.start()

    def _path(self, name):
        return (f"{os.environ['XDG_RUNTIME_DIR']}/hypr/"
                f"{os.environ['HYPRLAND_INSTANCE_SIGNATURE']}/{name}")

    def _query(self, command):
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
            connection.settimeout(0.15)
            connection.connect(self._path(".socket.sock"))
            connection.sendall(f"j/{command}".encode())
            chunks = bytearray()
            while chunk := connection.recv(65536):
                chunks.extend(chunk)
                if len(chunks) > 1_000_000:
                    raise ValueError("Desktop response too large")
            return json.loads(chunks)

    def _invalidate(self, connected=None, mapping_changed=False):
        with self._lock:
            if connected is not None:
                self._connected = connected
            if mapping_changed or connected is not None:
                self._keyboard_revision += 1
            self._revision += 1
            self._reason = "Desktop transition pending"
            self._updated = float("-inf")

    def _events(self):
        transitions = {b"workspace", b"workspacev2", b"focusedmon", b"focusedmonv2",
                       b"activewindow", b"activewindowv2", b"activespecial",
                       b"activespecialv2", b"openlayer", b"closelayer",
                       b"monitoradded", b"monitorremoved", b"activelayout",
                       b"configreloaded"}
        while not self._stop.is_set():
            try:
                with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
                    connection.settimeout(0.2)
                    connection.connect(self._path(".socket2.sock"))
                    self._invalidate(True)
                    pending = bytearray()
                    while not self._stop.is_set():
                        try:
                            chunk = connection.recv(4096)
                        except socket.timeout:
                            continue
                        if not chunk:
                            break
                        pending.extend(chunk)
                        if len(pending) > 65536:
                            raise ValueError("Oversized desktop event")
                        while b"\n" in pending:
                            line, _, remainder = pending.partition(b"\n")
                            pending = bytearray(remainder)
                            event = bytes(line.partition(b">>")[0])
                            if event in transitions:
                                self._invalidate(mapping_changed=event in {
                                    b"activelayout", b"configreloaded"
                                })
            except (OSError, KeyError, ValueError):
                pass
            self._invalidate(False)
            self._stop.wait(0.5)

    def _observe(self):
        monitors = self._query("monitors")
        focused = [monitor for monitor in monitors if monitor["focused"]]
        if len(focused) != 1:
            raise ValueError("Uncertain monitor focus")
        monitor = focused[0]
        workspace = monitor["activeWorkspace"]["id"]
        special = monitor["specialWorkspace"]["id"] != 0
        locked = self._query("locked")["locked"]
        if not isinstance(locked, bool) or type(workspace) is not int:
            raise ValueError("Invalid desktop state")
        shell = subprocess.run(
            ["omarchy-shell", "lock", "isLocked"], capture_output=True,
            timeout=0.3, text=True,
        )
        if shell.returncode or shell.stdout.strip() not in {"true", "false"}:
            raise ValueError("Omarchy lock state unavailable")
        locked = locked or shell.stdout.strip() == "true"
        layers = self._query("layers")
        prompt = any(layer.get("namespace") == "omarchy-polkit"
                     for output in layers.values()
                     for level in output["levels"].values() for layer in level)
        devices = self._query("devices")["keyboards"]
        selected = [device for device in devices if device["name"] in {
            "thomas-haukland-cheapino2", "dh747-w-corne"
        }]
        if not selected:
            raise ValueError("Selected keyboards unavailable")
        mappings = {(device["layout"], device["variant"], device["options"],
                     device["active_layout_index"]) for device in selected}
        if len(mappings) != 1:
            raise ValueError("Selected keyboard mappings differ")
        mapping = next(iter(mappings))
        if mapping != ("us", "", "omarchy:shift_caps_compose", 0):
            raise ValueError("Unsupported keyboard mapping")
        return suspension_reason(workspace, special=special, locked=locked,
                                 prompt=prompt, ipc_connected=True), mapping

    def _poll(self):
        while not self._stop.is_set():
            with self._lock:
                revision = self._revision
            try:
                reason, mapping = self._observe()
            except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired):
                reason, mapping = "Desktop observation failed", None
            with self._lock:
                if revision == self._revision:
                    self._reason = reason
                    self._mapping = mapping
                    self._updated = time.monotonic()
            self._stop.wait(0.1)

    def snapshot(self):
        with self._lock:
            if not self._connected or time.monotonic() - self._updated > 0.75:
                return "Desktop state unavailable or stale", None, self._revision
            return self._reason, self._mapping, self._revision

    def keyboard_revision(self):
        with self._lock:
            return self._keyboard_revision

    def close(self):
        self._stop.set()
        for thread in self._threads:
            thread.join(timeout=3)
