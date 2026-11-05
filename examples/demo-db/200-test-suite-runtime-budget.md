---
Name: Test Suite Runtime Budget
Owner: Ben Tsai
Status: Draft
Last Updated: 2025-09-19
---

## Problem

The full suite takes fifty-one minutes, up from eighteen two years ago. Nobody added fifty minutes; everybody added thirty seconds. There is no budget, so there is no moment at which adding a slow test is a decision rather than a default.

## Proposal

A runtime budget per suite with per-test attribution, enforced at the point of change.

- Total budget set at twenty minutes for the blocking suite
- Per-test runtime recorded, with the slowest fifty published
- A change that pushes the suite over budget fails, with the option to move tests to the nightly suite
- A nightly suite for anything genuinely slow and genuinely valuable

## Non-goals

No deletion of tests to meet the budget. Moving a test to nightly is a legitimate answer; removing coverage is not.

## Risks

A budget enforced at the margin punishes whoever adds the test that crosses the line rather than whoever wrote the slow ones already there. Publishing the slowest fifty and dedicating time to them is what makes the budget fair, and without that this becomes a tax on the unlucky.

## Measurement

Blocking suite runtime, tests moved to nightly, and defects escaping to the nightly suite that the blocking suite would have caught.

## Sequencing

Attribution comes well before enforcement. Recording per-test runtime and publishing the slowest fifty costs nobody anything and moves the suite down from fifty-one minutes without a single failed build, because much of the current time sits in a handful of tests nobody has looked at since writing them. Enforcement at fifty-one minutes against a twenty-minute budget fails every change on day one.

- Per-test timing recorded, slowest fifty published weekly
- Dedicated time spent on that list until the suite is near budget
- Nightly suite stood up and shown to report failures someone reads
- Enforcement enabled last, at whatever the suite then runs in

## Operational Impact

The nightly suite needs an owner from the day it exists. A nightly run whose failures nobody triages becomes a place to put tests to die, which turns the move-to-nightly option into the deletion the non-goals rule out. The budget check also has to run on consistent hardware; a shared runner varying by thirty percent makes a pass or fail near the line a coin toss.

## Open Questions

Twenty minutes is asserted, not derived. Nothing here argues for twenty over fifteen or twenty-five, and the choice mostly decides how much of the slowest-fifty work has to land before enforcement can be switched on at all.
