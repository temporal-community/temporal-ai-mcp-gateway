---
Name: Shipping Rate Calculation
Owner: Priya Raman
Status: In Review
Last Updated: 2026-04-09
---

## Problem

Shipping cost is entered by the seller as a flat figure per listing. It is frequently wrong for distant destinations, which sellers absorb or dispute afterwards, and it makes the checkout total unpredictable for buyers in smaller markets.

## Proposal

Calculate from dimensions and destination through the carrier interfaces.

- Package dimensions and weight captured at listing time, with templates for repeat items
- Rates from the carrier at checkout for the buyer's actual address
- Seller-configured handling fee added transparently rather than hidden in the rate
- Flat rate retained as an option for sellers who prefer it, clearly labeled

## Scope

The three carriers covering most of our volume. Other carriers keep flat rates.

## Risks

Carrier interfaces are slow and occasionally unavailable, and a checkout that waits on an external call will lose orders. A cached rate table per corridor as a fallback is necessary, with the live call as the preferred path and a timeout that favors completing the purchase.

## Measurement

Checkout completion with calculated rates against flat rates, shipping cost disputes, seller absorption of underquoted shipping, and checkout latency.

## Rollout

Dimension capture ships first and stays optional for a full listing cycle. A listing without dimensions cannot be quoted, and a flat-rate listing is better than a blocked one. Calculated rates turn on per corridor once the cached table for that corridor has two weeks of carrier quotes behind it.

- Dimensions optional at listing, with templates offered on the second listing of a similar item
- Calculated rates enabled on domestic corridors first, where the cache is densest
- Cross-border corridors last, since quotes vary most there and the fallback is least trustworthy

## Failure Modes

The cached fallback is the dangerous path, not the live call. A stale corridor rate quotes low, the buyer pays it, and the seller absorbs the difference silently, which is the failure this change exists to remove. Cache entries carry their quote date, entries older than thirty days are not served, and a corridor with no fresh entry falls back to the seller's flat rate rather than to a guess.

## Support Impact

Disputes will change shape rather than disappear. A seller who disagrees with a calculated rate has no field to edit, so the dispute arrives as a complaint that the rate is wrong with no obvious resolution path. Support needs the quote record attached to the order before this goes wide: carrier, corridor, dimensions used, and whether the figure came from the live call or the cache.
