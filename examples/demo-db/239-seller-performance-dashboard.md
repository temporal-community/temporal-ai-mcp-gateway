---
Name: Seller Performance Dashboard
Owner: Ruth Adeyemi
Status: Draft
Last Updated: 2026-04-05
---

## Context

Sellers are measured on dispute rate, response time, and cancellation rate, and are penalized when they breach thresholds. They cannot see any of these numbers until a warning arrives, which makes the system feel arbitrary and is a frequent complaint in our seller survey.

## Proposal

Show sellers their own numbers, continuously, with the threshold visible.

- The three measured metrics shown with the threshold and the current value
- Trailing window stated explicitly, since sellers reasonably assume the wrong one
- The specific orders contributing to a breach listed, not just the aggregate
- A warning state before the threshold rather than at it

## Non-goals

No change to the thresholds or to the consequences.

## Risks

Showing the contributing orders invites disputes about individual cases, which is a support cost we do not currently carry. It is also the only way a seller can actually act on the number, and refusing the detail while enforcing the consequence is not defensible.

## Measurement

Sellers viewing the dashboard, breaches preceded by a warning state, disputes about individual contributing orders, and whether metrics improve after the warning.

## Prior Art

Marketplaces that enforce seller thresholds eventually publish them, and the ones that publish an aggregate without the contributing orders collect the same complaint we collect now in a different form: visible and still unactionable. The internal precedent is the support quality scorecard, which showed people a score before it showed them the sampled tickets behind it, and the first quarter of that was spent arguing about the score rather than the tickets.

## Data We Have

All three metrics are already computed for enforcement, which is what makes this mostly a surfacing problem.

- Dispute rate and cancellation rate are computed nightly over a trailing ninety days
- Response time is averaged per message, with no per-order value kept
- The contributing orders are implicit in the enforcement query and have never been stored

Response time is the awkward one. Showing a seller which orders pulled the average down means keeping a per-order value we currently discard.

## Open Questions

Where the warning state sits, and whether it is the same distance below every threshold. A fixed margin is simple and arrives too late on a metric that moves quickly. We have also not settled what a seller sees in their first ninety days, when the trailing window is partial and two disputes read as a rate far above any threshold.
