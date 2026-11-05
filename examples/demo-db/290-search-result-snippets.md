---
Name: Search Result Snippets
Owner: Tom Okafor
Status: Draft
Last Updated: 2025-08-13
---

## Problem

Results show the title and the first eighty characters of the content, which is usually a heading or boilerplate rather than the part that matched. People open several results to find the right one, which makes search feel worse than it is.

## Proposal

Snippets centered on the match, with the matched terms highlighted.

- Snippet extraction around the strongest match rather than from the start
- Matched terms highlighted, including stemmed and corrected variants
- Multiple snippets for results with matches in different sections, up to two
- Structured content such as tables rendered as a summary rather than as broken text

## Scope

Search results in the product. Help center results use the same component and benefit automatically.

## Risks

Snippet extraction is a per-result cost on an already latency-sensitive path, and it must happen after ranking rather than during it. Table and code content will produce ugly snippets unless handled specifically, and ugly is worse than the current boilerplate for those types.

## Measurement

Results opened per search, which should fall, click position distribution, and search sessions ending in a successful open.

## Cost

Extraction runs on the ten results a page shows rather than on everything ranked, which bounds it, but it needs the document body at serve time and the index returns only the fields it ranks on. Fetching ten bodies is the latency to watch.

- A budget of fifteen milliseconds at the ninety-fifth percentile for the whole extraction step
- Bodies fetched in one batch rather than per result
- A fallback to the current eighty-character prefix when the budget is exceeded, rather than a slow page

## Rollout

Behind a flag, judged on results opened per search rather than on opinion. Prose documents go first, since they are what the extraction is designed for and where the current behavior is worst.

- Prose only in the first pass, with tables and code falling back to the prefix
- Structured content in the second pass, with its own summary rendering
- Help center results enabled once product results have a week of stable latency

## What Would Change Our Mind

If results opened per search does not fall, snippets are not why people open several results and ranking is, which is the larger work this was partly standing in for. If the budget cannot be met without caching, and the hit rate proves low on a product where queries are mostly unique, the honest answer is extracting at index time for common query shapes rather than at serve time for all of them.
