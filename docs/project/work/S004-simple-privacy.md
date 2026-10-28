---
id: S004
status: To do
parent: B003
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

- [ ] Identify the actual stream microphone path and how to preserve its muted
      state on exit until an explicit unmute.
- [ ] Select a minimal static presentation and an OBS-compatible way to enforce
      microphone mute on entering Privacy.
- [ ] Implement and test entry, repeated entry, and exit with authorized sources
      and audio checks, including initially muted and unmuted cases.
- [ ] Check behaviour with the browser service unavailable and document manual use
      and the remaining audio/privacy limitations.

## Open questions

- Which mechanism can enforce the required microphone behaviour in this OBS setup?

## Boundaries

This slice can be prepared independently of output discovery and camera tuning.
It does not define a Vial binding or broader automatic broadcasting workflow.
Presentation expansion and Break behaviour remain in B004. Separate music
routing and broader audio muting are outside this initial slice. Do not change
OBS or record microphone or screen content without the applicable approval.
