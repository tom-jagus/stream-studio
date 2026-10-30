# OBS live-layout snapshot

This directory preserves the Working, camera-led, and Privacy scene graph and
its output settings. It is a sanitized restoration starting point, not a full
machine backup or a verified one-click restore. No live OBS settings were
changed to create it.

## Files and scope

- `working-scenes.json` contains four Working variants, three camera-led
  scenes, and `Privacy`. The camera-led scenes are `Talking - Face Only`,
  `Talking - Desk and Face`, and `Talking - Desk Only`. It preserves their shared
  sources, transforms, colours, text styling, filters, and source relationships.
  One microphone source is shared across the seven Working/Talking scenes.
  The filename is retained from the original Working-only snapshot.
- `assets/privacy.svg` is the self-contained 2560 × 1440 branded holding card.
  `assets/privacy.png` is its opaque raster export, used by the Privacy image
  source. Both contain the wordmark, "Taking a moment off-screen", and
  `tom.jagus.me`. The image has no font or browser dependency.
- `output-settings.ini` records an allowlisted subset of the active profile's
  video, streaming encoder, bitrate, and audio-format settings. It is a reference
  for manual setup, not a complete importable profile.

The snapshot uses a 2560 × 1440 canvas and output at 30 fps, software x264 with
its veryfast preset, 13,500 Kbps video, and 160 Kbps audio. Audio format is 48 kHz
stereo. These are saved settings, not proof of network capacity or performance.

Only Working, the three camera-led scenes, Privacy, and their dependencies are
included. Other scenes, browser sources, scripts, timers, projectors, and
existing hotkeys are excluded. Working and Talking use native colour and text
sources; Privacy uses the supplied PNG. The snapshot also reflects the saved
Working website's regular font and updated horizontal position.

Face only fills the canvas and retains a hidden fullscreen border. Desk + face
uses the full-canvas desk view with the face inset at x = 1934, y = 15, size
611 × 344, matching Working. Desk only has the same desk framing without the
inset. These camera-led scenes contain no branding or text. The saved transition
is a 100 ms Fade, with no saved Privacy-specific override. This is not an
immediate Privacy transition.

## Privacy and local substitutions

Local source names and identifiers are replaced with consistent export names.
The shared scene relationships and scene-item geometry are preserved.

- Camera device identifiers are replaced with `SELECT_FACE_CAMERA` and
  `SELECT_OVERHEAD_CAMERA`.
- The PipeWire portal restore token is removed. Screen capture needs a fresh
  monitor selection and permission grant.
- Desktop and microphone audio device identifiers are replaced with
  `SELECT_LOCAL_AUDIO_DEVICE`. Both audio sources are muted in the export so
  restoration requires deliberate device selection and unmuting. The microphone
  is a scene source, not global Mic/Aux.
- The Privacy image path is replaced with `SELECT_PRIVACY_IMAGE`. Select the
  supplied `assets/privacy.png` at its local absolute path after import.
- Website text is replaced with `example.com`. Session-specific text is replaced
  with generic topic text. Camera-off labels use generic messages.
- Private source metadata and hotkey bindings are cleared.
- Streaming credentials, service settings, WebSocket credentials, and the rest
  of the OBS configuration directory are not included.

Saved camera capture modes and source-level control overrides are retained.
These are a snapshot of OBS configuration, not accepted B001 camera presets.
Review them before connecting devices; selecting a camera can apply its saved
source controls. This collection does not establish B002 audio tuning either.

## Privacy operation and audio limits

The local scene is named `PRIVACY`; the sanitized export calls it `Privacy`.
It contains only a visible, locked image at the canvas origin, at 1:1 scale
without cropping. The 2560 × 1440 opaque PNG fills the canvas. No camera,
screen capture, microphone, nested scene, or browser source is included.

Global Mic/Aux is absent from the saved collection. One PulseAudio microphone
source is reused once in each Working/Talking scene and omitted from Privacy.
The live source was unmuted when inspected, with OBS audio monitoring off.
This excludes the microphone from Privacy's steady-state scene mix; it does
not set or enforce the microphone's mixer mute state. Returning to a
Working/Talking scene includes the microphone again if it remains unmuted.
This does not meet S004's explicit-unmute-on-exit requirement.

