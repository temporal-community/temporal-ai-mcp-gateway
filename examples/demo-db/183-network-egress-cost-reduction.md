---
Name: Network Egress Cost Reduction
Owner: Dana Whitfield
Status: Draft
Last Updated: 2025-11-30
---

## Problem

Egress is the second largest line in the infrastructure bill and has grown faster than traffic. Nobody has analyzed where it goes; the assumption has been that it is customer downloads, and a quick sample suggests that assumption is wrong.

## Proposal

Measure egress by destination and by service, then act on the largest contributors.

- Flow analysis attributing egress to service, destination, and content type
- Cross-region service chatter identified separately, since that is suspected to be large and is entirely ours
- Compression and format review for the top content types
- A cost attribution report per team, aligned with how compute cost is already reported

## Non-goals

No architectural change in this phase. Several likely remedies involve moving services between regions, which is a larger decision needing this data first.

## Risks

Flow analysis at this granularity is itself expensive and can affect the data path if done carelessly. Sampling rather than full capture is sufficient for attribution and should be the default, with full capture reserved for a specific question.

## Measurement

Egress attributed to a service and destination, egress per thousand requests, and total egress cost against the trend line.

## Sequencing

Flow sampling comes first and runs for a full billing cycle before anything is concluded from it. Egress has a weekly shape and a month-end shape, and a two-week sample would misattribute whichever one it misses. Cross-region chatter is broken out in the same pass rather than a later one, because separating it afterwards means re-deriving destination ranges from flow records that no longer exist at that granularity.

- Sampling live and validated against the billed total within five percent
- Attribution report per team, then two weeks for teams to correct their own mappings
- Compression and format review on the top three content types only

## Cost

Sampled capture costs roughly a tenth of a percent of the egress line at a one-in-a-thousand rate, which is the rate attribution needs for anything above a terabyte a month. Smaller services sit below the noise floor at that rate and will be reported as a single unattributed bucket rather than guessed at. Raising the rate to resolve them would cost more than those services spend.

## Dependencies

The per-team report reuses the compute cost attribution pipeline, which keys on the service registry's ownership field. That field is stale for about a fifth of services, and egress attribution will inherit every one of those errors. Correcting the registry is out of scope here, so the report has to show the ownership source and its last-updated date, letting a team that disputes a number know where to go.
