---
Name: Database Connection Pooling
Owner: Clara Benton
Status: Approved
Last Updated: 2026-06-25
---

## Problem

Each service instance holds its own connection pool sized for peak. As instance counts have grown, the database now spends a meaningful share of its capacity managing connections that are idle, and we have twice hit the connection limit during scaling events rather than during load.

## Proposal

A pooling layer between services and the database, with pool sizing centralized.

- A connection proxy per region, with services connecting through it
- Pool size governed by database capacity rather than by instance count
- Transaction-level pooling where the service's access pattern permits it, session-level where it does not
- Per-service connection quotas, so one service cannot exhaust the pool

## Scope

The primary transactional database. Analytics connections have a different pattern and are separately managed.

## Risks

Transaction-level pooling breaks anything that depends on session state, including prepared statements and advisory locks, and we have at least two services using advisory locks in ways that are not documented. Those need identifying before the mode is chosen per service, not after.

## Measurement

Database connections at peak, connection-limit events, and query latency at the ninety-fifth percentile, watched for regression introduced by the extra hop.

## Sequencing

The advisory lock and prepared statement audit comes before any service moves, because the pooling mode per service is an output of it rather than a configuration choice. Services then move behind the proxy in session-level mode, which changes the connection topology without changing semantics and is where the extra hop gets measured honestly. Transaction-level pooling is enabled afterwards, one service at a time, with the two advisory lock services last or not at all.

## Failure Modes

- The proxy is a single point of failure per region, turning a degraded database into a total outage when it falls over
- A service exhausts its quota and queues, which surfaces as latency rather than the connection error it replaced
- Transaction-level pooling enabled for a service that takes an advisory lock on an undocumented path, where the lock outlives the connection that held it
- Sessions left idle in a transaction, which previously hurt only the instance holding them

## Rollback

Per service and per mode, which is the reason for moving one at a time. A service can be pointed back at the database directly with a configuration change and a restart, taking its own pool back with it. That is a real rollback for the proxy hop and not for the quota: once the other services are sized against database capacity, one service returning to direct connections takes that capacity out of the pool, so a rollback is announced rather than done quietly.
