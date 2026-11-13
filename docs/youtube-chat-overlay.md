# YouTube chat overlay

The local presentation service connects to YouTube's read-only live chat API
and provides a transparent OBS Browser Source at
`http://127.0.0.1:8766/chat`. It does not send messages or moderate chat.
The current implementation has been used with a live broadcast and OBS, but
retry, failure handling, and browser rendering have not been fully verified.

## Setup

Use Python 3.12 or newer and install the chat extra from this checkout. Include
`keys` as shown if the keystroke overlay is also in use.

```bash
uv tool install --force --editable '.[keys,chat]'
```

In Google Cloud, create or select a project, enable the YouTube Data API v3,
and create an API key. Apply restrictions appropriate to your setup and allow
the required YouTube API access. The key must work for both video lookup and
live chat. API availability, quota, and restrictions are governed by Google.

Save the key as `~/.config/stream-studio/youtube-api-key`, owned by your user
and readable only by you, with mode `600`. If `XDG_CONFIG_HOME` is set, use
`$XDG_CONFIG_HOME/stream-studio/youtube-api-key` instead. Do not put the key in
the repository, a command line, or OBS. After changing the installed service's
code or dependencies, restart the user service when it is safe to do so:

```bash
stream stop
stream start
```

Restarting clears transient chat and starts keystroke capture disabled.

## Operate

Start the local service, then select a live broadcast using its YouTube URL or
11-character video ID:

```bash
stream chat start 'https://www.youtube.com/watch?v=VIDEO_ID'
stream chat status
stream chat stop
```

Starting replaces the previous selection. Status reports the connection state,
reason, expiry preference, and skipped timestamp count. Connection and lookup
happen in the background, so check status after starting. Stop clears the
transient messages. The service does not select a broadcast automatically after
restart. Add a Browser Source for `/chat`; OBS controls its size, placement,
and visibility. Install JetBrains Mono for the intended font.

Messages are held in memory, not archived. The service keeps at most 50, with
bounded author and message lengths. The browser displays the newest messages
that fit. Continuous display is the default; use a positive whole number of
minutes to expire messages, or `off` to disable expiry:

```bash
stream chat expiry 5
stream chat expiry off
```

The preference persists in `~/.config/stream-studio/chat.json`, or the matching
`XDG_CONFIG_HOME` location. With expiry enabled, age is measured from YouTube's
posting time. Messages with missing or invalid timestamps, or timestamps more
than 60 seconds in the future, are skipped and counted in status. An inaccurate
system clock affects expiry.

## Privacy and troubleshooting

Viewer messages shown in OBS are public on the broadcast. Hiding the source and
moderating messages remain manual OBS and YouTube responsibilities. Privacy and
Break scenes do not stop the chat service; use `stream chat stop` when needed.

If status reports a missing or unsafe key, check the path, owner, and mode. If
lookup or connection fails, check that the broadcast is live, chat is enabled,
the key and API restrictions permit access, and quota and network access are
available. Errors may combine multiple causes. Lookup and connection failures
are retried with increasing delays capped at 60 seconds; check status rather
than assuming recovery. Missing chat dependencies or a missing or unsafe key
stop the worker rather than retrying. After correcting the key, use
`stream chat start` again with the broadcast URL or ID. After installing
dependencies, restart the service and start chat again. No message content is
deliberately logged by the service.

To rotate a key, create a replacement, replace the private key file, revoke the
old key in Google Cloud, and start the chat again. To remove access, stop chat,
delete the key file, and revoke the key in Google Cloud. Removing the local file
alone does not revoke it. The expiry preference is separate and can be removed
by deleting `chat.json` when the service is stopped.
