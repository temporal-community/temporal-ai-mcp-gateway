---
Name: Background Refresh Policy
Owner: Tom Okafor
Status: Draft
Last Updated: 2025-09-23
---

## Context

The application refreshes in the background on the platform's schedule and fetches everything it might need. On the platform that reports it, we appear in the top ten battery consumers for a meaningful share of users, which is the kind of thing that gets an application deleted.

## Proposal

Fetch less, less often, and prioritize by what the person actually opens.

- Refresh scoped to the three most recently used contexts rather than everything
- Frequency adapted to observed usage, not fixed
- Payloads reduced to what the list views render, with detail fetched on open
- A debug view in internal builds showing exactly what each background wake fetched

## Non-goals

No change to push-triggered fetch, which is small and necessary.

## Risks

Adaptive frequency means the application behaves differently for different people, which makes bug reports harder to reproduce and makes the behavior hard to describe in documentation. The debug view helps internally but customers will experience inconsistency they cannot explain.

## Measurement

Background data transferred per day, battery attribution where the platform reports it, and the staleness of content at foreground, which is the thing we are trading away.

## Rollout

Payload reduction first, because it carries no behavioral variance: everyone fetches less on the same schedule and the saving is readable within a week. Context scoping follows. Adaptive frequency goes last and behind a staged release, since it is the only part that makes two devices behave differently and the only part that cannot be reproduced on demand once somebody reports it.

## Support Impact

The reports that arrive will be about staleness, and they will not use that word.

- Content older than expected at foreground, described as items missing or not updating
- The three-context scope means someone working across many contexts finds the fourth stale every time, which is a real complaint rather than a misunderstanding
- Support cannot see what a device fetched, since the debug view is internal, so a reproduction step is usually unavailable

## Open Questions

Whether adaptive frequency should appear as a setting, trading some of the battery saving for an explanation people can act on. A visible control would also make the behavior describable in documentation, which the risks section says it is not. The other is what adaptation does with a device dormant for a fortnight, where observed usage says never refresh and the first foreground after a holiday is exactly when staleness is most visible.
