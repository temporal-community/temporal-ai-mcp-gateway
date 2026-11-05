---
Name: Cache Invalidation Strategy
Owner: Hugo Takahashi
Status: Draft
Last Updated: 2026-02-11
---

## Background

Caching is implemented per service with per-service conventions. Three services cache the same entity with different lifetimes, so the same object can appear with three different values depending on which surface you look at. Customers notice this and report it as a bug, correctly.

## Proposal

A shared invalidation channel keyed on entity identity, with lifetimes as a backstop rather than the mechanism.

- Entity change events published on mutation, consumed by every cache holding that entity
- Lifetimes retained as a safety net, lengthened once invalidation is trusted
- A standard cache client that subscribes automatically, removing per-service implementations
- Staleness measured by comparing cached values against source on a sample

## Scope

The five entity types that appear across multiple services. Service-local caching of derived values is unaffected.

## Risks

An invalidation channel is a dependency that can fail, and its failure mode is stale data served confidently. The lifetime backstop must stay in place rather than being removed once invalidation appears to work, which is the obvious cleanup that would make the next outage much worse.

## Measurement

Cross-surface inconsistency reports, measured staleness per entity type, and cache hit rate, which will fall and should be watched for whether the fall is worth it.

## Alternatives Considered

Shortening lifetimes across the board is the one-line version of this and fails on cost. Matching the same consistency with lifetimes alone means a lifetime shorter than the shortest window anyone complains about, which for the account entity is under a minute and would push most of its reads to the source database. Writing through a shared cache instead of invalidating was the other option; it founders on the five entity types having different write paths, two of them batch jobs that would have to learn to write through.

## Sequencing

Publishing events comes first and is harmless on its own, since nothing consumes them. The standard client lands next, service by service, and a per-service implementation is removed only after its replacement has run a week.

- Events published for all five entity types before any consumer exists
- Standard client adopted one service at a time, oldest implementation first
- Staleness sampling live before the first lifetime is touched

## Failure Modes

A dropped event is indistinguishable from no change, which is why the backstop stays. The worse case is partial delivery: two of three services invalidate, the third does not, and we have reproduced the original bug with a more complicated explanation behind it. Delivery lag has to be visible per consumer and per entity type, so one lagging consumer is an alarm rather than a customer report.
