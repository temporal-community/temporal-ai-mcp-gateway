---
Name: Agent Desktop Shortcuts for Billing Reps
Owner: Nora Sellers
Status: Draft
Last Updated: 2025-11-26
---

## Context

The internal console used by billing reps has grown to forty-one screens. The six screens that cover ninety percent of the work are buried at different depths, and new reps spend their first two weeks learning navigation rather than policy.

## Proposal

A keyboard-driven command bar over the existing console, plus a pinned work surface for the six common tasks.

- One shortcut to open the command bar from anywhere, including inside a form
- Fuzzy search over accounts, invoices, and actions in a single list
- The six common tasks pinned to a persistent sidebar, ordered by the rep's own usage
- Recently viewed accounts kept for the length of a shift

## Non-goals

No redesign of the underlying screens, no changes to permissions, and no new capabilities. This is navigation only.

## Risks

A command bar that can trigger actions as well as navigate is a way to issue a refund by muscle memory on the wrong account. Destructive and financial actions stay behind their existing confirmation screens and are deliberately not shortcut targets.

The second risk is that this papers over the real problem, which is that forty-one screens is too many. The shortcut layer should not become an argument against consolidating them.

## Measurement

Time to complete each of the six common tasks, measured from console open, and ramp time for new reps against the current two-week baseline.

## Rollout

Two pods for the first three weeks, roughly eighteen reps, picked to include the three most tenured and the two newest. The tenured ones will barely touch the command bar because their navigation is already muscle memory, and that is useful information rather than a failed pilot. The newest are where the ramp-time number comes from. Usage-ordered pinning needs a cold-start rule, since a new rep has no usage history; the default should be the pod's aggregate order rather than alphabetical.

## Prior Art

The console already has a search box, added three years ago and used by a handful of reps. That is the strongest argument against assuming this gets adopted on merit. The difference proposed here is that it opens from inside a form, where the existing search requires abandoning whatever is in progress. What reps actually use today is personal bookmark folders holding the same six screens, maintained by each floor lead for their own pod. The pinned sidebar is that folder made shared and official.

## What Would Change Our Mind

If task timings show the six common tasks are slow because of the screens themselves rather than the distance to them, three page loads to apply a credit being the obvious case, then navigation is not the bottleneck and the consolidation work should take priority outright. Timing each task end to end during the pilot, before the sidebar ships, makes that answerable instead of arguable.
