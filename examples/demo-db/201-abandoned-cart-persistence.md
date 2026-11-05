---
Name: Abandoned Cart Persistence
Owner: Victor Alves
Status: Shipped
Last Updated: 2025-07-17
---

## Background

Carts were held in the browser session and lost on close. For a marketplace where buyers routinely compare over days, this meant rebuilding a cart from memory, and our data showed a large share of multi-item carts never reaching checkout.

## Approach

Persist carts server-side per account, with sensible handling of the things that change.

- Cart contents persisted for thirty days for signed-in buyers
- Items that become unavailable shown as unavailable rather than silently removed
- Price changes flagged at checkout rather than applied invisibly
- Guest carts persisted in local storage with a prompt to sign in to keep them

## Non-goals

No reminder email in this phase, which was deliberately separated so the persistence could be judged on its own.

## Risks

The main risk was price change handling. Showing the old price and charging the new one is a complaint; silently updating is worse. Flagging at checkout with both figures was the least bad option and has generated some confusion but no disputes.

## Outcome

Shipped in June. Multi-item carts reaching checkout are up about nine percent, and the unavailable-item flag appears on roughly a fifth of returning carts, which suggests the previous silent removal was costing us more than we knew.

## Operational Impact

Carts became durable records, which moved them from a session concern to a storage one. Thirty days of contents for every signed-in buyer is a modest table and a non-trivial write rate, since each add and remove now persists instead of living in memory. The unavailable flag also made the catalog's availability field load-bearing where it had not been: a listing marked unavailable in error now shows that way inside a buyer's cart for up to thirty days, where before the item would simply have vanished and been forgotten.

## Review Notes

The guest path drew most of the discussion and shipped as written. Local storage means a guest cart is lost on a second device and survives a browser restart on the first, which is inconsistent and was accepted because the alternative was identifying guests. The prompt to sign in sits at cart view rather than at first add, since prompting on the first add reads as a wall. Nobody has measured how many guest carts are lost to a device switch, and nobody proposed measuring it.

## What Would Change Our Mind

The nine percent is a before-and-after comparison rather than a controlled one, and June carried a promotion. If the figure does not hold through a quiet quarter, the reminder phase that was deliberately held back deserves reconsidering before more effort goes into persistence itself.
