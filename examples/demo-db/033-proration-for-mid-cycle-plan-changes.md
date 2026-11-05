---
Name: Proration for Mid-Cycle Plan Changes
Owner: Priya Raman
Status: Shipped
Last Updated: 2025-11-04
---

## Summary

Customers who upgrade mid-cycle are charged the full new price immediately and credited later, which reads as an overcharge and generates a predictable spike in tickets every billing day.

## Why now

The upgrade flow is the single highest-leverage surface in the self-serve funnel, and the refund-shaped experience at the end of it suppresses conversion measurably. Finance has also asked for proration to be computed in one place, because the current logic is duplicated between checkout and the renewal job and the two have drifted.

## Plan

Compute proration once, in the billing service, and return a preview the client can show before the customer commits.

- A preview endpoint that returns the exact charge, the credit, and the next renewal amount
- Daily granularity, with the convention documented for the edge cases around month ends
- Downgrades hold until the period boundary rather than issuing cash back
- The renewal job calls the same code path as checkout

## Risks

Changing proration changes revenue recognition, so finance has to sign off on the convention before anything ships. The month-end cases are genuinely ambiguous: a plan change on the thirty-first of a month has no clean counterpart in February, and whichever rule we pick will look wrong to somebody.

## Metrics

Upgrade completion rate, tickets tagged as billing confusion within three days of a plan change, and the gap between previewed and charged amounts, which should be zero.

## Interfaces Affected

The preview endpoint is new and exposed to our own clients only. Its shape is the charge, the credit, the next renewal amount, and the effective date the convention resolved to. Checkout stops computing proration locally and calls it. The renewal job loses its copy of the logic and calls the same path, which changes nothing a customer sees but does change what the job writes to its log, so the reconciliation query finance runs against that log has to change in the same release. Invoices gain a line that names the credit instead of folding it into the subtotal.

## Migration

Plan changes already in flight at the cutover are the awkward case.

- Changes applied before the cutover keep the old credit, which finance has already recognized
- No backfill of past periods; the old convention stands for anything already invoiced
- The duplicated logic in the renewal job is deleted one release after the shared path proves out, not in the same one

## Review Notes

Finance accepted daily granularity and the rule that clamps a plan change to the last day of the shorter month, on the condition that the convention appears on the invoice and not only in the preview. The point left open is the downgrade hold: holding to the period boundary is right for revenue recognition and reads as a delay to the customer, so the flow has to say when the lower price starts rather than confirm a change that appears not to happen.
