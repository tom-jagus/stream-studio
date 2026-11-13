# Stream Studio

My personal streaming environment for sharing development, tools, and working
practices on YouTube. The goal is to make streaming easier to prepare and
operate, while keeping the work readable and giving viewers useful context.

The project brings together camera and audio settings, OBS scenes, keyboard
controls, and local backgrounds and overlays. It is tailored to my desktop and
workflow, with setup guidance so I can restore it without starting from scratch.

The repository contains a Python local presentation service with a topic
overlay, an experimental keystroke overlay, a YouTube chat overlay, a desktop
preview, project plans, camera experiment findings, and a sanitized OBS Working,
Talking, and Privacy scene snapshot with
restoration guidance. The snapshot predates the browser overlays.

## Get started

With Python 3.12 or newer, uv, and a systemd user session, run from this checkout:

```bash
uv tool install --editable .
stream install-service
stream topic "Building Stream Studio"
stream start
stream status
```

Add an OBS Browser Source pointing to `http://127.0.0.1:8766/topic` and position
it in your scene. Install JetBrains Mono locally for the intended typography.
Update the text with `stream topic "A new topic"`, clear it with
`stream topic ""`, and stop the service with `stream stop`.

The [topic overlay guide](docs/topic-overlay.md) covers setup, persistence,
scrolling, fallback, and verification limits.

For the experimental keystroke overlay, see the
[keystroke overlay guide](docs/keystroke-overlay.md) for optional dependencies,
keyboard permissions, OBS setup, and current limitations. Use `stream keys off`
before sensitive input or entering Privacy or Break. Scene changes do not
disable capture, and automatic suspension is not a confidentiality guarantee.

For YouTube chat setup and operation, see the
[YouTube chat overlay guide](docs/youtube-chat-overlay.md).

### Desktop preview

On Hyprland, `stream preview on` opens a Chromium app window with the topic,
keystrokes, and chat. It floats in the reserved right-hand area of `DP-1`.
Use `stream preview off`, `stream preview toggle`, or `stream preview status`
to control or check the window. These commands do not change the desktop layout.
The local service must be running for the preview page to load.

The preview remains part of a full-monitor capture. An opaque OBS sidebar can
visually cover it, but does not exclude it from capture. Check the actual OBS
output with harmless content before streaming.

## Documentation

- [Topic overlay](docs/topic-overlay.md): local service, CLI, and OBS setup.
- [Keystroke overlay](docs/keystroke-overlay.md): setup, privacy, and limitations.
- [YouTube chat overlay](docs/youtube-chat-overlay.md): API setup and operation.
- [Project charter](docs/project/charter.md): purpose, scope, and success criteria.
- [Work index](docs/project/work.md): planned outcomes and current work.
- [Camera experiments](docs/camera-experiments.md): findings and unresolved tuning.
- [OBS scene snapshot](obs/README.md): saved scenes, settings, and restore limits.

## License

No license has been selected. This repository does not currently grant a
third-party reuse license.
