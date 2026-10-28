# Stream Studio

## Problem

Tom needs a personal streaming environment with consistent camera and audio
inputs, readable OBS layouts, and controls that work without focusing OBS.
Device settings, scene presentation, and restoration guidance need to work
together rather than depend on ad hoc adjustments.

## Value

Repeatable settings and saved compositions reduce setup effort. Readable screen
content and useful camera views help viewers follow work and conversation.
Local backgrounds and overlays provide session context without replacing OBS.

## Success

- Camera settings can be restored, with reconnect and restart behaviour tested.
- A local recording validates camera and audio feeds together.
- Six OBS scenes support preparation, work, conversation, breaks, ending, and
  immediate privacy. Working preserves screen readability; Talking prioritizes
  the face camera.
- Vial controls operate OBS without OBS focus. Neovim input visualization stops
  outside focused Neovim and follows an explicit disclosure policy.
- Local presentation works before environmental effects are added, and remains
  usable when external data is unavailable.
- Shared styling and configuration avoid unnecessary duplication. Setup and
  verification guidance allow restoration without exposing private data.

## Boundaries

Stream Studio owns stream-specific configuration, services, presentation, and
setup guidance for Tom's Hyprland / Omarchy desktop. OBS handles capture, audio,
composition, and encoding; a local service supplies backgrounds and overlays.

Scope includes the EMEET C950 face camera, EMEET S600 overhead camera, repeatable
audio settings, and Starting, Working, Talking, Break, Ending, and Privacy
scenes. Working reserves the left 75% for screen content and the right 25% for
cameras and overlays. Talking prioritizes a large face view. Neither uses an
illustrated room. Starting, Break, and Ending share an anime-style room,
initially static and later animated with local daylight and weather variation.

A dedicated Vial layer, host-side handling, and OBS WebSocket are the intended
control path. Input visualization is limited to focused Neovim. Styling follows
the system's Catppuccin theme. Reusable logo design belongs to `brand-identity`;
this project integrates approved assets, but a final logo is not a prerequisite.

Keep credentials, exact private location, and confidential information out of
versioned configuration and browser-visible data. Inspect OBS exports before
publishing. Reserved screen areas and Neovim focus are not confidentiality
guarantees. A general-purpose product, public remote-control interface, and
automatic broadcasting workflow are outside agreed scope.
