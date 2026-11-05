---
Name: Mobile Search Experience
Owner: Clara Benton
Status: In Review
Last Updated: 2026-07-06
---

## Context

Mobile search returns the same results as web search, ranked the same way, presented as an undifferentiated list. On a small screen with a slow connection, the result people want is frequently below the fold, and the median mobile search ends in a second search rather than a tap.

## Proposal

Rank and present for the mobile context specifically.

- Recency and personal relevance weighted more heavily than on web, where people scan further
- An AI reranking pass over the top fifty results, using the person's recent activity as context
- Results grouped by type with the strongest single result promoted above the groups
- Query suggestions from recent searches, shown before the person finishes typing

## Scope

Search within the mobile applications. The underlying index and the web presentation are unchanged.

## Risks

Reranking on personal activity creates a loop where what you looked at recently is what you find, which is helpful for retrieval and actively harmful for discovery. The group structure is what keeps other result types visible, and it should not be collapsed in favor of a single ranked list however much better that tests on the first interaction.

## Measurement

Searches ending in a tap on the first screen, repeat searches within a session, and time to first tap.

## Cost

The reranking pass runs over fifty candidates per query, which puts it on the critical path of every mobile search rather than in a background job. That cost grows with searches, not with people. Two things keep it bounded.

- Skipped for queries matching a recent search exactly, which is about a third of mobile volume
- Held to a fixed per-query ceiling, with the unreranked order served when the ceiling is hit
- Reported per search alongside time to first tap, since the two trade against each other

## Failure Modes

A slow connection is the case this change exists for and the case where an extra pass hurts most. If reranking is treated as required, someone on a poor connection waits longer for a better-ordered list they were going to abandon anyway. The ordering has to degrade rather than block: the grouped list renders from the original ranking, and the promoted result appears when the pass returns.

## Rollback

Ranking weights, the reranking pass, and the grouped presentation ship behind separate switches. The presentation change is the one most likely to be wrong and the one least likely to be at fault in a latency regression, so they cannot share a switch. Turning off the pass alone restores the previous ordering without touching layout, which is the rollback we expect to need.
