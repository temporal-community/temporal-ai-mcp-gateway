---
Name: Dispute Resolution Timelines
Owner: Lena Fischer
Status: Approved
Last Updated: 2026-07-01
---

## Problem

Disputes between buyers and sellers have no published timeline. Cases sit for an average of eleven days, both parties contact support repeatedly during the wait, and the eventual decision frequently surprises one of them because the reasoning is not shared.

## Proposal

Published stages with deadlines, and reasoning given with every decision.

- Three stages with published durations: seller response, review, and decision
- Automatic progression when a deadline passes, defaulting against the party that did not respond
- The decision accompanied by the specific policy clause applied
- An appeal path with a different reviewer, once

## Scope

Marketplace disputes about orders. Payment chargebacks follow the card network timelines and are separate.

## Risks

Defaulting against non-response punishes sellers who are ill, traveling, or in a different time zone, and the deadline has to be long enough to be fair while short enough to matter. Vacation mode should pause the clock, which makes that feature a dependency rather than a nicety.

## Measurement

Time to decision by stage, appeals raised and upheld, contacts to support during an open dispute, and decisions defaulted on non-response.

## Dependencies

Vacation mode is the hard dependency and it does not exist yet. Without it, the deadline defaults against sellers for the one reason everybody considers legitimate. The decision text depends on the policy being written in clauses that can be cited, which parts of it are not; a decision pointing at a whole page rather than a clause recreates the current complaint in a new format. The appeal path needs a reviewer pool deep enough that a different reviewer is always available, which is a staffing constraint before it is a routing one.

## Staffing

Published durations turn review from a queue that absorbs load into a commitment that has to be met on the worst day of the week.

- Review capacity sized for the peak, since a published deadline missed is worse than one never promised
- Appeals handled by a separate rotation, not the same people on a different day
- Decisions written with the clause cited, which takes longer per case than the free-text note it replaces

## Rollout

Publish the timeline for new disputes only. Open cases stay on the current process rather than having a clock started mid-case against a seller who never saw the rule. Automatic progression switches on after one full cycle of published but manually advanced deadlines, so we learn where the eleven days actually sit before a timer starts deciding cases.
