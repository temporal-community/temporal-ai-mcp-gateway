---
Name: Incident Severity Definitions
Owner: Tom Okafor
Status: In Review
Last Updated: 2026-01-21
---

## Problem

Severity is assigned by whoever declares the incident, against definitions that describe impact in vague terms. The same event has been declared at two different levels by two different people in the same month, which makes our incident statistics unusable for trend analysis.

## Proposal

Definitions expressed in measurable terms, with worked examples.

- Each level defined by customer impact with a threshold: requests affected, revenue at risk, or data integrity
- Ten worked examples from our own history, each assigned and explained
- Severity reassessed at the first update rather than fixed at declaration
- A default when the impact is unknown, which is to assume the higher level until measured

## Non-goals

No change to response procedures, which are adequate. This is about the label and the consistency of the label.

## Risks

Severity labels carry social weight: declaring high severity wakes people, and people hesitate to do that. Definitions alone do not fix hesitation. Making reassessment normal and explicitly blameless is what gives people permission to start high.

## Measurement

Variance in severity for comparable events, time from detection to declaration, and reassessment frequency, which should be non-zero if the default is working.

## Migration

Past incidents are not relabelled. Rescoring two years of severities would improve the statistics and destroy the one thing they record honestly, which is how people judged events at the time. Trend analysis starts at the date the definitions land, with the old series kept and marked as scored under the previous wording.

- The ten worked examples scored under both schemes, so the discontinuity is visible rather than hidden
- Dashboards drawing a break at the cutover instead of one continuous series
- The old definitions kept readable, since earlier postmortems reference them

## Review Notes

On-call objected to the unknown-impact default: assuming the higher level wakes people for events that turn out minor, and waking people has a cost the proposal does not price. The answer was that reassessment at the first update caps that cost at about fifteen minutes of someone's attention, while a high-impact event sitting under a low label costs an unbounded amount. That answer holds only if reassessment is genuinely routine, which is the thing to watch.

## What Would Change Our Mind

If variance between comparable events has not fallen within two quarters, the thresholds are the problem rather than the wording. The likeliest cause is that requests affected is unknowable at declaration, so people fall back on judgment and the definition does no work. The fix is then to define severity on signals available in the first five minutes, even cruder ones, rather than on numbers that are only accurate in hindsight.