Desktop Audio remains global and was unmuted in the saved local configuration.
Music played through that output remains part of Desktop Audio, not a separate
application source. Privacy is not complete silence, and desktop playback of
microphone audio or another application's voice call could still be heard.
The sanitized export deliberately starts both audio sources muted for restore
safety; that differs from their inspected local state.

To select Privacy manually, click `PRIVACY` in OBS's Scenes list, or `Privacy`
in the restored collection. In Studio Mode, selecting it changes Preview;
transition it to Program before treating it as active. Scene selection does
not itself stop streaming. The saved 100 ms Fade briefly retains the outgoing
composition; an immediate concealment policy needs Cut or an appropriate
scene-specific override, which this export does not add.

The [S004 review](../docs/project/work/S004-simple-privacy.md) records the
remaining policy conflict and missing output tests. No microphone enforcement
script or application-audio plugin is required by this snapshot.

## Restore safely

Do not import or switch to this collection during a broadcast. Importing or
activating a collection can replace the active composition and audio setup.

1. Finish the broadcast, preserve the current local setup, and agree on an
   isolated or otherwise safe restoration test before proceeding.
2. Use OBS Studio 32.2.2 or a compatible version with Linux V4L2 camera capture,
   PipeWire screen capture and its desktop portal, PulseAudio-compatible audio
   capture, and the FreeType text source. Install the matching JetBrains Mono
   font family used by the saved text sources. No third-party presentation
   plugin is required by the exported source graph.
3. In OBS, use **Scene Collection → Import** to import `working-scenes.json` as
   a separate collection named `Stream Studio - Live Layouts`. Inspect it before
   selecting or activating it. Do not overwrite the existing live collection.
4. Create or select an appropriate separate OBS profile and apply the values
   in `output-settings.ini` through Settings. Scene collection import alone does
   not restore the encoder, bitrate, audio format, or output frame rate. Do not
   overwrite a live profile with this partial INI file.
5. Select the external 2560 × 1440 monitor in the screen capture source and grant
   portal permission. Reconnect each camera by its identity, preferably using
   persistent links under `/dev/v4l/by-id/`, rather than assuming numbered nodes
   are stable. Review capture modes and saved camera overrides first.
6. Select the intended Desktop Audio device and the shared `Microphone` source's
   device. Keep global Mic/Aux disabled to avoid bypassing Privacy or capturing
   the microphone twice. Check routing, levels, and mute states before
   explicitly unmuting either source.
7. Set `Privacy Card` to the local absolute path of `assets/privacy.png`. A
   missing image is not a usable holding card. Replace `example.com` and the
   generic topic with the intended public text. Configure any OBS service
   credentials or host-side controls separately in protected local
   configuration, never in these repository files.
8. Verify all four Working variants and the three camera-led scenes at output
   size. Check full-monitor capture, camera orientation and framing, the reserved
   right quarter, border alignment, camera-off placeholders, topic and website
   text, and clipping. Confirm the hidden fullscreen face border, matching face
   inset, and unchanged desk framing when switching desk variants. Check the
   audio sources separately. Check Privacy's image coverage and the actual
   output audio when entering and leaving from every live scene. Confirm the
   intended transition and microphone-return policy before live use. Do not
   treat cameras-off Working as Privacy.
9. Before live use, verify OBS rendering/encoding statistics and YouTube playback
   under the intended workload. Successful import alone does not validate this.

## Validation and limits

The JSON parses, source references resolve within the collection, and all
scene-item transforms were compared with the saved local collection during
export. Sanitization checks rejected portal tokens, credentials, local paths,
and network URLs. The output-settings file contains only the listed profile
fields, which still match the saved profile. Static inspection confirmed one
shared microphone reference in each live scene, no global Mic/Aux, and no
capture or microphone dependency in Privacy. The SVG renders, and its PNG
matches the image used by the saved local scene.

No restoration import, device activation, audio test, or broadcast was performed
for this snapshot. OBS import compatibility and restored visual/audio behaviour
remain untested. This does not complete S005's broader restoration criteria.

This is a point-in-time snapshot, not an automatic sync. Future scene changes
need a fresh, inspected export. Never replace this file with an unchecked copy
of the local scene collection or commit the whole OBS configuration directory.
