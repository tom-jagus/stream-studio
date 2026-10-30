---
id: S002
status: Done
parent: B003
---

# Readable Working layout

## Outcome

Provide a Working scene that preserves the external monitor capture and makes
terminal and browser work readable alongside face and overhead camera views.

## Acceptance criteria

- The scene uses the selected 2560 × 1440 canvas and output at 30 fps. It captures
  the entire external 2560 × 1440 monitor without cropping or resizing the source
  into a smaller region. Overlays may cover the reserved right quarter. Further
  S001 discovery is not a prerequisite for accepting this Working layout.
- The desktop working area occupies the left 75% of the canvas, with face and
  overhead cameras and enabled overlays contained in the right quarter.
- Representative terminal and browser content is readable at the chosen output
  size. Camera placement and framing preserve intended subjects without
  stretching their aspect ratios. Any proposed camera crop is agreed first.
- Styling uses Catppuccin Mocha and the existing brand guidance. Text sizes and
  contrast are checked in the actual output, not only the OBS editing view.
- A plain website address is sufficient explicit branding for Working. Use
  the shared typography and check its placement and legibility at actual output
  size. A wordmark, logo, or social-handle list is not required. Tom may accept
  the initial website treatment with visual refinement deferred.
- The scene contains no illustrated room. Live chat integration, input
  visualization, and a local overlay service are not prerequisites for the
  initial usable scene. Optional elements have an agreed default visibility and
  do not leave broken-source placeholders.
- Camera sources and filters can be shared with Talking without duplicating
  device tuning. Image-quality tuning remains in B001.

## Tasks

- [x] Establish the initial composition with face camera above overhead camera,
      manually edited topic below, and space reserved for later keystrokes and
      chat. Keep both cameras on by default; provide scene-switching variants
      for face only, overhead only, and neither camera.
- [x] Reuse the existing screen and camera source scenes, shared sidebar, and
      shared border scene without duplicating device-capture sources.
- [x] Apply the full-monitor composition and initial Mocha styling. The sidebar
      occupies the right 640 pixels with a Mantle background at 95% opacity.
      Camera-off variants reveal opaque placeholders beneath the camera slots.
- [x] Align all camera and border instances to the placeholder rectangles at
      611 × 344. Verify all 12 transforms across the four Working variants and
      confirm that OBS persisted the adjustments.
- [x] Confirm camera framing and terminal readability through Tom's review of
      the recording. Tom accepts both for the current composition.
- [x] Use a shared website text source as the only explicit identifier. Verify
      that it is visible in all four Working variants. Tom accepts its current
      treatment and defers visual refinement; no wordmark is required.
- [x] Assess observed performance of the new composition through Tom's review
      of the recording. Tom reports no issues and accepts current performance;
      this does not establish measured processing headroom or zero dropped frames.
- [x] Remove the S001 dependency at Tom's request. Keep the selected 1440p30
      Working setup without claiming that S001 itself is complete.
- [x] Complete final visual acceptance with Tom. He confirms readable website
      and camera-off text, no clipping, and accepts the overall output for the
      initial delivery. This is user acceptance, not a controlled legibility test.

## Review

S002 is Done by Tom's acceptance of the initial delivery. He accepts camera
framing, terminal readability, observed playback performance, and the current
website treatment. His final output check confirms readable website and
camera-off text, no clipping, and an acceptable overall result for this first
version. Website refinements are deferred, not delivery blockers. S001 is no
longer a dependency at Tom's request; its own status is unchanged.

- Full-monitor capture and output configuration are verified at 2560 × 1440,
  30 fps, without cropping the monitor into a smaller capture region.
- The sidebar begins at x = 1920 and occupies the right 640 pixels. All four
  variants share it. Twelve camera/border instances are aligned at 611 × 344,
  with x = 1934, face y = 15, and overhead y = 377. Live OBS readback and a saved
  configuration check verified the adjustments. Tom accepts the camera framing.
- Terminal readability and the initial overall output are accepted from Tom's
  visual review. Website and camera-off text are confirmed readable, with no
  clipping reported. This is qualitative user acceptance; no separate controlled
  browser, topic, or every-variant legibility test is claimed.
- Styling uses Mocha colours and JetBrains Mono. The panel is Mantle at 95%
  opacity. Placeholder interiors remain opaque Base with Surface0 text, about
  1.3:1 contrast. Tom chose to retain that styling and accepts the camera-off
  text after checking output. This does not claim a contrast-threshold pass.
- One shared website text source is visible in all four Working variants and
  uses JetBrains Mono. Its contents were omitted from inspection output. Tom
  accepts its current presentation; a wordmark is not required.
- The Working source graph has no illustrated room, browser source, or overlay
  service dependency. Keystrokes and chat remain deferred, with space reserved.
- Camera and screen sources are shared rather than independently duplicated.
  The four variants show both cameras, face only, overhead only, or neither.

The accepted [Working snapshot](../../../obs/README.md) preserves the scene
configuration and relevant output settings with private values replaced. Its
structural and privacy checks passed; restoration import remains untested and
does not complete S005.

Tom's playback review found no performance issue in the current composition.
No new instrumented performance measurement was made, so zero dropped frames or
spare processing capacity is not claimed. No screenshots, private text,
credentials, or raw OBS exports were added to the repository.

## Boundaries

Do not change Hyprland's working-area keybinding or tune device exposure,
colour, or presets. Desktop capture and camera access require approval before
testing. The reserved quarter and scene overlays do not guarantee that private
windows, notifications, or other screen content cannot be disclosed.
