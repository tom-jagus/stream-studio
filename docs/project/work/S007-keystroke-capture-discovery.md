---
id: S007
status: Done
parent: B006
---

# Keystroke capture and safety discovery

## Outcome

Recommend a practical capture and suspension approach for system-wide keystroke
presentation on Tom's actual desktop, with evidence and explicit limitations.

## Acceptance criteria

- Identify the relevant keyboard devices, layout and remapping path, terminal,
  multiplexer, Hyprland version, and lock and authentication components to the
  extent needed for the recommendation. Do not record private typed content.
- Compare viable custom capture approaches, including device permissions,
  keyboard layout and modifiers, device reconnect, and closing devices on manual
  disable. State whether the approach depends on elevated or broad access.
- Assess how to identify focused workspaces 1 through 10 and uncertain states,
  including multi-monitor focus, special or unknown workspaces, startup, IPC
  disconnects, and races between focus and input events. Distinguish documented
  guarantees from assumptions and observations.
- Assess lock screen and system authentication prompt detection on the actual
  setup, including whether focus can be established before input is disclosed.
  Identify uncovered cases and avoid claiming that terminal or browser password
  prompts can generally be detected.
- Recommend how to clear displayed and queued keys, discard events during
  suspension, avoid raw input retention, and handle manual off, restart, and
  return to an allowed workspace. Address Break and Privacy integration as an
  unresolved decision if it cannot be settled from evidence.
- Describe safe verification methods and evidence still required, including how
  to avoid exposing or logging secrets during experiments. State whether the
  intended guarantees are achievable and identify decisions needed before an
  implementation slice can be accepted.

## Tasks

- [x] Inspect relevant local setup and documentation without recording typed
      input or making configuration changes.
- [x] Investigate candidate input and Hyprland state interfaces, permissions,
      failure modes, and lock and authentication coverage.
- [x] Propose bounded experiments where necessary, with risks and required
      approval made explicit before any capture or system changes.
- [x] Report the evidence, unresolved gaps, and a recommended implementation
      approach for review and subsequent refinement.

## Review

Done by Tom's acceptance of the discovery findings and recommendation. He
selected both external keyboards and manual off for Privacy. Implementation
continues in [Slice 8](S008-keystroke-presentation.md).

Local read-only inspection established Hyprland 0.56.2, Alacritty's main-terminal
class, Herdr, Cheapino2 and W-CORNE keyboards, and US mapping with the Omarchy
Shift+Caps Compose option. Fcitx5 is running, so interpreted key events must not
be described as the final application text. Inspected keyboard devices were
root:input without a user ACL, and Tom was not in the input group.

The selected approach is passive Python evdev capture with xkbcommon mapping,
explicit stable device selection, and narrow device-specific access. It avoids
exclusive grabs, injection, broad input-group membership, and running HTTP as
root. A restricted privileged helper could reduce permission exposure but adds
installation and maintenance complexity; it was not selected. Auxiliary
interfaces need capability inspection before inclusion. Closing devices on
manual off does not revoke the user's operating-system access permission.

Hyprland workspace and monitor queries worked. An allowed workspace was focused
on the external monitor while workspace 9 remained visible on the laptop;
filtering must follow focus rather than visibility. Special or unknown workspace
state and IPC loss must suspend presentation. Independent input and IPC streams
cannot establish a race-free confidentiality boundary.

Both `hyprctl -j locked` and `omarchy-shell lock isLocked` returned unlocked.
Installed Omarchy sources expose a lock-request state and an exclusive-focus
polkit layer named `omarchy-polkit`. These support practical suppression, not
proof of suppression before every password keystroke. Hyprland `lockgroups`
concerns window groups, not screen locking. Terminal and browser password
recognition is not a reliable system-wide capability.

Delivery should use a separate keys page with bounded transient memory, clear
on suspension or communication failure, and prevent replay across reconnects.
Keep the topic page unchanged. Controlled checks should use harmless sample
input outside a broadcast, synthetic failure tests first, then approved device,
workspace, lock, and prompt exercises. Never use real passwords as test input.

No devices were opened, typing captured, permissions changed, or lock/prompt
transitions exercised. Device reconnect, layout reconstruction, buffer-loss
recovery, and suppression timing remain implementation verification work, not
proven discovery results.

References consulted:

- [Python evdev interfaces](https://python-evdev.readthedocs.io/en/latest/apidoc.html)
- [Linux input event protocol](https://docs.kernel.org/input/event-codes.html)
- [xkbcommon state handling](https://xkbcommon.org/doc/current/group__state.html)
- [Hyprland IPC](https://wiki.hypr.land/IPC/)

## Boundaries

Read-only inspection is the initial approach. Running capture, entering test
input, changing permissions or configuration, installing software, source
edits, and validation commands need explicit authorization. Do not test with
real passwords or broadcast input. This slice does not implement presentation,
change the live OBS setup, or treat a workspace gate as a security guarantee.
