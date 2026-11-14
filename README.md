# Stream Studio

Stream Studio is my personal streaming environment for sharing development,
tools, and working practices on YouTube. It brings together OBS scenes, camera
and audio settings, keyboard controls, and local overlays. The setup is tailored
to my Hyprland and Omarchy desktop.

The repository contains a Python service for topic, keystroke, and YouTube chat
overlays, a desktop preview, sanitized OBS scene snapshots, and project plans.

## Get started

With Python 3.12 or newer, uv, and a systemd user session, run from this checkout:

```bash
bash install-services.sh
stream topic "Building Stream Studio"
stream start
stream status
```

The installer replaces the Stream Studio uv tool with an editable installation
including the keys and chat extras. It refuses to update a running service,
preserves an existing user unit, and does not start or enable the service. Keep
the checkout in place and check that an existing unit uses the intended Python
environment. OBS, Chromium, system libraries, keyboard access, and YouTube
credentials need separate setup.

Add an OBS Browser Source at `http://127.0.0.1:8766/topic`. Install JetBrains
Mono for the intended typography. Change the text with
`stream topic "A new topic"`, clear it with `stream topic ""`, and stop the
service with `stream stop`.

**Use `stream keys off` before sensitive input or entering Privacy or Break.**
Scene changes do not disable keystroke capture, and automatic suspension is not
a confidentiality guarantee. See the operating guide before enabling it.

## Documentation

- [Operating guide](docs/topic-overlay.md): service, overlays, desktop preview,
  privacy, YouTube credentials, and OBS scene controls.
- [OBS scene snapshots](obs/README.md): saved scenes and restoration limits.
- [Streaming performance](docs/streaming-performance.md): inspected laptop
  configuration, resource findings, and workload checks.
- [Camera experiments](docs/camera-experiments.md): findings and unresolved tuning.
- [Project charter](docs/project/charter.md): purpose, scope, and success criteria.
- [Work index](docs/project/work.md): planned outcomes and current work.

## License

No license has been selected. This repository does not currently grant a
third-party reuse license.
