---
Name: Anomaly Alerts on Revenue Metrics
Owner: Tom Okafor
Status: In Review
Last Updated: 2026-06-19
---

## Context

Revenue anomalies are found by people looking at dashboards. The checkout outage in February cost about four hours of transactions and was noticed by an analyst opening a chart for an unrelated reason, roughly three hours in.

## Proposal

Automated detection on a small set of revenue metrics, tuned for precision over recall.

- Detection on six metrics only: checkout starts, completions, charge success, refunds, signups, and cancellations
- An AI forecasting model producing an expected range per metric per hour, accounting for weekday and seasonal shape
- Alerts routed to the business on-call with the contributing dimension already identified
- A weekly review of alerts raised and missed, feeding threshold adjustment

## Non-goals

No detection on the long tail of product metrics. Precision collapses and the alerts stop being read, which is worse than not having them.

## Risks

The model learns from history including the outages in it, so repeated incidents become expected behavior and stop alerting. Known incident windows need excluding from training, which requires the incident record to be accurate about time, and it currently is not.

## Measurement

Time from revenue anomaly to alert, false alerts per week, and incidents where the alert fired before a person noticed.

## Dependencies

The incident record is the blocking dependency, not the forecasting model. Excluding known incident windows from training needs start and end times accurate to the hour, and today they are written up afterwards by whoever drafted the review, usually to the day. Fixing that means recording a machine-readable window when the incident is closed, which is a change to the incident process rather than anything in this proposal. The six metrics also need an hourly feed: charge success and refunds currently land once a day with the billing load.

## Data We Have

Two years of hourly history for five of the six metrics, which is enough to learn weekday and seasonal shape.

- Cancellations are reliable for fourteen months only, after a definition change
- The February outage sits in the history and is the clearest example of what has to be excluded
- Dimension breakdowns exist for checkout but not for signups, so the contributing dimension can be named for four metrics of the six

## Rollout

Run in shadow for a full quarter, writing alerts to a channel that pages nobody, and compare them against what analysts found by hand. The quarter is the point: seasonal shape needs a season to be wrong about. Routing to the business on-call begins only when false alerts per week are inside the number agreed at the weekly review, and begins with checkout completions and charge success, the two metrics where the February case would have fired.
