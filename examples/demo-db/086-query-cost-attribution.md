---
Name: Query Cost Attribution
Owner: Marcus Reyes
Status: Approved
Last Updated: 2026-05-22
---

## Problem

Warehouse spend has tripled in eighteen months and we cannot say who spends it. The bill arrives as one number. Teams asked to reduce usage have no way to know which of their queries matters, so nothing changes until the next bill.

## Proposal

Tag every query with its originator and publish cost by team, by dashboard, and by scheduled job.

- Attribution from the connection credential, enforced rather than voluntary
- Cost per query estimated at submission and reconciled against the bill monthly
- A weekly report to each team showing their top ten queries by cost
- A threshold above which a single query requires acknowledgement before running

## Scope

The warehouse. The streaming infrastructure has a different cost model and is covered by a separate effort.

## Risks

Attribution by credential breaks for shared service accounts, which is exactly where the expensive scheduled jobs live. Those need individual credentials before the report means anything, and that migration is the long pole in this work rather than the reporting itself.

## Measurement

Share of spend attributable to a named owner, total spend against forecast, and whether the weekly report produces any query changes in the first two months.

## Sequencing

Credential migration first, reporting second. A report published while half the spend sits under three shared credentials gets read once, dismissed as wrong, and ignored later when it is right.

- An inventory of shared credentials and the jobs using them, which nobody holds today
- Individual credentials per scheduled job, with the shared ones revoked on a date rather than deprecated
- Reporting switched on once attributable spend passes ninety percent, not before

## Interfaces Affected

- The scheduler, which has to carry a credential per job rather than one per connection pool
- The dashboard tool, where a query inherits the viewer's credential, so cost lands on whoever opened the dashboard rather than whoever built it
- Notebook sessions, which already issue credentials per session and need only the tag carried through
- The billing export, joined to query history monthly for the reconciliation

The dashboard case needs a decision, not a tag: charging readers makes an expensive dashboard invisible and penalizes the person who looked.

## Failure Modes

The estimate is the weak point. An at-submission figure that diverges from the bill teaches people to distrust the weekly report, and the monthly reconciliation that would correct it arrives a month late. Publishing estimate error per team beside the costs is cheaper than arguing about it. The acknowledgement threshold fails differently: set it low and it becomes a reflex click, which is worse than no threshold because it looks like a control.
