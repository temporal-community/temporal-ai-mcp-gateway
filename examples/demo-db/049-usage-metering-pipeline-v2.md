---
Name: Usage Metering Pipeline v2
Owner: Erin Vasquez
Status: Approved
Last Updated: 2026-05-19
---

## Context

Metered usage is aggregated hourly by a job that reads the event stream and writes counters. It was built for one metered product and now serves nine. Late events are dropped, the counters are not idempotent, and a replay after an outage double-counts in ways that are hard to detect and embarrassing to explain.

## Proposal

Rebuild the aggregation on the stream processing framework the data platform team already runs.

- Event-time windows with a documented lateness allowance per product
- Idempotent writes keyed on event identity, so replay is safe by construction
- Per-product configuration instead of branches in a shared job
- A reconciliation job that compares raw events to counters daily and alarms on drift

## Non-goals

No change to how usage is priced, and no change to the event schema. Products that emit bad events keep emitting them; this makes the bad events visible rather than silently absorbed.

## Risks

The lateness allowance is a billing decision dressed as a technical parameter. Setting it generously means invoices can move after a customer has seen them; setting it tightly means dropping usage we were paid to measure. The proposal is a conservative default per product with explicit sign-off from each product owner.

## Success metrics

Drift between raw events and billed usage, incidents attributed to metering, and the time to safely replay a day of events, currently measured in careful hours.

## Migration

Both pipelines run side by side for a full billing cycle, with the new one writing shadow counters that nothing invoices from. The comparison is per product, per tenant, per hour, and the expectation is that the two disagree: the current job drops late events, so any product with a real lateness tail should show the new counters higher. Disagreement in the other direction is the one worth stopping for. Products cut over one at a time, smallest metered revenue first. The product with the longest late-event tail goes last, when the reconciliation has a cycle of history behind it.

## Operational Impact

Metering moves onto the data platform team's framework, so their on-call inherits a job that can hold up invoicing. That needs an explicit agreement about severity and escalation before cutover, not after the first page at three in the morning. The daily reconciliation alarm also needs an owner who can act on drift rather than acknowledge it; drift in a metering counter is a billing error that has not been noticed yet. The compensation is that replaying a day stops being a careful manual operation and becomes a command anyone on that rotation can run.

## Rollback

Falling back to the hourly job is possible only while it is still running, which is the argument for keeping it alive for a cycle past cutover instead of deleting it at the first clean reconciliation. Past that point the counters are keyed on event identity and the old job cannot resume against them without a rebuild from raw events. That is the point of no return and it should be named in the cutover plan, with the date it falls on.
