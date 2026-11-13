"""Manage only the dedicated Chromium preview window on Hyprland."""

import fcntl
import json
import re
import shlex
import subprocess
import time
from pathlib import Path

from .keys_control import runtime_directory

APP_CLASS = "stream-studio-preview"
CHROMIUM_APP_CLASS = "chrome-127.0.0.1__preview-Default"
ADDRESS = re.compile(r"^0x[0-9a-fA-F]+$")
URL = "http://127.0.0.1:8766/preview"


def query(name):
    result = subprocess.run(["hyprctl", "-j", name], capture_output=True,
                            text=True, timeout=3, check=True)
    return json.loads(result.stdout)


def preview_process(pid):
    if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 0:
        return False
    try:
        raw = Path(f"/proc/{pid}/cmdline").read_bytes().split(b"\0")
        args = [arg.decode("utf-8") for arg in raw if arg]
        # Chromium may rewrite its command line as one shell-quoted argument.
        if len(args) == 1:
            args = shlex.split(args[0])
    except FileNotFoundError:
        return False
    except (OSError, UnicodeDecodeError, ValueError) as error:
        raise ValueError("Cannot verify preview window process") from error
    profile = runtime_directory() / "preview-browser"
    return "--user-data-dir=" + str(profile) in args and "--app=" + URL in args


def windows():
    classes = {APP_CLASS, CHROMIUM_APP_CLASS}
    return [client for client in query("clients")
            if (client.get("initialClass") in classes or client.get("class") in classes)
            and preview_process(client.get("pid"))]


def dispatch(expression):
    result = subprocess.run(["hyprctl", "dispatch", expression], capture_output=True,
                            text=True, timeout=3, check=True)
    if result.stdout.strip() != "ok":
        raise ValueError("Hyprland rejected preview window operation")


def selector(window):
    address = window.get("address", "")
    if not ADDRESS.fullmatch(address):
        raise ValueError("Invalid preview window address")
    return f"address:{address}"


def geometry():
    monitors = [monitor for monitor in query("monitors") if monitor.get("name") == "DP-1"]
    if len(monitors) != 1:
        raise ValueError("External monitor DP-1 is unavailable")
    monitor = monitors[0]
    if monitor.get("transform") != 0 or monitor.get("scale", 0) <= 0:
        raise ValueError("Unsupported monitor transform or scale")
    left, top, right, bottom = monitor["reserved"]
    if right <= 0:
        raise ValueError("The external monitor has no reserved right-hand area")
    width = round(monitor["width"] / monitor["scale"])
    height = round(monitor["height"] / monitor["scale"])
    return monitor["x"] + width - right, monitor["y"] + top, right, height - top - bottom


def command(action):
    if action not in {"on", "off", "toggle", "status"}:
        raise ValueError("Invalid preview command")
    with (runtime_directory() / "preview.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        found = windows()
        if len(found) > 1:
            raise ValueError("Multiple preview windows found; close extras manually")
        if action == "status":
            return "open" if found else "closed"
        if action == "toggle":
            action = "off" if found else "on"
        if action == "off":
            if found:
                target = selector(found[0])
                dispatch(f'hl.dsp.window.close({{ window = "{target}" }})')
            return "closed"
        x, y, width, height = geometry()
        if not found:
            profile = runtime_directory() / "preview-browser"
            subprocess.Popen(["chromium", "--class=" + APP_CLASS,
                              "--user-data-dir=" + str(profile), "--no-first-run",
                              "--app=" + URL], stdin=subprocess.DEVNULL,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             start_new_session=True)
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            found = found or windows()
            if len(found) > 1:
                raise ValueError("Multiple preview windows found; close extras manually")
            if found:
                target = selector(found[0])
                pinned = found[0].get("pinned")
                if not isinstance(pinned, bool):
                    raise ValueError("Cannot determine whether preview is pinned")
                dispatch(f'hl.dsp.window.float({{ window = "{target}", action = "set" }})')
                dispatch(f'hl.dsp.window.resize({{ window = "{target}", x = {width}, y = {height}, relative = false }})')
                dispatch(f'hl.dsp.window.move({{ window = "{target}", x = {x}, y = {y}, relative = false }})')
                if not pinned:
                    dispatch(f'hl.dsp.window.pin({{ window = "{target}" }})')
                return "open"
            time.sleep(0.1)
        raise ValueError("Preview window did not appear; check Chromium and Hyprland")
