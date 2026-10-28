---
id: S002
status: To do
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

- [ ] Confirm camera sizes, sidebar ordering, optional element visibility, and
      permitted camera framing from an actual-size composition preview.
- [ ] Reuse suitable capture sources and establish shared camera/filter setup.
- [ ] Apply the agreed full-monitor composition and Mocha styling, integrating
      suitable approved brand assets or the permitted plain-name fallback.
- [ ] Check representative terminal/browser work and both camera views at output
      size, including the effect of enabled sidebar elements.
- [ ] Identify any performance or capture limitations against S001's baseline.

## Open questions

- What camera sizes and sidebar ordering best use the reserved quarter?
- Which optional elements, if any, should the initial scene show?
- Which capture source and source-sharing approach suit the actual OBS setup?

## Boundaries

Do not change Hyprland's working-area keybinding or tune device exposure,
colour, or presets. Desktop capture and camera access require approval before
testing. The reserved quarter and scene overlays do not guarantee that private
windows, notifications, or other screen content cannot be disclosed.
