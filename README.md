# Stream Studio

My personal streaming environment for sharing development, tools, and working
practices on YouTube. The goal is to make streaming easier to prepare and
operate, while keeping the work readable and giving viewers useful context.

The project brings together camera and audio settings, OBS scenes, keyboard
controls, and local backgrounds and overlays. It is tailored to my desktop and
workflow, with setup guidance so I can restore it without starting from scratch.

The repository contains a Python topic-overlay service, project plans, camera
experiment findings, and a sanitized OBS Working, Talking, and Privacy scene
snapshot with restoration guidance. The saved scene snapshot predates the local
browser overlay.

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

## Documentation

- [Topic overlay](docs/topic-overlay.md): local service, CLI, and OBS setup.
- [Project charter](docs/project/charter.md): purpose, scope, and success criteria.
- [Work index](docs/project/work.md): planned outcomes and current work.
- [Camera experiments](docs/camera-experiments.md): findings and unresolved tuning.
- [OBS scene snapshot](obs/README.md): saved scenes, settings, and restore limits.

## License

No license has been selected. This repository does not currently grant a
third-party reuse license.
