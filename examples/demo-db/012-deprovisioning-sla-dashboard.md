---
Name: Deprovisioning SLA Dashboard
Owner: Felix Braun
Status: Approved
Last Updated: 2026-06-05
---

## Background

We promise enterprise customers that a deprovisioning request takes effect within an hour. Nobody measures this. When a customer asked for evidence during a renewal, it took three days to assemble an answer, and the answer was worse than the promise.

## Proposal

Measure the full deprovisioning path and show it to customers who are entitled to it.

- A timestamp at each stage: request received, account deactivated, sessions revoked, integrations cut
- Per-customer visibility in the admin console, not an internal dashboard
- Alerting internally when the stage-to-stage time drifts toward the commitment
- The historical record retained for the contractual period

## Scope

Deprovisioning initiated through provisioning integration or admin action. Account deletion requested by the individual follows a different legal path and timeline.

## Risks

Publishing a measurement against a promise means publishing the times we miss it, and the first month will almost certainly show misses we currently do not know about. That is the point, but it should be known internally before it is visible externally.

## Measurement

Share of deprovisioning completed within the commitment, the slowest stage in the path, and renewal conversations where this came up, which is the commercial reason this is funded.

## Sequencing

Instrument first, publish internally, and hold the customer-facing view back for a full month of data. The risks section already expects the first month to show misses, and discovering those in front of a customer mid-renewal is the exact outcome this project exists to prevent. Internal alerting should be on from the first week regardless, because a drift alert on a path nobody has ever measured will fire for instrumentation reasons before it fires for real ones, and that noise is better absorbed early.

## Failure Modes

- A stage with no clean completion event: integrations cut is four integrations reporting differently, and the slowest one defines what the customer actually experienced
- A provisioning integration that retries, producing two requests and two start timestamps for one person
- Clock skew between stage emitters large enough to yield a negative duration, which reads as a broken dashboard rather than as broken clocks
- A corrected or backfilled timestamp changing a published number after a customer has already read it

## Open Questions

What to show for a deprovisioning still in progress and already past the hour. A running clock is the most honest display available and the least comfortable one to put in front of the customer it concerns. Also unresolved: whether the measurement ends at sessions revoked or at integrations cut. The commitment says takes effect, and those two readings differ by minutes in the good case and by much more in the case that matters.
