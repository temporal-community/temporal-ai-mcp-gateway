---
Name: Query Result Caching
Owner: Lena Fischer
Status: Approved
Last Updated: 2026-03-27
---

## Problem

A popular dashboard with fifty viewers runs the same twelve queries fifty times within a few minutes of the morning refresh. The warehouse charges us fifty times for one answer, and the fiftieth viewer waits as long as the first.

## Proposal

Cache results keyed on the query and the freshness state of its inputs.

- Cache key includes the query text and the last load time of every table it reads
- Invalidation by input freshness rather than by elapsed time
- Cache bypass available explicitly for anyone who needs to be certain
- Hit rate and saved cost reported per dashboard

## Scope

Dashboard queries. Ad-hoc analysis is excluded because the hit rate would be near zero and the staleness risk is real.

## Risks

Freshness-keyed invalidation is correct only if we know every table a query reads, which fails for queries that use dynamic construction or user-defined functions. Those need to be detected and excluded from caching rather than cached optimistically.

## Measurement

Cache hit rate, warehouse spend on dashboard queries, dashboard load time at the ninety-fifth percentile, and any instance of a cached result being served past its input's freshness.

## Dependencies

Knowing a query's inputs is the whole mechanism, and it has to come from the planner rather than from parsing text ourselves. The warehouse exposes a resolved table list per statement, accurate for static queries and silent about dynamically constructed ones, so detection means treating an unresolvable statement as uncacheable.

- Per-table last load time, which the freshness work already publishes
- The planner's resolved input list, available at submission rather than only after execution
- Result storage sized for the hot set, since a dashboard's twelve queries are the whole working set

## Failure Modes

The dangerous failure is a query whose inputs resolve correctly but which also reads something outside the planner's view, a user-defined function reaching a table of its own being the case we know about. That yields a cached answer that looks correctly keyed and is stale against an input nobody recorded. Excluding statements that call user-defined functions is crude and is the only reliable version of this until functions declare their reads.

## Timeline

Six weeks to caching behind a per-dashboard flag, with the ten most-viewed dashboards enabled first and the hit rate read before anything else is added. Warming on the load completion event follows once that rate is known, since warming a cache nobody hits is spend without saving. Per-dashboard saved cost ships alongside, because that number is what gets the remaining dashboards enabled.
