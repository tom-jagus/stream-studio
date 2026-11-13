#!/usr/bin/env bash
# Install the local presentation service and its optional Python dependencies.
set -eu

if [ "$(id -u)" -eq 0 ]; then
  printf '%s\n' 'Run this script as your normal desktop user, not root.' >&2
  exit 1
fi
for command in uv systemctl; do
  if ! command -v "$command" >/dev/null 2>&1; then
    printf 'Required command not found: %s\n' "$command" >&2
    exit 1
  fi
done

# Do not replace the Python environment underneath a running service.
state=$(systemctl --user show stream-studio.service --property=ActiveState --value) || {
  printf '%s\n' 'Cannot query the systemd user service manager.' >&2
  exit 1
}
case "$state" in
  inactive | failed | '') ;;
  *) printf '%s\n' 'Stop stream-studio.service before installing or updating.' >&2; exit 1 ;;
esac

root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if [ ! -f "$root/pyproject.toml" ]; then
  printf '%s\n' 'Run the script from a complete Stream Studio checkout.' >&2
  exit 1
fi

# --force replaces the existing uv tool installation of this project.
uv tool install --force --editable "${root}[keys,chat]"
tool_dir=$(uv tool dir)
python="$tool_dir/stream-studio/bin/python"
if [ ! -x "$python" ]; then
  printf '%s\n' 'The installed tool Python could not be found.' >&2
  exit 1
fi

unit="$HOME/.config/systemd/user/stream-studio.service"
if [ -e "$unit" ] || [ -L "$unit" ]; then
  printf '%s\n' 'Existing user unit preserved; verify its ExecStart points to the intended installation.'
else
  "$python" -m stream_studio install-service
fi

printf '%s\n' \
  'Python dependencies installed. The service was not started or enabled.' \
  'Keep this checkout available because the installation is editable.' \
  'Install the reviewed keyboard udev rule separately for keys access;' \
  'see docs/keystroke-overlay.md. Configure the private YouTube API key;' \
  'see docs/youtube-chat-overlay.md. OBS, Chromium, Hyprland, JetBrains Mono,' \
  'uv, systemd and any required system libraries are separate prerequisites.' \
  'When ready, start the service with: stream start'
