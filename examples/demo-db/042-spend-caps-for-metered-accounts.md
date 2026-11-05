---
Name: Spend Caps for Metered Accounts
Owner: Caleb Mortensen
Status: Draft
Last Updated: 2025-10-30
---

## Context

Metered products have no ceiling. A runaway integration can generate a five-figure invoice overnight, and when it does we almost always forgive it, which means the risk is ours and we are carrying it without measuring it.

## Proposal

Let accounts set a monthly spend cap, and act on it.

- A default soft cap for new accounts, set well above typical usage
- Notification at fifty, eighty, and one hundred percent of cap
- At the cap, metered features degrade to a documented limited mode rather than stopping dead
- Raising the cap is self-serve and takes effect immediately

## Non-goals

No per-feature caps, no shared caps across accounts in an organization, and no hard stop on anything that would cause data loss.

## Risks

A cap that stops a production workload is worse for the customer than an unexpected invoice, which is why the degraded mode matters more than the cap itself. Getting that mode wrong for even one product turns this from a safety feature into an outage we caused.

## Measurement

Accounts with a cap set, forgiven invoice value per quarter, and support contacts about unexpected charges, all three of which should fall together.

## Interfaces Affected

Every metered product has to define and document its limited mode before the cap can be enforced against it, and that definition belongs to the product team rather than to billing. Until a product has one, its meters count toward the cap but do not degrade at it.

- Billing settings gains a cap field, a usage-against-cap reading, and a raise control
- The metering pipeline emits threshold events at fifty, eighty, and one hundred percent
- Each metered surface documents what its limited mode does and what it stops doing

## Failure Modes

The threshold notifications are only useful if they reach someone who can raise the cap, and the billing contact on an account is often not the engineer whose integration is generating the usage. A notification that lands in a finance mailbox at midnight produces a cap hit nobody saw coming.

Usage is aggregated on a delay, so an account can cross its cap before the eighty percent notice is sent. Accepting the delay keeps the meter cheap; the cost is that a fast enough runaway skips its warnings entirely.

## Rollout

New accounts receive the default soft cap first, since they have no usage history to contradict it. Existing accounts are offered a cap set from their trailing three-month peak rather than having one applied, because a cap imposed on live usage is the outage the Risks section warns about.
