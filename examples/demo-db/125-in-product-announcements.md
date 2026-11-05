---
Name: In-Product Announcements
Owner: Sofia Marchetti
Status: Approved
Last Updated: 2026-05-09
---

## Context

Feature announcements go out by email and are read by a minority. Teams who want in-product visibility build a one-off banner, which means we currently have four different announcement components with four different dismissal behaviors and no frequency control between them.

## Proposal

One announcement surface with central scheduling and a frequency cap.

- A single component with defined placements and one dismissal model
- Scheduling through a shared calendar, with a hard cap of one announcement per person per week
- Targeting by plan, role, and feature usage, defined at schedule time
- Dismissal honored permanently per announcement, with no re-showing

## Non-goals

No change to email announcements, which serve a different purpose and reach people who are not currently in the product.

## Risks

A shared surface with a frequency cap creates a scarce resource, and the allocation of that resource will become a recurring argument between teams. Someone needs to own the calendar with authority to say no, or the cap will be relaxed within a quarter.

## Measurement

Announcements per person per week, dismissal rate, feature adoption following an announcement against a holdout, and the number of one-off banner components in the codebase, which should reach zero.

## Migration

The four existing banners retire in a fixed order, because two of them render in placements the new component will claim. The billing banner goes first; it is the only one with a server-side dismissal record we can read.

- Billing banner replaced first, with its dismissal records imported
- Trial and onboarding banners next, treating everyone as undismissed
- The release-notes banner removed rather than replaced, with its content moving to the calendar
- A lint rule added once the last one is gone, so a fifth component cannot appear quietly

Anyone who dismissed a local-storage banner sees its replacement once more. One re-show is cheaper than keeping two dismissal models alive through the migration.

## Staffing

Calendar ownership has no owner yet. The surface itself is a few weeks of front-end work, but the cap holds only if one person triages requests weekly and tells teams no. Product marketing is the obvious home since they already sequence launches, though they have no seat in the release process today that would let them see a request coming.

## Failure Modes

Targeting is evaluated at schedule time, so a person whose plan changes between scheduling and display can see an announcement for a plan they no longer hold. Evaluating at display time would cost a lookup on every page load, which is why we fixed it at schedule time; the cost is that announcements need a short lead rather than a long one.
