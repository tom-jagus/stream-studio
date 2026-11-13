---
id: S009
status: To do
parent: B004
depends_on:
  - S006
---

# Local YouTube chat overlay

## Outcome

Show recent YouTube live-chat messages in a styled local OBS Browser Source,
using one read-only connection managed by the existing presentation service.
Keep per-stream setup simple and allow an optional message expiry.

## Acceptance criteria

- With the service running, `stream chat start <youtube-url-or-id>` selects an
  accessible live broadcast and starts its chat connection. `stream chat status`
  reports connection state and actionable errors, including disabled chat,
  unavailable broadcast, missing credentials, quota or network failures.
  `stream chat stop` ends the connection and clears displayed messages. No
  YouTube sign-in page or credentials appear in the OBS source.
- Use the official YouTube Live Streaming API for read-only chat. Set up the
  required API access once and keep the key outside the repository and browser
  responses. Resolve the live-chat ID from the selected broadcast. Handle
  disconnects with bounded retry and recovery, avoid duplicate messages on
  reconnect, and stop retrying when explicitly stopped. Do not claim that public
  chat access works until checked against the actual broadcast.
- A separate local `/chat` page displays a bounded set of recent messages in a
  transparent OBS Browser Source, using JetBrains Mono and Catppuccin Mocha.
  OBS controls placement and scene visibility. Render usernames and message
  content as text, never executable markup. Keep memory and displayed content
  bounded, including message length; do not persist chat history. Display the
  latest messages continuously by default and remove the oldest as needed.
- `stream chat expiry off` disables expiry. `stream chat expiry <minutes>`
  accepts a positive whole number of minutes, including 1, 5, and 99; invalid
  values report an error without changing the setting. The preference survives
  service restart. With expiry enabled, remove messages based on YouTube's
  posting timestamp, including after reconnect, rather than local receipt time.
- When expiry is enabled, skip messages with missing or invalid posting times
  and report the skipped count through status without logging message content.
  Allow timestamps up to 60 seconds ahead of the local clock for clock skew;
  treat timestamps further ahead as invalid. When expiry is off, messages with
  missing or invalid timestamps may be displayed within the normal bounds.
  Explain that an inaccurate system clock affects expiry.
- Setup and operating guidance covers API access, key protection, CLI commands,
  OBS setup, expiry, quota and connection failures, and removal or rotation of
  credentials. Warn that viewer messages are public on the broadcast and that
  hiding or moderating the source remains a manual OBS/YouTube responsibility.
  Privacy remains independent of the chat service.
- Authorized synthetic tests cover URL/ID handling, API responses and failures,
  retry and deduplication, bounded state, safe rendering, settings persistence,
  expiry including invalid and future timestamps, and stopping. A separately
  authorized harmless-message check verifies the real YouTube connection and
  OBS presentation; missing access or evidence is reported, not treated as a pass.
  Existing topic and keystroke behavior remains intact.

## Tasks

- [ ] Confirm the official API's accessible-broadcast, credential, quota, and
      reconnect behavior for the selected integration; report any blocker.
- [ ] Add read-only chat acquisition, bounded state, expiry, and CLI controls.
- [ ] Add the local OBS page and safe rendering with the agreed styling.
- [ ] Add synthetic tests and, when authorized, check harmless messages with a
      real broadcast and OBS.
- [ ] Write setup, operating, privacy, and troubleshooting guidance after the
      implementation result is accepted.

## Boundaries

Automatic broadcast discovery, sending messages, moderation controls, chat
archiving, and third-party hosted overlay services are excluded. A future
on-desktop view that OBS does not capture is a separate outcome and is not
required here. Do not assume window transparency prevents screen capture.
Service startup does not need to select or connect to a broadcast automatically.
Actual credentials, network setup, service restarts, live broadcast checks,
source edits, tests, and Git actions require their applicable authorization.
