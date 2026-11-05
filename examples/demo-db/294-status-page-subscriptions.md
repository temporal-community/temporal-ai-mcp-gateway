---
Name: Status Page Subscriptions
Owner: Ines Duarte
Status: Draft
Last Updated: 2025-09-01
---

## Problem

The status page shows current state and requires people to check it. During an incident, customers find out by trying to work and failing, then look for the status page, which several have told us they cannot find.

## Proposal

Subscription to status updates, with granularity by component and region.

- Subscription by email or webhook, with no account required
- Component and region selection, so a customer in one region is not alerted about another
- Updates sent on state change and at a defined cadence during an ongoing incident
- A link to the status page from the product when a component is degraded

## Scope

The public status page. Enterprise incident communication through the account team continues separately.

## Risks

Subscription means committing to update the page promptly during incidents, which is work done by someone who is also handling the incident. If updates lag the reality, subscribers get a worse experience than checking the page, so the communication role needs to be staffed in the incident process rather than assumed.

## Measurement

Subscribers, update latency during incidents against the committed cadence, support contacts during incidents, and in-product status link usage.

## Failure Modes

The worst case is the status page depending on infrastructure that is down. The degraded-component link lives in the product, so during a product outage the link pointing at the status page is unreachable too. The page and the sender have to run outside the systems they report on, including the mail path.

- Status page and sender hosted separately from the product, with no shared dependency
- Subscription list replicated outside the main database
- Webhook delivery retried, since a subscriber's endpoint may be down for the same reason

## Staffing

The communication role has to be a named position in the incident rotation rather than a task the responder picks up. In the last three incidents the person updating the page was the person debugging, and the page went quiet exactly when it mattered. A separate person with no debugging responsibility, writing updates from the incident channel, is the only version of this that holds under load.

## Open Questions

The cadence is unset. Fifteen minutes is frequent enough to be useful and frequent enough to produce updates that say nothing new, which teaches subscribers to ignore them. There is also no decision on whether a subscriber hears when an incident is downgraded rather than resolved, which is the state most incidents sit in longest.
