---
Name: Self-Serve Refunds for Sellers
Owner: Tom Okafor
Status: In Review
Last Updated: 2026-03-02
---

## Context

Sellers cannot issue refunds themselves. Every refund goes through a support ticket, which means a median of nineteen hours between a buyer asking and a seller being able to say yes. Refund tickets are now the second largest queue by volume and the least interesting work the team does.

## Proposal

Give sellers a refund control in the order detail view, bounded by policy rather than by a human reviewer.

- Full and partial refunds within ninety days of the order
- A per-seller rolling cap, raised automatically as account history accumulates
- Refunds above the cap, or on orders flagged by risk, still route to review
- The buyer gets the same notification regardless of which path issued it

## Non-goals

No change to who bears the processing fee, no change to the dispute flow, and no bulk refund tooling in this phase.

## Risks

The obvious one is abuse: a seller refunding fraudulently to move money. The cap plus the risk flags cover the patterns we have seen, but we should expect to find at least one we have not. Less obvious is that faster refunds may increase refund volume outright, because the friction was doing work we were not accounting for.

## Success metrics

Median time from buyer request to refund issued, refund ticket volume, and dispute rate on refunded orders as a guardrail.

## Rollout

- Enabled first for sellers with twelve months of history and no risk flags, about a third of active sellers and a smaller share of refund volume
- Cap starting low and raised on account history, with the schedule published so sellers can see what raises it
- Risk flags evaluated at refund time rather than nightly, since the abuse case is fast
- Refund tickets from enabled sellers watched weekly; if they do not fall to near zero, the control is not findable

## Interfaces Affected

The refund control lives in order detail, which renders from a read model that does not carry the seller's remaining cap. A cap that is stale by minutes would let a seller start a refund that then fails, so it is fetched live when the control opens rather than read with the page. Issuance goes through the same path support uses, with the actor recorded as the seller, so the ledger and the buyer notification need no separate case.

## Open Questions

What happens to the cap after a dispute is undecided. A seller whose refunded order is later disputed has shown us something, but the current rule only ever raises the cap, and a one-way ratchet is the wrong shape for a risk control. There is also no agreed definition of the refund-volume increase that would count as the friction effect rather than as faster service.
