# Stream Studio operating guide

Stream Studio runs a local presentation service for OBS Browser Sources. It
provides a persistent topic, experimental keystroke display, and YouTube chat.
A separate Chromium preview and OBS scene-switching command are available on
Tom's Hyprland desktop. OBS owns capture, placement, audio, and encoding.

## Install and start

The installer needs Python 3.12 or newer, uv, and a Linux systemd user session.
OBS with Browser Source support and a locally installed JetBrains Mono font are
needed for the overlays. Installation may need network access. The keys and
chat features have additional requirements below.

Stop any running Stream Studio service before replacing its Python environment.
From the checkout, run:

```bash
bash install-services.sh
stream topic "Building Stream Studio"
stream start
stream status
```

The installer replaces the Stream Studio uv tool with an editable installation
including the keys and chat extras. Keep the checkout in place. It creates a
systemd user unit if absent, preserves an existing unit, and does not start or
enable it. Check that an existing unit points to the intended Python environment.
If `stream` is not on your PATH, run `uv tool update-shell` and open a new
terminal. Startup is manual unless you explicitly enable the unit:

```bash
systemctl --user enable stream-studio.service
```

Enabling affects future user sessions; `stream start` starts it now.
`stream stop` stops the service without clearing the topic. After a successful
service command, `stream start` requests cliamp volume at -15 dB and
`stream stop` requests 0 dB. The CLI checks the reported level and warns if it
cannot confirm it, without changing the service command's exit status. It does
not remember the previous level, reapply it when cliamp starts later, or reset
it when the service stops through another command. cliamp is optional; these
commands do not change the desktop master volume.

`stream status` reports service, topic, keys, chat, and preview status. It
continues if a module is unavailable and returns nonzero if it cannot check one.
`stream serve` runs the service in the foreground for debugging. Do not run it
alongside the user service: port 8766 must be free. `stream install-service`
creates the user unit without starting or enabling it and refuses to overwrite
an existing unit. To inspect service errors, run:

```bash
journalctl --user -u stream-studio.service -n 50 --no-pager
```

## Topic overlay

Add an OBS Browser Source at `http://127.0.0.1:8766/topic`. A 610 x 160
viewport is a starting suggestion, not the recorded size of the accepted source.
Position and size it in OBS. The HTTP interface is read-only and listens on
`127.0.0.1:8766`; the topic feature requires no external service or credentials.

```bash
stream topic "A new topic"
stream topic ""
```

The first command saves public topic text even when the service is stopped; the
second clears it and hides the label and topic. State lives in
`~/.local/share/stream-studio/topic.json`. Writes replace the file atomically;
the last completed write wins. Topics are limited to 2,000 characters, cannot
contain line breaks or ASCII control characters, and have surrounding
whitespace removed. A malformed state file produces an error; saving a
replacement topic writes a new valid file.

The transparent page shows "Currently working on" and the topic in JetBrains
Mono and Catppuccin Mocha. An outline and shadow improve contrast. Short topics
stay still; overflowing text loops left at 30 pixels per second with an
80-pixel gap. Changing the topic restarts the animation. Check readability and
shadow clearance at the actual OBS output size.

The page polls roughly once per second and inserts text, not HTML. A loaded
page retains its last topic and retries if updates fail, so stopping the service
does not hide a stale topic. Clear it while the service is running or hide the
source in OBS. If the initial page load fails, start the service and refresh the
source. Keep the previous OBS text source hidden as a manual fallback. Privacy
must remain browser-independent.

Styling lives in `src/stream_studio/web/topic.css` and scrolling speed in
`topic.js`. There is no general application configuration file yet.

## Keystroke overlay

**Use `stream keys off` before sensitive input or entering Privacy or Break.**
Scene changes do not disable capture. Enable it again explicitly only when safe.
A service restart starts with capture disabled. This experimental feature is
for demonstrations, not private input.

