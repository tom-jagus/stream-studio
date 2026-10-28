---
id: B004
status: Draft
---

# Local presentation and static room scenes

## Outcome

Serve local backgrounds and informational overlays and complete the six-scene
collection with Starting, Break, Ending, and Privacy behaviour.

## Why

Preparation, breaks, and endings need useful presentation without revealing the
desktop. A separate Privacy action provides immediate concealment and mute.

## Boundaries

This is the third agreed step, after Working and Talking. OBS handles capture,
audio, composition, and encoding. The local service owns presentation state and
Browser Source content; it does not replace OBS.

Starting, Break, and Ending share an anime-style illustrated room with a desk,
computer, window, and city outside. Begin with still artwork and scene-specific
text. Working and Talking may use informational overlays from the service but
must not inherit the room background. Environmental variation and animation
belong to B007.

Starting prepares viewers; Break conceals the desktop and mutes the microphone;
Ending summarizes the session. Privacy is a separate immediate concealment and
mute action, not a command to stop broadcasting. B003 introduces its simple,
browser-independent version; this brief owns any later presentation expansion.
Preserve its microphone-only muting policy, unchanged desktop/music audio, and
microphone mute on exit until an explicit unmute.

Recommended approaches, not selected implementations, include separating room
backgrounds from informational overlays, using layered SVG or transparent
artwork with HTML/CSS text, and sharing presentation state. Possible context
includes a session title, agenda, Now / Next, break message or timer, and ending
summary. Use original or appropriately licensed assets. Keep controls local and
OBS credentials outside browser-delivered content.

## Acceptance criteria

- The collection contains Starting, Working, Talking, Break, Ending, and Privacy,
  with saved configuration and guidance sufficient to restore them.
- Starting, Break, and Ending display the shared static room with appropriate
  scene-specific text. Working and Talking remain free of the room background.
- The local service supplies usable Browser Source content and the agreed
  session information without requiring weather or other external data.
- Entering Break or Privacy hides desktop captures and mutes the microphone.
  Privacy remains usable when the background service is unavailable and does
  not stop broadcasting.
- Browser-visible assets, versioned configuration, and inspected OBS exports do
  not expose OBS credentials or confidential information.
- Shared presentation state and styling avoid unnecessary duplication, and
  artwork has documented permission for its intended use.

## Open questions

- Which language, framework, persistence mechanism, and deployment method fit
  the local service?
- Which artwork and informational fields should the first version include?
- How should session information be edited locally?
- What should happen to microphone mute state when leaving Break?
