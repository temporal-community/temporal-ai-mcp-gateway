---
Name: Offline Draft Sync
Owner: Victor Alves
Status: In Review
Last Updated: 2026-04-30
---

## Problem

Drafts written without a connection are held in memory and lost if the application is killed, which on constrained devices happens routinely. We receive this report weekly and it is always from someone who was writing something long on a train.

## Proposal

Persist drafts locally and reconcile them on reconnection.

- Local persistence on every pause, not on an interval
- Conflict resolution that presents both versions rather than choosing, since drafts are not mergeable in any way the user would accept
- A visible sync state per draft: local only, syncing, synced
- Drafts retained locally for thirty days after sync, in case the server copy is wrong

## Scope

Text drafts. Attachments have a separate upload queue and a different failure profile.

## Risks

Showing both versions on conflict is the honest behavior and also the one people dislike, because they want us to know which is right. The alternative is losing work silently, which we have been doing, and which generates far angrier reports.

Storage on constrained devices is finite, and a thirty-day retention of long drafts could become a meaningful share of the application's footprint. The cleanup policy needs to exist before launch rather than after the first complaint.

## Measurement

Reports of lost drafts, conflicts presented per thousand syncs, and the share of drafts that complete to a published state after an offline period.

## Failure Modes

Persisting on every pause assumes the application is given enough time to write before it is killed, which on a constrained device under memory pressure is not guaranteed. A draft killed mid-write has to be detected as truncated rather than restored as if it were complete, so each local record carries a completion marker written last.

- A truncated record restores the previous complete one and reports the gap
- A device that fills its storage mid-session stops persisting and must say so, since silent failure here reproduces the original problem
- A draft that has been in syncing state for more than one connected minute is treated as failed and returned to local only
- Clock skew on the device makes local timestamps unusable for ordering, so conflict detection uses the server revision the draft was based on

## Cleanup Policy

Thirty-day retention is a ceiling, not a guarantee. Local copies are evicted oldest first once the drafts store passes its share of the footprint budget, and a draft that has synced is evicted before one that has not. Evicting a synced copy loses the fallback the retention was for, which is the cost of bounding the footprint on devices where the alternative is the operating system reclaiming the whole application.

## Review Notes

The open item from review is the conflict presentation itself. Both versions shown side by side is agreed; what is not agreed is whether the user has to resolve before continuing to write, or can keep the local version live and defer the decision. Forcing resolution keeps the store simple and interrupts someone mid-sentence.
