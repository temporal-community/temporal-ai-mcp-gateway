---
Name: Cold Start Time Budget
Owner: Hana Kobayashi
Status: In Review
Last Updated: 2026-05-26
---

## Problem

Cold start has drifted from one point two seconds to three point four over eighteen months. No single change caused it; each release added a little initialization work, and nothing measured the cumulative effect until the number became embarrassing.

## Proposal

A measured budget with per-component allocation and enforcement in the pipeline.

- Startup path instrumented by phase, with attribution per initializer
- A total budget set at one point five seconds, allocated to components by negotiation
- Regression beyond the allocation fails the build rather than filing a ticket
- Lazy initialization for anything not needed before first meaningful render

## Non-goals

No architectural change in this phase. If the budget cannot be met by deferring work, that is a finding worth having before anyone starts rewriting.

## Risks

Budgets are enforced where they are measured, and measuring on reference hardware tells us little about the low-end devices where startup actually hurts. The budget should be set on a device representative of the slower half of our installed base, which will make the number look worse and the work more valuable.

## Measurement

Cold start at the median and ninety-fifth percentile per device class, abandonment during startup, and whether the budget holds for two quarters without exemptions.

## Sequencing

Instrumentation and attribution first, with the current per-initializer numbers published and no budget attached. Letting teams see what their own initializer costs is the cheapest intervention available and usually moves the number before any rule does. Allocation is a negotiation and should happen with those numbers already on the table, because allocating in the abstract produces either an even split nobody can meet or a scramble for headroom. Build enforcement goes last, after one release has run with the budget published and advisory.

## Operational Impact

A build that fails on a startup regression often fails for a reason its author did not cause: a shared initializer growing pushes several components over at once. The failure has to name the initializer and its delta rather than report a total, or the first week of enforcement is spent bisecting. An exemption path is also required, with an expiry and a named approver, since the alternative to a documented exemption is an undocumented one. Measuring on representative hardware means real devices in the pipeline, which brings its own failures that belong to the rack rather than to the code.

## What Would Change Our Mind

If attribution shows the drift concentrated in one or two initializers rather than spread thin, the budget machinery is heavier than the problem and two focused fixes recover the number. The reverse result is the one that matters more: if the work genuinely cannot be deferred to meet one point five seconds, the non-goal on architecture stops being a scoping choice and becomes the finding this phase exists to produce.
