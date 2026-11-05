---
Name: Buyer Messaging Rate Limits
Owner: Grace Lindqvist
Status: Draft
Last Updated: 2026-01-24
---

## Problem

Buyers can message any seller without limit. A small number of accounts send hundreds of messages a day, mostly price negotiation at volume, and sellers report this as the most tiring part of the platform. We have no limit and no reporting path that leads anywhere.

## Proposal

Sensible limits, a report path with consequences, and seller controls.

- A daily message limit per buyer, set well above normal use
- Per-seller controls: minimum account age, or messages only from buyers with purchase history
- A report path that leads to review and, where warranted, restriction
- Repeat offenders restricted rather than warned indefinitely

## Scope

Buyer-initiated messages before purchase. Order-related messaging is unaffected and should never be limited.

## Risks

Seller-side controls will exclude legitimate new buyers, which is a cost to the marketplace that individual sellers will not feel. Making the controls opt-in and showing sellers the volume they are excluding keeps the decision informed.

## Measurement

Messages per buyer distribution, sellers enabling controls, reports leading to restriction, and new buyer first-purchase rate, watched for the exclusion effect.

## Data We Have

Message volume per buyer is recorded and has never been read as a distribution, which is where the limit has to come from.

- The ninety-ninth percentile buyer sends single-digit messages a day, so the heavy accounts sit orders of magnitude out
- Reports today are a button that files nothing actionable, so the report volume understates the problem
- Purchase history and account age are both available at send time, which is what makes the seller controls cheap

## Support Impact

Restriction is a decision someone makes and defends, which is new work rather than a configuration change.

- A review queue for reports, with the standard of evidence written before the first case rather than after it
- Appeals from restricted buyers, some of whom negotiate at volume and also buy at volume
- Sellers asking why a buyer is still messaging them, where the honest answer is that the limit sits deliberately far above normal use

## Open Questions

What the limit does to a buyer who messages many sellers once each, which resembles nothing in the problem statement and counts the same against a daily total. We have also not decided whether a seller who enables controls sees what was blocked, where showing it makes the exclusion informed and invites them to switch the controls off one message at a time.
