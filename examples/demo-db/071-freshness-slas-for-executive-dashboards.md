---
Name: Freshness SLAs for Executive Dashboards
Owner: Ruth Adeyemi
Status: Approved
Last Updated: 2026-06-26
---

## Problem

The executive dashboards are refreshed by a chain of eleven jobs. When one is late the dashboard shows yesterday's number with today's date, which has twice led to decisions being made on stale data without anyone realizing it was stale.

## Proposal

Declare a freshness commitment per dashboard and surface the state against it, on the dashboard itself.

- A commitment agreed with the audience, not assumed by the platform team
- A visible indicator showing the data's as-of time whenever it is outside commitment
- Alerting on the critical path early enough to intervene before the audience arrives
- A monthly report of commitment attainment per dashboard

## Scope

The nine dashboards used in the weekly leadership review. The pattern should generalize, but the commitment conversation does not scale and should be reserved for where it matters.

## Risks

A visible staleness indicator will, in the first months, be visible often. That is the honest state and it will produce pressure to remove the indicator rather than fix the chain. Agreeing in advance that the indicator stays is part of the proposal.

## Measurement

Commitment attainment per dashboard, time from breach to notification, and decisions traced to stale data, which should become impossible rather than rare.

## Dependencies

A commitment is only as good as what the orchestrator knows. Six of the eleven jobs publish a completion event; the other five are inferred from table modification times, which lie when a job writes nothing because there was nothing to write. Those five need real signals before any commitment resting on them means anything.

- Completion events on all eleven jobs, including a successful no-op
- The as-of timestamp carried into the dashboard query layer rather than computed at render
- Alert routing to the owning team, since the platform team cannot fix a late upstream job
- The monthly attainment report built from the same timestamps the indicator reads

## Staffing

One platform engineer for six weeks covers the indicator and the attainment report. The expensive part is the commitment conversation: nine dashboards, nine audiences, each ending in a number somebody has to defend when it is missed. That is the dashboard owner's work, about half a day each, and handing it to the platform team turns the commitment back into an assumption.

## What Would Change Our Mind

If attainment lands above ninety-five percent across all nine in the first month, the chain is healthier than the two incidents suggested, the real gap was visibility into a rare failure, and the monthly report can go. If attainment is below seventy, the commitments describe what the audience wants rather than what the chain can do, and the answer is to renegotiate the numbers rather than show nine red indicators every morning.
