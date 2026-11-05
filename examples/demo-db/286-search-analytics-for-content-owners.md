---
Name: Search Analytics for Content Owners
Owner: Yusuf Demir
Status: Draft
Last Updated: 2026-02-01
---

## Problem

People who maintain content have no idea what others search for and fail to find. The information exists in our query logs and is visible to nobody who could act on it.

## Proposal

A search analytics view scoped to the content a person owns.

- Top queries leading to their content, and top queries in their space returning nothing
- Click-through per result, so a poorly titled document is identifiable
- Scoped strictly to the owner's own space, with no cross-workspace visibility
- Aggregated with a minimum count, so individual queries are not attributable to a person

## Scope

Workspace content owners. The help center has its own analytics for the documentation team.

## Risks

Search queries are revealing, and in a small workspace even aggregated queries can be attributed to the one person who would have asked that. The minimum count threshold must be set with small workspaces in mind rather than tuned on our largest ones.

## Measurement

Owners using the view, content edited following a zero-result query, and zero-result rate per space over time.

## Data We Have

Query logs retain ninety days and already carry the space identifier on each search event, so the owner-scoped view needs no new instrumentation for top queries or zero-result queries. Click-through is weaker. The click event records result position and document id but not the query it came from, so attributing a click to a query means joining on session and timestamp. That join is lossy for people who search twice in quick succession, which is common. Either the click event gains a query id or the click-through column ships with a stated error margin.

## Alternatives Considered

Exporting the raw query list to space owners on request is cheaper to build, and it moves the aggregation threshold decision onto the requester, who is exactly the wrong person to hold it. Reusing the help center pipeline is the other option, but it keys on published article ids rather than workspace documents and would need its own ingestion path, which is most of the work with none of the scoping guarantees.

## Rollout

- Start with spaces above the minimum count threshold, where aggregation is safe by construction
- Publish the threshold in the view itself, so an owner seeing an empty panel knows why
- Hold the per-space zero-result baseline for four weeks before showing a trend line, since a metric that starts at an unknown level invites misreading
