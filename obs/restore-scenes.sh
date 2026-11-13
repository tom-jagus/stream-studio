#!/usr/bin/env bash
# Install a separate sanitized scene collection. Run only while OBS is closed.
set -eu

if pgrep -x obs >/dev/null 2>&1; then
  printf '%s\n' 'Close OBS before restoring the scene collection.' >&2
  exit 1
fi

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
snapshot="$here/current-scenes.json"
image="$here/assets/privacy.png"
target_dir="${XDG_CONFIG_HOME:-$HOME/.config}/obs-studio/basic/scenes"
target="$target_dir/stream-studio-restored.json"

if [ ! -f "$snapshot" ] || [ ! -f "$image" ]; then
  printf '%s\n' 'Snapshot or Privacy image is missing.' >&2
  exit 1
fi
if [ ! -d "$target_dir" ]; then
  printf '%s\n' 'OBS scene directory does not exist. Run OBS setup first.' >&2
  exit 1
fi

umask 077
python3 - "$snapshot" "$image" "$target" <<'PY'
import json
import os
import sys
from pathlib import Path

snapshot, image, target = map(Path, sys.argv[1:])
collection = json.loads(snapshot.read_text(encoding="utf-8"))
images = [source for source in collection["sources"]
          if source.get("id") == "image_source"
          and source.get("settings", {}).get("file") == "SELECT_PRIVACY_IMAGE"]
if len(images) != 1:
    raise SystemExit("Expected exactly one Privacy image placeholder; no file written.")
images[0]["settings"]["file"] = str(image.resolve())
body = (json.dumps(collection, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
try:
    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
except FileExistsError:
    raise SystemExit("The restored collection already exists; no file overwritten.")
try:
    with os.fdopen(fd, "wb") as output:
        output.write(body)
except BaseException:
    target.unlink(missing_ok=True)
    raise
print("Installed a separate Stream Studio Restored scene collection.")
print("Open OBS and select it, then reconnect devices and screen capture.")
print("Review text, audio mute states, browser sources, and Privacy before use.")
PY
