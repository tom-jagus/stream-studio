---
id: B005
status: Draft
---

# Vial streaming controls

## Outcome

Operate intended OBS actions from a dedicated layer on Tom's 36-key split
keyboard without requiring OBS focus.

## Why

Direct keyboard controls reduce interruptions while working and make scene and
microphone actions accessible during a stream.

## Boundaries

The agreed path is a Vial layer key, host-side handler, control action, and OBS
WebSocket. Hyprland bindings are not the intended control interface. A normal
Vial macro does not itself send network requests.

Dedicated spare keycodes such as F13 through F24 are a recommended bridge, not
selected bindings. Check firmware and Wayland support before choosing the
host-side mechanism. Avoid focus-dependent macros that type shell commands.
Keep control access local and credentials outside browser-visible assets.

Explicit scene selection and mute/unmute actions are recommended over blind
toggles. Controls should reflect actual OBS state rather than assume success.
The exact bindings and position in the implementation sequence remain open.

## Acceptance criteria

- The dedicated Vial layer operates the agreed OBS actions without OBS focus
  under Tom's actual Wayland environment and keyboard firmware.
- Scene and microphone actions produce the intended OBS state, with actual
  state checked rather than inferred solely from a key press.
- Missing OBS connectivity or a failed action does not appear to be a confirmed
  successful state change.
- Bindings, host-side setup, and OBS connection configuration can be restored
  without committing credentials.

## Open questions

- Which scene, microphone, and presentation actions need dedicated controls?
- Which keycodes, host-side handler, and state feedback mechanism are suitable?
- Where should this work fall relative to layouts and the local service?
