---
Name: Secrets Management Rotation
Owner: Ruth Adeyemi
Status: In Review
Last Updated: 2026-01-14
---

## Problem

Secrets live in the secret store, which is correct, and are never rotated, which is not. Rotation requires coordinated changes in several services, nobody owns the coordination, and so it does not happen. Several database passwords predate the current team.

## Proposal

Make rotation routine by making it possible without coordination.

- Dual-secret support in every consumer, so old and new are valid simultaneously during a rotation
- Rotation driven by the store on a schedule, not by a person on a ticket
- Consumers reloading on change rather than on restart, which several currently require
- An inventory with age per secret, visible to the owning team

## Scope

Service credentials and database passwords. Customer-held credentials follow the separate key rotation work.

## Risks

Dual-secret support has to land in every consumer before any automatic rotation begins, and a single consumer that cannot reload turns a routine rotation into an outage. The inventory should refuse to mark a secret as rotatable until its consumers are verified, rather than assuming readiness.

## Measurement

Secrets with dual-secret consumers, median secret age, and rotations completed without incident.

## Sequencing

The inventory comes first and is useful on its own: age per secret with the owning team named turns a vague concern into a list someone can work through. Dual-secret support lands per consumer afterwards, ordered by the age of the secret rather than by how easy the consumer is to change. The oldest database passwords belong to the services least likely to support reload, so doing the easy ones first would produce good coverage numbers and leave the actual risk untouched.

- Inventory with age and owner, published
- Dual-secret and reload support per consumer, oldest secret first
- Automatic rotation enabled per secret once every consumer is verified

## Failure Modes

A consumer that reads its secret once at startup and caches it keeps working through a rotation and fails at its next restart, perhaps weeks later, with nothing linking the failure to the rotation that caused it. Verification has to exercise a reload rather than check a configuration flag. The other case is the consumer nobody knows about: a scheduled job holding a copy of the credential outside the store, which no inventory will list because it was never registered.

## Rollback

Dual validity is the rollback. For the length of the overlap window the previous secret still works, so an aborted rotation is a matter of not promoting the new one. Once the window closes there is no rollback, only a forward rotation, which makes that window length a safety parameter rather than an implementation detail.
