---
Name: Checkout Payment Method Order
Owner: Hana Kobayashi
Status: In Review
Last Updated: 2026-06-26
---

## Context

Payment methods are listed in the same order everywhere: card first, then the alternatives. In three of our markets the alternatives are the dominant method by a wide margin, and burying them below the card form measurably costs us completions there.

## Proposal

Order methods by local prevalence, with the buyer's own history taking precedence.

- Default order per market from payment data rather than from assumption
- The buyer's previously used method first when there is one
- Method availability determined before rendering, so nothing appears and then disappears
- The order reviewed quarterly, since payment behavior shifts faster than our assumptions do

## Scope

Checkout for marketplace orders. Subscription billing has a different method set and its own flow.

## Risks

Ordering by prevalence reinforces prevalence, which makes the measurement self-fulfilling and gradually buries methods that are growing. Reserving a visible position for a rising method, or measuring against a periodic randomized sample, keeps the data honest at a small cost.

## Measurement

Checkout completion rate by market, method mix against market benchmarks, and completion for buyers whose preferred method was not first.

## Dependencies

Resolving availability before rendering is the hard dependency. Today the page renders the full list and each method resolves separately, which is why methods flicker in and out. Resolving first moves those calls ahead of first paint, and two of them are third-party with a ninety-fifth percentile above 400 ms. Either those two get cached availability per market and amount band, or checkout gets slower everywhere to fix a flicker in three markets.

## Failure Modes

A buyer whose history says one method and whose market says another is the case to get right, and history takes precedence here. That is wrong for a buyer who has moved countries: their last method may not be available at all, and promoting an unavailable method to first position is worse than today's fixed order. History should rank only among methods that resolved as available, with an unavailable one dropped rather than shown disabled.

## Review Notes

The three markets are not interchangeable. In two of them one alternative dominates, so the change is a swap of first and second place. In the third the alternatives split across four methods with no leader, and ordering by prevalence puts a method used by under a fifth of buyers at the top. Completion has to be read per market rather than pooled, or the third will be carried by the other two.
