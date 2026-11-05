---
Name: Search Filters Redesign
Owner: Dana Whitfield
Status: Draft
Last Updated: 2025-11-27
---

## Background

Filters are presented as a row of dropdowns that reflect the data model: type, owner, status, space, date, and four more. Usage data shows that two are used heavily, two occasionally, and the rest almost never, but all nine take up the top of every result page.

## Proposal

Show the filters people use and put the rest behind one control.

- The two common filters inline, applied with one interaction
- Remaining filters in a single panel, with the active ones summarized as removable chips
- Filter state in the address, so a filtered search is shareable
- Result counts per filter value shown before applying, where the index can produce them cheaply

## Scope

The search result page. Filter controls inside list views are a separate surface with their own conventions.

## Risks

Counts before applying are expensive on large workspaces and are the kind of feature that works in testing and times out in production. They should be omitted rather than slow, and the threshold where they are omitted should be measured rather than guessed.

## Measurement

Searches with a filter applied, time to apply a filter, use of the secondary panel, and result page latency.

## Interfaces Affected

Putting filter state in the address changes what a shared link means. Links in circulation today carry no filter parameters and have to keep resolving to an unfiltered search, so the parameters are additive and absent by default. Saved search stores a filter set in its own structure and should serialize from the same representation rather than a second one.

## Rollout

Layout and panel ship first with counts disabled everywhere. Counts come later, enabled below a workspace size threshold measured on production index timings rather than on a test corpus. Shipping both at once would make a latency regression ambiguous; with the layout alone, any movement in result page latency belongs to the counts.

- Layout, chips, and address state in one release, counts off
- Index timings measured by workspace size to set the threshold
- Counts enabled below it, and omitted silently above it

## Alternatives Considered

Letting each workspace pick which two filters sit inline was rejected: it moves the problem to a settings screen, and the usage data is consistent enough that the same two win nearly everywhere. Collapsing all nine behind the panel with none inline tested worse than today, because the two heavy filters then cost two interactions instead of one.
