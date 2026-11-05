---
Name: Rate Limiting at the Gateway
Owner: Hana Kobayashi
Status: In Review
Last Updated: 2026-06-17
---

## Problem

Rate limits are implemented per service, inconsistently, with different windows and different responses. A client hitting a limit gets a different experience depending on which part of the product it touched, and limits that should be per-organization are frequently per-instance, which makes them nearly meaningless under load.

## Proposal

Enforce at the gateway with a shared counter and a consistent response.

- Limits defined per endpoint class and per plan, in one place
- A shared counter so limits apply across instances rather than per instance
- A consistent response with the standard headers, including when the limit resets
- Burst allowance separate from sustained rate, since the two protect against different things

## Scope

The public interface. Internal service-to-service traffic uses quotas rather than rate limits and is unaffected.

## Risks

A shared counter is a dependency in the request path with a tight latency budget, and its failure needs a defined behavior: failing open allows abuse, failing closed causes an outage. The proposal is to fail open with an alarm, which is the right answer for us and should be stated explicitly rather than left as an implementation detail.

## Measurement

Consistency of limit behavior across endpoints, requests rejected by limit, and support contacts about unexpected limiting.

## Migration

The per-service limiters do not come out at once. Each keeps enforcing while the gateway runs alongside it, logging its decision rather than applying it, for two weeks per endpoint class. That shadow period is the only way to find existing limits tighter than the new per-plan numbers, and there will be some: at least two services enforce a limit nobody documented, and a few customers are quietly shaped by it today.

- Gateway decisions logged, not applied, for two weeks per endpoint class
- Local limiters removed only after the gateway has enforced for a full billing cycle
- Undocumented local limits found in the shadow period either written into the per-plan table or dropped on purpose

## Operational Impact

Rejections become attributable for the first time. A customer reporting errors can be matched to a limit and a plan in one lookup instead of by reading service logs. The alarm on counter failure is new load on the same rotation, and its runbook has to say plainly that the system is failing open and abuse is possible until the counter returns, so nobody spends the first ten minutes deciding whether it is urgent.

## Alternatives Considered

Leaving enforcement in the services and standardizing only the response format is cheaper and leaves per-instance counting in place, which is most of the problem. A counter running beside each service avoids the gateway dependency and reintroduces the inconsistency, because each service still decides when to consult it.
