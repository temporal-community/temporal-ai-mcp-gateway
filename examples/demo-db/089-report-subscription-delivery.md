---
Name: Report Subscription Delivery
Owner: Marcus Reyes
Status: Shipped
Last Updated: 2025-07-02
---

## Background

Scheduled reports were delivered by a job that rendered and mailed them. It had no retry, no delivery record, and no awareness of whether the underlying data had loaded, so a late pipeline produced a confidently empty report in several inboxes.

## Approach

Make delivery dependent on freshness and make failure visible.

- Delivery waits for the declared upstream datasets to be fresh, up to a deadline
- Past the deadline, the report is sent with an explicit staleness note rather than suppressed
- Delivery recorded per recipient with retry on transient failure
- Subscribers can see the delivery history for their own subscriptions

## Non-goals

No change to report content or rendering, which were not the problem.

## Risks

The deadline behavior was the contested decision. Suppressing a stale report hides a problem; sending it risks the note being ignored. We chose sending with a prominent note on the grounds that a missing report is interpreted as nothing to report, which is the more dangerous misreading.

## Outcome

Shipped in June. Empty-report complaints stopped entirely, and the staleness note has appeared on about four percent of deliveries, each of which corresponded to a real pipeline delay.

## Dependencies

Waiting on freshness only works where a dataset publishes a freshness signal. Twenty-eight of the thirty-four datasets behind scheduled reports do. The other six load on a schedule and say nothing, so their subscriptions keep the old behavior: send at the scheduled time, claim nothing either way. Subscribers cannot see which group their report is in, and that gap is the most likely source of the next complaint.

## Operational Impact

Delivery became a queue with retries behind it, which means it can back up, and it did once in August behind a provider rate limit. On-call also picked up a new alert: deadline approaching for a named report, which fires roughly forty minutes before a subscriber would see the staleness note and is often enough time to restart the pipeline. The delivery record pays for itself separately — answering whether a given report reached a given person used to take an hour of log reading.

## Failure Modes

- A dataset reports fresh while only partly loaded; the report renders complete, is wrong, and carries no note
- Retrying a hard bounce, which mail providers treat as a worse signal than a single failure
- A deadline set longer than the interval to the next run, so two deliveries of the same report overlap
- Delivery history scoped to the viewer, so a subscriber cannot tell whether the colleague who forwarded them a different number got a different copy
