---
id: S001
status: To do
parent: B003
---

# Output and capture discovery

## Outcome

Recommend a practical OBS canvas, output resolution, frame rate, and encoding
baseline for Tom's limited setup, with a full-monitor capture composition that
preserves readable work and the reserved overlay area.

## Acceptance criteria

- The recommendation identifies the relevant CPU/GPU and encoder capabilities,
  OBS environment, external display mode, representative workload, streaming
  destination limits, and available upload capacity. Unknowns are explicit.
- The proposed composition accounts for a 2560 × 1440 external monitor with its
  desktop working area restricted to the left 75%. Preserve the complete monitor
  source without resizing or cropping it into a smaller region. Sidebar overlays
  may cover the reserved right quarter. Whole-frame output scaling is a discovery
  choice, not a restriction to native 1440p. Explain the resulting readability
  before delivery slices rely on the recommendation.
- A bounded comparison of plausible output and frame-rate choices explains the
  trade-offs in text readability, motion, encoding load, and bandwidth. It
  distinguishes measured evidence from estimates and untested options.
- Where separately authorized, a representative local OBS recording compares
  candidates with normal work and the intended camera load. Results include
  rendering/encoding lag and recording readability. If capture or configuration
  changes are not authorized, the recommendation states the validation gap.
- The result recommends a baseline and fallback, with the remaining checks
  needed before live use. A local recording alone is not claimed to prove
  network or streaming-platform performance.
- Styling recommendations use Catppuccin Mocha and the existing brand guidance,
  assess JetBrains Mono Nerd at candidate output sizes, and do not redesign the
  identity. No live chat, overlay service, or input visualization is required.

## Tasks

- [ ] Verify YouTube's relevant output requirements and distinguish reported
      upload capacity from measured capacity.
- [ ] Inspect relevant hardware, OBS capabilities, and display/capture setup
      read-only; avoid collecting unrelated private configuration or credentials.
- [ ] Check that candidate compositions preserve the full monitor source with
      overlays over the reserved right quarter.
- [ ] Select a small candidate set using actual capabilities and constraints.
- [ ] Agree on a bounded capture and recording test before accessing cameras,
      recording desktop content, or changing OBS or device settings.
- [ ] Compare authorized candidates and report evidence, limitations, and the
      recommended baseline and fallback for Tom's decision.

## Open questions

- Does the current 1440p stream reliably support the intended workload, and would
  another output size or frame rate offer a better readability/reliability balance?
- What sustained upload capacity is available at intended streaming times?
- Which inspection and test actions will be authorized when discovery begins?

## Boundaries

The initial destination is YouTube, without routine simultaneous local
recording. Tom reports roughly 80 to 100 Mbps upload capacity with time-of-day
variation; this is not a measured minimum. Expected work includes a terminal
with Herdr and subscription-backed AI tools, a browser, and a music TUI. There
is no stated local inference workload. Temporary discovery recordings, if
authorized, are distinct from recording normal streams.

Tom reports that the current stream is set to 1440p and is running in part to
assess reliability. Treat it as an existing baseline to inspect, not evidence
that 1440p is suitable or permission to change settings during a live stream.
Do not interrupt the active stream for tests without explicit approval.

This slice is discovery, not permission to edit OBS, Hyprland, devices, or source
files. Camera tuning and preset acceptance remain in B001 and do not block this
slice. Use known camera aspect ratios for composition, but identify any untested
simultaneous-camera load. Do not start broadcasting or run network throughput
tests without approval. A reserved desktop area does not prevent disclosure of
notifications, floating windows, or other content in the captured monitor.
