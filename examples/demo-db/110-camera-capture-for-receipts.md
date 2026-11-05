---
Name: Camera Capture for Receipts
Owner: Nikhil Shah
Status: Approved
Last Updated: 2026-05-18
---

## Problem

Expense receipts are attached by photographing them and typing the amount, date, and merchant by hand. The typing is where the errors come from, and it is also why people batch a month of receipts into one unpleasant evening rather than capturing as they go.

## Proposal

Capture and extract in one step, with the person confirming rather than typing.

- Guided capture with edge detection and a quality check before accept
- An AI extraction pass returning merchant, date, total, and tax, each with a confidence value
- Low-confidence fields highlighted for confirmation rather than silently accepted
- The image always retained as the record of truth, since the extraction is a convenience

## Scope

Receipt capture in the mobile applications. Bulk import of scanned documents is a separate path.

## Risks

Extraction will be wrong sometimes, and a confirmed-wrong amount is harder to find later than an untyped one, because it carries the appearance of having been checked. Highlighting low confidence helps only if the confidence is calibrated, which we should verify on our own receipt mix rather than trusting the vendor's figures.

## Measurement

Time per receipt from capture to saved, field-level correction rate during confirmation, and expense reports submitted within a week of the expense, which is the behavior change we actually want.

## Data We Have

We hold about four hundred thousand receipt images with a typed amount, date, and merchant beside each one, which is a ready-made calibration set. The typed values are not ground truth, since people mistype and that is the problem this solves, but disagreement between extraction and typing is exactly the set worth reading by hand.

- Roughly a fifth of receipts are shot at an angle or in poor light, which is what the quality check targets
- Receipts from eight merchants account for a third of volume and share a layout
- Tax is absent or illegible on about one in six, so a low-confidence tax field will be common rather than exceptional

## Cost

Extraction is a per-image charge, and the batching behavior means volume arrives in spikes at month end rather than evenly. A spike is cheap to absorb on per-call pricing and expensive on reserved capacity, which argues for per-call even where it costs more in aggregate.

## Failure Modes

The quality check can refuse a receipt that is genuinely the best photograph available, taken on a crumpled slip in a dim restaurant. A capture flow that will not let someone proceed is worse than typing. The check should warn and allow; a poor image then produces low-confidence fields, which the confirmation step already handles.

## Open Questions

Whether a confirmed field should record that it was confirmed is undecided. Storing it makes later audits possible and makes an incorrect confirmation attributable to a person, which will change how people behave at that step in ways nobody has thought through.
