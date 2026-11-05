---
Name: Sampling for Expensive Aggregations
Owner: Victor Alves
Status: Parked
Last Updated: 2026-01-12
---

## Problem

Several exploratory dashboards run full-table aggregations on every load, against tables with billions of rows, to produce a chart whose shape would be identical on a one percent sample. These few dashboards account for a disproportionate share of warehouse cost.

## Proposal

Offer sampled execution as an explicit mode for exploratory use.

- A sampled mode selected by the dashboard author, never applied silently
- Confidence intervals rendered on every sampled chart, not a bare number
- Exact mode always one click away
- Sampling fixed by seed, so a chart does not change shape on refresh

## Scope

Exploratory dashboards. Anything used for financial reporting or shared externally is excluded by policy rather than by judgment.

## Risks

Sampled numbers get screenshotted and circulated without their intervals, and then they are just numbers, and they are wrong. This is the reason the work is parked: we do not currently have a way to keep the interval attached to the number once it leaves the dashboard, and without that the cost saving is not obviously worth it.

## Measurement

If it proceeds: cost of the affected dashboards, adoption of sampled mode, and any instance of a sampled number being cited as exact.

## Cost

The affected dashboards are few enough to price exactly rather than estimate: four of them, loaded a few hundred times a week, each scanning the full fact table on every load. A one percent sample moves the scan by about two orders of magnitude, though not the fixed overhead of the query itself, so the real saving is large but short of the arithmetic. Leaving this parked keeps that spend, which is a choice worth restating whenever the warehouse bill is reviewed.

## Prior Art

Two dashboards in the same family were converted by hand to read a pre-aggregated table. That costs nothing per load and goes stale between refreshes, and it worked because the grouping was known in advance. The ones still expensive are those where the grouping changes every time someone opens them, which is the case pre-aggregation cannot serve and sampling can.

## What Would Change Our Mind

The blocker is that the interval does not survive a screenshot. If chart rendering could stamp the sample rate and the interval into the image, the objection mostly dissolves. A narrower route is to allow sampled mode only on charts with no single headline figure, since a shape with an axis is much harder to misquote than a number. Either one is enough to take this off the parked list.
