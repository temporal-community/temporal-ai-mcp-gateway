---
Name: Per-Dataset Retention Policy
Owner: Felix Braun
Status: In Review
Last Updated: 2026-02-13
---

## Context

We keep everything forever. Storage cost is growing faster than usage, and more importantly, several datasets hold personal data well past the period we told customers we would hold it, which is a commitment problem rather than a cost problem.

## Proposal

Retention declared per dataset, enforced by a job, and visible in the catalog.

- Every dataset carries a retention period and a legal basis, set by its owner
- Datasets without a declared policy inherit a conservative default after a grace period
- Enforcement deletes rather than archives, with a documented exception process
- Deletion propagates to derived datasets through the lineage graph

## Non-goals

No change to backup retention, which is governed separately and has its own obligations.

## Risks

Propagating deletion through lineage is the part that can go badly. A derived dataset may aggregate to a point where the source rows are no longer personal, and deleting it would destroy legitimate history for no benefit. Owners need the ability to assert that a derivative is out of scope, with that assertion reviewed rather than taken on trust.

## Measurement

Datasets with a declared policy, storage volume, and the count of datasets holding personal data beyond the stated period, which needs to reach zero before the next review.

## Dependencies

Two things this rests on and does not own. The lineage graph has to be complete enough to carry a deletion, and it covers the modeling framework rather than the jobs that predate it, so a derivative built by a legacy job is invisible to propagation. Ownership has to be current, since the period and the legal basis are set by an owner, and a dataset whose owning team no longer exists has neither. The exception process needs a reviewer with standing to refuse, which is a role nobody holds today.

## Sequencing

Declaration first, enforcement considerably later. Every dataset records a period and a legal basis while nothing is being deleted, which turns the measurement into a count that can be watched rather than a cliff. The conservative default applies once the grace period ends, and the first enforcement run is a dry run whose list the owner reads before anything goes. Lineage propagation is last, after the coverage gap is known rather than assumed.

## Open Questions

How an owner's assertion that a derivative is out of scope gets reviewed, and by whom. Taken on trust it is the obvious way to opt out of retention entirely; handed to the data platform team it is a judgment about legal basis that team cannot make. The second is what a partial deletion does to a report built on that dataset, where the history quietly changes shape and nothing in the catalog says so.
