---
Name: Ticket Backlog Aging Policy
Owner: Ruth Adeyemi
Status: In Review
Last Updated: 2026-06-05
---

## Problem

About four hundred tickets are older than thirty days. Most are waiting on us, some are waiting on the customer, and nobody can tell which from the queue view. They are worked occasionally, by whoever feels guilty, in no particular order.

## Proposal

An explicit policy with states that mean something and an aging review.

- A waiting-on-customer state that pauses aging and auto-closes after two reminders
- A blocked state requiring a linked reason, such as an engineering escalation
- Weekly review of the oldest twenty, with a decision on each rather than a glance
- Tickets older than ninety days closed with a specific message and an easy reopen

## Non-goals

No bulk closure of the existing backlog, which would be tidy and would abandon people.

## Risks

Auto-closing after reminders will close cases where the customer was waiting for us to do something and the state was set wrongly. The reminder wording and the ease of reopening are what make this acceptable, and the reopen rate is the signal that the state is being misapplied.

## Measurement

Backlog size and age distribution, tickets reopened after auto-close, and the share of aged tickets in a state that explains why they are aged.

## Rollout

The states ship before any auto-close does. Running them for a month with aging paused but nothing closing gives us a read on how often waiting-on-customer is applied to a ticket that is actually waiting on us, and that read is what sets the reminder interval. Turning auto-close on first would make the misapplication visible only as reopened tickets from people who had already been waiting.

The ninety-day closures start with tickets created before the policy existed, worked newest first so the oldest and most abandoned cases get a human decision in the weekly review rather than a form message they never asked for.

## Support Impact

Staff gain two new states they have to choose between correctly, and the blocked state costs them a linked reason they do not have to supply today. That is friction on every escalation, and it is the point: an escalation with no link is how a ticket ends up ninety days old with nobody able to say what it is waiting for.

## Open Questions

Whether the weekly review of the oldest twenty should be owned by one person or rotated. Rotation spreads the knowledge of what is actually stuck across the team and loses the continuity that makes a second look at the same ticket useful.
