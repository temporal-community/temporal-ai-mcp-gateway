---
Name: Notification Delivery Reliability
Owner: Priya Raman
Status: Approved
Last Updated: 2026-03-12
---

## Context

We do not know whether notifications arrive. The sending service records a successful handoff to the provider and nothing afterwards, so a provider-side failure or a silent drop looks identical to a successful delivery in our data.

## Proposal

Track delivery end to end and act on the failures.

- Delivery and bounce events consumed from the providers and recorded per notification
- Per-recipient delivery state visible to support, which currently requires asking the provider
- Automatic suppression after repeated hard failures, with a path to re-enable
- A reliability figure per channel reported weekly

## Scope

Email and push. In-product notification is delivered by a path we control and already observe.

## Risks

Consuming delivery events means storing per-recipient delivery records, which is personal data with a retention question attached. A short retention for the detail and aggregate retention for the reporting is the obvious shape and should be decided before implementation.

## Measurement

Delivery rate per channel, bounces and their causes, suppressed addresses, and support contacts about notifications not arriving.

## Failure Modes

- Push tokens expire quietly, so a device that stopped receiving reads as delivered until the token is rejected, which can be weeks later
- The two providers classify bounces differently; a soft bounce at one is a hard failure at the other, and a suppression rule written in one vocabulary over-suppresses the other channel
- Delivery events can arrive before our own send record commits, so an event with no matching notification is routine rather than an error

The last one is harmless if the consumer buffers and retries the match, and damaging if it is counted as a drop.

## Support Impact

Per-recipient state removes the dependency on asking the provider, which takes a day and runs through the one person holding the credentials. What support gains in exchange is a screen that says delivered while the customer says nothing arrived, which is a harder conversation than not knowing. The record should therefore keep the provider's last event verbatim beside our reading of it.

## Open Questions

Retention for the detail records is unresolved and blocks implementation. The re-enable path after suppression is also undecided: whether an address returns on the customer's request, after a clean send on another channel, or only after a bounce-free interval. Each answer makes suppression a different promise.
