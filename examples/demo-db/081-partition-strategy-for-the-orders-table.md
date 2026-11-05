---
Name: Partition Strategy for the Orders Table
Owner: Clara Benton
Status: Draft
Last Updated: 2025-09-12
---

## Background

The orders table is partitioned by load date, which made sense when it was loaded nightly. Almost every query filters on order date instead, so almost every query scans the whole table. It is the single largest line in the warehouse bill.

## Proposal

Repartition by order date with clustering on the two columns that appear in most filters.

- A shadow table built with the new layout and validated against the current one
- Query performance compared across the fifty most frequent query shapes
- Cutover by view swap, so consumers do not change anything
- The old table retained for two weeks and then dropped

## Scope

The orders table and the four views built directly on it. Other large tables have the same problem and should follow once this establishes the pattern.

## Risks

Repartitioning changes the cost profile rather than removing it: queries that filter on load date, of which there are a handful in the reconciliation jobs, get slower. Those queries need identifying and rewriting before cutover rather than after.

## Measurement

Bytes scanned per query across the top shapes, total cost for the orders table, and the ninety-fifth percentile query time for the dashboards that read it.

## Sequencing

The reconciliation rewrites come first, because those jobs are the only consumers that get worse and the only ones needing code changes. Find them in the query log by predicate rather than by job name; two filter on load date inside a subquery and do not look like load-date queries from outside. Building the shadow table runs in parallel, since building it changes nothing for anyone.

- Query log swept for load-date predicates, nested ones included
- Reconciliation jobs rewritten and running against the current table
- Shadow table built and compared across the fifty query shapes
- View swap, then two weeks with both tables before the drop

## Cost

The shadow table doubles storage for orders during the build and the retention window. That is small against what full scans cost today, but the comparison run is not free either: fifty shapes against both layouts is a day of warehouse time, billed to the budget this proposal exists to cut. Both are one-off and both belong in the forecast, so the cutover month does not read as a regression.

## Rollback

The view swap is the rollback. Point the four views back at the original table and behavior returns within a query. That holds only while the old table exists, which is what the two-week retention buys. After the drop, recovery means a rebuild, so the drop should wait for a full monthly close to run against the new layout rather than for fourteen days to elapse.