Workspace, lock, and authentication-prompt checks reduce exposure but are not a
confidentiality boundary. Desktop and input events arrive independently, and
live lock and prompt suppression and their timing remain unverified. While
presentation is suspended, the capture process may still receive keyboard events
to track key state. Password fields cannot generally be detected. Never use a
real password for a test.

### Keys setup

The implementation targets the selected Cheapino2 and W-CORNE external
keyboard interfaces on the current Hyprland and Omarchy desktop, using the US
layout with `omarchy:shift_caps_compose`. The service and OBS do not need root.
The installer includes the keys extra. For a keys-only replacement installation,
use `uv tool install --force --editable '.[keys]'` from the checkout instead;
this omits the chat extra. If the user unit does not exist, run
`stream install-service` afterward.

The optional `system/70-stream-studio-keyboards.rules` grants the active local
session access to interfaces with the selected USB vendor and product IDs. It is
not limited to this program: other processes in the session can read them.
After reviewing it, install the rule as
`/etc/udev/rules.d/70-stream-studio-keyboards.rules`, reload udev rules, and
reconnect the keyboards. This system change requires administrative access.
To remove access, turn capture off, delete the installed rule, reload udev
rules, and reconnect the keyboards. Removing the rule does not close descriptors
already open in any process.

### Keys operation

With the service running:

```bash
stream keys on
stream keys toggle
stream keys status
stream keys off
```

Toggle switches the manual enabled state. If enabled but suspended, toggle turns
capture off and closes the devices. Use `off`, not toggle, before sensitive
input. Status reports disabled, suspended, or presenting and a reason, not key
history. Capture is passive, without an exclusive grab or injection. Only the
selected interfaces are opened, not the laptop keyboard or unrelated devices.
Device loss, input overflow, mapping changes, or uncertain state may require
recovery. Release held keys if activation remains suspended.

Add an OBS Browser Source at `http://127.0.0.1:8766/keys` and size and position
it in OBS. The transparent page displays up to eleven entries in one row. Older
entries disappear when the row is full or too narrow. Entries expire after four
seconds, refreshed by a consecutive repeat. Held-key auto-repeat is ignored.
The first two identical presses appear separately; the third combines them with
a count. A modifier used in a combination does not appear separately; one
pressed alone appears when released. When manually disabled, the OBS page and
preview show a small gray "Keys display disabled" message. Suspended and
unavailable states clear the display.

Presentation is allowed only on focused workspaces 1 through 5. Other, special,
unknown, or uncertain workspaces suspend it, as do observed lock and Omarchy
polkit prompt states. Suspension clears entries and discards events instead of
replaying them. Returning to a permitted state can resume only if manually
enabled. The browser checks for stale output every 100 ms and clears it once
the last successful update is more than 750 ms old. Browser scheduling can delay
this; it is not a guaranteed deadline.

Raw key history is not persisted or logged. Active entries are briefly available
through the read-only, unauthenticated loopback `/api/keys` endpoint; other
local processes can request them. The display interprets events with xkbcommon,
not the final text in an application. Firmware layers, remapping, and input
methods such as Fcitx can make the display differ from resulting text.

Tom reports that controls, device selection, workspace gating, reconnect, and
OBS presentation work. Live lock and authentication-prompt checks remain open;
see [Slice 8](project/work/S008-keystroke-presentation.md).

## YouTube chat overlay

The service connects to YouTube's read-only live chat API. It does not send or
moderate messages. A live connection and OBS presentation have been used, but
retry, failure handling, and browser rendering have not been fully verified.

### Chat setup

The installer includes the chat extra. In Google Cloud, create or select a
project, enable YouTube Data API v3, and create an API key. Apply appropriate
restrictions and allow the required YouTube API access. The key must work for both
video lookup and live chat. API availability, quota, and restrictions are
governed by Google.

