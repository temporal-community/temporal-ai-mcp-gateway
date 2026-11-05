---
Name: Cross-Region Replication Lag Monitoring
Owner: Sofia Marchetti
Status: In Review
Last Updated: 2026-02-20
---

## Problem

The secondary region's warehouse copy is assumed current. Nothing measures it. During the outage in March it turned out to be nine hours behind, which we discovered while trying to use it, which is the worst possible moment.

## Proposal

Measure replication lag continuously per dataset and alarm on the commitment rather than on the mechanism.

- A heartbeat row written to the primary every minute and read from the secondary
- Per-dataset lag computed from the last replicated partition, not from the connection state
- An alarm threshold derived from each dataset's recovery commitment
- A visible readiness indicator so a failover decision does not require investigation

## Scope

Warehouse replication. Operational database replication is monitored separately and adequately.

## Risks

A heartbeat measures the path the heartbeat takes, which is not necessarily the path every dataset takes. Per-dataset measurement is more work and is the part that actually answers the question, so the heartbeat should not be treated as sufficient once it is green.

## Measurement

Lag per dataset against commitment, time to establish readiness during a drill, and whether the next failover drill produces any surprises.

## Alternatives Considered

- Trusting the replication tool's own lag metric, which reports on its queue and goes to zero the moment a dataset stops being queued at all. That is precisely the failure of March: a healthy mechanism moving nothing.
- Row counts compared across regions, cheap to build and wrong for any dataset that is updated in place rather than appended
- A nightly reconciliation job, which answers the question once a day for a commitment measured in minutes
- Checking lag only at the start of a drill, which is the current practice and is how nine hours went unnoticed

## Failure Modes

The heartbeat writer stops and the secondary's last heartbeat stays fixed, which reads as growing lag and is a monitoring outage rather than a replication one. The two have to be distinguishable or the first week of alarms teaches everyone to discount them. The inverse is worse: a dataset whose partitions stop arriving while the heartbeat keeps flowing, which looks green and is the exact state we are trying to detect.

## Operational Impact

The readiness indicator becomes a thing people quote in an incident, which raises the bar on it considerably. It has to say which datasets are inside commitment and which are not, rather than resolving to a single word, because a failover is usually a decision to proceed without some of them. Thresholds derived per dataset also mean each new warehouse dataset arrives with a commitment or arrives unmonitored, and the default must not be silence.
