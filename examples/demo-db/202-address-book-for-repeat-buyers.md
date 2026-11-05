---
Name: Address Book for Repeat Buyers
Owner: Ines Duarte
Status: Draft
Last Updated: 2026-07-26
---

## Problem

Buyers retype their address at every checkout. We store it on the order but not on the account, so a returning buyer starts from an empty form, which on mobile is the slowest part of the purchase.

## Proposal

An address book on the account with sensible defaults.

- Addresses saved from orders with the buyer's consent, not automatically
- A default address selectable, with others one tap away
- Validation applied on save rather than at checkout, so the stored set is clean
- Addresses editable and deletable, with changes not affecting past orders

## Scope

Buyer shipping addresses. Billing addresses are held with the payment method and are unaffected.

## Risks

Stored addresses are personal data with a retention obligation, and an address book that outlives the account relationship is a liability. Retention should follow the account's own policy, and deletion must actually delete rather than hide.

## Measurement

Checkout completion time on mobile, repeat purchase conversion, addresses saved per account, and address-related delivery failures, which should fall with validation at save.

## Alternatives Considered

Saving every order address automatically is what most marketplaces ship. It fills the book faster and removes a prompt from checkout, but an address typed once for a gift then sits in the buyer's list forever, and the retention obligation attaches to data the buyer never chose to keep. Consent at save costs a tap and keeps the book to addresses a buyer recognizes. Browser autofill was the other option; it already helps the buyers who use it, but does nothing on the devices where the form is slowest and cannot be validated before checkout.

## Operational Impact

Validation at save moves the failure earlier, which is the point, but it also means a validation outage blocks saving and not just checkout. A save that fails validation should be accepted and marked unverified rather than refused, since a buyer who cannot store an unusual but correct address goes back to retyping it every time.

- Delivery failure investigations gain a per-address history, not a per-order one
- Deletion requests touch a second store, so the account deletion runbook needs a step
- Support can see the book but should not edit it, since edits change nothing on past orders

## Rollout

Mobile web first, where checkout time is worst, then native, then desktop. New addresses only at first: no backfill from historical orders until the consent wording is settled, because a book that arrives pre-filled from old orders is the automatic-save design coming in through the back door.
