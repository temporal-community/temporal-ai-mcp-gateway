---
Name: Schema Change Notifications
Owner: Grace Lindqvist
Status: Shipped
Last Updated: 2025-07-15
---

## Background

When a warehouse table changed, consumers found out when something broke. The information existed in the deployment log but nothing connected it to the people affected, so each change produced a small wave of confused messages.

## Approach

Derive the affected consumers from lineage and query history, and notify them before the change lands.

- Changes detected at the pull request rather than at deployment
- Consumers resolved from query history over the preceding sixty days
- Notification includes the specific columns affected and the queries that touch them
- A two-day window between notification and merge for breaking changes

## Non-goals

No blocking. Notification was the cheap intervention and blocking would have required a governance conversation we did not need to have first.

## Risks

The obvious failure mode was notification volume, since a widely used table touches dozens of people. Scoping notifications to the specific columns in each consumer's own queries kept the volume manageable and the relevance high.

## Outcome

Shipped in June. Breakages attributed to schema change dropped from about fifteen a quarter to three, and two of those three were consumers who had read the notice and underestimated it, which is a different problem.

## Operational Impact

The two-day window changed how people work. A breaking change has to be opened two days before it is wanted, which pushes schema changes out of the end of a sprint and into its start. That is a real constraint on the teams making them rather than a free improvement.

- Authors see the consumer list at review time, which is where most changes get reshaped into non-breaking ones
- Consumers with no recent query are never notified, so a quarterly job sits outside the window silently
- The notice is a message rather than a ticket, so nothing tracks whether a consumer acted

## Failure Modes

The sixty-day window is the known hole: anything running less often has no query history and no notice, and a quarterly reconciliation job is both the least able to absorb a surprise and the most likely to be missed. The second is the one the outcome names. Two of the three remaining breakages came from consumers who read the notice and underestimated it, which says the notice communicates what changed but not what it does to the reader's query. Showing each consumer their own query with the affected column marked would close part of that, at the cost of rendering query text into a notification.

## Open Questions

- Whether consumers of consumers should be notified, since lineage reaches them and the notice stops at direct readers
- Whether the two-day window should scale with the number of affected consumers, given one reader and forty differ
- What to do about scheduled jobs outside the sixty-day window, the hole everyone knows about and nobody owns
