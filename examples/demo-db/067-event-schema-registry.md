---
Name: Event Schema Registry
Owner: Jonas Keller
Status: Approved
Last Updated: 2026-03-05
---

## Problem

Product teams add event fields whenever they need them and remove them whenever they stop caring. Downstream, four hundred queries break silently or, worse, keep running against a field that now means something different. The warehouse team finds out from a dashboard that looks wrong rather than from a change notice.

## Proposal

A registry that holds the schema for every event, with compatibility rules enforced at publish time.

- Schemas registered before an event can be published, with a code-generated client
- Additive changes allowed freely, breaking changes requiring a new version
- Producers blocked at build time rather than warned at run time
- Consumers subscribe to a version and are notified when a newer one appears

## Scope

Product events flowing into the warehouse. Operational logs and metrics have different consumers and different tolerances and are not covered.

## Risks

A registry that blocks a release is a registry teams will route around, usually by publishing to a generic event with a payload blob. The exemption path needs to be visible and uncomfortable rather than absent: an escape hatch that creates a tracked item is better than one that does not exist.

## Success metrics

Events published through registered schemas, breaking changes caught before release, and downstream query breakages per quarter, which currently run at about fifteen.

## Migration

The registry starts empty while several hundred event types are already in flight. Backfilling a schema for each one from observed traffic is faster than asking every producing team to write theirs, but inferred schemas encode current accidents as rules, so each inferred schema is marked provisional until its owning team confirms it.

- Infer a draft schema from the last thirty days of traffic per event type
- Route each draft to the producing team for confirmation or correction
- Enforce at build time only for confirmed schemas, warn for provisional ones
- Treat an event type with no traffic in thirty days as retired rather than registering it

## Failure Modes

The registry becomes a release dependency, so its own availability matters more than the events it describes. A registry outage during a deploy window either blocks releases or has to fail open, and failing open means a breaking change can ship unseen. Build-time checks read a cached schema snapshot so a registry outage degrades to a stale check rather than no check.

The generic-payload escape described under Risks is the other failure, and it is invisible in the registry's own numbers. Counting payload-blob events separately is what makes routing around the registry show up.

## Open Questions

Whether consumer subscriptions should block a producer's version bump when no consumer has migrated, or only notify. Blocking gives the warehouse team a veto they have asked for and gives producers a dependency on consumers they have never had.
