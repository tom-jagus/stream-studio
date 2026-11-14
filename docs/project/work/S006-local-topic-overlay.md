---
id: S006
status: Done
parent: B004
---

# Local topic overlay

## Outcome

Operate a local Python presentation service with a `stream` command and show a
persistent, styled stream topic in an OBS Browser Source.

## Acceptance criteria

- `stream start`, `stream stop`, and `stream status` control and report the
  local service. Status distinguishes an unavailable service from a running
  one and reports the saved topic. Failures are reported clearly.
- `stream topic "<topic>"` saves a topic both while the service is running and
  while it is stopped. An empty topic clears it. The topic survives service
  restarts and is stored under `~/.local/share/stream-studio`.
- A local browser page displays changes without an OBS source reload. An empty
  topic hides both the label and topic. The page renders topic content as text,
  not executable HTML.
- The overlay has a transparent background and displays the fixed label
  "Currently working on" and the topic in JetBrains Mono with Catppuccin Mocha
  colors. A dark outline and a separate drop shadow remain visible without
  clipping at the chosen source dimensions.
- A topic that fits remains still. An overflowing topic scrolls slowly in a
  continuous loop with a gap, without moving the label or wrapping the topic.
  A topic change restarts the animation. The speed and gap are assessed at
  actual OBS output size.
- The HTTP service listens locally. If updates fail after the page has loaded,
  it retains the last displayed topic and retries; a restarted service can
  supply the saved state again. Initial page-load failure is documented and the
  existing OBS text source remains available as a manual fallback.
- Installation, service operation, local data and any configuration locations,
  browser-source setup, fallback, and verification are documented. No OBS
  plugin, TTS service, network service, or credentials are required at runtime.
- A safe, authorized OBS check demonstrates placement, transparency,
  readability, scrolling, updates, and empty state. It does not overwrite the
  live setup or require a broadcast. Missing checks are reported rather than
  treated as passes.

## Tasks

- [x] Define the local state and service interface, including clear error
      handling and safe writes when the service is stopped or running.
- [x] Implement the Python CLI and local service, with a user service lifecycle
      compatible with the existing TTS workflow where appropriate.
- [x] Implement the transparent topic page and its overflow animation, with
      reasonable initial visual defaults.
- [x] Provide installation and operating guidance, including an OBS setup and
      a manual fallback that preserves the existing topic source.
- [ ] With explicit authorization, exercise service failures and persistence,
      then check representative short and long topics in OBS at output size.

## Review

Done by Tom's explicit acceptance of the implementation. He added the Browser
Source to his OBS layout, aligned it, and reports that it works correctly. This
is user-reported operational and visual acceptance; no independent observation
of the live scene or itemized failure-case check is claimed.

The implementation includes the Python CLI and user-service installer, atomic
shared topic state, read-only loopback HTTP endpoint, and transparent styled
browser page. The [operating guide](../../topic-overlay.md) documents setup,
state, fallback, and verification limits.

At acceptance, automated tests had been written but not run by the assistant.
A later synthetic suite, including topic tests, passed 43 tests. The manual
failure-recovery and persistence task remains unchecked; that later run does not
establish that every error case or manual check was exercised.
At acceptance, the repository snapshot predated the Browser Source. The newer
[OBS snapshot](../../../obs/README.md) includes it; restoration remains untested.

## Boundaries

This slice covers topic presentation only. Keypress capture, YouTube chat, TTS
integration, room scenes, and changes to Privacy behaviour are excluded. OBS
controls placement; the browser page does not draw the sidebar or scene layout.
Source edits, local service installation, OBS changes, and validation commands
require their respective explicit approvals. The wider Brief 4 remains open.
