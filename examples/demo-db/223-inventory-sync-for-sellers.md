---
Name: Inventory Sync for Sellers
Owner: Tom Okafor
Status: Draft
Last Updated: 2025-08-22
---

## Background

Sellers who also sell elsewhere update stock levels by hand on each platform. The result is oversold items, which we handle as cancellations, which damage the seller's standing with us for a problem our lack of integration caused.

## Proposal

An inventory interface and integrations with the two platforms most of our sellers also use.

- A stock level interface with webhooks in both directions
- Prebuilt integrations with the two most common platforms, configured by the seller
- A reservation window at checkout so concurrent purchases cannot oversell
- Oversell incidents attributed to sync failure excluded from seller performance

## Scope

Stock quantity. Price synchronization is a commercial decision with different implications.

## Risks

Two-way sync has a conflict problem: the same item sold on both platforms within seconds. Reservation reduces the window but cannot eliminate it, and the policy for who wins needs to be explicit and in the seller's favor where possible, since the alternative is penalizing them for physics.

## Measurement

Oversold orders per thousand, sellers with sync configured, time from external sale to stock reflected here, and cancellations attributed to stock.

## Rollout

The interface and the webhooks go first, usable by the handful of sellers who have their own development capacity and who will find the edge cases cheaply and describe them precisely. Prebuilt integrations follow one platform at a time rather than both at once, since each has its own rate limits and its own idea of what a stock update means. The reservation window ships with the first integration rather than after it: without reservation, integration makes overselling faster instead of rarer, because stock is now moving automatically on both sides.

## Dependencies

- Rate limits on both external platforms, which decide how quickly a sale here reaches there and therefore the real width of the conflict window
- A stable item reference shared between the two systems, which sellers maintain themselves today with uneven discipline
- The seller performance calculation, which has to accept an exclusion reason it does not currently carry
- Checkout, which must hold a reservation and release it reliably when a basket is abandoned

## What Would Change Our Mind

If an external platform's rate limits keep the conflict window wide no matter how the sync is built, the honest product is a buffer: hold a unit or two back from the published count for sellers who sync, and tell them plainly that is what we do. That trades some sales for far fewer cancellations, and it is a decision for the sellers rather than one to make quietly on their behalf.
