---
id: B003
status: In progress
---

# Working and Talking layouts

## Outcome

Provide distinct OBS layouts for readable screen-based work and face-led
conversation, with shared styling and reusable source configuration.

## Why

Viewers need to read the work while still seeing useful camera views. A separate
Talking layout gives conversation an appropriate composition.

## Boundaries

This is the second agreed layout outcome, but layout discovery and composition
need not wait for B001 camera tuning. Use the known camera aspect ratios for
placement; exposure, colour, and preset restoration remain B001's responsibility.
Choose output dimensions before final layout tuning.

Working allocates the left 75% of the horizontal canvas to screen content and
the right 25% to face and overhead cameras and optional overlays. Optional
content includes keystrokes and Now / Next text. Exact camera sizes, sidebar
ordering, and optional source visibility need testing at the selected output
resolution.

Capture the entire external 2560 × 1440, 16:9 monitor. Tom has a keybinding that
restricts the desktop working area to the left 75% of its width, leaving the
right quarter for stream overlays. The laptop's 1920 × 1080 display is outside
the initial capture scope. Preserve the full monitor source without resizing,
cropping, or cutting it into a smaller capture region. Sidebar overlays may
cover the reserved right quarter. Choose whole-frame output scaling through
discovery rather than treating native 1440p output as a requirement. Tom reports
that the current stream is configured for 1440p and is being used to test
reliability; that configuration is a comparison baseline, not a validated choice.
The reserved area is not a confidentiality boundary.

YouTube is the initial streaming destination. Routine simultaneous local
recording is not required. Tom reports upload capacity around 80 to 100 Mbps,
varying with time of day; this is not a measured sustained minimum. The expected
workload is a terminal with Herdr and subscription-backed AI tools, a web browser,
and a music TUI, rather than local model inference or other heavy workloads.

Talking makes the face camera dominant. Optional overlays support conversation;
it does not need Working's sidebar, screen capture, or overhead arrangement.
Neither scene uses the illustrated room background.

Use Catppuccin Mocha and follow the visual guidance in
`~/src/default/brand-identity/docs/brand/visual-usage.md` and `asset-handoff.md`.
JetBrains Mono Nerd is the preferred candidate for stream text; test its
legibility at the selected output size before settling text sizes. The brand
uses JetBrains Mono with a monospace fallback; Nerd Font icons are optional.
Keep accents restrained and use the supplied wordmark without recreating its
lettering or changing its geometry. Reusable logo design remains in
`brand-identity`; this project owns streaming placement. A plain name treatment
is acceptable where the full wordmark would be too small. For Working, Tom has
chosen a plain website address as the only explicit identifier; a wordmark is
not required, and refinement of the initial website treatment is deferred.

Shared sources or nested scenes are recommended where they avoid duplicating
camera and filter configuration. Include a simple Privacy scene at this stage
that conceals captures and mutes only the microphone without a browser
background or stopping the broadcast. Leave desktop audio and music unchanged;
separate music routing is outside the initial scope. The microphone remains
muted after leaving Privacy until explicitly unmuted. Further presentation
belongs to B004. Local informational overlays and input visualization are
separate outcomes in B004 and B006, not prerequisites for a usable initial layout.

## Acceptance criteria

- Working keeps screen content readable in the left three quarters and contains
  cameras and enabled overlays in the right quarter at the chosen output size.
- Talking visibly prioritizes the face camera and is distinct from Working.
- Neither layout contains the illustrated room background.
- Styling follows Catppuccin Mocha and the existing brand guidance, with readable
  text and sufficient contrast over the intended screen content.
- A simple browser-independent Privacy scene conceals captures and mutes the
  microphone without stopping the broadcast or changing desktop/music audio.
  Leaving Privacy keeps the microphone muted until an explicit unmute.
- Shared camera and filter settings avoid unnecessary duplication, and saved
  scene configuration and verification guidance allow the layouts to be restored.
- Explicit branding suits the selected layout and follows the existing identity.
  Working may use only a plain website address; a final logo or wordmark is not
  a prerequisite for usable scenes.

## Open questions

- Which output resolution, frame rate, and encoding settings suit the actual
  hardware, workload, upload connection, and streaming destination? Begin with
  [S001, output and capture discovery](S001-output-capture-discovery.md).
- Which text sizes, camera sizes, and sidebar ordering work at the chosen output?
- Which optional overlays should be visible by default? Chat is a possible
  future sidebar use, not a new integration requirement.
