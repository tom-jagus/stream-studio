# Design brief

This records the discussed setup and development sequence. Technical approaches
labelled as recommendations are not selected implementations.

## Hardware and environment

| Item | Role / current arrangement |
| --- | --- |
| Emeet C950 | Face camera |
| Emeet S600 | Overhead view of the desk and keyboard |
| 36-key split keyboard | Primary subject of the overhead view; Vial streaming layer planned |
| Adjustable double LED desk lamp | Above the desk, on the same arm as the overhead camera; illuminates the desk and partly the face |
| Desk-lamp controls | Adjustable intensity and warm, neutral, or cool colour temperature |
| Main room light | Neutral white |
| Window | To Tom's left, usually covered |
| Desktop | Hyprland / Omarchy, with a Catppuccin colour scheme |

These are user-reported details, not a device capability inventory. Exact
camera controls, audio hardware, theme flavour, and firmware capabilities have
not been inspected for this project.

## Phase 1: cameras and presets

Inspect both devices before prescribing exposure, white balance, focus,
resolution, or frame rate. Do not assume either camera supports every control.

- Tune the face camera for natural skin tones, useful framing, and consistent
  exposure.
- Tune the overhead camera for keyboard legibility, stable focus, and readable
  hand movement.
- Establish a repeatable lighting arrangement. A consistent neutral-light
  baseline is a recommended starting experiment, not a settled preset.
- Compare baseline and adjusted frames under the same lighting.
- Use recordings to check movement, lighting flicker, and synchronization;
  still frames alone cannot establish these.
- Check USB coexistence, reconnect behaviour, and whether settings reset when
  OBS opens a device.

Recommended storage split: device-level presets for supported controls, OBS
configuration for capture/composition/processing, and separate private values
for secrets or machine-specific details. Whether V4L2 tooling is sufficient
must be established from the devices.

A basic audio check during this phase is recommended; deeper audio processing
and its place in the sequence remain to be determined.

## Phase 2: Working and Talking

### Working

- Screen content occupies the left 75% of the horizontal canvas.
- The right 25% accommodates face and overhead cameras, optional keystrokes,
  and optional Now / Next text.
- No illustrated room background.
- Exact camera sizes, sidebar ordering, and optional source visibility remain
  to be tested at the selected output resolution.

### Talking

- The face camera is the dominant visual element.
- Optional overlays should support conversation rather than reproduce the
  Working sidebar.
- No illustrated room background. Screen capture and overhead placement are
  not requirements of this layout.

Choose output dimensions before final layout tuning. Reuse shared sources or
nested scenes where useful rather than duplicating camera/filter configuration.
A simple Privacy scene independent of browser backgrounds is recommended at
this stage; it should hide captures and mute the microphone.

## Phase 3: local presentation and room scenes

Use OBS for capture, audio, composition, and encoding. The local service owns
presentation state and serves Browser Source content; it is not a replacement
for OBS.

Starting, Break, and Ending share an anime-style room: a desk and computer,
a window, and a city outside. Begin with still artwork and scene-specific text.
Working and Talking may use informational overlays from the same service, but
must not inherit the room background.

Recommended structure:

- Separate background presentation from informational overlays.
- Use layered SVG or transparent artwork, with HTML/CSS for text and later
  lighting/effects; original or appropriately licensed assets only.
- Share state for session title, agenda, Now / Next, break message or timer,
  and ending summary as needed.
- Provide a usable default presentation without waiting for external data.
- Keep controls local and OBS credentials outside browser-delivered assets.

Starting prepares viewers; Break conceals the desktop and mutes the microphone;
Ending summarizes the session. Privacy remains a separate immediate concealment
and mute action, not an instruction to stop broadcasting.

No server language, framework, persistence mechanism, or deployment method is
selected yet.

## Phase 4: Neovim-focused input visualization

The agreed requirement is visualization only while Neovim is focused. A
terminal's active-window identity alone may not prove that Neovim is the active
application inside it, especially with a terminal multiplexer.

Recommended investigation: Neovim-side input events with tested focus handling,
rather than unrestricted system-wide collection. Confirm behaviour with the
actual terminal and any multiplexer before choosing an approach.

Recommended initial safety policy, to confirm before implementation:

- Explicit session opt-in.
- An allowlist of useful Normal/Visual-mode commands.
- No Insert-mode text or command-line contents.
- Clear displayed and queued events on focus loss or entry to Break/Privacy.
- No retained raw keystroke history.

This policy reduces exposure; it does not guarantee that all displayed editor
commands or their context are non-sensitive.

## Cross-cutting work

### Vial controls

Intended path: Vial layer key → host-side handler → control action → OBS
WebSocket. A normal Vial macro does not itself send network requests.

Dedicated spare keycodes, such as F13–F24 where supported, are a recommended
bridge. Select the host-side mechanism after checking Wayland and firmware
support. Avoid focus-dependent macros that type shell commands.

Prefer explicit scene selection and mute/unmute actions, and reflect actual
OBS state rather than assuming every command succeeded. Exact bindings and the
implementation phase are still open.

### Colour and identity

Choose the Catppuccin flavour, typography, and a small set of shared colour and
spacing tokens during scene-layout work. Verify contrast over arbitrary screen
content. A plain name treatment can stand in for a final logo.

Reusable logos and identity decisions belong to `brand-identity`; this project
consumes approved assets and defines their streaming placement.

## Later environmental enhancements

Keep sky, city, window, room, and lighting separable from the start. Add day/night
variation, weather, and animation only after the core presentation works.

Recommended progression: daylight states first, weather states next, subtle
motion last. Derive daylight from local sunrise/sunset; keep location private,
cache weather, and retain a usable presentation when external updates fail.

Weather provider, location precision, refresh cadence, and final animation
style remain undecided.
