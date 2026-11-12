---
id: S007
status: Draft
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

- [ ] Inspect relevant local setup and documentation without recording typed
      input or making configuration changes.
- [ ] Investigate candidate input and Hyprland state interfaces, permissions,
      failure modes, and lock and authentication coverage.
- [ ] Propose bounded experiments where necessary, with risks and required
      approval made explicit before any capture or system changes.
- [ ] Report the evidence, unresolved gaps, and a recommended implementation
      approach for review and subsequent refinement.

## Boundaries

Read-only inspection is the initial approach. Running capture, entering test
input, changing permissions or configuration, installing software, source
edits, and validation commands need explicit authorization. Do not test with
real passwords or broadcast input. This slice does not implement presentation,
change the live OBS setup, or treat a workspace gate as a security guarantee.
