---
Name: Index Freshness for New Content
Owner: Ben Tsai
Status: In Review
Last Updated: 2026-04-02
---

## Problem

Newly created content takes between two and nine minutes to become findable. People search for something they just made, do not find it, and create it again. We can see the duplicates in the data and they are not rare.

## Proposal

Index on write for the creating workspace, and reconcile with the batch path afterwards.

- Write-path indexing for the creating workspace only, which bounds the cost
- The batch pipeline retained as the source of truth and the reconciler
- A visible indicator while indexing is pending, rather than silence
- Duplicate detection at creation, which helps regardless of index latency

## Scope

Document and item creation. Bulk import follows the batch path and should say so.

## Risks

Two write paths into one index is a consistency problem, and the failure mode is a document that exists in search and not in the product, or the reverse. Reconciliation needs to be continuous rather than nightly, and discrepancies should alarm rather than be silently corrected.

## Measurement

Time from creation to findable at the median and ninety-fifth percentile, duplicate creation rate, and index discrepancies found by reconciliation.

## Operational Impact

The reconciler becomes a continuously running service with an alarm attached, which is a new on-call surface rather than an extension of an existing one. Search pages today on query errors and index lag; it does not page on correctness. An alarm that fires on every transient write-path retry will be muted within a week, so it has to tolerate a bounded window. A document missing from the index for under thirty seconds is in flight, not wrong. The pending indicator also changes what support sees: a report of not being able to find something becomes a question about whether the indicator was shown, so the indicator's state has to appear in the session record.

## Alternatives Considered

Shortening the batch interval was the first option and was rejected on cost. Holding the ninety-fifth percentile under a minute means running the pipeline roughly ten times more often for every workspace, including the large majority where nobody is waiting on a fresh document. Write-path indexing spends that effort only where someone just created something. The other option was to search the creating workspace's recent writes directly and bypass the index for anything under ten minutes old. That avoids the two-write-path consistency problem entirely, but it ranks new content by different rules than old, and a result that shifts position once it ages out is worse than one that arrives late.
