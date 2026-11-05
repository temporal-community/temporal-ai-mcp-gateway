---
Name: Data Quality Checks at Load
Owner: Yusuf Demir
Status: Approved
Last Updated: 2026-07-08
---

## Context

Data quality is checked by whoever notices. Most problems are found by an analyst who sees a strange number, days after the bad load, by which point the downstream datasets have propagated it and several reports have been circulated.

## Proposal

Declarative checks attached to datasets, run at load, with failures blocking promotion.

- Row count, null rate, and distribution checks declared alongside the model definition
- An AI anomaly detection pass over the numeric columns to catch shifts no fixed rule would express, proposing thresholds rather than enforcing them
- Failures hold the load in a staging area instead of promoting it
- A daily digest of near-misses, because the checks themselves need tuning

## Scope

The modeled layer. Raw ingestion keeps whatever arrives, because rejecting source data creates a gap rather than a fix.

## Risks

Blocking promotion means a false positive makes data stale, which for the finance datasets is worse than a small quality defect. The blocking set should be narrow and explicitly chosen per dataset. The anomaly pass is advisory for exactly this reason: a model that cannot explain why a distribution moved should not be allowed to stop a load on its own.

## Measurement

Quality incidents found by a check rather than by a person, false positive rate per check, and time from bad load to detection.

## Rollout

Every check runs advisory first, for four weeks, across every dataset. Nothing blocks until the near-miss digest has shown what the checks actually catch, because a check written from an assumption about the data fails on a day the data is fine.

- Weeks one to four: all checks advisory, digest reviewed weekly, thresholds adjusted
- Week five: blocking enabled on the dozen datasets with no finance consumer
- Week nine: blocking on the finance datasets, with the staleness escalation path written down first

## Operational Impact

A held load needs an owner awake. Promotion blocked at two in the morning with nobody to release it is a stale dataset by breakfast, which is the failure the risk above names, arriving through nobody being on call rather than through a false positive.

- A named owner per dataset, who receives the hold and can override with a recorded reason
- Escalation after ninety minutes for datasets carrying a downstream freshness commitment
- The digest sent to the owning team rather than the data platform, since tuning a check needs knowledge of the data

## Open Questions

- Whether a held load blocks only its own dataset or everything downstream, which is the difference between a stale table and a stale half of the warehouse
- What the override records, given a free-text reason is easy to type and hard to use later while a reason code is the reverse
- Whether anomaly proposals are reviewed on a schedule or only when someone opens the digest
- How a check is retired once the problem it was written for is fixed
