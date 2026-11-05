---
Name: Query Understanding for Long Queries
Owner: Marcus Reyes
Status: In Review
Last Updated: 2026-07-28
---

## Problem

About fifteen percent of queries are full sentences rather than keywords, and those perform terribly: the engine treats every word as a required term and returns nothing. People who search in sentences are frequently the newest users, so the first search many people run is also their worst.

## Proposal

Interpret longer queries rather than matching them literally.

- An AI query understanding pass that extracts the intent, the entities, and any implied filters from a natural-language query
- The interpretation shown to the person and editable, never applied invisibly
- Fallback to the existing keyword path when confidence is low
- Interpretation cached per query shape, since the distribution has a long head

## Scope

Workspace search. The help center has its own answering path with its own corpus.

## Risks

An interpretation that quietly narrows a search is worse than a literal match that returns nothing, because the person sees plausible results and assumes they are complete. Showing the interpretation is what makes this honest, and the editing control must be prominent rather than a small link. Latency is the other constraint: an interpretation pass that adds a second to every search would not be worth it even if the results improved.

## Measurement

Zero-result rate on sentence queries, result click-through, interpretation edit rate, and added latency at the ninety-fifth percentile.

## Rollout

The pass runs only on queries that look like sentences, the fifteen percent, and the rest keep the keyword path untouched. That bounds both the latency exposure and the blast radius. Within that group, the first release should hold the interpretation behind an explicit control: the person sees that their query was long, sees the proposed reading, and chooses to run it. Only after that does a version apply the interpretation directly and show it afterwards. The second shape is better when interpretations are good and considerably worse when they are not, and the first release is how we learn which we have.

## Cost

Interpreting each query is the recurring cost, and the cache is what keeps it tolerable. The head of the sentence-query distribution is short enough that a modest cache should cover a large share of traffic. The key has to be a normalized query shape rather than the raw string, and normalization that reaches too far will serve one person's interpretation to someone else's different question. Entries also need to expire when a workspace's own vocabulary moves, since a reading that mapped a word to a project is wrong the day that project is renamed.

## Open Questions

Whether the interpretation may add filters the person did not state. A date range implied by last week is obviously useful and is also exactly the mechanism by which a search narrows without being noticed. Also unsettled: what the low-confidence fallback actually shows. Dropping back to the literal keyword path reproduces the zero-result experience this exists to fix, and saying plainly that the query was not understood may serve people better than returning nothing quietly.
