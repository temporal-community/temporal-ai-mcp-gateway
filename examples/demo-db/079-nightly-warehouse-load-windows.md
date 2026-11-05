---
Name: Nightly Warehouse Load Windows
Owner: Hana Kobayashi
Status: In Review
Last Updated: 2026-01-19
---

## Context

Everything loads at two in the morning. As the number of sources has grown, the window has stretched from forty minutes to nearly four hours, and the dashboards people open at seven are increasingly built on data that finished loading at six fifty-five.

## Proposal

Stagger loads by dependency and by consumer need rather than running everything at once.

- A dependency graph derived from the transformation definitions, not maintained by hand
- Loads scheduled by the freshness requirement of what consumes them
- Independent branches run concurrently with a cap on warehouse slot usage
- A critical path report so the slowest chain is visible and attributable

## Non-goals

No move to streaming for any of these sources in this phase. Several of them should eventually stream, but sequencing that work needs the dependency graph first.

## Risks

Concurrency against a fixed slot budget means a slow job can now delay unrelated jobs, which is a new failure mode that is harder to diagnose than the current sequential one. Slot reservations per branch would mitigate it at the cost of some throughput.

## Measurement

Time from source cutoff to dashboard freshness for the ten dashboards with the earliest audiences, total warehouse spend, and the number of mornings where a critical dashboard is stale at eight.

## Operational Impact

On-call changes shape. A sequential window fails in one place and the pager names the job; a staggered graph fails in a branch, and the question becomes which of four running chains is blocking the seven o'clock dashboards. The critical path report has to be readable at three in the morning by someone who did not build the graph.

- Alerting moves from job failure to branch lateness against the consumer's freshness requirement
- The runbook needs a way to find tonight's critical path, not last month's
- Reruns become partial, which is the point, and the tooling only reruns the whole night today

## Rollback

The schedule is data, so returning to the single two o'clock window is a configuration change that takes one night. What does not revert is the slot budget: branches running concurrently will have been sized against a cap, and going back to sequential leaves that cap set for a workload that no longer exists. Record the pre-change cap beside the schedule so a revert restores both.

## Open Questions

- Whether per-branch slot reservations are worth the throughput they cost, which only the first two weeks of concurrency can answer
- What a branch does when its source is late: wait, run on yesterday's data, or fail, since each is right for different consumers
- Whether the dependency graph covers the four transformations reading tables written outside the transformation layer
- Who owns a branch, given the current window has one owner for the whole night
