---
Name: In-App Update Prompts
Owner: Felix Braun
Status: Shipped
Last Updated: 2025-07-23
---

## Problem

Version adoption was slow enough that we supported four releases simultaneously, and a quarter of sessions ran on a version more than three months old. Those versions carried bugs we had fixed and could not help with.

## Approach

Prompt in the application rather than relying on store auto-update.

- A soft prompt after a release has been available for two weeks, dismissible
- A firm prompt for versions carrying a security fix, with the reason stated
- A hard block only for versions the service can no longer serve, with a clear message
- Prompts suppressed during an active task, never interrupting work in progress

## Non-goals

No forced update for ordinary releases, which would be an overreach for a bug fix.

## Risks

The interruption cost is paid by everyone and the benefit accrues to the support team, which is a trade that is easy to get wrong in our favor. Capping prompt frequency per user per release was the control that kept this honest.

## Outcome

Shipped in June. Sessions on versions older than three months fell from twenty-four percent to six over two months, and we now support two releases rather than four.

## Operational Impact

Supporting two releases instead of four is what support actually feels: a reproduction starts from two candidate versions rather than four, and the compatibility matrix in the release notes halved. Release engineering took the opposite side of the trade. Faster adoption means a shorter window between shipping a release and most people being on it, so a bad build reaches more of the installed base before anyone notices.

## Review Notes

- Suppressing prompts during an active task needed a definition of active the client could evaluate cheaply; the shipped rule treats any unsaved edit as active, which is conservative enough that some people see no prompt for a week
- The firm prompt states the reason for a security fix in general terms, which was agreed with the security team rather than chosen as copy
- The hard block names a version and a date and promises nothing else, because it is shown to people who are already stuck

## Open Questions

Whether two weeks is still the right delay before the soft prompt. The delay existed to avoid pushing people onto a release that might be rolled back, and the rollback rate since has been low enough to argue for shortening it. Shortening it also shortens the window in which a bad release stays contained, which is the same tension the release engineering side raised, and nobody has owned the decision.
