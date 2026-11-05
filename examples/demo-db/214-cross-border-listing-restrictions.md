---
Name: Cross-Border Listing Restrictions
Owner: Jonas Keller
Status: Draft
Last Updated: 2026-03-14
---

## Problem

Listings are visible in every market we operate in, regardless of whether the item may lawfully be sold or shipped there. The seller discovers the problem at dispatch, the buyer discovers it at customs, and we discover it when one of them tells us.

## Proposal

Restrict visibility by category and destination from a maintained rule set.

- Rules per category and destination market, covering prohibited and restricted goods
- Listings filtered from search in markets where the item cannot be shipped
- Clear seller-facing explanation of where a listing is visible and why
- Buyer-side messaging when an item is unavailable for their destination rather than silence

## Scope

The categories with known restrictions, which is a minority by volume and most of the problem.

## Risks

The rule set is a compliance artifact that will be incomplete, and incompleteness fails open, allowing listings that should be restricted. Failing closed would hide legitimate listings, which sellers would notice immediately and complain about, whereas failing open produces harm nobody sees until it is serious. That asymmetry argues for conservative rules in the highest-risk categories.

## Measurement

Restricted listings filtered correctly on audit, customs rejections reported, seller complaints about visibility, and categories covered by rules.

## Dependencies

Category assignment on a listing is seller-entered and approximate, which makes it a weak key for a compliance rule. A rule written against a category binds only the listings filed correctly, and the categories most often misfiled are the ones that attract restrictions. Destination is the cleaner input: the buyer's market is known at search time, though the shipping destination is not always that market, and the rules are about the second.

- Category assignment reviewed across the restricted set before rules are written against it
- Search able to filter on buyer market, which it can, and on stated shipping destination, which it cannot today
- A rule store legal can read and amend without a release

## Rollout

The highest-risk categories first and alone, in the two destination markets with the most customs rejections on record. Running narrow makes the first seller complaints readable: a complaint volume that is tolerable across three categories says what fifty will cost, and a silent first month says the rules are matching nothing. Expansion happens per category, each reviewed by legal before it goes live.

## Staffing

Someone owns the rule set, and that person is not an engineer. Rules change when regulation changes, which is unpredictable and frequent enough that routing each change through a release would guarantee the set goes stale. Engineering owns the filtering and the messaging; the standing cost is a named person in compliance with a quarterly review and a path to make an urgent change the same day.
