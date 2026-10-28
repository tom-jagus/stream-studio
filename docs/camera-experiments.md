# Camera experiments

Supporting evidence for
[B001, repeatable camera setup](project/work/B001-repeatable-cameras.md).
These are historical observations, not a fresh device inspection or an accepted
preset. B001 remains Draft during the documentation migration.

## Status after 2026-10-22

The first session established device capabilities and explored the C950 face
camera. No camera preset is approved or implemented. The S600 overhead camera
was inventoried but not adjusted. No software colour correction was applied.

Tom wants device-level settings outside OBS where possible, with manual exposure
and white balance and automatic focus. Repeatability remains untested.

## Device inventory

Both cameras expose V4L2 controls through the Linux `uvcvideo` driver.

| Camera | Confirmed role | Capture node during inspection |
| --- | --- | --- |
| EMEET SmartCam C950 4K | Face | `/dev/video4` |
| EMEET SmartCam S600 | Overhead | `/dev/video0` |

Both advertise MJPEG capture at 3840 × 2160 and 2560 × 1440 at 30 fps, and
1920 × 1080 at 30 or 60 fps. Their uncompressed YUYV modes are limited to lower
resolutions. Advertised modes are not proof of reliable simultaneous capture.

Both expose manual and automatic exposure, white balance, and focus, plus
brightness, contrast, saturation, hue, gamma, gain, sharpness, and zoom. Their
control ranges differ, so identical numbers are not interchangeable presets.
Persistent links exist under `/dev/v4l/by-id/`; resolve these by camera rather
than relying on the numbered nodes above.

The C950 connects through several USB hubs. The S600 is on a separate USB bus.
Neither arrangement was validated with both cameras streaming together.

## Lighting and capture conditions

Tom reports that the window is covered and the desk lamp normally stays on.
Its neutral setting is estimated at 4800 to 5000 K, not measured.

Tests began with the ceiling lights off. Later comparisons used the desk lamp
on neutral with the ceiling lights on. The blue/purple background light was
then switched off for colour comparisons. This final arrangement is an
experimental baseline, not a requirement for the finished setup. Lamp brightness
and position were not measured precisely.

The C950 preview and still captures used 1920 × 1080 MJPEG at 30 fps. This is a
test mode, not the selected final streaming resolution. No audio or video
recordings were made.

## Findings and limits

- Automatic exposure initially produced washed-out face highlights. Lowering
  gamma alone did not solve this; forehead samples showed red-channel clipping.
- Manual exposure and gain provide useful brightness control. A requested
  20 ms exposure became the main test point. Motion blur and lighting flicker
  still need validation; still frames cannot establish either.
- With the ceiling lights off, useful face brightness required more gain and
  the dark background showed objectionable grain. A 30 ms exposure with lower
  gain offered only a modest visual improvement.
- Ceiling lighting allowed lower gain and a visibly cleaner background. Grain
  remained, especially in dark areas. Increasing contrast hid some shadow
  detail and noise; it did not establish a reduction in sensor noise.
- Gamma changes were subtle in the tested captures. Contrast and hue had more
  obvious effects. Negative hue shifted skin toward magenta; positive hue
  shifted it toward yellow/green. Hue +10 was a provisional visual compromise,
  not evidence of accurate white balance.
- Manual temperature sweeps and white-paper references retained a pink/magenta
  tint. Switching off the coloured background light did not remove it. Paper
  position changed between captures, and some samples clipped, so these were
  approximate comparisons rather than colour calibration.
- Tom reported more natural skin in a later preview, but automatic white
  balance was subsequently found enabled. Do not credit that result to the
  manual temperature/hue combination. Disabling automation again brought back
  the pink tint; that trial did not freeze the automatic correction.
- Tom observed that opening `omarchy-webcam` enables automatic white balance.
  Device readback confirmed an unexpected enabled state during the session.
  The trigger and underlying cause have not been reproduced in a controlled
  test. Check this state after opening the panel or another camera application.

The installed plugin is `io.github.kristoferlund.webcam`. Its `webcamctl` helper
writes controls through `v4l2-ctl`, the same interface used in this session.
No plugin or OBS configuration was changed. The earlier suggestion that software
colour correction was necessary was premature; device-only tuning remains the
intended next investigation.

## Last verified C950 state

Read back at session wrap-up on 2026-10-22. These are unfinished trial values,
not a recommended preset, and may not survive another application opening the
camera, reconnecting it, or rebooting.

| Control | Readback |
| --- | --- |
| Capture mode | 1920 × 1080 MJPEG, 30 fps |
| Exposure mode | Manual |
| Exposure time | `200`, corresponding to a requested 20 ms |
| Gain | `25` |
| Automatic white balance | Off |
| White-balance temperature | `3798 K`; most recent comparison used `3800 K` |
| Continuous autofocus | On |
| Brightness | `0` |
| Contrast | `60` |
| Saturation | `64` |
| Hue | `10` |
| Gamma | `150` |
| Sharpness | `32` |
| Backlight compensation | `0` |
| Zoom | `0` |
| Power-line frequency | `50 Hz` |

The last brightness comparison favoured gain 25 and contrast 60 visually, but
it ran with automatic white balance enabled. Its colour is not a validated
manual-white-balance result. Tom was still unsure about overall darkness and
flatness; no final image was accepted.

## Resume procedure

1. Confirm the lighting arrangement. Renew permission for captures and device
   adjustments if starting a new session; the earlier grant was session-scoped.
2. Read the actual controls before resetting or restoring anything. Reproduce
   the white-balance change by comparing readback before and after opening
   `omarchy-webcam`, without moving sliders. Use only one preview at a time.
3. Establish manual white balance after opening the chosen preview, then verify
   that it remains off during capture. Keep autofocus on. Avoid software colour
   correction unless a separate experiment is agreed.
4. Use a non-clipped paper reference for approximate colour checks. Remove it
   before judging normal face brightness, because it can reflect light and
   changes the scene composition. Change one control or a documented comparison
   group at a time and save actual readback with each sample.
5. Once the picture is accepted, test motion and flicker, camera reopening,
   reconnects, reboot, and OBS behaviour before implementing a preset. Then tune
   the S600 under the chosen lighting.

Existing machine-local OBS camera sources use numbered device paths and saved
manual white-balance values of 4800 K for the C950 and 3800 K for the S600.
These were inspected, not changed; their effect on opening OBS is untested.

## Temporary artifacts

Control snapshots and private camera images remain under
`/tmp/stream-studio-camera.XrtTMu/`. The original C950 control snapshot is
`c950-before.txt`; the last comparison is in `brightness-tone.cjHbyg/`.
These files are temporary and may disappear before the next session. No images
were copied into the repository. This note preserves the findings independently
of those files.
