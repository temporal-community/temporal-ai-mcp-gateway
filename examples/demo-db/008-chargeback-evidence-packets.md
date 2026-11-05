---
Name: Chargeback Evidence Packets
Owner: Nikhil Shah
Status: Draft
Last Updated: 2025-10-14
---

## Problem

When a chargeback arrives, somebody assembles the evidence by hand from five systems: the order, the delivery record, the login history, the policy the buyer accepted, and any correspondence. It takes about forty minutes per case and we lose cases on technicalities more often than on merits.

## Proposal

Generate the evidence packet automatically when the chargeback notification lands.

- A template per reason code, because the processors want different things
- Evidence pulled at notification time and snapshotted, not re-queried at submission
- A human review step that can edit and add, but starts from a complete draft
- Submission through the processor interface rather than the portal

## Scope

Card chargebacks only. Bank disputes follow a different timeline and a different evidence standard, and folding them in would double the template work for a tenth of the volume.

## Risks

Snapshotting evidence at notification time means a packet can be assembled from data that later turns out to be wrong, and we would be submitting it with more confidence than it deserves. The review step is not optional for this reason.

## Measurement

Win rate by reason code against the current baseline, minutes of handling time per case, and the share of cases lost for incomplete evidence, which should go to roughly zero.

## Interfaces Affected

Five read paths and one write path. The order and delivery systems already expose what the packet needs. Login history sits behind an internal console with no programmatic access, and the correspondence archive can be queried by ticket but not by order, so correspondence will be missing for any case where the buyer wrote in from a different address than the one on the order. Submission moves from the portal to the processor interface, which means we own retries, rate limits, and the submission receipt that is currently a screenshot somebody files.

## Staffing

The work shifts from assembly to review, and a reviewer needs more context than an assembler did.

- One reviewer a day on rotation, rather than whoever picks the case up
- Reason-code templates owned by the disputes lead, since processors change requirements without announcing it
- Handling time measured on review alone, so the forty-minute baseline is not compared against a different task

## Open Questions

What the review step does when the snapshot and the current data disagree. Rebuilding from fresh data breaks the snapshot guarantee; submitting the snapshot knowingly is the case the risks section warns about, and the reviewer needs a rule rather than a judgment call. We have also not decided whether to generate a packet for cases we expect to lose, where the handling time buys a near-certain loss and the only argument for submitting is that the processor watches the ratio.