Save the key as `~/.config/stream-studio/youtube-api-key`, owned by your user
and readable only by you, with mode `600`. If `XDG_CONFIG_HOME` is set, use
`$XDG_CONFIG_HOME/stream-studio/youtube-api-key` instead. Do not put the key in
the repository, a command line, or OBS. After changing the installed service's
code or dependencies, restart it when safe:

```bash
stream stop
stream start
```

Restarting clears transient chat and starts keystroke capture disabled.

### Chat operation

With the service running, select a live broadcast by YouTube URL or 11-character
video ID:

```bash
stream chat start 'https://www.youtube.com/watch?v=VIDEO_ID'
stream chat status
stream chat stop
```

Starting replaces the previous selection. Lookup and connection happen in the
background, so check status afterward. Status reports connection state, reason,
expiry preference, and skipped timestamp count. Stop clears transient messages.
The service does not select a broadcast automatically after restart. Add an OBS
Browser Source at `http://127.0.0.1:8766/chat`; OBS controls its placement and
visibility.

Messages are held in memory, not archived. The service keeps at most 50, with
bounded author and message lengths. The browser shows the newest messages that
fit. Each chat page assigns author colors randomly from a Catppuccin palette
while the author's messages remain in its current set. Authors can share colors,
and OBS and the preview may choose different colors.

Messages remain visible by default. To expire them, use a positive whole number
of minutes of at most nine digits; use `off` to disable expiry:

```bash
stream chat expiry 5
stream chat expiry off
```

The preference persists in `~/.config/stream-studio/chat.json`, or under
`XDG_CONFIG_HOME` when set. With expiry enabled, age uses YouTube's posting
time. Messages with missing or invalid timestamps, or timestamps more than 60
seconds in the future, are skipped and counted in status. An inaccurate system
clock affects expiry. The input limit remains an open discrepancy with
[Slice 9](project/work/S009-youtube-chat-overlay.md).

Viewer messages shown in OBS are public on the broadcast. Hiding the source and
moderation remain manual OBS and YouTube responsibilities. Privacy and Break
do not stop chat; use `stream chat stop` when needed.

For a missing or unsafe key, check its path, owner, and mode. For lookup or
connection failures, check that the broadcast is live, chat is enabled, the key
and API restrictions permit access, and quota and network access are available.
Errors may combine causes. Lookup and connection failures are retried with
increasing delays capped at 60 seconds; check status rather than assuming
recovery. Missing chat dependencies or a missing or unsafe key stop the worker.
After correcting the key, start chat again. After installing dependencies,
restart the service and start chat again. The service does not deliberately log
message content.

To rotate a key, create a replacement, replace the private file, revoke the old
key in Google Cloud, and start chat again. To remove access, stop chat, delete
the file, and revoke the key. Deleting the local file alone does not revoke it.
The separate expiry preference can be removed by deleting `chat.json` while
the service is stopped.

## Desktop preview

On Hyprland, `stream preview on` opens a Chromium app window with the topic,
keystrokes, chat, and last confirmed OBS scene. Use `stream preview off`,
`stream preview toggle`, or `stream preview status` to control or check it.
The service must be running for the page to load. These commands do not change
the desktop layout.

The preview floats in the reserved right-hand area of `DP-1`, inset by three
logical pixels at the left edge, and is pinned across that monitor's workspaces.
It requires Chromium, Hyprland window dispatch support, and exactly one connected
monitor named `DP-1`, with no transform and a positive scale. Hyprland must
already report a right-hand reserved area wider than three logical pixels. The
preview does not create it; inspect `hyprctl monitors` and restore the
reservation in your desktop configuration if needed.

The preview remains part of a full-monitor capture. An opaque OBS sidebar can
visually cover it, but does not exclude it. Check actual OBS output with
harmless content before streaming. Key presentation still follows the workspace
restrictions above.

## OBS scene controls

The Vial streaming layer sends shortcuts to Hyprland. Bindings run
`obs-scene-switch`, which uses `obs-cmd` and OBS WebSocket to select the Program
scene without focusing OBS. The wrapper queries OBS and records the last
confirmed scene for the preview.

