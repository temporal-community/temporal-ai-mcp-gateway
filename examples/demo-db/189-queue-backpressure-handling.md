---
Name: Queue Backpressure Handling
Owner: Ines Duarte
Status: Draft
Last Updated: 2025-09-08
---

## Problem

When a consumer falls behind, the queue grows until it hits its retention limit and then drops the oldest messages silently. We have lost work this way twice, both times discovered days later by a customer noticing something had not happened.

## Proposal

Make backpressure explicit and make loss impossible without an alarm.

- Depth and age alarms per queue, set from the consumer's processing rate rather than from a fixed number
- Producers slowed or rejected when depth exceeds a threshold, rather than allowed to fill the buffer
- Retention exhaustion treated as a critical alarm, never as a routine eviction
- A dead letter path with an owner for every queue, which several currently lack

## Scope

The shared message infrastructure. The two services using their own queues should migrate.

## Risks

Rejecting producers moves the failure upstream to a service that may handle it worse, and for the request path it becomes a customer-visible error. The alternative is silent loss, which is worse, but the upstream handling needs checking per producer before this is enabled.

## Measurement

Messages lost to retention, which must reach zero, dead letter volume by queue, and the age of the oldest message in each queue at peak.

## Sequencing

Alarms first, rejection last. Depth and age alarms observe only, cost nothing upstream, and produce the per-queue processing rates the thresholds are derived from; setting a rejection threshold before we have those rates means guessing twice. Dead letter owners come next, because rejecting a producer with nowhere for the failed message to land converts one kind of loss into another. Producer rejection then goes on queue by queue, with the request-path producers last, after each upstream service has been checked.

## Operational Impact

Every queue acquires an owner, a threshold, and a dead letter path that someone reads.

- Dead letter volume becomes a daily signal instead of a buffer filling unobserved
- Thresholds are reviewed after consumer deploys, since a slower consumer changes the safe depth
- Retention exhaustion pages the team that owns the queue, not the infrastructure on-call

## Open Questions

What a producer should do when it is rejected on the request path. Returning an error is honest and turns a backlog into a visible failure; buffering locally recreates the same silent loss one layer up. The two services running their own queues are also unresolved. Migration gives them the alarms and the dead letter path, and nobody has costed that work or named a quarter for it.
