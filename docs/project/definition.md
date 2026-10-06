# Project definition

## Purpose

Build Tom's personal streaming environment: consistent camera and audio inputs,
readable OBS compositions, convenient controls, and a maintainable local service
for scene backgrounds and informational overlays.

This is more than an OBS configuration repository. Stream Studio owns the
stream-specific configuration, services, presentation, and setup guidance.

## Agreed scope

- Tune the Emeet C950 face camera and Emeet S600 overhead camera; make settings
  repeatable through programmatic presets where supported and saved OBS
  configuration where necessary.
- Include repeatable audio settings and validation, with exact processing and
  device choices determined after inspection.
- Build six OBS scenes: Starting, Working, Talking, Break, Ending, and Privacy.
- In Working, allocate the left three quarters of the horizontal canvas to
  screen content and the right quarter to cameras and other overlays.
- In Talking, prioritize a large face-camera view with optional overlays. It
  must be visibly different from Working.
- Do not use illustrated room backgrounds in Working or Talking.
- Serve backgrounds and overlays locally. Starting, Break, and Ending share
  an anime-style illustrated room, initially static.
- Provide optional live context such as what is being worked on now and what
  is planned next.
- Use a dedicated Vial keyboard layer for streaming controls, with host-side
  handling and OBS WebSocket integration rather than Hyprland bindings as
  the intended control interface.
- Add keystroke visualization active only while Neovim is focused. The capture
  mechanism and filtering policy require validation before implementation.
- Coordinate stream colours with the system's Catppuccin theme.
- Later, animate the illustrated room and make its appearance respond to local
  day/night conditions and weather.

## Agreed order and dependencies

1. Camera adjustment and repeatable presets.
2. Working and Talking layouts.
3. Local service and static Starting, Break, and Ending room scenes.
4. Neovim-focused keystroke visualization.
5. Later environmental variation and animation.

Colour decisions belong alongside layout and overlay work. Vial controls,
audio refinement, and final logo integration remain in scope, but their exact
position in the sequence is not yet fixed.

## Boundaries and safeguards

- Keep credentials, exact private location, and other confidential information
  out of versioned presets, OBS exports, and browser-visible data.
- Inspect OBS exports before publishing; do not treat the entire OBS user
  configuration directory as safe to commit.
- A reserved desktop area is a layout aid, not a confidentiality guarantee.
- Neovim focus does not make every keystroke safe to broadcast. Filtering and
  explicit activation must be considered before enabling visualization.
- Reusable personal logo design and approved assets belong to `brand-identity`;
  Stream Studio owns their stream-specific integration. A finished logo is not
  a prerequisite for usable scenes.
- No general-purpose product, public remote-control interface, or automatic
  broadcasting workflow is currently agreed.

## Success criteria

- Camera settings can be restored through supported device controls and/or
  documented OBS configuration, with reconnect and restart behaviour tested.
- Audio and camera feeds are checked together in a local test recording.
- Working preserves screen readability and keeps cameras and overlays in the
  intended sidebar; Talking clearly prioritizes the face camera.
- The six-scene collection supports preparation, live work, conversation,
  breaks, ending, and privacy.
- Vial controls can operate intended OBS actions without requiring OBS focus.
- The local presentation is usable before animation or weather integration.
- Keystroke visualization demonstrably stops outside focused Neovim and follows
  an explicit disclosure policy.
- Shared styling and saved configuration avoid unnecessary duplication.
- Setup and verification instructions match the implemented repository and
  allow the environment to be restored without exposing secrets.

## Related documents

- [Design brief](../design.md)
- [Current progress](progress.md)
