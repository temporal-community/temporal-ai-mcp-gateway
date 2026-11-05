---
Name: Time-to-Value Instrumentation
Owner: Nora Sellers
Status: In Review
Last Updated: 2026-02-28
---

## Context

We talk about time to value constantly and measure it nowhere. Each team has a private notion of what the value moment is for their part of the product, and none of those notions is instrumented end to end.

## Proposal

Define the value moment per use case, instrument it, and report the distribution rather than an average.

- Three use cases to start, each with a value moment agreed with the team that owns it
- Measured from workspace creation to the moment, with the distribution reported in full
- Segmented by acquisition channel and team size, since the shape differs sharply
- The definition stored in the semantic layer with the others, not in a dashboard

## Non-goals

No single company-wide time-to-value number. The use cases differ enough that an aggregate would be meaningless, and someone would put it on a slide.

## Risks

The tail is the interesting part and the average will hide it. Reporting the distribution is a commitment that has to survive the first executive request for one number, which it will receive within a month.

## Measurement

Use cases instrumented, the median and ninetieth percentile per use case, and whether product decisions begin citing the distribution rather than the average.

## Dependencies

Measuring from workspace creation needs a reliable creation timestamp, which exists, and a stable workspace identity across the trial-to-paid transition, which does not. Workspaces converted through the sales path are recreated under a new identifier and their clock restarts. Those conversions are a small share of volume and a large share of the tail, so the stitching has to be settled before the distribution means anything.

- Workspace identity stitched across the sales-assisted conversion path
- Each of the three owning teams signs off on its value moment before instrumentation starts

## Sequencing

Instrument one use case end to end before defining the other two. The first will surface events that fire twice, events that fire for an administrator rather than the person who reached the moment, and at least one moment that is unmeasurable as written. Learning that on one use case costs a few weeks. Learning it on three at once costs the credibility of the first report, which decides whether anyone reads the second.

## What Would Change Our Mind

If two of the three distributions turn out close enough in shape to report together, the argument against an aggregate weakens for that pair and a shared number becomes defensible. If instead the acquisition channel explains most of the spread, the per-use-case split matters less than the channel split, and the instrumentation should follow the channel.
