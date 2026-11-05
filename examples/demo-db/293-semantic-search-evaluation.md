---
Name: Semantic Search Evaluation
Owner: Victor Alves
Status: In Review
Last Updated: 2026-07-30
---

## Context

Our search matches words. People frequently search for a concept and use different words than the content does, and for those queries we return nothing useful however good the ranking is. The question is whether embedding-based retrieval would help enough to justify its cost.

## Proposal

Evaluate before committing, with a bounded experiment against the judged query set.

- An AI embedding model used to build a vector index over a representative content subset
- Hybrid retrieval evaluated against keyword-only on the judged set, offline
- Cost modeled honestly, including embedding generation on write and index storage
- A written recommendation with the evidence, including the option to decline

## Scope

Evaluation only. No production deployment is proposed here, and the evaluation should be able to conclude that this is not worth doing.

## Risks

Semantic retrieval is good at finding related content and bad at exact lookup, which is most of what people actually do. A hybrid is the realistic shape and it doubles the retrieval path's complexity, cost, and failure modes. The evaluation needs to separate the queries where it helps from the queries where it is neutral, because an average improvement that hides regressions on common queries would be a bad trade.

## Measurement

Retrieval quality on the judged set by query type, embedding and storage cost per million documents, and latency for hybrid retrieval against the current path.

## Data We Have

The judged query set is four hundred queries with graded relevance, assembled eighteen months ago and weighted toward what support was being asked at the time. It is large enough to detect a big difference and too small to resolve a small one, especially once it is split by query type and some buckets hold a few dozen queries. Logs can supply fresh candidates but not judgments, and judging is the expensive part.

- Four hundred graded queries, skewed toward support-driven topics
- Click logs for every query, usable as a weak signal and not as truth
- No judgments at all for the concept-style queries this work targets, which is the first gap to close

## Timeline

Six weeks, most of it not spent on retrieval. Two weeks to extend the judged set with concept queries and grade them, since evaluating against a set that excludes the failing case proves nothing. Two weeks to build the index over the content subset and run both paths. Two weeks to model cost against real write volumes and write the recommendation. Compressing the judging phase is the obvious way to go faster and the surest way to produce a result nobody trusts.

## What Would Change Our Mind

A clear gain confined to concept queries, with no regression on exact lookup, makes the hybrid worth building even at double the retrieval complexity. A real gain concentrated in queries that occur a handful of times a day does not, whatever the relative improvement looks like. If embedding cost per million documents lands above the entire current search budget, the recommendation is to decline regardless of quality.
