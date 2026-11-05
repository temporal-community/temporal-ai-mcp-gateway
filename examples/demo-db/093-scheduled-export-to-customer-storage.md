---
Name: Scheduled Export to Customer Storage
Owner: Yusuf Demir
Status: Draft
Last Updated: 2025-11-21
---

## Context

Enterprise customers ask for their data on a schedule, into their own storage. Today this is a professional services engagement: a bespoke job per customer, built by a solutions engineer, maintained by nobody in particular. There are nineteen of them.

## Proposal

A configurable export that customers set up themselves.

- Destination configured by the customer with credentials they control and can rotate
- A fixed set of exportable datasets with documented schemas and versioning
- Scheduling, partitioning, and format chosen by the customer within supported options
- Delivery status visible to the customer, including failures and their cause

## Scope

The eight datasets that cover the existing nineteen bespoke jobs. Anything beyond that remains a services engagement until demand justifies adding it.

## Risks

Export destinations are customer-controlled, which means failures are frequently theirs and the error messages are ours to explain. Without good delivery status this becomes a support burden that exceeds the services work it replaces.

## Measurement

Bespoke jobs retired, exports configured without services involvement, delivery success rate, and support contacts per configured export.

## Migration

The nineteen bespoke jobs do not convert automatically. Each is mapped to the eight supported datasets, and any column it produces that no documented schema covers is either added to that schema or dropped with the customer's agreement. Three or four will resist mapping; those stay services work and are counted as such rather than quietly left running.

- Map each job to supported datasets and record the gaps
- Run the bespoke job and the configured export in parallel for two cycles, comparing row counts
- Retire the bespoke job only after the customer confirms a clean cycle

## Support Impact

Delivery failures move from a solutions engineer who knows the customer to a queue that does not. Three causes are worth distinguishing: expired credentials, a destination that rejects the write, and a schema version change on our side. The first two are the customer's to fix and delivery status should say so in those words; the third is ours, and blurring them teaches customers to open a ticket for everything.

## Cost

Egress to customer destinations is ours up to the handoff. Eight datasets at daily cadence across nineteen customers is a modest bill, but partitioning changes it by an order of magnitude: hourly partitions on the largest dataset produce small files and far more requests than a daily export of the same rows. The supported options should be bounded by that, not by what is expressible.
