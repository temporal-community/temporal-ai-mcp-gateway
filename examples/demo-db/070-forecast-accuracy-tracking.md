---
Name: Forecast Accuracy Tracking
Owner: Caleb Mortensen
Status: Draft
Last Updated: 2026-03-09
---

## Problem

We forecast revenue monthly and never look back at how the forecast did. Each month's forecast is built from the current pipeline and judgment, with no feedback loop, so systematic bias persists indefinitely because nobody measures it.

## Proposal

Record every forecast at the time it is made and report accuracy against outcome.

- Forecasts snapshotted when submitted, immutable afterwards
- Error reported by segment and by forecaster, as a distribution rather than a single number
- Systematic bias surfaced separately from variance, because they have different remedies
- A quarterly review of accuracy alongside the forecast itself

## Scope

Revenue forecasting. Capacity and cost forecasting have the same problem and should adopt the pattern afterwards.

## Risks

Reporting accuracy by forecaster is a performance measurement whether we intend it that way or not, and the predictable response is conservative forecasting to avoid being wrong in the visible direction. Reporting bias separately from variance at least makes that behavior legible.

## Measurement

Forecasts recorded, mean absolute error by segment over time, and whether the bias in any segment measurably narrows across two quarters.

## Data We Have

Eleven months of submitted forecasts exist in the spreadsheets they were built in, and in principle they could seed the first accuracy report instead of waiting two quarters for fresh data. In practice several of those files have been edited since submission, because the forecast and the re-forecast live in the same cells, so that history is not a trustworthy baseline and should be labeled indicative if it is used at all. Outcome data is clean: recognized revenue by segment closes on the same calendar every month and has not been restated in three years. The real gap is segment mapping, which changed in January and will make any comparison across that boundary wrong unless the old segments are mapped forward deliberately.

## What Would Change Our Mind

If the first two quarters show error dominated by a handful of large deals landing one month either side of the boundary, the thing being measured is timing rather than forecasting judgment, and the remedy is a different cut of the report rather than a feedback loop aimed at forecasters. That pattern would also make per-forecaster reporting actively misleading, since whoever owns the largest accounts would post the worst numbers for reasons unrelated to how they forecast. The test is cheap and should run before the first review: produce the report with and without the five largest deals and see whether the ranking survives.
