---
Name: Org Merge Tooling
Owner: Maya Brennan
Status: Draft
Last Updated: 2026-01-15
---

## Background

Customers who acquire another company, or who discover they have been running two workspaces for years, ask us to merge them. We do this by hand, roughly once a month, through a sequence of console operations that one engineer knows and that has gone wrong twice.

## Proposal

A guided merge that plans first, shows the plan, and then executes it transactionally.

- A dry run producing a complete list of conflicts: duplicate members, colliding names, incompatible settings
- Conflict resolution decided up front rather than encountered mid-merge
- Execution in a single transaction per domain of data, with a documented rollback point
- Billing consolidated as an explicit step, after everything else has settled

## Scope

Two organizations at a time, same region, same plan family. Cross-region merges hit data residency rules and are deliberately excluded.

## Risks

A merge touches every system that stores an organization identifier, and the failure mode is partial completion, which is worse than failure. The transactional boundary per domain is the main design decision in this proposal and is the part that most deserves scrutiny.

## Measurement

Merges completed without manual repair, engineer hours per merge against the current two days, and incidents arising from a merge, currently running at about one in fifteen.

## Rollback

The documented rollback point is per domain, so a merge can be abandoned cleanly up to a boundary and not past it. That boundary belongs in the plan the customer approves, because the practical question during a failed merge is not whether rollback is possible in principle but whether it is possible now. Billing going last is partly for this reason: an unconsolidated billing arrangement is recoverable, and a consolidated one that has issued an invoice is not.

## Dependencies

Every system holding an organization identifier is a participant, and no list of them exists. Producing that list is the first task and is likely to reshape this proposal, because a system that cannot enumerate its records by organization cannot appear in a dry run and therefore cannot be part of a plan.

- An inventory of systems storing an organization identifier
- Each able to enumerate and reassign by organization, not only by record
- A conflict catalog the dry run can be checked against

## Staffing

The one engineer who knows the manual sequence is both the design input and the risk, because that knowledge is the specification and it is unwritten. Two weeks of their time transcribing the sequence, including the two occasions it went wrong and what was done about them, comes before any code. After that the merges stop needing them, which is the point of the work.
