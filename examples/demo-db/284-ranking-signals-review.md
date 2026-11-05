---
Name: Ranking Signals Review
Owner: Erin Vasquez
Status: Draft
Last Updated: 2025-10-18
---

## Background

The ranking formula has eleven signals with weights that were set by hand three years ago and adjusted twice since, both times to fix a specific complaint. Nobody can explain why the weights are what they are, and we have no offline evaluation to tell us whether a change helps.

## Proposal

Build the evaluation first, then revisit the weights.

- A judged query set covering the common intents, built with people who use the product
- Offline evaluation running against the judged set on every ranking change
- Weights revisited only once the evaluation exists and is trusted
- Online testing reserved for changes that pass offline, not as the first measurement

## Scope

Workspace content ranking. Listing search in the marketplace has its own signals and its own team.

## Risks

A judged set reflects the judgments of the people who built it and ages as the product changes. It will be most wrong for the newest content types, which are the ones most likely to be ranked badly. Refreshing it annually is part of the proposal rather than an aspiration.

## Measurement

Judged set coverage of query intents, offline evaluation scores across ranking changes, and agreement between offline predictions and online results.

## Staffing

The judged set is the part that cannot be bought with engineering time. Covering the common intents at usable depth means roughly 400 queries with five judged results each, and the judging has to come from people who use the product rather than from the ranking team, who know what the system returns today and will reward it. Two days a week from three product specialists for six weeks is the shape of it, committed before the engineering work starts rather than found afterwards.

## Prior Art

Both previous weight adjustments were made the same way: a complaint arrived, a signal was turned up until the complaint stopped, and nothing else was checked. Neither change recorded what it cost elsewhere in the results, which is why the eleven weights are now unexplainable. The offline evaluation exists to make that trade visible, not to prevent weight changes.

## Timeline

Nothing about the weights moves this quarter. Building and judging the set takes most of it, and the first useful output is a baseline score for the current ranking, which says how bad the starting point is. Weight work follows only once the evaluation has predicted an online result correctly at least once. Until then it is a number nobody has reason to believe.
