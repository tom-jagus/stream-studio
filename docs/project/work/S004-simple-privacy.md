---
id: S004
status: In progress
parent: B003
blocked_by: Immediate entry and composed output tests remain unverified.
---

# Simple independent Privacy scene

## Outcome

Provide immediate concealment and microphone exclusion that work without a
browser background or local presentation service.

## Acceptance criteria

- Entering Privacy replaces captured screen and camera content with a simple
  non-capture presentation and excludes the microphone from the stream mix.
- Privacy works without a local service or Browser Source and does not stop the
  broadcast. A plain static colour is sufficient; elaborate artwork is excluded.
- Privacy excludes the microphone while active. On leaving Privacy, it may
  become audible if not separately muted. Entry and exit are tested from both
  initially muted and unmuted states; repeated entry does not unmute it.
- Testing checks the composed video and stream audio path, not just a hidden
  source or a scene name. Privacy excludes the microphone while desktop audio
  and music retain their existing state. This is not a guarantee of silence.
- A manual way to select Privacy is documented without requiring Vial controls
  or completion of the other scene slices.

## Tasks

- [x] Select the static branded holding card and supply SVG and PNG assets.
- [x] Inspect the saved scene graph and microphone routing, refresh the sanitized
      snapshot, and document manual selection and current limitations.
- [x] Agree on microphone behavior after leaving Privacy. Tom accepts automatic
      return when the shared source was not separately muted.
- [ ] Provide immediate Privacy entry rather than the saved 100 ms Fade, and
      implement the agreed microphone policy.
- [ ] Test composed video and output audio on entry, repeated entry, and exit
      from initially muted and unmuted states, with the browser service absent.

## Review

The current implementation does not meet all existing acceptance criteria.
Tom accepted the holding-card appearance and automatic microphone return, but
has not reported the planned output check. The criteria above reflect the
revised microphone policy; the slice is not yet accepted as complete.

The saved active collection and profile were inspected read-only. The
[sanitized snapshot and manual guidance](../../../obs/README.md) now preserve
Privacy and the shared microphone routing. At the earlier inspection, saved
output settings matched the repository's 1440p30 reference. No live scene,
device, mute state, recording, broadcast, or plugin installation was changed
for this review.

- **Criterion 1, partial.** Local `PRIVACY` contains only the locked, opaque
  2560 × 1440 holding-card image at 1:1 scale, with no screen, camera, browser,
  or microphone dependency. The source is omitted, not muted. The saved
  transition is a 100 ms Fade without a Privacy override, so immediate
  concealment is not established. Actual composed output remains unverified.
- **Criterion 2, structurally satisfied.** Privacy uses a local PNG and native
  OBS Image source, without a Browser Source, local service, or stop-broadcast
  action. Tom selected this static branded card. Operation with the service
  unavailable has not been tested.
- **Criterion 3, structurally supported under the revised policy.** Global
  Mic/Aux is absent. The shared microphone is omitted from Privacy and included
  in live scenes. Tom accepts its automatic return when not separately muted.
  Initially muted/unmuted and repeated entry cases remain untested in output.
- **Criterion 4, unverified.** Desktop Audio remains global and unmuted in the
  saved local collection; no dedicated music capture was added. Structure
  preserves that path, but no recording, listening test, or composed-output
  test was performed or reported. The export mutes desktop and microphone
  sources for safe restoration, not as evidence of live Privacy muting.
- **Criterion 5, documented.** The OBS guide describes manual scene selection,
  Studio Mode's Program transition requirement, and audio limitations without
  Vial. Manual operation has not been observed in a test.

Before acceptance, resolve immediate entry and check actual output video and
audio across entry, repeated entry, and exit from initially muted and unmuted
states. Desktop audio/music must retain its intended state, and Privacy must
remain usable without the browser service.
Restoration import remains untested and belongs to S005.

## Boundaries

This slice can be prepared independently of output discovery and camera tuning.
It does not define a Vial binding or broader automatic broadcasting workflow.
Presentation expansion and Break behaviour remain in B004. Separate music
routing and broader audio muting are outside this initial slice. Do not change
OBS or record microphone or screen content without the applicable approval.
