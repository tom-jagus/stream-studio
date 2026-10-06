# Current progress

## Verified state

- Repository: `~/src/default/stream-studio`, initialized on `main` with no commits
  at the time of initial inspection.
- The repository was empty apart from Git metadata before this documentation
  was added.
- Initial project documentation now records the agreed scope and work order.
- No camera inventory, presets, OBS scenes, local service, keyboard integration,
  or input visualization has been implemented or validated here.

The hardware and lighting descriptions are user-reported. No device settings
have been captured or changed for this project.

## Current focus

Camera setup: inspect the Emeet C950 face camera and Emeet S600 overhead camera,
establish a repeatable lighting baseline, and compare sample frames before
saving supported presets.

## Open decisions

Near-term:

- Supported controls, capture modes, and stable device identification for both
  cameras.
- The lighting arrangement and whether multiple presets are needed.
- Audio device and baseline settings.
- Output resolution/frame rate and the Catppuccin flavour used for styling.

Later, when their phases begin:

- Local-service stack and asset approach.
- Host-side bridge for Vial controls and its place in the implementation order.
- Neovim focus detection, event capture, and approved disclosure policy.
- Final branding assets, weather integration, and animation treatment.
- Repository visibility and license before public distribution.

These choices do not block beginning camera inspection.

## Next useful action

Perform a read-only inventory of the two cameras and their exposed controls.
Then, with explicit approval to capture frames and apply device adjustments,
compare baseline images under documented lighting and develop the first
repeatable presets.

## References

- [Project definition](definition.md)
- [Design brief](../design.md)
