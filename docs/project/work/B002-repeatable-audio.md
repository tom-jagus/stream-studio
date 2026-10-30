---
id: B002
status: Draft
---

# Repeatable audio and audiovisual validation

## Outcome

Establish repeatable audio settings and validate the microphone and both camera
feeds together in a local recording.

## Why

A usable stream needs intelligible audio and coordinated audio and video, not
only acceptable camera stills.

## Boundaries

Inspect the actual audio hardware before choosing devices or processing. OBS
owns audio capture and processing for the stream. A basic audio check during
camera work is recommended; the place of deeper audio refinement in the agreed
sequence remains open.

Scene-specific mute behaviour belongs to the relevant scene and control briefs.
This brief establishes the underlying audio setup and combined validation.

## Acceptance criteria

- The chosen audio input and necessary settings or processing are documented
  and can be restored.
- An accepted local recording checks microphone intelligibility, levels, and
  audio/video synchronization with both cameras under intended conditions.
- Restoration and verification instructions match the actual configuration and
  do not expose credentials or unrelated machine configuration.

## Open questions

- What audio hardware and existing OBS processing are in use?
- What processing and validation conditions are needed for acceptable audio?
- When should audio refinement happen relative to scene and service work?
- Should cliamp music have a dedicated application-audio capture or routing path
  independent of the selected desktop/default audio device? This is deferred
  investigation, not an accepted implementation or part of the current layouts.

## Reported issue for follow-up

Tom reports that an OBS audio selection pointed to the Fifine microphone and
music was absent for most of a stream. He changed that selection to Default.
The affected OBS audio slot, actual routing, and effect of the correction have
not been independently verified. Confirm these before choosing a solution;
Default follows the system's device selection and is not a fixed music route.
Check any future dedicated cliamp path for duplicate music capture and preserve
the scene policy of muting only the microphone for Privacy.
