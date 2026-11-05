---
Name: Dunning Retry Schedule Overhaul
Owner: Marcus Reyes
Status: Approved
Last Updated: 2026-01-23
---

## Problem

Failed renewal payments are the largest source of involuntary churn on self-serve plans. The retry schedule has not changed since the original billing build: a declined card is retried four times over six days on a fixed cadence, regardless of the decline code, the amount, or the customer's history.

## What we will build

A decline-code-aware policy table, owned by billing, that decides when and whether to retry.

- Hard declines stop after one attempt and move straight to recovery
- Soft declines retry on a widening curve tuned per issuer region
- Retry windows shift into local business hours for the billing address
- Every attempt writes a structured outcome record for later analysis

## Rollout

Two weeks in shadow, scoring what the new policy would have done against what the old one did. Then ten percent of monthly plans, then everything except enterprise, which keeps the legacy path because those renewals are handled by a human anyway.

## Open questions

Issuer behavior varies more than our data explains, so the tuned curves may not hold outside the three regions with enough volume to measure. The policy table is also a new moving part, and a careless edit could suppress retries silently, so it ships behind review with an alarm on attempt volume.

## Measurement

Recovered revenue per failed charge over a trailing thirty days, with involuntary churn and support contact rate as guardrails.

## Data We Have

Eighteen months of attempt history exists, but not in a usable shape: the outcome is stored as the gateway's raw response string, so decline codes have to be parsed out rather than read from a column. The structured outcome record fixes that going forward, while the shadow period depends on parsing the past, and the parser is the first thing to get wrong.

- Decline codes recoverable for roughly ninety percent of historical attempts, the rest from one gateway version that logged differently
- Recovery outcomes joinable to the attempt, which is what lets shadow scoring compare policies rather than guess
- Issuer region derivable from card metadata we already retain, well for the three regions with volume and thinly elsewhere

## Support Impact

A customer whose card declines hears from us before they hear from their bank, and the retry schedule decides when. Shifting retries into local business hours means the notification lands when someone can act on it, and the resulting support contact arrives during the day rather than overnight.

- Hard declines reaching recovery after one attempt produce earlier contacts, which is better but is a change in pattern
- The outcome record gives a responder the actual decline reason instead of a generic failure message
- Enterprise stays on the legacy path, so a responder has to know which path an account is on before explaining the schedule

## Failure Modes

A curve tuned on a region's good months is the subtle failure. Issuer behavior shifts with their own risk settings, so a curve that was right in March can be wrong by September with nothing in our data saying so. Scoring the live policy against the old one for a quarter after full rollout costs nothing and is the only way to notice.
