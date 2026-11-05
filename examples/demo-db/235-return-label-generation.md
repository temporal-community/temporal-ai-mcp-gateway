---
Name: Return Label Generation
Owner: Nikhil Shah
Status: Draft
Last Updated: 2025-12-18
---

## Context

Returns are arranged between buyer and seller by message. The buyer pays for shipping and claims it back, or the seller sends a label by email, or more commonly nothing happens for a week. Returns are the lowest-rated part of our buyer experience by a wide margin.

## Proposal

Generate return labels in the product, with the cost attributed by the return reason.

- A return request flow with reasons that determine who bears the cost
- Labels generated through the carrier interface, downloadable or sent to a collection point
- Tracking visible to both parties, with refund triggered on carrier receipt rather than on seller confirmation
- Seller-not-responding handled by the platform after a deadline rather than left open

## Scope

Our three main carriers in the markets where return services exist.

## Risks

Triggering refunds on carrier receipt rather than seller inspection means refunding before anyone has verified what was returned, which opens an obvious abuse. The policy should differ by item value, with inspection retained above a threshold, and the threshold is a risk decision rather than a product one.

## Measurement

Time from return request to refund, returns abandoned mid-process, buyer satisfaction with returns, and abuse cases detected above and below the inspection threshold.

## Rollout

- One market first, chosen for having all three carriers and the simplest consumer return law
- Reason-based cost attribution live from the start, since it is what sellers will argue about and those arguments are better early
- Refund on carrier receipt limited to low-value items until abuse numbers exist
- The seller deadline enabled last; it is the platform taking a position between two parties and should not be the first thing they meet

## Operational Impact

The platform becomes a party to the return rather than a venue for it. A label we generated and a refund we triggered are decisions we have to defend, and disputes that used to sit between buyer and seller will arrive at support with us already in them. Seller-facing dispute volume will rise before buyer satisfaction does, and the two should not be read in the same month. Label costs also land on us first and are recovered afterwards, which creates a receivable where there was none and a write-off rate nobody has estimated.

## Open Questions

The inspection threshold has no number and no owner. Risk holds the data to set it, product holds the deadline, and the two have not met on it. There is also no answer for a carrier marking a return received when the seller says nothing arrived. The current draft refunds the buyer, which makes the seller carry a carrier's error.
