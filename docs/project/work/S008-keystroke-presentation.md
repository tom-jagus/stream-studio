---
id: S008
status: In progress
parent: B006
depends_on:
  - S006
  - S007
---

# Controlled keystroke presentation

## Outcome

Present keyboard input from the Cheapino2 and W-CORNE in a local OBS browser
page, with manual controls, workspace gating, and practical lock and system
prompt suppression.

## Acceptance criteria

- `stream keys on`, `stream keys off`, and `stream keys status` operate without
  OBS focus. Status distinguishes disabled, enabled-but-suspended, and presenting
  states and explains suspension without revealing typed input. Service restart
  starts disabled. Manual off clears all display and pending events and closes
  input devices; workspace changes cannot override it.
- Capture is passive and limited to explicitly selected interfaces of the two
  external keyboards, identified independently of unstable event numbers.
  The laptop keyboard and unrelated devices are excluded. No exclusive grab,
  input injection, or showmethekey runtime dependency is introduced.
- Setup provides narrow device-specific access and explains its remaining
  exposure to other processes running as the user. The HTTP service does not
  run as root; world-readable devices and broad input-group membership are not
  installation shortcuts. Installation and removal instructions are explicit.
- While manually enabled, the focused workspace permits display only on 1
  through 5. Workspaces 6 through 10, special or unknown workspaces, uncertain
  focus, and failed or stale IPC state suspend it and clear queued and visible
  keys. Returning to a known allowed state resumes without replaying discarded
  events. Multi-monitor handling follows focus, not workspace visibility.
- Screen lock and the installed Omarchy polkit prompt suspend presentation.
  Use compositor lock state, Omarchy lock-request state, and observed layer
  state as appropriate; missing or untrustworthy required observations suspend
  rather than permit display. Actual timing and uncovered prompt cases are
  documented without promising suppression before every sensitive keystroke.
- Layout interpretation uses xkbcommon with the actual US and Omarchy mapping.
  Modifiers, shortcuts, repeats, and supported lock-key behavior are demonstrated.
  Device loss, reconnect, buffer overflow including SYN_DROPPED, or uncertain
  mapping cannot cause stuck modifiers or replay of stale input. Suspend until
  usable state is restored. Explain firmware, remapping, and Fcitx differences
  between displayed key events and final application text.
- A separate transparent `/keys` page shows ordinary characters and shortcuts
  in JetBrains Mono and Catppuccin Mocha, with readable dark outlines and shadow.
  OBS controls placement. The existing topic page and commands continue working.
  A bounded recent-key display is checked with Vim motions and workflow input;
  its visual defaults can be adjusted during user review.
- Display memory and delivery queues have explicit bounds. No raw keystroke
  history is persisted or logged. Browser updates render text safely, use local
  delivery, clear on suspension and communication loss within a documented and
  tested timeout, and reject stale events across disable, reconnect, or restart.
  Diagnostic and control interfaces do not expose key history unnecessarily.
- Guidance states that Break and Privacy do not automatically disable this
  feature. Tom must use manual off before either scene or any sensitive input;
  reactivation is explicit. No OBS scene integration or Hyprland keybinding
  installation is required. Privacy remains browser-independent.
- Authorized synthetic tests cover state transitions, stale delivery, mapping
  failures, and transport loss. Separately authorized checks with harmless input
  cover both keyboards, reconnect, workspace changes, lock/prompt suppression,
  manual device closure, and OBS output-size readability. Record missing checks
  and observed timing limits rather than treating them as passes.

## Current findings and follow-up

Tom reports that the latest overlay changes and manual toggle appear to work.
During Herdr workspace switches that cleared the display, Hyprland emitted
active-window and title events but no workspace events. The implementation now
ignores active-window events while retaining workspace and layer invalidation.
The display supports up to eleven entries, omits standalone modifiers used in
combinations, and groups identical consecutive presses on the third press.

The earlier synthetic suite passed 43 tests. Tests added or changed since then
have not been run. Complete live checks against the acceptance criteria, including
reconnect, lock and prompt timing, and output-size readability, remain
outstanding. The slice is not yet accepted as complete.

## Tasks

- [x] Inspect candidate keyboard interface capabilities and select stable device
      identities without publishing unnecessary private device identifiers.
- [x] Implement passive capture, layout interpretation, and the manual and
      automatic suspension state machine with bounded transient delivery.
- [x] Prepare narrow-access installation artifacts and removal guidance; obtain
      separate approval before changing system permissions or installing them.
- [x] Add CLI controls and the keys browser page without changing topic behavior.
- [x] Write synthetic tests for the implemented state and capture behavior.
- [x] Investigate the reported Herdr workspace clearing, suppress redundant
      standalone modifiers, and group repeats starting on the third press.
- [x] Increase the maximum display capacity to eleven entries while keeping
      the single-row, oldest-first width limit.
- [x] Add a manual `stream keys toggle` command.
- [ ] Agree on and demonstrate the remaining safe live-device and OBS checks;
      update setup, privacy, recovery, and limitations guidance as needed.

## Boundaries

Application and web-app restrictions, terminal/browser password detection,
mouse display, automatic OBS scene controls, and firmware-layer visualization
are excluded. Device-event access is not a confidentiality boundary. The
permission approach is accepted in principle, but this slice does not authorize
system installation, live capture, testing, source edits, or Git actions.
