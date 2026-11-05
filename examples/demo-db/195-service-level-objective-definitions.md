---
Name: Service Level Objective Definitions
Owner: Dmitri Volkov
Status: Draft
Last Updated: 2026-01-07
---

## Context

We have an availability number in our enterprise contracts and no internal objective that corresponds to it. Teams make their own judgments about what is acceptable, which means the services behind the contract are held to a lower standard than the contract requires and nobody has noticed because nothing measures it end to end.

## Proposal

Objectives defined per customer journey rather than per service, with error budgets derived from them.

- Six journeys with latency and availability objectives, measured at the edge
- Per-service objectives derived from the journey objectives and the dependency chain
- Error budget tracked per journey with a monthly reset, visible to every contributing team
- Contractual commitments mapped to journey objectives so the relationship is explicit

## Non-goals

No budget enforcement policy in this phase. Defining what happens when a budget is exhausted is a separate conversation that needs the measurement first.

## Risks

Deriving service objectives from journey objectives produces numbers that look arbitrary to the service team and are hard to argue with, which breeds resentment rather than ownership. Deriving them collaboratively, with the dependency chain visible, is slower and necessary.

## Measurement

Journeys with a defined objective, budget consumption per journey, and whether contractual commitments are now provably met rather than assumed.

## Prior Art

Two teams already keep their own availability targets, written down and tracked honestly, and both measure at their own service boundary. That is the pattern worth borrowing and the reason the journey framing is necessary: a request can traverse four services each comfortably inside its own target and still miss at the edge, because the failures compound and the latencies add. Neither team is wrong about its own number. The gap is that nobody owns the sum, which is exactly what the contract commits to.

## Staffing

The derivation is the expensive part. Mapping six journeys onto the dependency chain and agreeing per-service numbers with each contributing team is a few weeks of meetings, not a dashboard build, and it needs someone with the standing to settle a disagreement about where a budget belongs. The ongoing cost afterwards is smaller but is not zero: budgets reset monthly, journeys change as the product changes, and a stale objective is worse than none because it is quoted with confidence.

## Open Questions

Where the edge measurement actually sits. Measuring at the load balancer excludes client-side time that customers unquestionably experience, and measuring in the client introduces a population we cannot control and a reporting path that itself fails. The contractual language does not settle it.

- Whether a journey with two contributing teams has one budget or two views of one budget
- How a shared dependency's consumption is attributed when it degrades several journeys at once
- What happens to the monthly reset during an incident spanning the boundary
