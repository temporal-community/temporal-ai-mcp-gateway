---
Name: Cohort Retention Reporting
Owner: Dmitri Volkov
Status: Approved
Last Updated: 2026-07-13
---

## Context

Retention is reported as a single curve for all accounts, which blends self-serve and enterprise and therefore describes neither. Teams rebuild cohorted versions in notebooks, and there are currently at least five such notebooks with different cohort definitions.

## Proposal

First-class cohort retention in the analytics product, with the definitions centralized.

- Cohorts by signup period, plan, acquisition channel, and region, combinable
- Retention measured on a defined activity event rather than on subscription state
- An AI assistant that reads the resulting curves and drafts a short written readout, with every claim linked to the chart it came from
- Notebook versions deprecated once the product version covers their cases

## Scope

Account-level retention. Seat-level and feature-level retention are different questions and would need their own models.

## Risks

The drafted readout is where this could mislead. A plausible narrative over a noisy curve is worse than no narrative, because it travels further. The draft should state the sample size and the confidence interval before its conclusion, and nobody should circulate one without reading the chart.

## Measurement

Teams using the product version, notebook cohort models retired, and consistency of reported retention across surfaces, which is the actual goal.

## Migration

The five notebooks do not retire by being superseded. Someone has to confirm each one's cases are covered and then delete it, and the author of a notebook is rarely motivated to delete it. The workable sequence is to reproduce each notebook's cohort definition in the product, show the author both curves side by side, and settle in that conversation whether a difference is a definition gap or a defect.

- Each notebook's cohort definition reproduced and compared curve to curve
- Differences resolved as a definition gap or a defect, never left as both
- The notebook deleted by its author, with the product view linked where it lived

## Data We Have

The activity event this measures on has been instrumented and stable for two years, which is longer than the subscription history is trustworthy: plan records were restructured eighteen months ago and the older rows do not reconstruct cleanly. That bounds how far back a plan-based cohort can honestly reach, and the product should decline to draw the curve rather than draw it from reconstructed rows.

## Failure Modes

Combinable filters produce small cells quickly. Signup period crossed with plan crossed with channel crossed with region leaves a curve drawn from a handful of accounts, and a readout drafted over that cell still reads as confident prose. A minimum cohort size, below which the curve appears without a drafted readout, is the cheapest guard. It has to apply to the chart too, since the chart is the part people screenshot.
