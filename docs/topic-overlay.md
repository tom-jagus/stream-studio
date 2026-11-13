# Local topic overlay

The Python service supplies styled topic text to an OBS Browser Source. OBS
controls its placement. The service does not generate a sidebar, control audio,
or depend on TTS. The `stream` CLI can adjust cliamp volume when starting or
stopping the service. The HTTP interface is read-only and listens on
`127.0.0.1:8766`.

## Install and start

Requirements are Python 3.12 or newer, uv, a Linux systemd user session, OBS
with Browser Source support, and a locally installed JetBrains Mono font.
Installation may need network access to obtain build tools and dependencies.
The topic feature itself does not require external services. The
[keystroke overlay](keystroke-overlay.md) has additional privacy requirements.

From the repository root, stop any running Stream Studio service before
replacing its Python environment, then run:

```bash
bash install-services.sh
stream topic "Building Stream Studio"
stream start
stream status
```

The installer replaces the Stream Studio uv tool with an editable installation
including the keys and chat extras. It creates the systemd user unit if absent
and does not start or enable it. An existing unit is preserved; verify that it
points to the intended Python environment. Keep the installation and checkout
available at their installed locations. If you have already run the installer,
skip that command and continue with the topic and start commands.

If `stream` is not on your PATH, run `uv tool update-shell` and open a new
terminal. Startup is manual unless you explicitly enable the user unit:

```bash
systemctl --user enable stream-studio.service
```

Enabling it affects future user sessions; `stream start` starts it now.

## Commands and state

| Command | Effect |
|---|---|
| `stream start` | Start the systemd user service, then request cliamp volume at -15 dB. |
| `stream stop` | Stop the service without clearing the topic, then request cliamp volume at 0 dB. |
| `stream status` | Report service and topic health, saved topic, keys, chat, and preview status. |
| `stream topic "A new topic"` | Save the public topic, even while the service is stopped. |
| `stream topic ""` | Clear the topic and hide both label and topic. |
| `stream serve` | Run in the foreground for debugging; stop with Ctrl+C. |
| `stream install-service` | Create the user unit without starting or enabling it. |

The cliamp volume change runs only after the service command succeeds. The CLI
checks cliamp's reported level and warns if it cannot confirm it; the service
command's exit status is unchanged by that warning. It does not remember a
previous level. Starting or restarting cliamp later does not reapply the level,
and stopping the service outside `stream stop` does not reset it. cliamp is
optional; these commands do not change the desktop master volume.

`stream status` continues reporting other modules if one is unavailable. It
returns a nonzero status if the service, topic, keys, chat, or preview status
cannot be checked. The individual `stream keys status`, `stream chat status`,
and `stream preview status` commands remain available.

Topic state lives at `~/.local/share/stream-studio/topic.json`. Writes replace
the file atomically so readers do not see partial updates. The last completed
write wins. Topics are limited to 2,000 characters, cannot contain line breaks
or ASCII control characters, and have surrounding whitespace removed.

There is no application configuration file yet. Future application configuration
belongs under `~/.config/stream-studio`; the systemd unit uses its conventional
user-unit directory instead. Current styling lives in
`src/stream_studio/web/topic.css` and scrolling speed in `topic.js`.

## OBS setup

Start the service before loading the Browser Source. Add a source with URL
`http://127.0.0.1:8766/topic`. A 610 × 160 viewport is a starting suggestion,
not a record of the accepted local source's dimensions. Position and size it in
OBS, and reuse the source or shared scene where appropriate.

The page has a transparent background, a fixed "Currently working on" label,
and JetBrains Mono text in Catppuccin Mocha colors. Crust outlines and a separate
drop shadow give the letters definition. Keep enough source height for the
label, topic, and shadow. A short topic stays still; an overflowing topic loops
left at 30 pixels per second with an 80-pixel gap. Changing the topic restarts
the animation. Browser width determines when it overflows.

The page polls roughly once per second and inserts topics as text, not HTML.
An empty topic hides everything. A loaded page retains its last topic and
retries when updates fail. That retained topic may be stale, so stopping the
service is not a way to hide it. Clear the topic while the service is running
or hide the source in OBS instead.

If the service is unavailable during the initial page load, OBS may show an
error or blank source. Start the service and refresh the source. Keep the
previous OBS text source hidden as a manual fallback. Privacy must remain
browser-independent.

The [OBS snapshots](../obs/README.md) include an earlier collection without
browser overlays and a newer sanitized collection with the topic Browser Source.
The newer restoration has not been tested in OBS.

## Troubleshooting and verification

Use `stream status` to distinguish an inactive user service from an active
service whose topic endpoint is unavailable. View service errors with:

```bash
journalctl --user -u stream-studio.service -n 50 --no-pager
```

Port 8766 must be free. Do not run `stream serve` alongside the user service.
Malformed saved state produces an error rather than silently clearing it;
`stream topic "Replacement topic"` writes a new valid state file.

Tom reports that the overlay works in his aligned OBS layout and accepts the
implementation. That is user-reported visual and operational evidence, not a
record of every failure case. The latest synthetic suite, including topic and
keystroke tests, passed 56 tests. To run it from the checkout with Python 3.12
or newer:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

For a bounded manual check outside a broadcast, compare short and long topics,
clear the topic, and check outline and shadow visibility at actual output size.
Check saved state across stop/start and recovery of an already loaded page.
These are suggested checks, not claims that each was performed.
