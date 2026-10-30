---
id: S004
status: In progress
parent: B003
blocked_by: Current scene routing conflicts with explicit unmute on exit; output tests remain unverified.
---

# Simple independent Privacy scene

## Outcome

Provide an immediate concealment and microphone-mute option that works without
a browser background or local presentation service.

## Acceptance criteria

- Entering Privacy replaces captured screen and camera content with a simple
  non-capture presentation and mutes the stream microphone.
- Privacy works without a local service or Browser Source and does not stop the
  broadcast. A plain static colour is sufficient; elaborate artwork is excluded.
- The microphone stays muted while Privacy is active and after leaving it.
  Unmuting requires an explicit action. Entry and exit are tested from both
  initially muted and unmuted states; repeated entry does not unmute it.
- Testing checks the composed video and stream audio path, not just a hidden
  source or a scene name. Privacy changes only microphone mute; desktop audio
  and music retain their existing state. Microphone mute is not presented as a
  guarantee of complete silence.
- A manual way to select Privacy is documented without requiring Vial controls
  or completion of the other scene slices.

## Tasks

- [x] Select the static branded holding card and supply SVG and PNG assets.
- [x] Inspect the saved scene graph and microphone routing, refresh the sanitized
      snapshot, and document manual selection and current limitations.
- [ ] Resolve the conflict between scene-specific microphone inclusion and the
      required muted state after leaving Privacy. Do not change the criteria
      without Tom's agreement.
- [ ] Provide immediate Privacy entry rather than the saved 100 ms Fade, and
      implement the agreed microphone policy.
- [ ] Test composed video and output audio on entry, repeated entry, and exit
      from initially muted and unmuted states, with the browser service absent.

## Open questions

- Should the original explicit-unmute-on-exit requirement remain, or should Tom
  approve automatic microphone return when switching to Working/Talking?
- If explicit unmute remains required, which mechanism will enforce it without
  depending on a browser service? Scripts and plugin installation are deferred.

## Review

The current implementation does not meet all existing acceptance criteria.
Tom accepted the holding-card appearance and configured scene-specific audio,
but has not reported the planned recording check. This review records interim
findings at his request, not acceptance or a change to the criteria.

The saved active collection and profile were inspected read-only. The
[sanitized snapshot and manual guidance](../../../obs/README.md) now preserve
Privacy and the shared microphone routing. Output settings remain 1440p30 and
match the repository reference. No live scene, device, mute state, recording,
broadcast, or plugin installation was changed for this review.

- **Criterion 1, partial.** Local `PRIVACY` contains only the locked, opaque
  2560 × 1440 holding-card image at 1:1 scale, with no screen, camera, browser,
  or microphone dependency. The source is omitted, not muted. The saved
  transition is a 100 ms Fade without a Privacy override, so immediate
  concealment is not established. Actual composed output remains unverified.
- **Criterion 2, structurally satisfied.** Privacy uses a local PNG and native
  OBS Image source, without a Browser Source, local service, or stop-broadcast
  action. Tom selected this static branded card. Operation with the service
  unavailable has not been tested.
- **Criterion 3, unmet.** Global Mic/Aux is absent. One unmuted PulseAudio
  microphone source is reused once in each of the four Working and three
  Talking scenes, and is absent from Privacy. No mute automation is configured.
  Returning to a live scene includes the microphone again without explicit
  unmute if it was unmuted before entry. Initially muted/unmuted and repeated
  entry cases have not been tested in output audio.
- **Criterion 4, unverified.** Desktop Audio remains global and unmuted in the
  saved local collection; no dedicated music capture was added. Structure
  preserves that path, but no recording, listening test, or composed-output
  test was performed or reported. The export mutes desktop and microphone
  sources for safe restoration, not as evidence of live Privacy muting.
- **Criterion 5, documented.** The OBS guide describes manual scene selection,
  Studio Mode's Program transition requirement, and audio limitations without
  Vial. Manual operation has not been observed in a test.

Before acceptance, resolve the microphone-return policy and immediate entry,
then check actual output video and audio across entry, repeated entry, and
exit from initially muted and unmuted states. Desktop audio/music must retain
its intended state, and Privacy must remain usable without the browser service.
Restoration import remains untested and belongs to S005.

## Boundaries

This slice can be prepared independently of output discovery and camera tuning.
It does not define a Vial binding or broader automatic broadcasting workflow.
Presentation expansion and Break behaviour remain in B004. Separate music
routing and broader audio muting are outside this initial slice. Do not change
OBS or record microphone or screen content without the applicable approval.
