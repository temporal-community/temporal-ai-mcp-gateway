---
Name: Alert Fatigue in Product Notifications
Owner: Ruth Adeyemi
Status: Draft
Last Updated: 2026-03-26
---

## Problem

Nine different product surfaces can raise an in-product notification, each added by a different team with its own judgment about what warrants attention. The combined volume is high enough that the notification area is routinely cleared without being read.

## Proposal

One budget, centrally governed, with categories ranked by what people act on.

- A per-person per-day budget for non-urgent notifications, enforced centrally
- Categories ranked by observed action rate, with low-action categories dropped first
- A monthly review of category action rates, with the lowest removed rather than retuned indefinitely
- Urgent categories exempt and defined narrowly, with additions requiring review

## Non-goals

No change to mentions or direct messages, which are not subject to the budget.

## Risks

A central budget means one team's notification is dropped so another team's can appear, and the ranking that decides this will be contested by whoever ranks last. Using observed action rate rather than stated importance is what makes the ranking defensible, and it should be published internally.

## Measurement

Notifications per person per day, action rate per category, bulk-clear events, and whether the categories removed produce any measurable complaint.

## Data We Have

Action rate is computable today for seven of the nine surfaces. The other two render through their own component and record a view but no follow-through, so their rate is unmeasurable until they move to the shared one. Ranking without them means ranking seven categories and exempting two by accident, which is the outcome the ranking exists to prevent.

- Seven surfaces already emit a usable action event
- Bulk-clear events are recorded and cluster into a few minutes of the day
- Nothing distinguishes a notification ignored from one never seen, since the area is not always on screen

## Failure Modes

A daily budget rewards whoever emits earliest, because the budget fills in arrival order unless something else decides. Ranking has to apply before the budget rather than after, or the first notification of the morning wins regardless of what it is. The other workaround is obvious: a team whose category ranks poorly reclassifies it as urgent, which is why additions to the urgent set need review and why that set should be published next to the ranking.

## Review Notes

Removing the lowest category each month is stated as a rule and will stop being followed around the third month, when the lowest belongs to a team that has just rebuilt it. Removal should be automatic and the appeal explicit, rather than the other way round.
