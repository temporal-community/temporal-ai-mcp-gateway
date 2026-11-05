---
Name: Purchase Order Billing for Enterprise
Owner: Hugo Takahashi
Status: In Review
Last Updated: 2026-02-18
---

## Problem

Enterprise customers pay against purchase orders, and we have no concept of one. The number is pasted into a note field, finance copies it onto the invoice by hand, and when it is wrong the invoice is rejected by the customer's procurement system without reaching a human who could fix it.

## Proposal

Model the purchase order properly and validate against it.

- A purchase order object with a number, a value, a validity window, and a remaining balance
- Invoices reference it and cannot exceed the remaining balance without an override
- Expiry warnings to the account team thirty days out
- The number printed in the field procurement systems actually read

## Scope

Invoiced accounts only. Nothing about card-paid subscriptions changes.

## Risks

Blocking an invoice because a purchase order is exhausted is correct behavior that will, the first time it happens at quarter end, look like us refusing money. The override exists for that reason and should be logged rather than discouraged.

## Measurement

Invoices rejected by customer procurement, days sales outstanding on invoiced accounts, and the share of invoices carrying a validated reference, which starts near zero.

## Migration

Every invoiced account carries a number somewhere in a note field, in no consistent format. Parsing those gives a number but no value, window, or balance, and an object missing three of its four fields validates nothing. Accounts get a real object only when the account team enters one, so coverage grows account by account rather than arriving at a cutover.

- Existing note-field numbers carried over as unvalidated references, marked as such
- Validation applied only where a complete object exists
- The note field kept readable for a year, since finance reconciles older invoices against it

## Operational Impact

Finance stops copying numbers and starts maintaining objects, which is less work only if the account team enters them. If it falls to finance by default this moves the manual step rather than removing it, and days sales outstanding will not move either. The thirty-day expiry warning goes to the account team for the same reason: they are the ones who can ask the customer for a new purchase order.

## Timeline

The object and the invoice reference ship together; there is no useful half of that. The override and its log ship in the same release, because the first blocked invoice will arrive within days of the block existing, and an override added afterwards is an incident. Expiry warnings can follow a release later, since nothing depends on them until validity windows are populated.
