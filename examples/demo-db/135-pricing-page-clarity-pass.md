---
Name: Pricing Page Clarity Pass
Owner: Ben Tsai
Status: Draft
Last Updated: 2025-12-30
---

## Background

The pricing page lists nineteen feature rows across four plans. Session recordings show people scrolling the comparison table repeatedly, and the most common support question before purchase is a variation of which plan they need.

## Proposal

Lead with a recommendation shaped by a few questions, and keep the full table below for those who want it.

- Three questions: team size, primary use, and whether single sign-on is required
- A recommended plan with the two or three reasons it was recommended
- The full comparison table retained, unchanged, below the recommendation
- Feature rows rewritten in customer vocabulary, with internal names removed

## Non-goals

No change to the plans or to pricing, both of which are out of scope for this work and are owned elsewhere.

## Risks

A recommendation that points people to a cheaper plan than they need produces a worse experience and a later upgrade conversation; one that over-recommends is a trust problem. The question set should be tested against what customers actually ended up on, not against what we would prefer to sell.

## Measurement

Pre-purchase support questions about plan choice, plan selection distribution, and the rate of plan changes within sixty days of purchase, which indicates a bad initial fit.

## Alternatives Considered

Cutting the table down to the rows that actually differ between plans was the first idea, and it is still worth doing inside this work. On its own it leaves the question unanswered, since a shorter table is quicker to read and no easier to decide from. A guided flow ending in checkout rather than in a recommendation was rejected because it hides the comparison from the people the session recordings show using it. A chat prompt on the page moves the question to support instead of answering it.

## Rollout

The recommendation goes to a fraction of traffic against the current page, because the measure that matters is the sixty-day plan change rate and it only arrives two months later. The rewritten feature rows ship to everyone at once: removing internal names is a correction rather than a test, and they stand on their own if the recommendation is held back.

## Open Questions

Whether single sign-on belongs among the three questions. It splits the plans cleanly, which is why it is there, and it is also a question most small teams cannot answer about themselves, so it can push someone onto a plan for a reason they did not follow. The second is what the recommendation does when the three answers point at different plans, where choosing the higher one is safer for us and is exactly the over-recommendation the risks section warns about.
