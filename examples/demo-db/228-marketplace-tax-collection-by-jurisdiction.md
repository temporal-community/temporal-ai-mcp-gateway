---
Name: Marketplace Tax Collection by Jurisdiction
Owner: Hugo Takahashi
Status: In Review
Last Updated: 2026-02-25
---

## Context

In several jurisdictions the marketplace is now the party obliged to collect and remit tax on behalf of sellers. We currently do this in two and are out of step in at least four others, which is a compliance exposure rather than a product gap.

## Proposal

Collect and remit where we are obliged, with the obligation determined by rule rather than by case.

- A jurisdiction rule table maintained with external tax counsel, reviewed quarterly
- Collection at checkout with the tax shown separately from the item price
- Remittance reporting per jurisdiction in the format each requires
- Seller-facing documentation of what we collect on their behalf and what remains theirs

## Scope

Jurisdictions where marketplace liability applies to our categories. Seller-collected tax elsewhere is unchanged.

## Risks

The rule table is the compliance artifact and its maintenance is the ongoing obligation, not the implementation. A rule that goes stale produces under-collection that compounds silently until an authority notices. The quarterly review needs a named owner outside engineering.

## Measurement

Jurisdictions in compliance against the obligation list, collection accuracy sampled against counsel review, and seller contacts about tax handling.

## Dependencies

External tax counsel owns the rule table's content. Engineering owns its shape and the checkout code that reads it. The remittance formats differ per jurisdiction, so the reporting work cannot start until counsel has confirmed which four jurisdictions we are out of step in and what each one requires.

- A versioned rule table with an effective date per row, so a rate change does not retroactively alter past orders
- Checkout line-item support for a separately displayed tax amount
- Per-jurisdiction report generation in each required format
- Seller documentation published before the first jurisdiction switches on

## Rollout

One jurisdiction at a time, starting with the one carrying the largest exposure. Each switch-on waits a full remittance cycle before the next begins, which makes the rollout slower than the compliance timeline would like but means a format error surfaces against one jurisdiction rather than five.

## Operational Impact

The quarterly review becomes a recurring obligation with a date, a named owner, and a written record of what counsel confirmed. Sellers in a switched-on jurisdiction will contact support about amounts they used to collect themselves, so support needs the per-jurisdiction split documented before each switch-on rather than after.
