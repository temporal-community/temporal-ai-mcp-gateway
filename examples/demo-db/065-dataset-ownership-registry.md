---
Name: Dataset Ownership Registry
Owner: Priya Raman
Status: Shipped
Last Updated: 2025-08-07
---

## Context

About a third of warehouse datasets had no owner. When one broke, the triage step was asking in a channel whether anyone recognized it, and the answer was frequently no, which left the data platform team maintaining transformations whose business meaning nobody could explain.

## Approach

Require an owning team on every dataset and enforce it at creation.

- Ownership recorded as a team rather than an individual, to survive staffing changes
- New datasets cannot be created without one
- Existing unowned datasets assigned through a claim process, with a deprecation path for genuine orphans
- Alerts route to the owning team rather than to the platform team by default

## Non-goals

No change to access control. Ownership is about responsibility, and conflating it with permissions would have made both harder to reason about.

## Risks

The claim process for existing datasets was expected to stall, and it did for about six weeks. What unblocked it was deprecation: announcing that unclaimed datasets would be dropped on a date produced owners for most of them and confirmed the rest were genuinely dead.

## Outcome

Shipped in July. Forty-one datasets were dropped as orphans, ownership coverage is at ninety-six percent, and alert routing to the platform team is down by roughly two thirds.

## Operational Impact

Ownership moved the work rather than removing it, and the teams now receiving alerts feel that.

- Owning teams take dataset alerts directly, which for two of them was a new on-call surface rather than an addition to one
- The platform team still triages the remaining four percent, which is where the hardest datasets sit
- Ownership is checked at creation, so a dataset created by a scheduled job needs an owning team recorded in the job definition

That four percent is not a rounding error. Those are the datasets whose claim stalled twice, and they are disproportionately the ones feeding reporting that leadership reads.

## Review Notes

The deprecation date was the contested decision and the one worth recording. Dropping forty-one datasets on an announced date was called reckless in review, and the argument held: a dataset nobody will claim when told it is about to be deleted is a dataset nobody is using. One of the forty-one came back from backup two weeks later, claimed by a team that had been told and had not read the announcement. That is the cost of the approach rather than an argument against it.

## Open Questions

How ownership survives a reorganization. Teams are recorded rather than people, and a dissolved team leaves datasets pointing at nothing, which nothing currently detects. The second is whether the claim process should run again on a schedule, or whether coverage above ninety percent is the point at which this stops being worth revisiting.
