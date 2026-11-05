---
Name: Search Autocomplete Latency
Owner: Caleb Mortensen
Status: Approved
Last Updated: 2026-05-12
---

## Context

Autocomplete suggestions arrive after about three hundred milliseconds at the median and over a second at the tail. At those latencies people have finished typing before the suggestions appear, which means the feature costs us a request per keystroke and returns nothing of value.

## Proposal

Meet a latency budget or do not show suggestions at all.

- A budget of eighty milliseconds at the ninety-fifth percentile, measured client-side
- A prefix index separate from the main search index, sized to fit in memory
- Client-side debouncing and request cancellation, which are currently absent
- Suggestions suppressed entirely when the budget is missed, rather than arriving late

## Scope

Search autocomplete. Mention and entity pickers have their own completion paths.

## Risks

Suppressing late suggestions means the feature disappears for people on slow connections, who are also the people for whom it would save the most typing. A regional prefix index improves this; it does not fix it, and we should be honest that this feature is better for people with good connections.

## Measurement

Suggestion latency at the median and ninety-fifth percentile, suggestion acceptance rate, suppression rate by region, and request volume per search session.

## Alternatives Considered

Serving suggestions from the main search index with a tighter timeout keeps one index and misses the budget. That index is on disk and shared with full queries, and eighty milliseconds at the tail is not reachable there without reserving capacity full search needs. Precomputing suggestions per workspace and shipping them to the client was the other option; it gets latency to zero and dies on large workspaces, where the prefix set is too big to send and stale by the time it arrives.

## Cost

A separate prefix index means resident memory in every region we serve from, which is new capacity rather than reused. Against that, debouncing and cancellation remove most of the request volume: a request per keystroke becomes roughly one per word, a four-to-one reduction on the median query. The net is close to neutral on infrastructure and clearly positive on search-tier load.

- Prefix index growth is linear in distinct terms, not in documents
- Regional copies are read-only and rebuilt rather than replicated
- Debouncing lands first, since it cuts load whether or not the rest ships

## Rollback

Suppression is the piece that has to be switchable on its own. If the suppression rate by region lands higher than expected, late suggestions are better than none, and that call should not wait for a release. The prefix index and the client changes stay in place either way.
