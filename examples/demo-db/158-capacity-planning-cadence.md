---
Name: Capacity Planning Cadence
Owner: Omar Haddad
Status: Draft
Last Updated: 2026-04-16
---

## Context

Capacity is added when something gets slow. There is no forecast, no lead-time awareness, and no connection between the product roadmap and the infrastructure that will carry it. The last two capacity events were both discovered by customers.

## Proposal

A quarterly planning cycle with a forecast, a lead-time map, and named decisions.

- Demand forecast from product plans and historical growth, by service
- Lead times documented per resource type, since some are weeks and some are hours
- A capacity decision per service each quarter, recorded with its assumptions
- Monthly tracking against forecast, with a trigger for re-planning on material divergence

## Non-goals

No change to autoscaling, which handles variation within a capacity envelope rather than the envelope itself.

## Risks

Forecasts from product plans assume product plans are accurate about timing, which they are not. The value is less in the forecast's accuracy than in the conversation, and the plan should be written so that being wrong is cheap: shorter commitments on long-lead resources, with explicit re-planning triggers.

## Measurement

Capacity events discovered internally rather than by customers, forecast error by service, and lead-time surprises, which should be none since they are now documented.

## Data We Have

Historical growth per service comes from the metrics store at monthly granularity going back three years. That is enough to fit a trend and not enough to separate real growth from the three migrations that moved load between services in that window. Those migrations have to be marked before the history is used, or two services will show growth and decline that never happened.

- Per-service utilization and request volume, monthly, three years
- Lead times known informally for most resource types and written down nowhere
- No record of the assumptions behind the last two capacity additions, which is the gap this closes going forward

## Staffing

The cycle needs a facilitator who does not own the services, because a service owner forecasts the capacity they already want. Half a week per quarter for the facilitator and two hours per service owner is the honest cost. Monthly tracking is far cheaper and is also the part that decays first, so it should be a generated report with a named reader rather than another meeting.

## Open Questions

Material divergence is undefined and has to be set per service: one whose lead time is hours can drift well past forecast, while one waiting weeks for hardware cannot. Who decides when the forecast says buy and the budget says wait is also unsettled, and nothing here resolves it.
