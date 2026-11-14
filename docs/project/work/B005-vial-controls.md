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

The selected path uses Vial's Ctrl+Alt+Shift function-key combinations,
Hyprland bindings, a local command, and OBS WebSocket. The scene wrapper selects
and checks the Program scene, then records the last confirmation for the
preview. It does not continuously monitor OBS. Keep credentials outside
browser-visible assets and avoid focus-dependent typed commands.

Explicit scene selection is in use. Microphone and other presentation actions
remain undecided; separate mute and unmute actions are preferable to blind
toggles. Privacy scene entry does not itself disable the keystroke overlay.

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

- Are microphone or other presentation actions needed beyond scene selection?
- Has failure reporting and restoration been checked on the actual setup?

## Current evidence

Tom reports that Vial scene bindings and the preview confirmation work. The
wrapper and its [setup guide](../../topic-overlay.md#obs-scene-controls) are in place.
Failure reporting and restoration remain unverified. The preview reports the
last checked scene, not live changes made directly in OBS. This brief remains
Draft while the remaining actions and acceptance evidence are unsettled.
