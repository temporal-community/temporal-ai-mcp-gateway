---
Name: Gift Options at Checkout
Owner: Caleb Mortensen
Status: Parked
Last Updated: 2025-09-29
---

## Background

Buyers ask sellers to omit the invoice or include a message, by message, after ordering. Sellers comply inconsistently, and the request arrives after packing often enough to be useless. The volume is seasonal and concentrated.

## Proposal

Structured gift options at checkout, passed to the seller with the order.

- A gift flag suppressing price on any included documentation
- An optional message passed to the seller, with length limits and moderation
- Shipping to an address other than the billing address, which currently triggers risk checks
- Seller opt-in, since fulfillment practices vary

## Scope

Physical goods from opted-in sellers.

## Risks

Gift shipping to a different address is also the signature of card fraud, and the risk checks exist for good reason. Relaxing them for a gift flag would be straightforwardly exploitable, so the right approach is to improve the risk signal rather than to add a bypass.

Parked pending the risk team's view, without which the main buyer-facing benefit cannot ship.

## Measurement

If it proceeds: gift orders as a share of seasonal volume, seller opt-in rate, post-order messages requesting gift handling, and fraud rate on gift-flagged orders.

## What Would Change Our Mind

The parked state rests entirely on the different-address problem. If the risk team can show that a gift flag combined with account tenure and order history separates gift orders from card testing well enough to hold the current fraud rate, the rest of the proposal is small work and should proceed. A second route is dropping different-address shipping from the first version and shipping only the suppressed price and the message, which leaves the seasonal post-order message volume largely untouched but proves seller opt-in is achievable.

## Dependencies

- A risk signal that treats the gift flag as input rather than as an exemption
- Moderation capacity for messages at seasonal peak, not at average volume
- Packing documentation templates that can render without price, per seller integration

Seller fulfillment runs through three integration paths, and only the hosted one controls what the packing slip prints. The other two hand documentation generation to the seller, so the gift flag reaches them as a field they may ignore.

## Open Questions

Whether a buyer sees that a seller has not opted in before placing the order, or only after, is unsettled, and showing it at the item level means surfacing a seller capability in the browse experience for a seasonal feature.
