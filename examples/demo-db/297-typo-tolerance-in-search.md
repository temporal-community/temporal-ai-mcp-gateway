---
Name: Typo Tolerance in Search
Owner: Sofia Marchetti
Status: Draft
Last Updated: 2025-09-05
---

## Context

Search matches exact terms. About eight percent of queries return nothing, and a sample of those shows most are near-misses: a transposed letter, a missing accent, or a plural where the content is singular.

## Proposal

Edit-distance tolerance with sensible bounds, plus normalization.

- One edit for short terms, two for longer ones, never for terms under four characters
- Accent and case normalization at both index and query time
- Stemming for the supported languages, with the rules per language rather than one set
- Original query preserved and shown, with the interpretation stated when it differs

## Scope

Full-text search across documents and items. Identifier lookup stays exact, deliberately.

## Risks

Tolerance on identifiers would be actively harmful, since a near-miss on an order reference returns the wrong order confidently. The boundary between a term and an identifier needs to be explicit in the query parser rather than inferred from shape.

## Measurement

Zero-result rate, result click-through on corrected queries, and any case of a near-miss returning the wrong specific record, which should be impossible by construction.

## Cost

Normalization and stemming change the index, so both need a full reindex before they take effect: roughly eleven hours at current corpus size, run against a shadow index and swapped. Edit-distance matching is a query-time cost instead, and not a free one. A two-edit match on a long term expands to a wide candidate set and the ninety-fifth percentile rises. Bounding edits by term length is as much a latency decision as a precision one.

- Reindex once for normalization and stemming together, not twice
- Per-language rules keep a bad rule set contained to one language
- Latency measured separately for tolerant and exact queries, since pooling hides the regression

## Migration

Saved searches and alert rules were written against exact matching and some of them depend on it. A rule watching for a specific product name will start firing on near-misses of it. Saved rules keep exact semantics unless their owner opts in, which leaves two matching behaviors in the system for as long as those rules live.

## What Would Change Our Mind

If the zero-result sample is unrepresentative, and the eight percent is mostly searches for content that genuinely does not exist, tolerance moves nothing and the effort belongs elsewhere. The sample is small. Redrawing it across a full month, split by workspace size, is cheap and should happen before the reindex is scheduled.
