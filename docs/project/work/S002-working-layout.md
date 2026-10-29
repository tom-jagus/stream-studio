---
id: S002
status: In progress
parent: B003
depends_on:
  - S001
---

# Readable Working layout

## Outcome

Provide a Working scene that preserves the external monitor capture and makes
terminal and browser work readable alongside face and overhead camera views.

## Acceptance criteria

- The scene uses S001's accepted canvas and output recommendation. It captures
  the entire external 2560 × 1440 monitor without cropping or resizing the source
  into a smaller region. Overlay coverage and any whole-frame output scaling
  follow Tom's confirmed choices from S001.
- The desktop working area occupies the left 75% of the canvas, with face and
  overhead cameras and enabled overlays contained in the right quarter.
- Representative terminal and browser content is readable at the chosen output
  size. Camera placement and framing preserve intended subjects without
  stretching their aspect ratios. Any proposed camera crop is agreed first.
- Styling uses Catppuccin Mocha and the existing brand guidance. Text sizes and
  contrast are checked in the actual output, not only the OBS editing view.
- Suitable available approved branding is integrated into Working using supplied
  assets and their usage rules. Check placement and legibility at actual output
  size; use a plain name treatment where the full wordmark would be too small.
  A redesigned or unfinished logo is not a prerequisite.
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
- [ ] Confirm camera framing and representative terminal/browser readability in
      actual output with the new sidebar, including the topic text and camera-off
      states. Check contrast and clipping rather than relying on configuration.
- [ ] Reconcile the branding criterion with Tom's chosen no-wordmark layout.
      No separate supplied asset or plain-name treatment was verified; do not
      add one or silently change the criterion during this review.
- [ ] Identify performance or capture limitations of the new composition against
      S001's baseline and resolve the still-open baseline acceptance dependency.

## Open questions

- Does actual output confirm readable work, useful camera framing, and readable
  sidebar text with no clipping in all four variants?
- How should the branding criterion reflect the chosen no-wordmark layout?
- Does the new composition introduce rendering, encoding, or capture issues
  compared with the initial 1440p30 setup?

## Review

Partial delivery is verified. S002 remains In progress, not Done. This review
records completed implementation steps without claiming final user acceptance.

Verified through saved configuration inspection and live OBS transform
readback: the 2560 × 1440 monitor composition is uncropped; camera rectangles
remain within the right quarter; four variants reuse shared source scenes;
placeholder and border layering supports scene switching; and all 12 adjusted
camera/border rectangles are 611 × 344. Their positions are x = 1934 with
face y = 15 and overhead y = 377. A later saved-file check confirmed persistence.
The Working source graph has no illustrated room or browser-service dependency.
Text sources use the JetBrains Mono family. The initial topic is manually
editable; keystrokes and chat integrations remain deferred.

Known limitations remain. Placeholder interiors use opaque Base rather than
Mantle, and Surface0 placeholder text has approximately 1.3:1 contrast against
Base. Tom chose to retain the current styling and fix only rectangle alignment;
sufficient placeholder-text contrast is therefore not established. The existing
branding criterion also needs reconciliation with the no-wordmark preference.
Neither point was silently removed from acceptance criteria.

Actual-output checks of the new composition, camera subject framing, and
post-overlay performance remain unverified. Tom reported readable playback of
the previous stream, which supports the provisional 1440p30 baseline but does
not validate today's new layout. Earlier logs showed 0.7% rendering lag and
6 encoding-skipped frames before this overlay review; they are not measurements
of the finished composition. S001 remains open, so its dependency is not treated
as completed. No screenshots, private text, credentials, or raw OBS exports were
added to the repository.

## Boundaries

Do not change Hyprland's working-area keybinding or tune device exposure,
colour, or presets. Desktop capture and camera access require approval before
testing. The reserved quarter and scene overlays do not guarantee that private
windows, notifications, or other screen content cannot be disclosed.
