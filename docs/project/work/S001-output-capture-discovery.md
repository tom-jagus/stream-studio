---
id: S001
status: To do
parent: B003
---

# Output and capture discovery

## Outcome

Recommend an OBS canvas, output resolution, frame rate, and encoding baseline
for Tom's laptop. Preserve the full external monitor capture and assess
readability with the reserved overlay area.

## Acceptance criteria

- The recommendation identifies the relevant CPU/GPU and encoder capabilities,
  OBS environment, external display mode, representative workload, streaming
  destination limits, and available upload capacity. Unknowns are explicit.
- The proposed composition accounts for a 2560 × 1440 external monitor with its
  desktop working area restricted to the left 75%. Preserve the complete monitor
  source without resizing or cropping it into a smaller region. Sidebar overlays
  may cover the right quarter. Whole-frame output scaling is a discovery
  choice, not a restriction to native 1440p. Explain the resulting readability
  before delivery slices rely on the recommendation.
- A bounded comparison of plausible output and frame-rate choices explains the
  trade-offs in text readability, motion, encoding load, and bandwidth. It
  distinguishes measured evidence from estimates and untested options.
- The original criterion calls for a separately authorized local OBS recording
  to compare candidates under normal work and the intended camera load. The
  current plan instead uses YouTube archives; resolve this conflict before
  assessing the criterion. Compare rendering/encoding lag and readability, and
  state validation gaps if the necessary tests are not authorized.
- The result recommends a baseline and fallback, with the remaining checks
  needed before live use. A local recording alone is not claimed to prove
  network or streaming-platform performance.
- Styling recommendations use Catppuccin Mocha and the existing brand guidance,
  assess JetBrains Mono Nerd at candidate output sizes, and do not redesign the
  identity. No live chat, overlay service, or input visualization is required.

## Tasks

- [x] Inspect hardware, saved OBS settings, capture geometry, and display
      reservation using read-only extraction. The initial observation found a
      Ryzen 7 4700U, integrated AMD graphics, about 7.1 GiB usable RAM, a full
      2560 x 1440 source, and a 640-physical-pixel right reservation.
- [ ] Re-establish the current settings and full source load. Reconcile actual
      outgoing bitrate with saved values and applicable YouTube guidance; record
      separate rendering, encoding, and network loss counters.
- [ ] Assess representative terminal and browser readability, including
      punctuation and muted text, at agreed desktop and mobile viewing sizes.
- [ ] Agree on safe test timing, content, permitted changes, and restoration.
      Compare camera modes and 1440p30 versus 1080p30 under representative load;
      consider hardware encoding only if available and separately authorized.
- [ ] Measure resource headroom and delivery during authorized comparisons.
      Recommend a baseline and fallback, with evidence and remaining gaps.

## Open questions

- Should the local-recording criterion be revised to use YouTube archives, or
  should both methods be retained?
- Which settings maintain readability and sufficient CPU, GPU, and memory
  headroom with the full workload? Which camera modes retain useful detail?
- What bitrate reaches YouTube, and what sustained upload capacity is available
  at intended streaming times?
- Which tests and configuration changes will Tom authorize?

## Boundaries and evidence

An earlier discovery session used 1440p30 as a provisional comparison baseline.
The later [performance guide](../../streaming-performance.md) records a separate
1080p30 x264 baseline and its limits; neither is an accepted result of this
slice. Past saved bitrate and encoder-start values differed, so neither alone
establishes the outgoing rate. Readability, full-load headroom, and fallback
remain to be assessed. Working and Talking were accepted independently of this
slice; see [Slice 2](S002-working-layout.md) and
[Slice 3](S003-talking-layout.md).

The initial destination is YouTube. Routine simultaneous local recording is not
required. Tom reports roughly 80 to 100 Mbps upload capacity with time-of-day
variation, not a measured minimum. The intended workload includes a terminal,
Herdr, subscription-backed AI tools, a browser, and a music TUI, without stated
local inference. The intended sources are the external monitor, two webcams,
microphone, and desktop audio. Keep comparisons at 30 fps on this machine;
revisit higher rates with a future laptop.

Read-only inspection was authorized for the earlier session. Changes, camera
access, recordings, broadcast tests, and network throughput tests require
applicable approval. Do not interrupt an active stream. Camera tuning and
presets belong to [Brief 1](B001-repeatable-cameras.md). A reserved desktop area
is not a confidentiality boundary.
