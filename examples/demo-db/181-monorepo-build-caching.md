---
Name: Monorepo Build Caching
Owner: Yusuf Demir
Status: Draft
Last Updated: 2025-11-12
---

## Background

Every build builds everything. The repository has grown to a point where a one-line change triggers twenty-two minutes of work that produces identical output to the previous run, which is both slow and a meaningful share of our compute bill.

## Proposal

Content-addressed build caching with remote cache sharing.

- Build outputs keyed on the hash of inputs, including toolchain versions
- A shared remote cache, so the first person to build a target pays and nobody else does
- Local cache for iterative work, remote for continuous integration
- Cache correctness verified by periodic full rebuilds compared against cached output

## Scope

The main repository. The two smaller repositories do not have the problem.

## Risks

Incorrect cache keys produce stale artifacts that are extremely difficult to diagnose, because the symptom is a build that is wrong in a way the source does not explain. The periodic verification rebuild is not optional, and it should compare outputs rather than merely confirming the build succeeds.

## Measurement

Median build time for a small change, cache hit rate, build compute cost, and verification mismatches, which must be zero.

## Rollout

A read-only remote cache first: continuous integration writes it, everyone reads from it, no local build writes to it. That confines the correctness risk to one well-understood producer while delivering most of the benefit, because the twenty-two minutes is mostly paid repeatedly in continuous integration rather than on anyone's laptop. Local write access comes later or not at all, since a developer machine with a slightly unusual toolchain is the likeliest source of a poisoned entry.

## Dependencies

- Hermetic builds for every cached target, which several are not: a few steps read the host environment or the clock and will hash differently on every run
- Toolchain versions declared rather than inherited from whatever happens to be installed on the machine
- Cache storage with an eviction policy someone has actually chosen, because the default is growing until the bill is noticed
- A documented way to bypass the cache for one build, which is the first thing anyone will ask for the moment a build looks wrong

## Cost

Storage and egress on the remote cache replace part of the compute bill rather than adding to it, but only while the hit rate is high. The first weeks will look worse than the baseline: the cache is cold, the storage is new, and the verification rebuilds are pure additional compute. Saying so before the first invoice lands is cheaper than explaining it afterwards.
