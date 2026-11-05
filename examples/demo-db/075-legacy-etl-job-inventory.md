---
Name: Legacy ETL Job Inventory
Owner: Omar Haddad
Status: Draft
Last Updated: 2025-10-16
---

## Context

Before the modeling framework, transformations were scheduled jobs written in whatever was convenient. About seventy of them still run. Some feed live dashboards, some feed nothing, and nobody has a list that distinguishes the two.

## Proposal

Inventory all of them, classify by consumer, and retire the ones with none.

- Automated discovery from the scheduler rather than a manual list
- Each job traced to its outputs and each output traced to its readers
- Jobs with no reader in ninety days proposed for retirement with a notice period
- Jobs with readers scheduled for migration or documented as deliberately legacy

## Non-goals

No migration work in this phase. The inventory is a prerequisite for planning migration, and conflating the two would stall both.

## Risks

Reader detection is based on query logs, which miss consumers that read through an export or a cached copy. The notice period is the safety net, and it needs to be long enough to catch a quarterly consumer, which means at least one quarter.

## Measurement

Jobs inventoried and classified, jobs retired, and compute spend on the legacy scheduler, which is currently about a sixth of the platform total.

## Data We Have

The scheduler knows what runs. Everything after that is inference.

- Job definitions and run history for all seventy, including the ones that have failed quietly for months
- Query logs covering warehouse reads, which is where reader detection comes from
- Nothing on exports or on copies taken into other tools, which is the gap the notice period covers

Run history is a classifier in its own right: a job that has failed for six months without a complaint has no reader worth the name, whatever the query logs suggest.

## Timeline

Discovery and output tracing take about three weeks and can run while nothing is being decided. Classification follows and is the part that needs people, since a job with one reader is a conversation rather than a lookup. The notice period then runs a full quarter, which puts the first retirements two quarters out, and the compute saving arrives at the end rather than being promised earlier.

## Failure Modes

A job retired because its only reader runs annually, which a quarter of notice does not catch. A job whose output feeds another legacy job, where retiring the first breaks the second quietly because the chain was never mapped. And a job nobody reads that writes to a table another job overwrites, where retiring it changes a published number without anything appearing to fail.
