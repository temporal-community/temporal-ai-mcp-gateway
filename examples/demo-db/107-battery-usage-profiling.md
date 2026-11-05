---
Name: Battery Usage Profiling
Owner: Ben Tsai
Status: Draft
Last Updated: 2025-10-19
---

## Background

We have no visibility into our own battery consumption. Complaints arrive through support, are impossible to reproduce, and are closed as unresolved. The background refresh work is proceeding on an assumption about where the drain comes from, which nobody has verified.

## Proposal

Instrument energy-relevant activity and build a profile from the field rather than the lab.

- Wake counts, network calls, and location access recorded per session with durations
- Aggregated by device class and application version, reported weekly
- A lab baseline on three reference devices for comparison against field data
- Per-feature attribution where the platform permits it

## Scope

Measurement only. Remediation follows the findings and is deliberately not scoped yet.

## Risks

Energy instrumentation itself costs energy, and poorly implemented sampling could become a measurable share of what it measures. Sampling rates should be conservative and the overhead should be measured before the data is trusted.

## Measurement

Devices reporting profile data, correlation between profile metrics and platform-reported consumption, and whether the data supports or contradicts the current assumption about background refresh.

## Rollout

Overhead measurement comes before any field data is used. Instrumentation ships to the three reference devices at full sampling, measured against the same devices running an uninstrumented build, and the field rate is set from that difference rather than a guess.

- Internal builds for two weeks, to confirm collection survives background suspension and resumes
- The beta channel next, which gives device spread but skews new and flagship
- Production at a low sample, raised only if the weekly aggregate is too thin to separate device classes

## Support Impact

Battery complaints close as unresolved today and will for a quarter yet, since the profile is aggregate and one complaint cannot be matched against it. What support can do sooner is capture the version and device class on the ticket, which is what makes complaints joinable to the profile at all.

- A complaint template capturing version, device, and background refresh state
- No per-ticket diagnosis promised to a customer until per-feature attribution exists
- The weekly aggregate shared with support, so a cluster on one device class is visible

## Open Questions

- Whether location access is recorded as a count or as time held, which differ sharply when a feature keeps a handle open
- What the profile does with a session ending in a crash, since those are the interesting sessions and have no clean closing record
- Whether the lab baseline uses the three reference devices or the three most common devices in the field, which are not the same list
