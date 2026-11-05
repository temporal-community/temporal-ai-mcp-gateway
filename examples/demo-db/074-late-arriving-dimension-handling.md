---
Name: Late-Arriving Dimension Handling
Owner: Tom Okafor
Status: Draft
Last Updated: 2026-01-26
---

## Background

Fact rows sometimes arrive before the dimension rows they reference, usually because the operational systems publish on different schedules. Today the join drops them, which means a transaction can simply be missing from reporting until someone notices a total that does not match.

## Proposal

Hold unmatched facts in a pending area and resolve them when the dimension arrives.

- Unmatched facts written to a pending table with their arrival time, not dropped
- A resolution pass on each load that promotes pending rows once their dimension exists
- Facts unresolved after a configurable period raised as a data quality issue
- Reporting totals include a disclosed pending count rather than silently excluding

## Scope

The six fact tables that feed financial and usage reporting. Behavioral fact tables tolerate the current behavior and are not worth the complexity.

## Risks

A pending area is a place where data goes to be forgotten. Without the unresolved alert, this proposal would make the current silent loss into a slower silent loss, which is not an improvement. The alert is the load-bearing part.

## Measurement

Facts dropped per load, which should go to zero, the size and age distribution of the pending area, and reporting totals that reconcile to source counts.

## Interfaces Affected

Six fact tables gain a pending sibling and a resolution step, which changes the shape of each load job rather than only its content: a load now has two outcomes per row instead of one, and its success criterion has to treat rows that went pending as something other than failure. Downstream, any view that assumes a fact row is complete on arrival has to decide whether it reads pending rows. Financial reporting must not; usage dashboards probably should.

## Operational Impact

The unresolved alert lands on whoever runs the pipeline and is not actionable by them. A fact unresolved for a week is a problem in the operational system that never published the dimension. The alert has to route to that system's team with the specific missing key attached, or it gets acknowledged and closed by someone with no way to fix it. That routing is the difference between this working and it producing a second queue nobody reads.

## Open Questions

The unresolved period is configurable and nobody has proposed a value. Twenty-four hours catches a publishing delay and fires over weekends; a week is quiet and lets a month's close run with facts still pending. It likely differs per table, and the financial tables are where a short window matters most. Whether the pending count disclosed in a total is a row count or a value sum is also undecided, and only the second is meaningful to a finance reader.
