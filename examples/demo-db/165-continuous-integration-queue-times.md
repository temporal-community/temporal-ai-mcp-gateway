---
Name: Continuous Integration Queue Times
Owner: Tom Okafor
Status: Approved
Last Updated: 2026-02-19
---

## Problem

The median wait for a build to start is eleven minutes at peak, and the median total time to a result is thirty-four. Engineers context-switch while waiting, which is where most of the real cost is, and the queue is worst in the hours when most people are working.

## Proposal

Add capacity where the queue forms and remove work that does not need to run.

- Runner pool scaled on queue depth rather than on a fixed schedule
- Jobs skipped when the change cannot affect them, determined by path rather than by convention
- The three slowest jobs profiled and parallelized, which covers most of the critical path
- Queue time reported per repository, visible to everyone

## Non-goals

No reduction in what is tested. Skipping by path is about relevance rather than about coverage.

## Risks

Path-based skipping is correct until a dependency is not expressed in paths, at which point a change skips the test that would have caught it. The dependency expression has to be derived from the build graph rather than from a hand-written list, or this will silently reduce coverage.

## Measurement

Queue wait at peak, total time to result, runner cost, and escaped defects in the classes of test that skipping affects.

## Cost

Scaling on queue depth trades runner spend for engineer time, and at peak the trade is obvious: eleven minutes of waiting multiplied across everyone pushing in that window costs more than the instances. Off peak it inverts, which is why scaling on depth rather than on a schedule matters more than the pool size.

- Peak capacity roughly double today's fixed pool, with a floor low enough that nights cost less than now
- Warm instances for the first few slots, since a cold start inside an eleven-minute queue is invisible and a cold start in an empty queue is not
- Skipping cuts total runner minutes, which partly funds the peak capacity rather than adding to it

## Sequencing

Skipping ships last rather than first. It is the cheapest win and the only change that can reduce coverage, so it waits for the build-graph derivation and a shadow period.

- Queue-depth scaling first, reversible and touching nothing about correctness
- The three slow jobs profiled and parallelized second, which shortens the critical path for everyone
- Skipping third, shadowed two weeks: jobs the rule would skip still run, and a failure among them is a defect in the rule

## Review Notes

The platform team asked whether per-repository queue reporting becomes a comparison between teams, and it probably will. The number is dominated by repository size and test count rather than by anything a team chooses day to day, so the report carries both beside the queue time, or the comparison gets made without them.
