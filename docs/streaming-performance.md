# Streaming performance on the current laptop

This guide records the inspected baseline on the Ryzen 7 4700U laptop with
integrated Radeon graphics and about 7.1 GiB usable memory. It is a starting
point, not proof that a full stream will remain smooth. The findings and
settings below were inspected on 14 November 2026.

## Current baseline

### OBS

The saved `Untitled` OBS profile uses Simple output mode with x264 software
encoding and the `veryfast` preset. Its base canvas is 2560x1440, output is
1920x1080 at 30 fps, and the downscale filter is bicubic. The saved video
bitrate is 13,500 kbps. Check the effective settings and stream destination
before broadcasting; the scene snapshot does not restore the output profile.

The latest inspected OBS log showed both cameras capturing 1920x1080 MJPEG at
60 fps. This is not necessary for 30 fps output. Try 30 fps on each camera
and consider 720p capture if image quality permits, then verify the negotiated
modes in the OBS log. These are proposals, not confirmed current settings.

An earlier 1440p x264 stream lost frames to both rendering and encoding lag,
not only network drops. A later 1080p VAAPI test started successfully, but
Hyprland aborted after the AMD driver reported framebuffer failures and
insufficient memory for command submission. VAAPI may have contributed to
shared graphics memory pressure; the evidence does not establish it as the
sole cause. The current x264 baseline avoids relying on VAAPI, but moves
encoding work to the CPU.

### Local text-to-speech

The separate `tts-local` service uses the `en_US-hfc_female-medium` Piper voice,
two ONNX inference threads and the persistent per-message worker. Markdown and
plain-text requests are split into sections of at most 1,000 characters. The
worker loads the voice once per message, retains it during playback and exits
when the message finishes or is skipped. It does not synthesize the next
section during playback. Configure `inference_threads` and
`persistent_worker` in `~/.config/tts-local/config.toml`; restart the service
to apply changes. Restarting interrupts playback and discards queued messages.
See the TTS repository README for commands and configuration.

An isolated test showed unrestricted Piper inference using nearly all eight
CPU cores. A one-run comparison with two inference threads reduced average
sampled CPU usage substantially. A later manual multi-section test appeared to
stay below about 30% total CPU, with the worker using about 3% of memory. These
observations do not establish a hard process-wide CPU limit or a safe peak
memory bound. Keeping the worker loaded trades memory for fewer model reloads;
set `persistent_worker = false` to compare process-per-section behavior.

### Dictation

Voxtype is configured for local Whisper `base.en`, English, with `threads = 2`
in `~/.config/voxtype/config.toml`. Recent logs showed Vulkan GPU processing;
the thread setting does not establish a hard limit on the whole process or
GPU. The user found `base.en` accurate and faster than the earlier `medium`
model. In one recent observation, a 20.6-second recording was transcribed in
about 1.8 seconds. This is not a controlled comparison of model speeds.

After the change and Voxtype restart, available system memory was about
2.5 GiB in a snapshot, compared with roughly 580 to 730 MiB during the earlier
high-pressure observation. Other workloads and the restart also affect this
comparison. `small.en` was tried but did not provide enough perceived benefit
to justify using it. Voxtype logs may contain transcribed text; treat its
journal as private.

## Check the complete workload

Before a public stream, save work and run a private or unlisted test with the
full scene, both cameras, browser sources, TTS, dictation, cliamp and any
communication app or active call that will be used. Exercise long Pi responses
and representative dictation. Test screen and audio output with harmless
content, including the Privacy scene and its audio behavior.

In OBS, use View > Stats to monitor actual frame rate, rendering lag, encoding
lag and network-dropped frames. Rendering and encoding losses are different
stages; zero network drops does not rule them out. Check output readability at
1080p and listen for TTS gaps and dictation accuracy. Continue long enough to
cover typical activity and monitor the final OBS log after stopping.

Monitor available memory, active swap traffic, CPU and desktop responsiveness.
A high swap-used value alone does not prove a current stall. During an earlier
observation, active zram swap traffic and kernel memory reclaim coincided with
a CPU burst; the system was under memory pressure. Do not disable swap or run
`swapoff` as a quick fix: forcing pages back into limited RAM can worsen the
stall or cause processes to be killed.

If the test stalls, first identify which workload was active and reduce one
factor at a time. Options include closing a nonessential preview or browser
tab, reducing camera capture modes, comparing TTS worker modes, or lowering
OBS output resolution. Compare readability and OBS statistics after each
change. Do not assume the current baseline can support additional applications
without another representative test.
