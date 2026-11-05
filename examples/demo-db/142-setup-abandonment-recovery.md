---
Name: Setup Abandonment Recovery
Owner: Felix Braun
Status: Draft
Last Updated: 2026-04-18
---

## Problem

About a quarter of workspaces abandon setup partway: created, one or two steps done, then nothing. We treat them as signups in reporting and as nothing operationally, and most never return.

## Proposal

Detect the abandonment, understand the step it happened at, and offer help specific to that step.

- Abandonment defined as no activity for seventy-two hours with setup incomplete
- A single message referencing the specific step and offering the shortest path through it
- The three most abandoned steps investigated directly, since a pattern suggests a product problem rather than a motivation problem
- No second message; one attempt, then the account joins the dormant population

## Scope

Workspaces in their first two weeks.

## Risks

Recovery messaging treats a product problem as a communication problem. If a step is abandoned by a quarter of people, the message is a workaround and the step needs fixing. The investigation is therefore the more important half of this proposal and should not be dropped if the message tests well.

## Measurement

Setup completion after contact against a holdout, abandonment rate per step before and after the step investigations, and the share of abandoners who return at all.

## Sequencing

The step investigations start before the message, not after it. Ranking abandonment by step takes a week of existing data and no new instrumentation, and whatever the top three turn out to be decides what the message would say. Shipping the message first would be faster and would also make the per-step baseline unreadable, because contacted and uncontacted workspaces stop being comparable at the moment the baseline is needed.

- Week 1: rank abandonment by step, pick the three to investigate
- Weeks 2-4: investigate those steps while the holdout baseline accumulates
- Week 5: the single message goes live, holdout held back

## Alternatives Considered

An in-product prompt shown on return is cheaper, but it only reaches workspaces that come back, which is the population least in need of help. A sequence of three messages over two weeks was rejected: the seventy-two hour definition already selects for people who stopped deliberately, and repeated contact turns a quiet abandonment into an unsubscribe.

## Open Questions

Seventy-two hours is a guess. It is long enough to exclude a weekend pause and short enough that the step is still remembered, but nothing in the data prefers it to forty-eight or ninety-six. What counts as setup complete is also unsettled for workspaces created by an invited member rather than the owner, where the remaining steps may not be theirs to finish.
