---
Name: Performance Regression Testing
Owner: Tom Okafor
Status: Draft
Last Updated: 2025-11-19
---

## Context

Performance regressions are found in production. The last three were each introduced weeks before anyone noticed, and in two cases the responsible change was obvious in hindsight and would have been caught by any measurement at all.

## Proposal

Benchmark the critical paths on every change and fail on significant regression.

- Twelve benchmarks covering the paths that carry most traffic
- Run on dedicated hardware to keep variance low enough to be meaningful
- Comparison against the baseline with a statistical threshold rather than a fixed percentage
- Results published per change, so improvements are visible too

## Scope

Server-side request handling. Client performance needs different instrumentation and is separate.

## Risks

Benchmark variance on shared hardware produces false failures, and false failures train people to re-run until green, which is the flaky test problem transplanted. Dedicated hardware costs money and is the only way this produces a signal anyone trusts.

## Measurement

Regressions caught before merge, false failure rate, benchmark coverage of request volume, and production performance incidents.

## Alternatives Considered

Sampling production latency per deploy and alerting on a shift is cheaper. It catches a regression after it ships, which is where we catch them now, and it cannot attribute the shift to a change when four deploys land in an hour. Running the twelve benchmarks nightly on the main branch halves the hardware and loses the property that matters most: a failure that names the change that caused it. Nightly runs stay as a backstop for paths the twelve do not cover.

## Cost

One dedicated machine per benchmark lane, plus the work to keep the baselines honest.

- Hardware is the whole cost argument, and it is small against one production performance incident
- The baseline is rerun on a schedule, so a drifting machine is detected rather than blamed on a change
- Each benchmark needs an owner, since an unowned benchmark that starts failing gets disabled

## Failure Modes

The one to watch is a true regression that stays under the threshold on every single change and accumulates over twenty of them. A per-change comparison cannot see it, so the baseline also has to be compared against itself across a release window. The other is a benchmark that stops exercising what it claims to after a refactor and keeps passing, which is caught only by checking coverage of request volume rather than counting green runs.
