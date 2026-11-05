---
Name: Reverse Sync to Operational Stores
Owner: Maya Brennan
Status: In Review
Last Updated: 2026-05-30
---

## Context

Computed attributes such as account health, usage tier, and churn score live in the warehouse. The product cannot read the warehouse, so each attribute that a product surface needs is recomputed in application code against operational data, differently, by a different team.

## Proposal

A sync that writes a defined set of warehouse-computed attributes back to an operational store the product can read.

- A declared contract per attribute: name, type, freshness, and owner
- Written to a dedicated store, never into a product team's own tables
- Staleness exposed alongside the value, so consumers can decide what to do with an old one
- Attributes removed from the contract only with a deprecation period

## Non-goals

No real-time attributes. Anything needing sub-hour freshness should be computed in the operational path, not synced.

## Risks

Once the product depends on a warehouse-computed attribute, a warehouse delay becomes a product incident, and the data platform inherits an availability commitment it has never had. That commitment should be written down and agreed before the first attribute ships, not negotiated during the first outage.

## Measurement

Attributes served through the contract, duplicate implementations removed, and staleness at read time against the declared freshness.

## Alternatives Considered

Letting the product query the warehouse directly is simpler and was rejected on latency and blast radius: warehouse queries are measured in seconds, and a product surface holding a connection to the analytical cluster turns an expensive query someone else wrote into a checkout problem. Publishing each attribute as an event for teams to consume into their own tables keeps ownership clean, but ends with the same attribute materialized five times under five retention choices, which is roughly where we are now.

## Operational Impact

The data platform takes a pager for the first time. An attribute with a declared freshness of six hours needs someone to notice at hour seven, and that someone cannot be the product team reading the staleness field.

- On-call coverage for the sync itself, separate from the warehouse job owners
- A runbook per attribute saying what the product does with a stale value, written by the consumer
- The deprecation period enforced by the contract rather than by a message in a channel

## Rollback

Each attribute is independently revocable: a flag on the contract stops the sync and leaves the last written value in place with its staleness climbing. That is deliberately not a delete. Removing the row forces every consumer to handle a missing value at the worst moment, while a stale value with an honest timestamp lets each consumer apply its own rule. Usage tier goes last for the same reason, since it is the attribute most likely to gate a feature and hardest to withdraw.
