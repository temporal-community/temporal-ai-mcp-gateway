---
Name: Search Infrastructure Cost
Owner: Ben Tsai
Status: Draft
Last Updated: 2026-01-13
---

## Problem

The search cluster is the third largest infrastructure line and has grown faster than content volume. We index everything, keep every field, and replicate the whole index to every region regardless of where the content is accessed from.

## Proposal

Index less, store less, and place indexes where they are read.

- A field audit removing what is never queried or displayed, which is a surprising share
- Content older than a threshold moved to a slower tier with a documented latency difference
- Regional placement following workspace residency rather than replicating globally
- Index size and query cost reported per workspace tier

## Non-goals

No reduction in what is findable. Moving to a slower tier changes latency, not availability.

## Risks

A slower tier for older content sounds harmless until someone searches for something from two years ago and waits six seconds. The threshold and the latency difference both need measuring against real query patterns, which skew toward recent but have a persistent tail.

## Measurement

Cluster cost, index size per workspace, query latency by content age, and search abandonment on queries hitting the slower tier.

## Sequencing

The field audit goes first because it can be tested on one shard before it is applied anywhere. Tiering by age comes second, and regional placement last, since placement depends on the residency decision and inherits whatever it settles on.

- Field audit on a single shard, with query logs replayed to catch fields used only by rare queries
- Tier threshold chosen from the measured latency difference, not before it
- Regional placement after residency, because moving an index twice costs what the saving is worth

## Dependencies

Regional placement follows workspace residency, which is not yet decided, so that part is waiting on a decision owned elsewhere. The estimate here assumes residency lands on two additional regions; more regions means larger replication savings and faster-growing fixed cost. Neither the field audit nor the tiering depends on it, which is why they come first.

## Rollback

Reindexing from source is always possible and takes about eleven hours at current volume, so every change here is recoverable in a day. What is not recoverable in a day is a tier threshold that is wrong in a way nobody notices. Abandonment on slow queries is a gradual signal, and a threshold set too aggressively will look fine for a month, so it wants watching weekly rather than at review time.
