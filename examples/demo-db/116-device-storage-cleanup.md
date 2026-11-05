---
Name: Device Storage Cleanup
Owner: Hugo Takahashi
Status: Draft
Last Updated: 2026-05-02
---

## Problem

The application's local cache grows without bound. On devices with limited storage this eventually triggers the platform's own cleanup, which deletes our data at an arbitrary moment and produces behavior that looks to the user like data loss.

## Proposal

Manage our own footprint with explicit policy and visible controls.

- A cache budget per category: images, documents, offline content
- Eviction by least recent use within each category, run on a schedule rather than at pressure
- A storage view in settings showing what is held and allowing selective clearing
- Content marked for offline use exempt from automatic eviction and clearly labeled as such

## Scope

The mobile applications. The desktop application has effectively unlimited storage and does not need this.

## Risks

Exempting offline-marked content means a person can mark enough content that the budget cannot be honored, which puts us back where we started with the platform deciding. The exemption needs its own ceiling and a clear message when it is reached.

## Measurement

Storage used per installation at the median and ninety-fifth percentile, platform-triggered cache clears, and reports of missing offline content.

## Data We Have

Total installation size comes from the crash reporter, which samples it on every report, but nothing attributes a cached file to images, documents, or offline content. The budget figures in the proposal are guesses from a handful of instrumented builds, so category attribution has to ship before the budgets do.

- Median installation sits near 900 MB, with the ninety-fifth percentile above 4 GB
- Platform-triggered clears show up only as an unexplained empty cache on next launch
- Offline marking is recorded server-side, so the exempt set is known before the client reports it

## Alternatives Considered

Evicting at storage pressure rather than on a schedule is what the platform already does and what this replaces. It never evicts more than necessary, and it loses on timing: pressure arrives while someone is using the application, and eviction is visible as a stall. The scheduled pass runs backgrounded and idle, at the cost of headroom that goes unused.

## Support Impact

Someone who cannot find a document they expected offline has no way to tell whether it was never downloaded, evicted, or cleared by the platform. The storage view answers the first two by showing what is held. The third stays invisible unless we record a clear when we detect one, which is cheap and turns the hardest conversation support has here into a readable timestamp.
