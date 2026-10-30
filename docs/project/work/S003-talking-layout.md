---
id: S003
status: Done
parent: B003
depends_on:
  - S002
---

# Talking and desk-camera layouts

## Outcome

Provide a face-led Talking scene and two desk-led demonstration variants using
Working's shared camera configuration. Keep them distinct from Working's
screen-and-sidebar composition.

## Acceptance criteria

- Face only makes the face camera dominant at the selected 2560 × 1440 output
  and 30 fps, with framing accepted by Tom and no aspect-ratio distortion.
  Further S001 discovery is not a prerequisite for this initial delivery.
- Desk + face shows the full-canvas overhead view with a small face inset at the
  same position and size as Working. Desk only uses the same overhead framing
  without the face inset or its border.
- All three scenes are visibly different from Working and contain no illustrated
  room or screen capture.
- Optional elements have agreed visibility and support the intended subject.
  The fullscreen face border is hidden; the small face inset has a border.
  Initial scenes work without chat, a local overlay service, or input
  visualization.
- Camera sources and filters reuse S002's shared configuration so that switching
  between Working and Talking does not require retuning the device.
- Existing Mocha styling is reused where decoration is present. These three
  scenes intentionally contain no branding or text overlays; no wordmark,
  website, plain-name treatment, or typography test is required for this version.
- Switching between Working and Talking preserves their intended composition
  and does not introduce duplicate camera capture or unresolved sources.

## Tasks

- [x] Establish Face only, Desk + face, and Desk only with the accepted framing
      and no additional composition crops. Keep the fullscreen face border hidden.
- [x] Reuse the existing camera scenes without duplicate device capture. Match
      the small face inset to Working at x = 1934, y = 15, size 611 × 344.
- [x] Reuse the shared Mocha border around the face inset. Omit branding, text,
      chat, and service dependencies from this initial scene family.
- [x] Check source references and shared composition. Tom reports successful
      Working/Talking switching during the live stream and accepts the result.
- [x] Save all three scenes alongside Working in the sanitized repository
      snapshot, preserving shared sources and removing private local values.

## Review

S003 is Done by Tom's explicit acceptance of the initial three-scene delivery.
Its scope includes the desk-led companions and deliberately omits branding.
The selected output is 1440p30; S001 is not a completion dependency for this
layout, and S001 itself remains unchanged.

Read-only configuration inspection verified fullscreen face and desk views,
matching desk framing between desk variants, and the face inset matching
Working at 611 × 344. The fullscreen border is hidden. The scenes reuse the
same two 2560 × 1440, 30 fps camera inputs as Working, with no duplicate capture,
missing references, scene cycles, screen capture, illustrated room, text, or
browser dependency in the three camera-led compositions.

Tom reports correct switching during the live stream and accepts the current
framing and composition. His proposed recording rewatch has not been reported
as completed. Acceptance is based on his live observation and the structural
checks, not a claim of recording verification, measured performance headroom,
or new camera-quality testing.

The [sanitized scene snapshot](../../../obs/README.md) includes all three TALK
scenes and four Working variants. Scene-item transforms and source references
were checked against the saved local collection. No live OBS changes or import
were made during export; restoration remains untested and belongs to S005.

A future face-plus-chat variant may place chat on the left with Tom framed to
its right. It is deferred, not an outstanding requirement of this delivery.

## Boundaries

This slice does not tune camera exposure, colour, or presets. Camera quality
remains B001's responsibility. Testing requires camera-access approval; no live
broadcast is needed to review the composition.
