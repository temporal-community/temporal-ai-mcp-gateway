---
Name: Saved Searches and Alerts
Owner: Hugo Takahashi
Status: Draft
Last Updated: 2026-01-20
---

## Problem

People run the same search repeatedly to check whether anything new matches. We know this from the query logs: a meaningful share of queries are identical repeats from the same person within a week.

## Proposal

Saved searches, with optional notification when new results appear.

- Saving from the result view, with the filters captured as part of the search
- Optional alerts at a chosen frequency, never real time by default
- Alerts showing only results new since the last notification
- A limit on saved searches per person, because evaluation cost scales with them

## Scope

Search within a workspace. Cross-workspace saved searches are out of scope and have a permissions problem.

## Risks

Alert evaluation is a scheduled query per saved search per person, which at scale is a load problem that grows quietly. The limit is the control, and the evaluation should run against the index rather than the primary store, which is a design constraint rather than an optimization.

## Measurement

Saved searches created and retained after a month, repeated identical queries, alert open rate, and evaluation cost per thousand saved searches.

## Cost

Evaluation cost is the number that decides the shape of this feature.

- A saved search costs one index query per evaluation, so the daily total is searches times frequency rather than searches
- New-since-last semantics need a watermark per saved search, which is cheap to store and has to survive an index rebuild
- The per-person limit is the only hard control, and it should be set from a measured cost per thousand rather than picked round

A floor on frequency matters more than the limit does: a hundred hourly searches cost what twenty-four hundred daily ones do.

## Interfaces Affected

The result view gains a save control, and the search service gains a scheduled path whose shape differs from the interactive one. Permissions are the subtle part. A saved search runs later, so results have to be filtered by what the person can see at evaluation time rather than at save time, or an alert becomes a disclosure.

## Open Questions

What a saved search does when its filters reference something that has been deleted, where it either returns nothing quietly or fails on every evaluation from then on. We have also not decided whether alerts respect the notification cadence a person already chose or arrive on their own schedule, which is the difference between a feature that fits the digest and one that routes around it.
