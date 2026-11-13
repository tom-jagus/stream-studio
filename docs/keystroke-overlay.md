# Keystroke overlay

The experimental `/keys` browser page displays input from the selected
Cheapino2 and W-CORNE keyboard interfaces. It is intended for demonstrations,
not for private input. The service and OBS do not need to be run as root.

## Privacy first

Use `stream keys off` before entering sensitive information or switching to
Privacy or Break. Those scenes do not automatically disable capture. Enable it
again explicitly when it is safe. A service restart also starts with capture
disabled.

Workspace, lock, and authentication-prompt checks reduce exposure but are not
a confidentiality boundary. Desktop and input events arrive independently,
and not every prompt or timing case has been verified. While presentation is
suspended, the capture process may still receive keyboard events to track key
state. Device access also allows other processes in the active user session to
read these keyboards. Do not rely on the overlay to detect password fields.

## Install and operate

This setup targets the current Hyprland and Omarchy desktop and its US layout
with `omarchy:shift_caps_compose`. Install the optional dependencies from the
checkout using the following command in place of the installation command in
the [topic guide](topic-overlay.md):

```bash
uv tool install --editable '.[keys]'
```

If the tool is already installed without the extra, use
`uv tool install --force --editable '.[keys]'`. Restart an existing service
after installing or changing the backend. The service unit points to the
Python environment that created it. Follow the topic guide's remaining service
setup and start steps if the service is not already installed.

The optional rule `system/70-stream-studio-keyboards.rules` grants the active
local session access to keyboard interfaces with the selected USB vendor and
product IDs. It is not restricted to this program. After reviewing the rule,
install it as `/etc/udev/rules.d/70-stream-studio-keyboards.rules`, reload udev
rules, and reconnect the selected keyboards. System changes require appropriate
administrative access. To remove access, turn capture off, delete the installed
rule, reload udev rules, and reconnect the keyboards. Removing the rule does not
close descriptors already open in any process.

With the service running, use:

```bash
stream keys on
stream keys status
stream keys off
```

Status reports disabled, suspended, or presenting and a reason, not key history.
The reader uses passive input access without an exclusive grab or injection.
Only the selected keyboard interfaces are opened, not the laptop keyboard or
unrelated devices. Device loss, input overflow, mapping changes, or uncertain
state can require recovery; release held keys if activation remains suspended.

Add an OBS Browser Source at `http://127.0.0.1:8766/keys` and size and position
it in OBS. Install JetBrains Mono for the intended appearance. The page is
transparent and displays one row of up to eight key entries; older entries are
removed when the row is full. Entries expire after four seconds, refreshed by
a consecutive repeat. Held-key auto-repeat is ignored. Currently, separate
consecutive identical presses combine on the second press with a count.

Presentation is allowed only on focused workspaces 1 through 5. Other, special,
unknown, or uncertain workspaces suspend it, as do observed lock and Omarchy
polkit prompt states. Suspension clears displayed entries and discards events
instead of replaying them; returning to a permitted state can resume only if
manually enabled. The browser checks for stale output every 100 ms and clears
it once the last successful update is more than 750 ms old. Browser scheduling
can delay this; it is not a guaranteed deadline.

Raw keystroke history is not persisted or logged, but active entries are
available briefly through the read-only, unauthenticated loopback `/api/keys`
endpoint. Other local processes can request them while they are available.

The display interprets keyboard events using xkbcommon, not the final text in an
application. Firmware layers, remapping, and input methods such as Fcitx may
therefore make the displayed keys differ from the resulting text.

## Current limitations and verification

Tom reports that capture works and that the latest changes improved switching.
`Ctrl+Shift+3` works as a Herdr workspace shortcut, while `Ctrl+Shift+1`, `2`,
`4`, and `5` still appear to act like Hyprland workspace changes. The cause is
not established, and additional Herdr workspaces have not been tested.

A combination such as `Ctrl+W` currently displays a standalone `Ctrl` before
`Ctrl+W`. The requested follow-up is to omit the standalone modifier and to
start combining identical presses on the third press instead of the second.
See [Slice 8](project/work/S008-keystroke-presentation.md) for the open work.

The latest synthetic suite passed 43 tests. Live reconnect, lock and prompt
suppression timing, and OBS output-size readability still need verification.
The saved OBS scene snapshot predates this browser source. Do not infer that the
snapshot restores it.
