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

### Establish the current baseline without changing the live stream

- [x] Inspect hardware and saved OBS settings through allowlisted read-only
      extraction. Initial findings identify a Ryzen 7 4700U, integrated AMD
      graphics, about 7.1 GiB usable RAM, and OBS 32.2.2 using x264 veryfast at
      2560 × 1440 and 30 fps. Hardware encoding remains unverified.
- [x] Inspect saved capture geometry and display reservations. The screen source
      is uncropped with 2560 × 1440 bounds. The external monitor's 400 logical
      pixels of right reservation at scale 1.6 correspond to 640 physical pixels.
- [ ] Reconcile the saved 13,500 Kbps bitrate with the current session's encoder
      start log showing 6,000 Kbps. Check actual outgoing bitrate and YouTube's
      received-stream information rather than treating either saved value as
      proof of the current live rate. Verify the applicable codec-specific row
      in YouTube's official encoder guidance and any dashboard advice.
- [ ] Before closing OBS after the stream, collect duration and separate counters
      for network-dropped frames, rendering lag, and encoding lag. Confirm which
      sources were active and whether screen capture, both cameras, microphone,
      and desktop audio ran together for the observed interval.
- [ ] Repeat a short CPU, available-memory, swap-activity, and temperature sample
      during representative normal work. Compare with the initial snapshot of
      limited RAM headroom and active swapping. Do not infer sustained capacity
      or attribute all system load to OBS from a single sample.
- [ ] Identify which camera uses the saved 1080p60 mode and which uses 4K30.
      Inspect existing metadata first, without opening another camera client.
      Check available OBS hardware encoders read-only; distinguish advertised
      support from a verified working encoder path.

### Establish a viewer-facing readability reference

- [ ] Review Tom-selected segments of the current YouTube archive once processing
      is complete. Use terminal/Herdr text, browser content, and scrolling. Note
      playback resolution, player size, and any visible stutter or camera issue.
      Check a normal desktop player and fullscreen first, then assess mobile
      separately with Tom rather than assuming equal readability is achievable.
- [ ] Confirm a representative text sample and acceptable reading size with Tom.
      Check JetBrains Mono Nerd, punctuation, muted text, and Mocha contrast in
      actual playback. Treat brand-guide sizes as starting points only. Larger
      terminal fonts and browser zoom are acceptable candidates, not approved
      desktop or keybinding changes.

### Run only the comparisons that need further evidence

- [ ] Agree on test timing, permitted changes, safe screen content, and a way to
      restore the original settings before making changes. Propose comparable
      10-minute candidate segments with the full intended source load and normal
      work. Use YouTube archives, not local recordings. Test broadcasts, camera
      access, and configuration changes still require explicit approval.
- [ ] First test whether lower camera capture cost preserves useful framing at
      1440p30 output. Consider 1080p30 for sidebar cameras while retaining enough
      detail for Talking or agreed crops. Change one camera mode at a time and
      compare lag, system load, motion, and detail without tuning image controls.
- [ ] If CPU encoding remains a constraint and a suitable hardware encoder is
      available, compare one hardware-encoded 1440p30 candidate with x264 under
      separately approved settings. Compare text quality as well as load; do not
      assume hardware encoding is automatically preferable.
- [ ] Compare 1440p30 with 1080p30 using the same workload, camera modes, and
      encoder where practical. Keep the 2560 × 1440 canvas and complete monitor
      source; scale only the whole-frame output. The work/sidebar regions become
      1440/480 pixels wide at 1080p, versus 1920/640 at 1440p. Test existing text
      sizes first, then an agreed larger-font or browser-zoom variant if needed.
      Record bitrate differences and other unavoidable comparison differences.
- [ ] Check network delivery during authorized streams at intended streaming
      times. Keep reported upload capacity distinct from measured capacity. Only
      propose a separate throughput test if delivery remains uncertain, with
      explicit approval and never alongside an active broadcast.

### Recommend and hand off

- [ ] Confirm the preferred candidate over a proposed 30-minute normal-work
      interval with the full source load, using a user-authorized stream. Record
      settings, duration, OBS counters, system headroom, YouTube health, and
      archive readability. Do not claim this proves all-session reliability.
- [ ] Recommend a baseline and fallback for Tom's decision. Keep 1440p30 as the
      provisional baseline and 1080p30 as an untested fallback until comparisons
      justify a choice. Identify measured results, estimates, untested options,
      camera-mode trade-offs, remaining upload uncertainty, and any proposed
      font adjustment. Keybinding implementation and final scene styling remain
      outside this discovery plan.

## Open questions

- Does 1440p30 retain sufficient processing and memory headroom with the full
  source load and normal work? Can camera-mode changes improve that headroom
  without reducing useful camera detail?
- What bitrate is actually reaching YouTube, and how does it compare with the
  applicable current encoder guidance?
- What terminal text size is acceptable at normal desktop playback size, and
  what mobile readability can reasonably be supported?
- Does 1080p30 with larger text provide a useful fallback, or lose too much
  working space and detail?
- What sustained upload capacity is available at intended streaming times?
- Which configuration changes and broadcast tests will Tom authorize after the
  current stream?

## Boundaries

The initial destination is YouTube, without routine simultaneous local
recording. Tom reports roughly 80 to 100 Mbps upload capacity with time-of-day
variation; this is not a measured minimum. Expected work includes a terminal
with Herdr and subscription-backed AI tools, a browser, and a music TUI. There
is no stated local inference workload. The intended source load is screen
capture, two webcams, microphone audio, and desktop audio. Tom prefers YouTube
archive playback for discovery; no local recording is planned. Keep 30 fps for
this machine. Revisit higher frame rates with a future laptop, not in this
comparison.

Tom reports that the current stream is set to 1440p and is running in part to
assess reliability. Treat it as an existing baseline to inspect, not evidence
that 1440p is suitable or permission to change settings during a live stream.
Do not interrupt the active stream for tests without explicit approval.

Tom has authorized read-only inspection. Extract only relevant technical fields;
do not print credentials, complete configuration, private content, or raw logs.
This does not grant permission to edit OBS, Hyprland, devices, or source files,
open camera streams, or initiate desktop capture. Camera tuning and preset
acceptance remain in B001 and do not block this slice. Use known camera aspect
ratios for composition, but identify any untested simultaneous-camera load. Do
not start broadcasting or run network throughput tests without approval. A
reserved desktop area does not prevent disclosure of notifications, floating
windows, or other content in the captured monitor.
