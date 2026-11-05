---
Name: Build Reproducibility
Owner: Ines Duarte
Status: Draft
Last Updated: 2025-12-08
---

## Problem

Building the same commit twice produces different artifacts. The differences are timestamps and path embedding rather than anything behavioral, but it means we cannot verify that a deployed artifact corresponds to the source we think it does, which matters for both security review and incident investigation.

## Proposal

Make builds byte-identical for identical inputs.

- Timestamps normalized, build paths made relative, and locale pinned
- Toolchain versions pinned and recorded in the artifact metadata
- A verification build run independently and compared, on every release
- Artifact provenance recorded, linking artifact to commit and build environment

## Scope

Server-side artifacts. Mobile builds involve platform signing and are a separate problem.

## Risks

Reproducibility is achievable and then continuously broken by ordinary changes, because the ways to introduce nondeterminism are numerous and unobvious. The verification build is what keeps it true, and it has to run always rather than when someone remembers.

## Measurement

Share of releases with a verified reproducible build, time to trace a deployed artifact to its source, and verification failures per month.

## Sequencing

Provenance first, reproducibility second. Recording which commit and build environment produced an artifact is useful on its own during an incident, needs no normalization, and makes a verification failure diagnosable rather than merely red.

- Provenance metadata including toolchain versions on every artifact, first two weeks
- Normalization service by service, starting with the three on the security review path
- Verification enabled per service once it reproduces twice in a row, rather than globally and then muted

## Cost

A verification build doubles build time per release rather than per change. Our cadence is about forty releases a month, comfortably inside existing capacity. The ongoing cost is different in kind: every verification failure is an investigation, and in the first months most will be nondeterminism nobody knew about.

## Operational Impact

The verification build becomes a release gate, so a failure can block a release for a reason unrelated to the change being released. That is the point, and it will be unpopular the first time it lands during an incident fix. The override is logged with who used it and why, which makes overrides countable rather than habitual.

- The release pipeline reports the comparison beside test results
- Provenance queryable from the deploy record, since an incident starts from a running version, not a commit
- Pinned toolchains become an upgrade obligation, a recurring task that will be forgotten unless owned
