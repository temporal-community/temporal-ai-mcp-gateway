---
Name: Shared Component Library Adoption
Owner: Maya Brennan
Status: Draft
Last Updated: 2025-10-14
---

## Problem

The component library covers most of what product surfaces need, and adoption is about forty percent. Teams reimplement components locally, usually because the shared one was missing a variant at the moment they needed it, and then the local version drifts.

## Proposal

Close the gaps that drive reimplementation, then migrate the duplicates.

- An audit of local implementations to find which shared components are inadequate
- The top gaps closed first, since those are the reasons people leave
- A contribution path with a stated review turnaround, so adding a variant is faster than forking
- Duplicates migrated team by team, with the local version deleted rather than deprecated

## Scope

Web product surfaces. The marketing site has different constraints and is deliberately excluded.

## Risks

Migration without closing the gaps first produces exactly the same reimplementation six months later, with more resentment. The audit is the important half of this work and the half that will feel like it is not making progress.

## Measurement

Component usage from the shared library as a share of rendered components, local implementations remaining, and contribution turnaround time.

## Data We Have

Rendered component telemetry already separates shared from local, which is where the forty percent comes from, and it can name surfaces rather than only the total. The audit needs the one thing telemetry cannot give: why each local version exists, which comes only from asking whoever wrote it.

- Local implementations by component type, which ranks the gaps before anyone opens a file
- Commit dates on the local versions, since one written last month is a live gap and one from two years ago may be inertia
- Contribution history to the shared library, about two merges a month, which is the baseline a turnaround commitment has to beat

## Staffing

The audit is four weeks for one engineer, most of it conversations rather than code. Closing the top gaps is the larger number and cannot be sized until the audit names them. Contribution turnaround is the part needing permanent staffing: a stated review time with nobody committed to it becomes a longer wait than forking, and that is exactly the comparison a team makes in the moment.

## Timeline

Audit through the first four weeks, gap closure through the following quarter, migration starting only once the three most-reimplemented components have shipped their missing variants. Migration runs team by team with no deadline, because a deadline pushes teams to delete the local version and keep its behavior by overriding the shared one, which is the same drift under a different name.
