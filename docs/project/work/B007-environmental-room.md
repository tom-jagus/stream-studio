---
id: B007
status: Draft
---

# Daylight, weather, and room animation

## Outcome

Extend the shared illustrated room with local daylight and weather variation
and subtle animation after the core static presentation works.

## Why

Environmental changes give the room a sense of local time and conditions while
preserving a usable presentation when updates are unavailable.

## Boundaries

This is the final agreed stage after the core presentation and input
visualization. Apply the room effects to Starting, Break, and Ending, not to
Working or Talking.

Keep sky, city, window, room, and lighting separable during initial artwork and
presentation work. The recommended progression is daylight states first,
weather states next, and subtle motion last. Deriving daylight from local
sunrise/sunset and caching weather are recommended approaches rather than
selected implementations.

Keep exact private location and provider credentials out of versioned settings
and browser-visible data. External updates must not be necessary for a usable
room presentation.

## Acceptance criteria

- Starting, Break, and Ending share room variations that reflect the selected
  local daylight and weather conditions.
- Agreed animation works alongside scene text without making it unreadable.
- Missing or failed external updates leave a usable room presentation rather
  than preventing the scenes from displaying.
- Working and Talking do not inherit the illustrated room or its effects.
- Configuration and restoration guidance cover the selected provider and
  environmental behaviour without exposing exact private location or secrets.

## Open questions

- Which weather provider, location precision, and refresh cadence are suitable?
- Which daylight and weather states should be represented?
- What animation style and amount of motion are appropriate?
- What fallback should be shown when environmental data is missing or stale?
