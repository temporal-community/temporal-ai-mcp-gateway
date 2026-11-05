---
Name: Load Shedding at the Edge
Owner: Sofia Marchetti
Status: Draft
Last Updated: 2025-12-14
---

## Problem

Under overload, every request is accepted and all of them become slow. The result is a system where nothing works rather than one where most things work, and recovery takes longer because the backlog has to drain before anything improves.

## Proposal

Shed deliberately at the edge, by request class, before the system saturates.

- Request classes defined by what they are: interactive, background, bulk
- Shedding thresholds per class, with bulk shed first and interactive last
- Shed requests receiving a clear retry response with a backoff hint rather than a timeout
- Shedding state visible in the operational view, because silent shedding looks like an outage to everyone else

## Scope

The public request path. Internal service calls have their own backpressure mechanism.

## Risks

Classifying requests requires every caller to be honest about what class its traffic is, and the incentive is to claim interactive. The classification should derive from the endpoint rather than from a header the caller sets, which is less flexible and much harder to game.

## Measurement

Success rate for interactive requests during overload events, time to recovery after a traffic spike, and the share of traffic shed per class during drills.

## Failure Modes

Shedding is itself a system that can be wrong, and two of its failures are worse than the overload they prevent.

- Thresholds set too low shed interactive traffic during a normal peak, which reads from outside as an outage with a polite error body
- A backoff hint clients ignore produces a retry storm, and the edge spends its capacity on rejections
- An endpoint misfiled as interactive is shed last while driving the saturation, which only shows up under load

## Rollout

Classification and per-class counters go on first with shedding disabled, so the class shares can be read for two weeks before any request is rejected. Bulk shedding comes next, with a threshold above the highest observed bulk rate. Interactive shedding is last. Observing first costs a quarter of exposure to overload events; enabling everything at once means the first wrong threshold is found in production.

## Dependencies

Deriving the class from the endpoint depends on a complete endpoint inventory, and anything added since the last routing cleanup has no class. Unclassified traffic has to default somewhere, and defaulting to interactive keeps correctness while leaving open exactly the gap the Risks section describes. The operational view needs the per-class shed counters before interactive shedding is enabled, because without them the on-call responder cannot tell shedding from failure.
