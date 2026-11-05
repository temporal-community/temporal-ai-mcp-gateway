---
Name: Semantic Layer for Core Metrics
Owner: Nikhil Shah
Status: In Review
Last Updated: 2026-03-23
---

## Problem

Active accounts is defined four times: once in the executive dashboard, once in the growth model, once in the billing reconciliation, and once in a notebook that several people have copied. The four definitions produce numbers that differ by up to eight percent, and every quarter somebody spends a week finding out why.

## Proposal

Define core metrics once in a semantic layer and make every consumer resolve through it.

- Twelve core metrics to start, each with a written definition and a named owner
- Dimensional slicing handled by the layer rather than by each consumer
- Definition changes versioned, with the change log visible in the product
- Dashboards migrated one at a time, with the old number shown alongside until they agree

## Non-goals

No attempt to cover every metric. The long tail belongs to the teams that use it, and forcing it through a central layer would make the layer the bottleneck it is meant to remove.

## Risks

The migration period, where two numbers are visible, is uncomfortable and will be read as the layer being wrong. It needs a clear communication plan and a firm end date, or the parallel period becomes permanent.

## Measurement

Dashboards resolving core metrics through the layer, instances of the same metric differing across surfaces, and the time spent reconciling definitions each quarter.

## Migration

The notebook copies are the hard part, because they are not a surface anyone owns. A dashboard can be migrated by its owner; a copied notebook has no owner and keeps producing the old number long after the dashboards agree.

- Dashboards first, in descending order of audience, each with a stated four-week parallel window
- Billing reconciliation last, since an auditor reads it and the parallel period there needs a written explanation
- Notebooks handled by deprecating the underlying tables rather than by asking people to update, because the tables are the only lever that reaches a copy

## Staffing

Twelve definitions is three weeks of writing and about three months of arguing, and the arguing is the work. Each one needs an owner who can say no, and four of the twelve cross team boundaries where no such person exists today. One analyst can hold the layer itself; what the definitions need is a decision-maker per metric and a standing forum to settle the contested four.

## Open Questions

- Whether the eight percent spread on active accounts resolves to one correct definition or to two legitimate ones that need different names
- What happens to a dashboard whose owner declines to migrate, given the non-goal of making the layer a bottleneck
- Whether the layer serves product surfaces that read metrics or only analytical consumers
- How long the old tables stay queryable once a dashboard has migrated
