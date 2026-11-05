---
Name: Identity Event Stream for Audits
Owner: Ines Duarte
Status: In Review
Last Updated: 2026-07-02
---

## Background

Identity events are written to the application log and expire after thirty days. Customers in regulated industries need twelve months and need it in a form their own tooling can consume, which today means they screen-scrape the activity view.

## Proposal

A durable, structured identity event stream with a retention policy that matches the obligation.

- A fixed schema per event type, versioned, with additive changes only
- Twelve-month retention by default, longer on contract
- Delivery by webhook and by scheduled export to customer storage
- An AI summarization layer over the stream that turns a day of raw events into a readable narrative for reviewers who are not security specialists

## Scope

Identity events: sign-in, permission change, credential lifecycle, session revocation. Product activity events are a separate stream owned by another team and should stay separate.

## Risks

The summarization layer is the part that needs care. A narrative that quietly omits an event because it did not fit the summary is worse than no narrative, so the raw events stay the record of truth and every summary links to the events it was built from. We should also be clear in the documentation that summaries are not an audit artifact.

## Measurement

Customers consuming the stream directly, screen-scraping detected against the activity view, and audit findings about log retention.

## Interfaces Affected

The activity view keeps its current behavior, so customers who screen-scrape it today do not break on the day the stream ships.

- Webhook registration, subscribed per event type rather than as one firehose, since most customers want credential lifecycle and nothing else
- Export destination configuration, which exists only for billing exports and has to accept a second payload shape
- The documentation, which states thirty-day retention in four places and will be wrong in all four

## Cost

Twelve months of structured identity events is a different storage profile from thirty days of log lines. A large tenant writes on the order of forty thousand identity events a day, so a year is roughly fifteen million rows for that tenant alone, held in a store we have to be able to query by actor and by time. Storage is the small part. The summarization layer runs over each tenant-day and is the recurring cost, which is why it should be generated on request for the first release rather than precomputed for every tenant every night.

## What Would Change Our Mind

If the customers asking for twelve months only ever read the data at quarter end, a scheduled export with no webhook and no narrative covers them for a fraction of the work, and the stream becomes a file-drop feature. The signal to watch is whether the pilot tenants register webhooks at all. Two of the four asked for retention without mentioning delivery.
