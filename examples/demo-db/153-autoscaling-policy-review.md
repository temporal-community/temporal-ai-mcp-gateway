---
Name: Autoscaling Policy Review
Owner: Yusuf Demir
Status: In Review
Last Updated: 2026-05-13
---

## Context

Autoscaling policies were set per service by whoever created the service. Thresholds vary between twenty and eighty percent utilization with no rationale recorded, and several services scale on a metric that does not correlate with their actual bottleneck.

## Proposal

Review every policy against the service's real constraint and standardize where the shape is common.

- Each service's bottleneck identified by load test rather than assumed
- Scaling metric chosen to match the bottleneck, which for several services means queue depth rather than processor use
- Standard policy shapes offered for the three common patterns, with deviation requiring a reason
- Scale-down behavior reviewed separately, since that is where the incidents come from

## Non-goals

No change to capacity floors, which are a cost conversation and should be held separately with their own data.

## Risks

Scale-down is where aggressive policies cause harm, and the damage appears as latency during a traffic trough rather than as an obvious failure. Reviewing scale-down with the same attention as scale-up is the part most likely to be skipped for time.

## Measurement

Services scaling on a validated metric, scaling-related incidents per quarter, and compute cost, which should fall slightly as over-provisioned floors are corrected.

## Dependencies

Load testing every service needs a test environment that reproduces production's data shape, and ours does not for the four largest: their datasets are sampled down to a size where the bottleneck moves. Those four have to take their bottleneck from production observation under natural peak instead, which is slower and less precise. That is good enough for choosing a metric and not for setting a threshold, so they get a conservative threshold and a note saying why.

- Queue depth is not exported as a scaling signal today for two of the services that need it
- Standard policy shapes need somewhere to live that service definitions can reference
- Load test environment work is a prerequisite only for the smaller services

## Sequencing

Metric correction comes before threshold tuning. A service scaling on the wrong metric has a threshold that means nothing, and tuning it first does the work twice. The scale-down review runs as its own pass rather than as the second half of each service's review, so it does not get compressed when the schedule slips.

## Review Notes

The twenty-to-eighty spread reads worse than it is. Several low thresholds belong to services with long warm-up times, where scaling early is correct and the rationale was simply never written down. The review should record the reason for every threshold it keeps, not only for the ones it changes.
