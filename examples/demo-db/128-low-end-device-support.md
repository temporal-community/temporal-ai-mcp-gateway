---
Name: Low-End Device Support
Owner: Sofia Marchetti
Status: In Review
Last Updated: 2026-03-31
---

## Problem

Our minimum supported specification was set three years ago and we test on current flagship hardware. In two of our growth markets the median device in use is well below our test fleet, and our crash and abandonment numbers in those markets are correspondingly worse.

## Proposal

Define a reference low-end device, test on it, and set performance targets against it.

- A reference device chosen from field data rather than from a price point
- Added to the test fleet with the same gating weight as the flagship
- Memory and startup budgets set against it, not against the flagship
- A reduced mode that disables animation and prefetch below a memory threshold

## Scope

The mobile applications in the two markets where this is measurably hurting us, though the targets apply globally once set.

## Risks

A reduced mode is a second experience to design, test, and support, and the temptation will be to let it degrade since few people internally will ever see it. If it is not held to the same quality bar it becomes a worse product for the people with the fewest alternatives.

## Measurement

Crash rate and session length in the two markets against the global baseline, and time to first meaningful render on the reference device.

## Cost

Giving the reference device flagship gating weight roughly doubles device-hours per release on the slowest hardware in the fleet, which is also where a suite takes longest to run. Expect the gating run to move from forty minutes to over an hour unless the suite is split across devices. The units themselves are cheap. The schedule cost is the real one, and it lands on every release rather than once.

## Operational Impact

Crash reports from the two markets arrive today without device context precise enough to separate a memory kill from a defect. Grouping by device class is a prerequisite for the measurement this proposal promises, and it changes triage work: a crash that only reproduces under memory pressure needs the reference device in hand, not a stack trace. Keeping two units with the on-call rotation is the cheapest form of that.

## What Would Change Our Mind

If the crash rate in those markets turns out to be dominated by memory kills rather than defects, the reduced mode is the whole proposal and the test fleet change is secondary. If network conditions dominate instead, neither helps much and the work belongs with request timeouts and offline behavior. The field data that separates these exists and has not been read in this frame.
