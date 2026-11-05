---
Name: AI Search for Internal Docs
Owner: Sofia Marchetti
Status: Draft
Last Updated: 2026-01-25
---

## Context

Internal documentation is spread across the wiki, the repository markdown files, and a folder of design documents. Search covers only the wiki, and it matches on exact terms, so finding anything requires knowing what it is called.

## Proposal

One index across all three sources with better ranking and better filters.

- A crawler covering the wiki, repository documentation, and the design document folder
- Ranking that weights recency and authorship, since stale documents are the main complaint
- Filters by source, team, and date, applied before ranking rather than after
- Results showing the document's last update and owner, so staleness is visible without opening it

## Non-goals

No change to where documentation lives. Consolidating the three sources is a worthwhile and separate project, and search should not wait for it.

## Risks

Indexing repository markdown includes a large volume of low-value files, which will dilute results unless the crawler is selective. The selection rule needs to be explicit and reviewable rather than a regular expression somebody tuned once.

## Measurement

Searches ending in a document open, repeat searches per session, and the share of results coming from each source, which tells us whether the ranking is sensible.

## Dependencies

Three sources means three access models, and only the wiki has one the search path can reuse. Repository documentation inherits repository permissions, so results have to be filtered per viewer or the index leaks the existence of private work. The design document folder records no owner per document, which results are meant to show, so the owner is derived from the last editor until that metadata exists.

- Per-viewer permission filtering for repository results
- Last-editor fallback wherever no owner is recorded
- A crawl schedule the repository hosts tolerate on the largest repositories

## Rollout

The wiki is indexed first under the new ranking, because it is the one corpus people already search and the only place a ranking change can be judged against something. Design documents follow: few, and high value. Repository documentation goes last, since that is where the selection rule is exercised and where a bad rule does the most damage to result quality.

## Failure Modes

Weighting recency pushes down documents that are old and correct, which describes most of the architecture material. The complaint behind this work is about documents that are wrong, and age is only a proxy for that. A selection rule tuned to drop low-value repository files will also drop the one README that answers the question, and nobody will report it, because a search returning nothing useful looks exactly like a question with no answer.
