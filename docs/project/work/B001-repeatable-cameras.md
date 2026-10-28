---
id: B001
status: Draft
---

# Repeatable camera setup

## Outcome

Establish useful face and overhead camera images and a tested way to restore
supported device controls and any required OBS settings.

## Why

Camera consistency is the first agreed step and gives layout work reliable
inputs instead of images that change with each application or reconnect.

## Boundaries

Use the EMEET C950 for the face and EMEET S600 for the desk and 36-key split
keyboard. Inspect actual capabilities before selecting controls or modes.
Prefer device-level settings outside OBS where supported. Tom's current tuning
intent is manual exposure and white balance with continuous autofocus.

The user-reported arrangement includes an adjustable double LED desk lamp on
the overhead camera arm, a neutral-white room light, and a usually covered
window to Tom's left. The lamp illuminates the desk and partly the face. Its
intensity and warm, neutral, or cool setting are adjustable. The final lighting
baseline is not selected; neutral lighting is a recommended starting experiment.

Store supported device presets separately from OBS capture, composition, and
processing settings. Keep private or machine-specific values separate. Whether
V4L2 tooling is sufficient remains to be validated. Saved OBS exports must be
inspected for private data rather than copied from the entire user directory.

No preset is accepted. The C950 has undergone initial comparisons; the S600 has
only been inventoried. Findings and unfinished trial values remain in
[camera experiments](../../camera-experiments.md), not in a restoration preset.
Camera access and device adjustment require renewed approval in a new session.

## Acceptance criteria

- Both cameras have accepted framing, exposure, colour, and focus under a
  documented, repeatable lighting arrangement. The overhead view makes the
  keyboard and hand movement readable.
- Selected capture modes work with both cameras streaming simultaneously.
- Matched-light comparisons and recordings establish image quality, movement,
  and lighting-flicker behaviour rather than relying on still frames alone.
- Restoration uses stable device identification and supported controls or
  documented OBS configuration. Reopening, reconnecting, restarting, and OBS
  opening the cameras have been tested for resets or overrides.
- Setup and verification guidance distinguish accepted settings from experiments
  and allow restoration without exposing private values.

## Open questions

- Does opening `omarchy-webcam` enable automatic white balance? Compare control
  readback before and after opening it without moving sliders, then verify the
  manual state after opening the chosen preview.
- Which lighting baseline and manual colour settings are acceptable? Some
  preferred C950 comparisons used automatic white balance and do not validate
  the manual settings. Brightness and background grain remain unresolved.
- Which capture modes, preset mechanism, and OBS processing are necessary?
- Is one lighting preset sufficient, and how do settings persist across resets?

## Risks

Camera applications may override settings. Verify actual control readback during
comparisons and test the chosen restoration path with OBS before accepting it.
USB arrangements may limit simultaneous capture; advertised modes alone are not
proof of reliable operation.
