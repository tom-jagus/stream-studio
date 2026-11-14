# OBS scene snapshots

This directory contains sanitized scene-collection snapshots and a restore
script. They are starting points, not complete OBS backups or verified one-step
restorations. Neither the current snapshot nor the script has been tested by
importing or opening the restored collection in OBS.

## Files

- `current-scenes.json` is a sanitized snapshot of the saved collection,
  including the latest added scene, nested sources, and topic, keys, and chat
  Browser Sources. It preserves scene-item geometry and visibility. Some scene
  and source names are generic, and text contents are placeholders.
- `restore-scenes.sh` installs that snapshot as a separate collection named
  `Stream Studio Restored`; it does not activate it.
- `working-scenes.json` is the earlier sanitized Working, Talking, and Privacy
  snapshot. It predates the Browser Sources and remains available for manual
  import; the restore script does not use it.
- `assets/privacy.png` is the opaque Privacy card. The script points the
  restored image source at this file in the checkout. Keep the checkout at that
  path or select the image again in OBS.
- `output-settings.ini` is an allowlisted reference for the earlier saved output
  profile, not a complete importable profile or proof of current settings.

The current snapshot comes from the collection saved on disk while OBS was
running. It may not contain changes OBS had not yet saved. It retains saved
camera modes and control overrides, which may be applied when a camera is
selected; these are not accepted camera presets.

## Restore the current snapshot

Do not restore or switch scene collections during a broadcast. Close OBS first
and preserve your existing OBS configuration before attempting restoration.
From the repository root, run:

```bash
bash obs/restore-scenes.sh
```

The script requires Bash, Python 3, and `pgrep`. It refuses to run if a process
named `obs` is running, installs a separate file in the OBS scene directory,
and refuses to overwrite its fixed destination. It does not replace the active
collection, restore a profile, or start OBS. If the destination already exists,
inspect it before deciding how to remove or rename it; the script does not
update it in place.

Open OBS and select `Stream Studio Restored`. The script has not been tested
against OBS collection discovery, so confirm the collection is available and
inspect it before using it. Complete these manual steps:

1. Select the face and overhead cameras, review their saved capture modes and
   overrides, and reconnect the intended microphone and desktop audio devices.
   Both audio sources are muted in the snapshot; check levels and routing before
   deliberately unmuting them. Keep global Mic/Aux disabled to avoid bypassing
   Privacy or capturing the microphone twice.
2. Select the external monitor in the screen capture source and grant a fresh
   portal permission. The saved PipeWire restore token is intentionally omitted.
3. Replace the generic text placeholders with the intended public text. The
   Privacy image points to the supplied card in this checkout. Check that it
   loads and fills the canvas.
4. Start the local presentation service and check the topic, keys, and chat
   Browser Sources. Follow the [operating guide](../docs/topic-overlay.md) for
   their separate setup.
5. Check each scene at output size, including the new scene, source ordering,
   camera framing, the opaque sidebar, and browser overlays. Verify Privacy
   video and output audio, then check the intended transition and microphone
   return behavior. Do not treat a successful installation as proof of output.
6. Configure and verify output settings separately. The scene collection does
   not install encoder, bitrate, audio-format, or streaming-service settings.
   Verify performance and playback under the intended workload before live use.

The snapshot removes keyboard shortcuts, private metadata, device identifiers,
portal tokens, original text contents, and local paths. It does not contain OBS
streaming credentials, service settings, or WebSocket credentials. Browser
sources use only the local service endpoints. The sanitization and structural
inspection found matching source-type and scene-item counts, matching inspected
geometry and visibility, and no unresolved item references. These checks do not
prove OBS import compatibility, restored appearance, or audio behavior.

## Privacy operation

The saved Privacy scene uses a local image rather than a Browser Source and
omits the microphone, screen, and cameras. The saved configuration has global
Desktop Audio, so cliamp and other desktop sounds can continue in Privacy.
Omitting the microphone from Privacy does not mute its shared source. On return
to a live scene, it can be audible immediately if it was not muted separately;
Tom accepts this behavior and can use his Hyprland `Super+M` binding when he
needs a separate microphone mute.

The saved default transition was a 100 ms Fade during inspection, so it does not
establish immediate concealment. Check composed video and audio with harmless
content. In Studio Mode, selecting Privacy changes Preview; transition it to
Program before treating it as active. Selecting a scene does not stop the
broadcast or disable key capture. Use `stream keys off` before Privacy, Break,
or sensitive input. See the [operating guide](../docs/topic-overlay.md#keystroke-overlay)
for its limits.

The snapshots are point-in-time artifacts, not automatic synchronization.
Review future scene changes and sanitize a fresh export rather than copying the
entire OBS configuration directory into the repository.
