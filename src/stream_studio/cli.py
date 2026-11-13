"""Command-line controls. Only this local process writes topic state."""

import argparse
import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

from .server import BASE_URL, serve
from .state import read_topic, state_path, write_topic

SERVICE = "stream-studio.service"


def systemctl(*arguments: str) -> int:
    return subprocess.run(["systemctl", "--user", *arguments, SERVICE]).returncode


def install_service() -> int:
    target = Path.home() / ".config/systemd/user" / SERVICE
    target.parent.mkdir(parents=True, exist_ok=True)
    # systemd has its own quoting and %-specifier rules, not shell quoting.
    executable = str(Path(sys.executable).absolute())
    executable = executable.replace("\\", "\\\\").replace('"', '\\"')
    executable = executable.replace("%", "%%").replace("$", "$$")
    unit = (
        "[Unit]\nDescription=Stream Studio local presentation\n\n"
        "[Service]\nType=simple\n"
        f'ExecStart="{executable}" -m stream_studio serve\n'
        "Restart=on-failure\nRestartSec=2\nUMask=0077\n\n"
        "[Install]\nWantedBy=default.target\n"
    )
    # Preserve an existing service rather than silently replacing local changes.
    with target.open("x", encoding="utf-8") as output:
        output.write(unit)
    result = subprocess.run(["systemctl", "--user", "daemon-reload"])
    print(f"Created {target}. The service was not started or enabled.")
    return result.returncode


def status() -> int:
    result = systemctl("is-active")
    print(f"Saved topic: {read_topic() or '(empty)'}")
    print(f"State: {state_path()}")
    print(f"Overlay: {BASE_URL}/topic")
    if result != 0:
        print("Service is not active.")
        return 1
    try:
        # Ignore proxy environment variables for this loopback-only request.
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(f"{BASE_URL}/api/topic", timeout=2) as response:
            payload = json.load(response)
        if not isinstance(payload, dict) or not isinstance(payload.get("topic"), str):
            raise ValueError("Unexpected topic response.")
    except (OSError, ValueError, urllib.error.URLError) as error:
        print(f"Service is active but the topic endpoint is unavailable: {error}",
              file=sys.stderr)
        return 1
    print("Topic endpoint is responding.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="stream")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("start", help="Start the local user service")
    commands.add_parser("stop", help="Stop the service without clearing the topic")
    commands.add_parser("status", help="Show service health and saved topic")
    commands.add_parser("serve", help="Run the service in the foreground")
    commands.add_parser("install-service", help="Create the user service, without starting it")
    keys = commands.add_parser("keys", help="Control transient keystroke presentation")
    keys.add_argument("action", choices=("on", "off", "toggle", "status"))
    preview = commands.add_parser("preview", help="Control the desktop stream preview")
    preview.add_argument("action", choices=("on", "off", "toggle", "status"))
    chat = commands.add_parser("chat", help="Control YouTube chat presentation")
    chat_commands = chat.add_subparsers(dest="action", required=True)
    chat_commands.add_parser("start").add_argument("argument")
    chat_commands.add_parser("expiry").add_argument("argument")
    chat_commands.add_parser("stop")
    chat_commands.add_parser("status")
    topic = commands.add_parser("topic", help="Save the topic; use an empty string to clear")
    topic.add_argument("text")
    args = parser.parse_args()
    try:
        if args.command in {"start", "stop"}:
            return systemctl(args.command)
        if args.command == "status":
            return status()
        if args.command == "install-service":
            return install_service()
        if args.command == "keys":
            from .keys_control import request

            result = request(args.action)
            print(f"Keys: {result['state']} ({result['reason']})")
            return 0
        if args.command == "preview":
            from .preview import command

            print(f"Preview: {command(args.action)}")
            return 0
        if args.command == "chat":
            from .chat_control import request

            result = request(args.action, getattr(args, "argument", None))
            expiry = result.get("expiry")
            print(f"Chat: {result['state']} ({result['reason']}); "
                  f"expiry: {expiry if expiry is not None else 'off'}; "
                  f"skipped: {result['skipped']}")
            return 0
        if args.command == "topic":
            saved = write_topic(args.text)
            print(f"Topic saved: {saved}" if saved else "Topic cleared.")
            return 0
        serve()
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"stream: {error}", file=sys.stderr)
        return 1
