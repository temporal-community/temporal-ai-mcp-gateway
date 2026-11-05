---
Name: Pipeline Failure Triage Runbook
Owner: Erin Vasquez
Status: Approved
Last Updated: 2026-04-14
---

## Context

Pipeline failures page the data platform on-call, who in most cases has no idea what the failing job does. The first twenty minutes of every incident go to establishing what broke, who cares, and whether it matters at this hour.

## Proposal

Automate the first twenty minutes and give the on-call a populated case rather than an alert.

- The alert carries the dataset, its owner, its downstream consumers, and its freshness commitment
- An AI triage step reads the job logs and the recent code changes and drafts a first hypothesis with links to the evidence
- Severity derived from the freshness commitment, so overnight failures of weekly datasets do not page anyone
- A one-click path to notify the owning team rather than fixing it on their behalf

## Scope

Scheduled pipeline failures. Warehouse outages and infrastructure incidents follow the normal operational path.

## Risks

A drafted hypothesis anchors the person reading it, and a confident wrong hypothesis costs more than no hypothesis at all. The draft must lead with the evidence it used and be visibly separable from fact, and we should track how often the first hypothesis was wrong rather than assuming it is helpful.

## Measurement

Time from alert to first useful action, pages outside business hours, and the share of failures resolved by the owning team rather than by the on-call.

## Dependencies

The alert can only carry an owner, consumers, and a freshness commitment if the catalog holds all three. Ownership is populated for most datasets and consumers are derived from the lineage graph, but freshness commitments exist for about a third. Severity derivation is blocked on the rest. A dataset with no commitment defaults to the lowest severity rather than the highest, so a missing entry suppresses a page instead of creating one.

## Rollout

- Enriched alerts first, with no severity derivation and no drafted hypothesis
- Severity derivation next, on the datasets that already carry a commitment
- The drafted hypothesis last, shown collapsed for a month so the on-call opts into reading it

## Failure Modes

The one-click notification path can send a page to a team with no rotation. Several owning teams work business hours only, and a notification at three in the morning that nobody will see leaves the failure unowned while looking handled. Notification has to check for a rotation first and otherwise file against the team with a morning deadline.

## Open Questions

How to count a wrong first hypothesis is unsettled. The on-call rarely records having discarded one, so the measurement would rest on a prompt that itself changes behaviour. There is no decision yet between asking at resolution time and inferring it from whether the recorded cause matches what the draft proposed.
