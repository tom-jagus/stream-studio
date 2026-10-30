# OBS Working snapshot

This directory preserves the saved Working scene graph and its output settings.
It is a sanitized restoration starting point, not a full machine backup or a
verified one-click restore. No live OBS settings were changed to create it.

## Files and scope

- `working-scenes.json` contains an OBS scene collection with four Working
  variants and their required shared sources, transforms, colours, text styling,
  filters, and source relationships.
- `output-settings.ini` records an allowlisted subset of the active profile's
  video, streaming encoder, bitrate, and audio-format settings. It is a reference
  for manual setup, not a complete importable profile.

The snapshot uses a 2560 × 1440 canvas and output at 30 fps, software x264 with
its veryfast preset, 13,500 Kbps video, and 160 Kbps audio. Audio format is 48 kHz
stereo. These are saved settings, not proof of network capacity or performance.

Only the Working setup and its dependencies are included. Other scenes, browser
sources, scripts, timers, projectors, and existing hotkeys are excluded. There
are no external image assets in this snapshot; the presentation uses native
colour and text sources. Talking, Privacy behaviour, and their restoration are
not delivered by this collection.

## Privacy and local substitutions

Local source names and identifiers are replaced with consistent export names.
The shared scene relationships and scene-item geometry are preserved.

- Camera device identifiers are replaced with `SELECT_FACE_CAMERA` and
  `SELECT_OVERHEAD_CAMERA`.
- The PipeWire portal restore token is removed. Screen capture needs a fresh
  monitor selection and permission grant.
- Desktop and microphone audio device identifiers are replaced with
  `SELECT_LOCAL_AUDIO_DEVICE`. Both audio sources are muted in the export so
  restoration requires deliberate device selection and unmuting.
- Website text is replaced with `example.com`. Session-specific text is replaced
  with generic topic text. Camera-off labels use generic messages.
- Private source metadata and hotkey bindings are cleared.
- Streaming credentials, service settings, WebSocket credentials, and the rest
  of the OBS configuration directory are not included.

Saved camera capture modes and source-level control overrides are retained.
These are a snapshot of OBS configuration, not accepted B001 camera presets.
Review them before connecting devices; selecting a camera can apply its saved
source controls. This collection does not establish B002 audio tuning either.

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
   a separate collection named `Stream Studio - Working`. Inspect it before
   selecting or activating it. Do not overwrite the existing live collection.
4. Create or select an appropriate separate OBS profile and apply the values
   in `output-settings.ini` through Settings. Scene collection import alone does
   not restore the encoder, bitrate, audio format, or output frame rate. Do not
   overwrite a live profile with this partial INI file.
5. Select the external 2560 × 1440 monitor in the screen capture source and grant
   portal permission. Reconnect each camera by its identity, preferably using
   persistent links under `/dev/v4l/by-id/`, rather than assuming numbered nodes
   are stable. Review capture modes and saved camera overrides first.
6. Select the intended desktop-audio and microphone devices. Check routing,
   levels, and mute states before explicitly unmuting either source.
7. Replace `example.com` and the generic topic with the intended public text.
   Configure any OBS service credentials or host-side controls separately in
   protected local configuration, never in these repository files.
8. Verify all four Working variants at output size. Check full-monitor capture,
   camera orientation and framing, the reserved right quarter, border alignment,
   camera-off placeholders, topic and website text, and clipping. Check the
   audio sources separately. Do not treat cameras-off Working as Privacy.
9. Before live use, verify OBS rendering/encoding statistics and YouTube playback
   under the intended workload. Successful import alone does not validate this.

## Validation and limits

The JSON parses, source references resolve within the collection, and all
scene-item transforms were compared with the saved local collection during
export. Privacy checks rejected portal tokens, credentials, local paths, and
network URLs. The output-settings file contains only the listed profile fields.

No restoration import, device activation, audio test, or broadcast was performed
for this snapshot. OBS import compatibility and restored visual/audio behaviour
remain untested. This does not complete S005's broader restoration criteria.

This is a point-in-time snapshot, not an automatic sync. Future scene changes
need a fresh, inspected export. Never replace this file with an unchecked copy
of the local scene collection or commit the whole OBS configuration directory.
