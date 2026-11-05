---
Name: Blue-Green Deploy for the API
Owner: Grace Lindqvist
Status: In Review
Last Updated: 2026-03-21
---

## Problem

Deploys are rolling, which means a deploy and a rollback both take eleven minutes to propagate. During a bad deploy, those eleven minutes are the incident, and the shape of the rolling window makes the error rate ambiguous while it is happening.

## Proposal

Blue-green deployment with an instant switch and a held previous environment.

- Full environment deployed and verified before any traffic moves
- Switch at the load balancer, complete within seconds
- Previous environment held warm for thirty minutes, so rollback is also a switch
- Database migrations decoupled from deploys, with compatibility required in both directions

## Scope

The public interface service. Background workers have different characteristics and should be considered separately.

## Risks

The migration requirement is the real work. Backward and forward compatible migrations are a discipline the team does not currently practice, and blue-green without it is a trap: the switch is instant and the rollback is impossible. This proposal is only sound if the migration discipline lands first.

## Measurement

Time to roll back, duration of deploy-related incidents, and the share of migrations that are verifiably compatible in both directions.

## Sequencing

Migration discipline ships first and alone: expand-then-contract as the only accepted pattern, a check that rejects a migration dropping or renaming a column in the same release that stops writing it, and a full quarter of migrations shipped that way before any traffic switches. Built in the other order this is worse than what we have, because an eleven-minute rollback that works beats a two-second rollback that does not.

## Cost

Holding the previous environment warm for thirty minutes doubles the footprint of the public interface service for that window, which at roughly nine deploys a week is a few hours of double capacity and is the cheap part. The expensive part is that the new environment must be sized for full production traffic at the instant of the switch, with no ramp. Connection pools, caches, and anything that performs badly cold have to be warm before the switch, which is work that rolling deploys never required.

## Failure Modes

- A cold cache on the new environment, turning an instant switch into a latency incident with no error rate to point at
- Long-lived connections still pinned to the old environment, so draining is gradual even though switching is not
- A migration compatible in both directions on paper but not in practice, discovered at the moment rollback is needed
- The thirty-minute hold expiring while an incident is still being debated, which removes the rollback path at the worst moment
