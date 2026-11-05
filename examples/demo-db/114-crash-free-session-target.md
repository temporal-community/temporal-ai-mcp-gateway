---
Name: Crash-Free Session Target
Owner: Dana Whitfield
Status: In Review
Last Updated: 2026-03-13
---

## Context

We report a crash-free session rate of ninety-nine point four percent and treat it as healthy. Broken down by device class, the figure for devices older than four years is ninety-seven point one, which is about eleven thousand people having a bad time every week.

## Proposal

Set the target per device class and fix the distribution rather than the average.

- Crash-free rate reported by device class, memory tier, and platform version
- A target of ninety-nine point three for every class, not for the aggregate
- Release gating on the worst class rather than the overall figure
- The top three crash signatures per class triaged weekly rather than by total volume

## Non-goals

No change to crash reporting infrastructure, which is adequate. This is about which number we look at.

## Risks

Gating releases on the worst-performing class will slow releases, and the first time it blocks something urgent there will be pressure to make an exception. Agreeing the exception process now, in writing, is better than inventing it under pressure.

## Measurement

Crash-free rate by class against target, the gap between best and worst class, and release cadence, watched to see what this costs.

## Sequencing

Reporting by class ships before any gate. Three releases of per-class numbers with nothing enforced gives a baseline for what each class actually reaches and whether ninety-nine point three is attainable on the oldest devices at all. Gating against a target nobody has ever hit stops every release, which is not an argument against the target but is one against enforcing it on day one.

- Per-class reporting live, no gate, three releases
- Weekly triage by class starts immediately, since it needs no gate
- Gate enabled once each class has come within reach of the target at least once

## Failure Modes

Small classes are noisy. The oldest class is a few percent of sessions, so a handful of crashes moves its rate by more than a tenth of a point and a release fails the gate on noise. The gate needs a minimum session count per class, with classes below it reported and not gated. Splitting on three dimensions at once makes this sharper: device class crossed with memory tier crossed with platform version produces buckets holding almost nobody.

## Review Notes

The exception process was raised by two reviewers and is still unwritten. The suggestion on the table is that an exception has to name the class being shipped below target and the date it returns to target, recorded where the next release's gate will show it.
