---
Name: Listing Quality Score
Owner: Hana Kobayashi
Status: Draft
Last Updated: 2025-11-25
---

## Problem

Listing quality varies enormously and affects buyer conversion more than price does in our own analysis. Sellers receive no feedback about the quality of what they have published, so poor listings stay poor indefinitely.

## Proposal

A quality score shown to the seller with specific, actionable components.

- Components a seller can act on: image count and resolution, description length, attribute completeness, and response time
- Shown with the specific gap rather than only a number
- Not used in ranking initially, so sellers can improve before it affects them
- Review of whether the components predict conversion before any ranking use

## Scope

Seller-facing feedback. Any use in search ranking is a separate decision with separate consequences.

## Risks

A score that is not used for ranking will be ignored by the sellers who most need it. A score that is used for ranking becomes a target and will be optimized rather than satisfied, with description length padded and images duplicated. Verifying that the components predict conversion before using them is the step that prevents us enforcing our own superstitions.

## Measurement

Score distribution over time, listings improved after feedback, and the relationship between each component and conversion, measured rather than assumed.

## Data We Have

Conversion by listing is already in the warehouse, and so are image count, description length, and attribute fill rate, so three of the four components can be scored historically without any new collection. Response time is the exception: it is recorded only for listings with at least one buyer message, so roughly a third of active listings have no value for it. Scoring those as missing rather than as slow is the honest choice, and it leaves the score incomplete for the quietest sellers.

## Rollout

Scores are calculated for all active listings first and kept internal for four weeks, so the distribution can be examined before any seller sees a number.

- Week five: visible to sellers in the top two listing-volume tiers, who have the staff to act on feedback
- Week eight: visible to every seller, with the per-component gap text
- The component-to-conversion review runs on the week-four internal data, not after launch

## What Would Change Our Mind

If a component moves with conversion historically but shows no conversion improvement when sellers actually fix it, the component is a symptom rather than a cause and comes out of the score. Attribute completeness is the likeliest candidate, since well-run sellers fill in attributes and also do everything else well. If fewer than three components survive that test, the score is not worth showing and plain per-listing warnings are the better form.
