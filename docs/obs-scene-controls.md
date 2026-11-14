# OBS scene controls

The Vial streaming layer sends keyboard shortcuts to Hyprland. Bindings run
`obs-scene-switch`, which uses `obs-cmd` and OBS WebSocket to select the Program
scene without focusing OBS. The wrapper then queries OBS and records the last
confirmed scene for the Stream Studio preview.

## Setup

Enable the WebSocket server and authentication in OBS under Tools > WebSocket
Server Settings. Note the port and password. Install `obs-cmd` separately; the
local setup used version 1.0.3. The wrapper also needs Bash, `jq`, `flock`,
`timeout`, and `date`. It expects `obs-cmd` at `~/.local/bin/obs-cmd`. Keep the
checkout in place and link the wrapper into the same directory:

```bash
mkdir -p ~/.local/bin
ln -s "$HOME/src/default/stream-studio/obs-scene-switch" ~/.local/bin/obs-scene-switch
```

Adjust the checkout path if necessary. The link must point to an executable
wrapper; it is not installed by `install-services.sh`. Avoid overwriting an
existing command. The `obs-cmd` installation is separate from this repository.

Store the WebSocket settings in `~/.local/share/stream-studio/obs-connection`.
The wrapper sources this file as Bash, so do not source a file you do not
trust. To create it privately, use the OBS password prompt below and adjust the
port if necessary:

```bash
mkdir -p ~/.local/share/stream-studio
read -r -s -p 'OBS WebSocket password: ' obs_password; printf '\n'
(umask 077; printf 'export OBS_WEBSOCKET_URL=%q\n' \
  "obsws://localhost:4455/$obs_password" > ~/.local/share/stream-studio/obs-connection)
chmod 600 ~/.local/share/stream-studio/obs-connection
unset obs_password
```

The password is plaintext in this file and is passed in the `obs-cmd` process
environment. Keep it out of Git and browser assets. Use an alphanumeric
password to avoid URL delimiter handling issues. Local WebSocket access permits
OBS control; use authentication and avoid exposing the server to untrusted
networks.

## Bind and operate

Map the Vial layer to shortcuts that Hyprland recognizes, then check for
collisions with `omarchy menu keybindings --print`. In the personal Hyprland
bindings file, for example:

```lua
o.bind("CTRL + ALT + SHIFT + F12", "OBS Privacy",
  [[obs-scene-switch "PRIVACY"]])
o.bind("CTRL + ALT + SHIFT + F11", "OBS Work",
  [[obs-scene-switch "WORK - Face: ON, Desk: ON"]])
```

Scene names must match the active OBS collection exactly, including case.
Adapt the examples and other bindings to the actual collection. Keep each
command string on one line. After editing, run `hyprctl reload` and
`hyprctl configerrors`. The wrapper can also be invoked in a terminal:

```bash
obs-scene-switch 'PRIVACY'
```

These commands switch the live Program scene, including in Studio Mode. Use
them only when safe. The wrapper serializes its own requests, asks OBS to
switch, and queries the Program scene. It writes the result atomically to
`~/.local/share/stream-studio/scene.json`. It depends on the human-readable
output format of the installed `obs-cmd`; an unexpected format is treated as a
failure. It does not change microphone mute state or disable the keys overlay.

The preview shows the last confirmed scene and check time, or the last error.
A failure preserves the previous confirmation, which may be stale. Changes made
directly in OBS are not tracked, and a successful check does not establish
continued connectivity. The preview is unavailable without the local service;
the switching command does not depend on that service. Do not rely on this
status as a privacy guarantee.

Privacy still has outstanding immediate-entry and output-audio checks. Desktop
audio and music are not promised silent. Use `stream keys off` before Privacy,
Break, or sensitive input. See the [OBS guide](../obs/README.md) and
[keystroke guide](keystroke-overlay.md).

Tom reports that the Vial bindings, scene confirmation, and preview work. The
failure path and restoration on another setup have not been verified as part of
this work. Check those separately when safe and never test privacy assumptions
with confidential material.
