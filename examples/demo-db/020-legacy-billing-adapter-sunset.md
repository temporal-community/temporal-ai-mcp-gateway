---
Name: Legacy Billing Adapter Sunset
Owner: Hana Kobayashi
Status: Approved
Last Updated: 2026-07-15
---

## Background

The adapter that bridges the original billing system to the current one has been scheduled for removal three times. Eleven accounts still depend on it, all of them from the first two years of the company, and each has a pricing arrangement that the current model cannot express.

## Proposal

Migrate the eleven accounts individually, then delete the adapter and the system behind it.

- One migration plan per account, written with the account team and agreed with the customer
- Custom arrangements expressed as explicit discounts or credits, not as code paths
- Where the model genuinely cannot express the arrangement, renegotiate rather than rebuild
- Adapter removed the week after the last account moves, with no deprecation period

## Scope

The eleven accounts and the adapter itself. The reporting views that read from the old schema are a separate piece of work and are already owned by the data team.

## Risks

These are long-standing customers with arrangements made by people who no longer work here, and some of those arrangements are more generous than anything we would offer today. Migration surfaces that fact to the customer, which is a commercial conversation the account team must lead and must be ready for before we touch anything.

## Measurement

Accounts migrated, lines of code deleted, and the number of systems in the billing dependency graph, which drops by two.

## Prior Art

Three attempts, each stopping in the same place: the engineering work was planned and the commercial conversation was not. The second reached migration code for two accounts before the account team learned what that migration would reveal about their pricing. The difference now is the order. The commercial conversation comes first and the code is written per account afterwards, which is also why there is no general migration tool in the proposal.

## Sequencing

Account by account, simplest arrangement first, with the two most generous ones last rather than first. Starting on the hardest commercial conversation stalls the whole effort behind a single negotiation, which is roughly what happened the second time. Removing the adapter is one change once the eleventh account has moved, and the reporting views that read the old schema are confirmed migrated before that week, since the data team owns them and their timeline is not ours.

## Open Questions

What happens if an account refuses to move. Renegotiation is the stated path, and a customer who declines both the current model and a renegotiated arrangement leaves the adapter alive for one account, which is the outcome the three previous attempts produced. The second is whether the credits and discounts replacing the custom code paths appear on the customer's invoice, where showing them is honest and also makes an unusually generous arrangement legible to whoever reads it next.
