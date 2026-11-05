---
Name: Wallet Top-Up Flow
Owner: Ines Duarte
Status: Parked
Last Updated: 2025-09-09
---

## Background

Two markets have meaningful card decline rates driven by low issuer approval for recurring foreign charges. Prepaid balance is the normal pattern in both, and we do not support it, so customers in those markets churn at roughly twice the rate of comparable accounts elsewhere.

## Proposal

A stored balance that customers top up on their own schedule and that charges draw down.

- Top-up by card or local method, with the local method taking priority in the interface
- Automatic top-up at a threshold, opt-in and clearly disclosed
- Balance expiry governed by the stricter of local rules and our policy
- Refund of remaining balance on request, within the rules of the originating method

## Scope

Two markets, one local method each, no transfers between accounts.

## Risks

Stored balance is regulated differently in each market and the obligations attach to us, not the processor. Legal review is a gate, not a parallel track, and this is parked until that review lands. There is also a real possibility that the right answer is a local acquirer rather than a wallet, which would make this work unnecessary.

## Measurement

If it proceeds: charge success rate in the two markets, churn against the comparable cohort, and balance held, which is a liability and should be watched as one.

## Alternatives Considered

- A local acquirer in each market, which removes the regulatory exposure rather than managing it, at the price of two more processor integrations and a contracting cycle measured in quarters
- Per-issuer retry schedules, cheap and already worth a few points of the decline rate, but powerless against an issuer that declines recurring foreign charges as policy
- Annual billing in both markets, which cuts the number of declinable charges from twelve to one and asks for a large single payment in markets where prepaid is normal precisely because large payments are not

## Operational Impact

Held balance is a liability, which pulls finance into month-end reporting on it, an expiry process they have to run, and a refund path they have to own rather than hand to support. Each market has its own rules about unclaimed balance, so the two markets will not share one process no matter how similar the product looks. Support also inherits a question they have never been asked here: where the money went, with an answer that involves a balance rather than a card statement.

## Open Questions

Whether automatic top-up at a threshold satisfies the disclosure rules in both markets, which the legal review should settle before any interface is designed around it. Also unresolved: what happens to a positive balance on an account that closes and a customer who cannot be reached. That case is rare, it is the one a regulator asks about, and nothing in the proposal addresses it yet.
