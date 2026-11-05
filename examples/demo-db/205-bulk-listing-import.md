---
Name: Bulk Listing Import
Owner: Sofia Marchetti
Status: Draft
Last Updated: 2025-10-31
---

## Background

Sellers with large catalogs create listings one at a time. Several have told us this is why they list a subset of their inventory with us and their full catalog elsewhere. The template import we offer is undocumented, silently drops rows, and is not mentioned anywhere in the seller interface.

## Proposal

A proper import with validation, preview, and error reporting.

- A documented file format with a downloadable template per category
- Validation before import with a row-level error report, not a single failure
- Preview of what will be created or changed, with confirmation before commit
- Update as well as create, matched on the seller's own item reference

## Scope

Listing data and images by reference. Inventory quantity is handled by the sync work.

## Risks

Bulk update matched on a seller-supplied reference will, when the reference is ambiguous, update the wrong listing at scale. The preview is the safeguard and it must be read rather than clicked through, which argues for showing the count of changes prominently and requiring explicit confirmation above a threshold.

## Measurement

Sellers using import, listings created or updated through it, error rate per import, and catalog coverage for sellers who also sell elsewhere.

## Prior Art

The existing template import is the prior art, and its failure is instructive. Dropping rows silently means a seller believes their catalog is complete and finds out otherwise when a buyer asks for something that was never listed. No seller has reported it as a bug, which tells us the failure is invisible rather than rare. The replacement should treat silence as the thing to design against, which is what the row-level report is for, and the old path should be removed rather than left running beside the new one with different behaviour.

## Rollback

A bad import needs an undo, not a way to turn the feature off. Each import should be one reversible unit: the listings it created can be removed and the ones it changed restored to their previous values, for some window, from the import's own record. Without that, recovery from a wrong bulk update is support making the same edits by hand at exactly the scale that made import attractive in the first place.

## Support Impact

These failures will not arrive labeled as import problems. They arrive as listings being wrong, so support needs to see which import last touched a given listing and what it changed, from the listing itself. The confirmation threshold will also produce requests to raise it for the largest sellers, who are the ones this is built for and the ones a mistaken import hurts most. The answer to that request should be written down before the first seller asks.