### Scene-control setup

Enable the WebSocket server and authentication in OBS under Tools > WebSocket
Server Settings. Note the port and password. Install `obs-cmd` separately; the
local setup used version 1.0.3. The wrapper also needs Bash, `jq`, `flock`,
`timeout`, and `date`, and expects `obs-cmd` at `~/.local/bin/obs-cmd`. Keep the
checkout in place and link the executable wrapper into the same directory:

```bash
mkdir -p ~/.local/bin
ln -s "$HOME/src/default/stream-studio/obs-scene-switch" ~/.local/bin/obs-scene-switch
```

Adjust the checkout path if necessary and avoid overwriting an existing command.
The installer does not install the wrapper or `obs-cmd`.

Store WebSocket settings in `~/.local/share/stream-studio/obs-connection`. The
wrapper sources this file as Bash, so do not use a file you do not trust. Create
it privately using the password prompt below and adjust the port if necessary:

```bash
mkdir -p ~/.local/share/stream-studio
read -r -s -p 'OBS WebSocket password: ' obs_password; printf '\n'
(umask 077; printf 'export OBS_WEBSOCKET_URL=%q\n' \
  "obsws://localhost:4455/$obs_password" > ~/.local/share/stream-studio/obs-connection)
chmod 600 ~/.local/share/stream-studio/obs-connection
unset obs_password
```

The password is plaintext in this file and passed in the `obs-cmd` process
environment. Keep it out of Git and browser assets. Use an alphanumeric password
to avoid URL delimiter issues. Local WebSocket access permits OBS control; use
authentication and avoid exposing the server to untrusted networks.

### Scene-control operation

Map the Vial layer to shortcuts recognized by Hyprland and check collisions with
`omarchy menu keybindings --print`. For example, in the personal Hyprland
bindings file:

```lua
o.bind("CTRL + ALT + SHIFT + F12", "OBS Privacy",
  [[obs-scene-switch "PRIVACY"]])
o.bind("CTRL + ALT + SHIFT + F11", "OBS Work",
  [[obs-scene-switch "WORK - Face: ON, Desk: ON"]])
```

Scene names must match the active OBS collection exactly, including case. Adapt
the examples and other bindings to the collection and keep each command string
on one line. After editing, run `hyprctl reload` and `hyprctl configerrors`.
The wrapper can also be invoked in a terminal:

```bash
obs-scene-switch 'PRIVACY'
```

These commands switch the live Program scene, including in Studio Mode. Use
them only when safe. The wrapper serializes its own requests, asks OBS to
switch, and queries the Program scene. It atomically writes the result to
`~/.local/share/stream-studio/scene.json`. Unexpected `obs-cmd` output is a
failure. It does not change microphone mute state or disable key capture.

The preview shows the last confirmed scene and check time, or the last error.
Failure preserves the previous confirmation, which may be stale. Direct OBS
changes are not tracked, and a successful check does not establish continued
connectivity. Preview needs the local service; switching does not. Do not rely
on this status as a privacy guarantee.

Tom reports that Vial bindings, scene confirmation, and preview work. Failure
reporting and restoration on another setup have not been verified. Privacy still
has outstanding immediate-entry and output-audio checks. Desktop audio and music
are not promised silent. See the [OBS snapshot guide](../obs/README.md) for
manual Privacy operation and restoration limits.

## Verification

The synthetic test suite can be run from the checkout with Python 3.12 or newer:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Historical test counts do not prove the current checkout passes. For a bounded
manual check outside a broadcast, use harmless content to check topic updates,
scrolling, clearing and recovery, keys controls and OBS output, and chat
connection and presentation. Live lock and authentication-prompt timing, chat
failure paths, and restored OBS output remain unverified. The
[OBS snapshot guide](../obs/README.md) describes restoration checks; the
[performance guide](streaming-performance.md) covers a representative workload.
