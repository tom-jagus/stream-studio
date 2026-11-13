---
id: B006
status: In progress
---

# System-wide keystroke presentation

## Outcome

Show selected sessions of system-wide keyboard input in an OBS browser overlay
for Vim motion, keyboard, and workflow demonstrations, with explicit controls
and workspace-based suspension.

## Why

Viewers can follow the keys used during a demonstration, including ordinary
typed characters. Showing all input can also reveal passwords and other private
text, so presentation must be intentional and easy to stop.

## Boundaries

The Neovim-only scope is replaced by system-wide presentation. The initial
feature includes ordinary typed characters and keyboard shortcuts. Use a custom
solution, potentially with existing input libraries; showmethekey may inform
the design but is not a runtime dependency. The local presentation service and
an OBS Browser Source are the intended presentation path. Initially support
only the Cheapino2 and W-CORNE external keyboards. Use passive evdev capture,
xkbcommon interpretation, and narrow device-specific access rather than broad
input-group membership or running HTTP as root. See the accepted findings in
[Slice 7](S007-keystroke-capture-discovery.md) and the proposed implementation in
[Slice 8](S008-keystroke-presentation.md), which is in progress.

Presentation starts manually disabled after service restart. A local command
must enable and disable it, and be suitable for a later Hyprland keybinding.
Manual disable persists until explicit re-enablement and closes the input
devices. While manually enabled, workspaces 1 through 5 permit presentation;
workspaces 6 through 10 suspend it and returning to an allowed workspace resumes
it. Unknown workspaces, unavailable or uncertain focus state, and lost IPC
must suspend presentation. On suspension or disable, clear displayed and queued
keys and discard events rather than replaying them on return. Do not retain raw
keystroke history or log typed input.

Investigate automatic suspension for the actual lock screen and system
authentication prompts. Do not assume ordinary window or workspace state proves
which surface has keyboard focus. Application and web-app restrictions are
possible later additions, not initial requirements. Terminal and browser
password fields cannot generally be detected reliably by a system-wide input
reader; Tom will manually disable presentation before sensitive input.
Workspace restrictions and automatic suspension are not confidentiality
guarantees. The capture process may receive sensitive keys even when the
workspace gate suppresses display.

Keep Privacy browser-independent. Initially rely on manual off before Privacy,
Break, or sensitive input; automatic OBS scene integration is deferred. A scene
change alone does not close devices or clear key presentation. No actual
keyboard capture or privileged access is authorized by this brief.

## Acceptance criteria

- An explicit session command enables and disables presentation without OBS
  focus. A service restart starts disabled; manual disable closes input devices
  and does not automatically reverse on a workspace change.
- While enabled, ordinary characters and shortcuts can be presented in a local
  OBS Browser Source for the intended demonstrations, with keyboard layout,
  modifiers, and supported devices documented.
- Tests demonstrate the agreed workspace gating, automatic resumption, and
  fail-closed behaviour for unknown state and IPC loss. Suspended events do not
  reappear, and displayed and queued keys are cleared when suspension begins.
- Tests cover activation, manual disable, restart, device disconnect and
  reconnect, and rapid focus or workspace changes, including the limitations of
  independently delivered focus and input events.
- The implementation and guidance explain input-device permissions, what may
  be captured, automatic lock and system prompt coverage and its limits,
  browser-visible state, safe shutdown, and manual precautions. Raw keystrokes
  are not retained or logged.
- The selected lock and system-authentication handling is tested on the actual
  setup. Any uncovered prompt or uncertainty is explicit; no confidentiality
  guarantee is claimed. Guidance and checks cover manual off before Break or
  Privacy and explicit re-enablement afterward.

## Open questions

- What lock and authentication suppression timing and remaining races can be
  demonstrated on the actual setup?
- Which visual defaults best support the demonstrations at OBS output size?

## Risks

All-key display can expose private input. Workspace gating is a convenience and
risk reduction, not a security boundary. Manual disable before sensitive input
remains necessary, including for terminal and browser passwords. If the
required focus or prompt state cannot be established, suspend presentation and
report the limitation rather than treating uncertain state as safe.
