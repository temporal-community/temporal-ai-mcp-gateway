---
Name: Marketplace Fee Transparency
Owner: Omar Haddad
Status: In Review
Last Updated: 2026-06-20
---

## Context

Sellers see the net payout and work backwards to the fees. The fee schedule is published but spread across three help articles, and the figure includes components that vary by category and by payment method. Sellers consistently misestimate their own margins, which they discover at month end.

## Proposal

Show the fee breakdown at listing time and on every transaction.

- An estimate at listing creation, given the price and category, with each component named
- The actual breakdown on each order, reconciling exactly to the payout
- A monthly statement summarizing fees by component
- One published schedule replacing the three articles

## Non-goals

No change to the fees themselves, which is a pricing decision.

## Risks

Making fees legible will cause sellers to notice components they had not registered, particularly the payment processing and promoted listing elements, and some of them will price accordingly or leave. That is the honest outcome, and it is better learned now than through a gradual erosion we cannot explain.

## Measurement

Seller contacts about fees, variance between estimated and actual fees, listing price adjustments following launch, and seller retention.

## Interfaces Affected

- Listing creation, which gains an estimate that has to recompute as the seller edits the price or changes category, and has to say plainly that it is an estimate
- The order detail view, where the breakdown must reconcile to the payout to the cent or it is worse than showing nothing
- The monthly statement, which is a new document and therefore a new thing to be wrong in front of an accountant
- The payouts export, since a seller reconciling by hand will compare the export against the statement and expect identical component names

## Sequencing

The published schedule goes first and goes alone. Consolidating three help articles into one page is cheap, it is the piece most likely to be wrong today, and it establishes the component names everything else has to use. Per-order breakdowns follow, then the listing estimate, then the statement. Shipping the estimate before the actual breakdown would invite the comparison without supplying the second number.

## Support Impact

Fee contacts rise before they fall. Components a seller had not registered become visible at the moment they are deciding a price, and the first month of questions will be about promoted listings and payment processing specifically. Support needs the component definitions and the category variations in front of them on day one, not the help article. The guardrail is that a question becomes answerable in one reply rather than requiring someone to reconstruct a payout.
