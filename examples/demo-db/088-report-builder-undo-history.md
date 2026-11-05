---
Name: Report Builder Undo History
Owner: Victor Alves
Status: In Review
Last Updated: 2026-05-04
---

## Context

The report builder has no undo. A mis-click that removes a series or changes a grouping is unrecoverable, and the most common support request on the analytics product is some version of asking whether a previous state can be restored.

## Proposal

An edit history per report with named restore points.

- Every edit recorded as a discrete operation, with undo and redo in the builder
- Automatic snapshots at save, retained for ninety days
- Named restore points the author can create before a large change
- History visible to anyone who can edit the report, with the author of each change

## Scope

Report definitions. Dashboard layout has a similar problem and should follow once the model proves out here.

## Risks

Recording every edit as an operation requires the builder's state to be expressible as a sequence of operations, and parts of it currently are not: the filter editor mutates state in place. Refactoring that is most of the work, and if it is not done properly the history will be subtly wrong, which is worse than absent.

## Measurement

Undo use per editing session, support requests to restore a previous state, and reports abandoned mid-edit.

## Sequencing

The filter editor refactor comes first and ships behind no visible change. It is the risk named above, and doing it under an undo feature means a refactor bug arrives looking like an undo bug.

- Filter editor converted to explicit operations, behavior unchanged and covered by tests
- Automatic snapshots at save, which need no operation model and give support something to restore from
- Undo and redo once the operation log is complete across every editor
- Named restore points last, since they are useful only when the history behind them is trustworthy

## Support Impact

Snapshots arriving early is what support feels first: the most common request on the analytics product becomes answerable rather than a conversation about what was lost, worth having a month before undo exists.

- A restore path a responder walks the customer through rather than performs for them
- Retention stated plainly, since ninety days answers some requests and not others
- History showing who made each change, which turns some restore requests into a conversation between colleagues

## Open Questions

- What undo does when two people edit a report, given the history is shared and the operations are not
- Whether a restore counts as an edit on the next person's undo stack or resets it
- Whether ninety days is retention or only the snapshot window, which differ for a report edited daily
- What happens to history when a report is duplicated, since the copy inherits a past it never had
