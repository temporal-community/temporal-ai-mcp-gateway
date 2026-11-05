---
Name: Search Ranking for Listings
Owner: Dmitri Volkov
Status: In Review
Last Updated: 2026-03-06
---

## Context

Listing search ranks by text relevance and recency. It ignores whether a listing converts, whether the seller responds, and whether the item is in stock, all of which we know. Buyers complain about dead listings at the top of results, and they are right to.

## Proposal

Add behavioral and availability signals to ranking, with guardrails against runaway concentration.

- Availability as a hard filter rather than a ranking signal, since an unavailable item is never the right answer
- Conversion rate and seller responsiveness as ranking signals, normalized by category
- An exploration allowance so new listings get impressions before they have a history
- Ranking changes evaluated on buyer outcomes, not on click-through alone

## Scope

Listing search. Category browse and recommendations are separate surfaces.

## Risks

Ranking on conversion concentrates traffic on established sellers and starves new ones, which degrades the marketplace over time in a way that is slow and hard to see. The exploration allowance is the countermeasure and needs to be large enough to matter, which will cost measurable conversion in the short term.

## Measurement

Buyer outcomes including returns and disputes, not just conversion, impression distribution across seller tenure, and new seller time to first sale.

## Data We Have

The inputs exist already and differ sharply in quality.

- Stock state is recorded per listing and is as current as the seller keeps it, which in some categories means daily and in others means never
- Conversion per listing is reliable only above a volume floor that most of the long tail never reaches
- Seller responsiveness is computed for the seller metrics and can be reused rather than defined again
- Returns and disputes sit on the order and are the slowest signal, arriving weeks after the impression that caused them

That volume floor is why normalization is by category: a listing with four sales in a thin category is not comparable to one with four in a dense one.

## Rollout

Availability filtering first and on its own. It is the change buyers asked for, it needs no model, and it moves the top of results enough that shipping it beside the behavioral signals would make both unreadable. Conversion and responsiveness follow behind a holdout, with the exploration allowance set from the first day rather than added once concentration shows, because by then the distribution has already moved.

## What Would Change Our Mind

If impression distribution across seller tenure narrows despite the allowance, the allowance is too small, and the ranking weight comes down rather than exploration going up. The other signal is returns. A result set that lifts sales and lifts returns with them is not better, and that is the reason this is judged on buyer outcomes rather than click-through.
