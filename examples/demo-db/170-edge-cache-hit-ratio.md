---
Name: Edge Cache Hit Ratio
Owner: Felix Braun
Status: Draft
Last Updated: 2026-05-21
---

## Problem

Our edge cache hit ratio is sixty-one percent, which is poor for a product where most responses are identical across users. The main cause appears to be cache headers set defensively years ago and never revisited, plus a query parameter that varies per request and defeats the key.

## Proposal

Audit caching behavior per response class and fix the obvious defeats.

- Cache headers reviewed per endpoint, with a documented reason for anything uncacheable
- The varying parameter removed from the cache key, since it is used for analytics rather than for content
- Vary headers narrowed to what actually changes the response
- Stale-while-revalidate enabled for the classes where slightly old is clearly better than slow

## Scope

Public responses served through the edge. Authenticated responses are a separate and more careful conversation.

## Risks

Caching more aggressively means serving stale content when invalidation lags, and for pricing or availability content that is a correctness problem rather than a performance one. Those endpoints need identifying and excluding deliberately rather than being caught by a general rule.

## Measurement

Hit ratio by response class, origin request volume, latency at the median, and any instance of stale content being served where it mattered.

## Sequencing

The parameter comes out of the cache key first. It is one change, it needs no per-endpoint judgment, and the movement it produces says how much of the sixty-one percent is key fragmentation rather than policy.

- Week one: the parameter dropped from the key, with analytics still receiving it from the request log
- Weeks two to five: the header audit endpoint by endpoint, pricing and availability classified before anything widens
- Week six: stale-while-revalidate on the classes the audit cleared, one class at a time

## Rollback

Every step is an edge configuration change and reverts in minutes, which is the reassuring half. The other half is that a revert does not undo what is already cached: content served with a long lifetime stays servable until it expires or is purged, so a mistaken header is a purge rather than a revert. The purge path has to be exercised before the first widening, not during the first incident, and the audit should record the maximum lifetime per endpoint so the blast radius of a mistake is known in advance.

## Cost

Origin request volume falls and edge request volume does not change, so a higher ratio moves cost from origin compute to edge requests and egress. At sixty-one percent the trade is clearly favorable, but it is a trade and not a pure reduction. Stale-while-revalidate adds one background revalidation per expiry per location, small in total and concentrated on the hottest objects.
