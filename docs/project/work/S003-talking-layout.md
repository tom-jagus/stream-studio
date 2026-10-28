---
id: S003
status: To do
parent: B003
depends_on:
  - S001
  - S002
---

# Face-led Talking layout

## Outcome

Provide a Talking scene that prioritizes conversation and reuses Working's
camera configuration without reproducing its screen-and-sidebar composition.

## Acceptance criteria

- The face camera is the dominant visual element at the output size selected
  through S001, with framing accepted by Tom and no aspect-ratio distortion.
- The scene is visibly different from Working and contains no illustrated room.
  Screen capture and the overhead camera are not required.
- Any optional elements have agreed visibility, support conversation, and do not
  compete with the face view. An initial scene works without the local overlay
  service or input visualization.
- Camera sources and filters reuse S002's shared configuration so that switching
  between Working and Talking does not require retuning the device.
- Mocha colours, typography, and any branding follow the existing guidance and
  remain legible at actual output size. Use a plain name rather than an illegible
  or altered wordmark where appropriate.
- Switching between Working and Talking preserves their intended composition
  and does not introduce duplicate camera capture or unresolved sources.

## Tasks

- [ ] Agree on the face framing and any optional elements using an output-size
      preview; confirm any proposed camera crop before applying it.
- [ ] Reuse the shared camera/filter setup and apply the Talking composition.
- [ ] Apply consistent brand styling and check output-size legibility.
- [ ] Test Working/Talking switching and identify source-sharing limitations.

## Open questions

- How large should the face view be, and which framing is acceptable?
- Which optional elements, if any, should Talking show initially?

## Boundaries

This slice does not tune camera exposure, colour, or presets. Camera quality
remains B001's responsibility. Testing requires camera-access approval; no live
broadcast is needed to review the composition.
