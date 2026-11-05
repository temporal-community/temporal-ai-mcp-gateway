---
Name: Login Rate Limits by Region
Owner: Erin Vasquez
Status: Draft
Last Updated: 2025-11-11
---

## Context

Sign-in rate limits are global and tuned for our largest market. In smaller markets the same thresholds are too loose to stop credential stuffing, and behind large shared networks they are too tight and lock out legitimate users in bursts.

## Proposal

Per-region thresholds derived from observed traffic, with a separate and stricter path for failure bursts.

- Limits computed per region from a trailing baseline, reviewed monthly rather than set once
- Failure-rate limiting separated from request-rate limiting, since the two signal different things
- Shared-network ranges identified and given their own threshold rather than being penalized
- Limits applied per account as well as per source, because stuffing distributes

## Scope

Sign-in endpoints. Password reset and registration have their own abuse patterns and deserve their own analysis.

## Risks

Derived thresholds move with traffic, which means an attack large enough to shift the baseline can raise its own limit. The baseline should be computed from traffic that succeeded, not from all traffic, and there needs to be a ceiling that does not move automatically.

## Measurement

Credential stuffing attempts blocked per region, legitimate sign-ins rejected by rate limit, and the ratio between them, which is the only number that really matters here.

## Data We Have

Sign-in logs carry source address, result, and account for thirteen months, enough to compute a trailing baseline per region today with no new instrumentation. What the logs do not carry is whether a source is a shared network, so that identification depends on an external list refreshed quarterly and reliably wrong at the edges: corporate ranges that recently changed provider look residential for weeks.

- Per-region successful sign-in rates are computable now at hourly resolution
- Failure bursts are already distinguishable from request bursts
- Shared-network attribution is the only input with no in-house source

## Operational Impact

A monthly review is a recurring task with no deadline pressure until it is skipped twice and a region's thresholds are a year stale. The review should produce a diff of proposed thresholds against current ones rather than a dashboard, because a diff gets approved in ten minutes and a dashboard gets opened once there is already an incident. Lockout reports reaching support need the region and the limit that fired attached, or the responder debugs sign-in instead of the threshold.

## Rollback

Each region reverts to the current global thresholds independently, with no data migration and no client change. The ceiling is the part that cannot be undone in a hurry: lowering it while stuffing is in progress drops legitimate sign-ins alongside the attack, and raising it back takes a deploy. Set the ceiling before the per-region limits ship rather than during the first incident that tests it.
