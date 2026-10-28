---
id: B006
status: Draft
---

# Neovim-focused input visualization

## Outcome

Show useful editor input on stream only while Neovim is focused, under an
explicitly agreed disclosure policy.

## Why

Selected editor commands can help viewers follow the work, but unrestricted
keystroke display can disclose private text or actions.

## Boundaries

This is the fourth agreed step, following the initial local presentation and
static room scenes. The agreed focus requirement concerns Neovim itself, not
merely the terminal window containing it. A terminal multiplexer may further
complicate identifying the active application.

Investigating Neovim-side input events with tested focus handling is recommended
instead of unrestricted system-wide collection. No capture mechanism or
filtering policy has been selected.

The proposed initial safety policy is explicit session opt-in, an allowlist of
useful Normal/Visual-mode commands, no Insert-mode text or command-line contents,
clearing displayed and queued events on focus loss or entry to Break/Privacy,
and no retained raw keystroke history. This is a proposal to confirm before
implementation, not an accepted disclosure policy.

Neovim focus and filtering do not guarantee that commands or their context are
non-sensitive. A reserved screen area is also not a confidentiality guarantee.

## Acceptance criteria

- An explicit disclosure policy is agreed before visualization is enabled.
- Visualization is demonstrably inactive outside focused Neovim, including
  changes within the actual terminal and any multiplexer in use.
- Tests demonstrate that displayed, queued, and retained input follow the
  agreed policy, including its activation and clearing rules.
- Break and Privacy behaviour is tested against the agreed policy, and
  restoration guidance explains activation, limits, and safe shutdown.

## Open questions

- Which terminal and multiplexer arrangements must focus detection support?
- What capture mechanism can reliably enforce Neovim-level focus?
- Is the proposed safety policy sufficient, and which commands are useful and
  acceptable to display?

## Risks

Editor input can reveal private information even when Neovim is focused. Agree
and test the disclosure policy before enabling display; do not describe focus
filtering as a guarantee against disclosure.
