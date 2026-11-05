---
Name: Support Metrics Definitions
Owner: Hugo Takahashi
Status: Draft
Last Updated: 2025-12-28
---

## Problem

Resolution time means three things depending on which report you read: time to first resolution, time to final closure, or time excluding customer wait. Team performance conversations use whichever figure is to hand, which makes them unproductive.

## Proposal

One definition per metric, documented, with the others removed from reporting.

- Six core metrics defined precisely, including what is excluded and why
- Customer wait time excluded consistently, since including it measures the customer
- Definitions in the semantic layer alongside the product metrics, not in a support document
- Old reports retired rather than left alongside the new ones

## Non-goals

No new metrics. We have enough; they just do not mean one thing each.

## Risks

Changing a definition changes the number, and several of these numbers appear in team objectives for the current period. Restating history under the new definitions is necessary so that the change does not look like performance movement, and that restatement needs to land before the definitions do.

## Measurement

Reports using the shared definitions, variance between surfaces for the same metric, and whether performance conversations stop beginning with an argument about the number.

## Interfaces Affected

Four surfaces report resolution time today and none of them read it from the same place.

- The weekly support review deck, built from a scheduled query that computes time to final closure
- The team dashboard, which uses time to first resolution and labels it identically
- The executive summary, which pulls from the review deck and inherits whatever it chose
- The ticket detail view, which shows elapsed time including customer wait

The first three move to the semantic layer definition. The ticket detail view keeps elapsed wall-clock time, because a single ticket is the one place where customer wait is the relevant fact, and it gets a label that says so.

## Migration

Restatement comes first: twenty-four months of history recomputed under the six definitions and published beside the current numbers for one reporting cycle, so each team can see where its number moves and why. Objectives for the current period are reset against the restated baseline. Running both costs a cycle of exactly the ambiguity this is meant to end, so the dual window is capped at one cycle and the old reports are deleted rather than archived.

## Open Questions

- Whether customer wait is dropped from the clock or reported as its own metric, since it explains most slow tickets
- Who owns a definition once it lands, support operations or the semantic layer owner
- What to do with the two metrics that have no clean historical equivalent
