---
id: S005
status: To do
parent: B003
depends_on:
  - S002
  - S003
  - S004
---

# Restorable layout configuration

## Outcome

Preserve the accepted Working, Talking, and simple Privacy setup with enough
configuration and guidance to restore and verify it without exposing private
machine settings or duplicating camera tuning.

## Acceptance criteria

- Saved scene configuration and required presentation assets cover the accepted
  layouts, shared source/filter relationships, and simple Privacy behaviour.
- Required plugins, capture permissions, source/device identification, fonts,
  asset locations, and any machine-specific substitutions are documented.
- Configuration is inspected for credentials, stream keys, private paths, and
  unrelated settings before being included in the repository. Do not publish
  the entire OBS user configuration directory as a shortcut.
- A bounded restoration check reproduces the accepted composition and shared
  configuration and verifies Privacy video concealment and microphone behaviour.
  It does not overwrite the live setup without explicit approval.
- Verification guidance covers output-size readability, source availability,
  scene switching, and Privacy operation. It distinguishes layout restoration
  from B001 camera presets, B002 audio tuning, and untested live-stream behaviour.
- Remaining manual steps and unavailable validation evidence are explicit. A
  successful import alone is not claimed to prove the restored setup works.

## Tasks

- [ ] Identify the minimal configuration, assets, and external dependencies needed
      to reproduce the accepted scenes.
- [ ] Prepare and inspect exports or other restoration artifacts with private
      values separated from reusable configuration.
- [ ] Write setup and verification guidance matching the actual artifacts.
- [ ] Agree on a safe restoration-test location or method before importing.
- [ ] Perform the authorized check and report any gaps against accepted layouts.

## Open questions

- Which OBS export and restoration mechanism preserves the chosen shared sources
  and any Privacy automation without unsafe machine-wide configuration?
- How can restoration be tested without disrupting the active OBS setup?

## Boundaries

No broadcast, public publication, or Git action is required. Restoration does
not retune cameras or settle audio processing. Source/configuration edits and
changes to machine-local OBS state need explicit implementation approval.
