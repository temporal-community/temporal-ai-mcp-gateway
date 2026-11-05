---
Name: Sample Data for New Workspaces
Owner: Dmitri Volkov
Status: In Review
Last Updated: 2026-06-03
---

## Problem

New workspaces cannot evaluate features that need data, which is most of them. Reporting, search, and filtering all appear broken rather than empty, and several interviewees described trying a feature, seeing nothing, and concluding it did not work.

## Proposal

Optional sample data, clearly marked, removable in one action.

- A realistic sample set per use case, aligned with the template gallery
- Visually distinct so nobody mistakes it for their own content
- Removal in one action, complete and immediate, with no residue in reports
- Automatically offered for removal once the workspace has its own content

## Non-goals

No sample data by default. It has to be chosen, because a workspace that did not ask for it will experience it as mess.

## Risks

Sample data that lingers pollutes the workspace's own reporting and, worse, can be shared externally by someone who did not realize it was sample. The automatic removal offer matters, and the visual distinction has to survive export and print.

## Measurement

Sample data adoption at creation, feature trial rate for workspaces with and without it, removal rate, and any instance of sample data appearing in an export.

## Failure Modes

Removal that is complete and immediate is the hard promise here. Once a workspace builds its own objects on top of the sample set, a saved filter pointing at a sample field or a report grouped on a value only sample rows carry, deleting the samples leaves the workspace broken rather than clean. The two honest options are to refuse removal until those references are resolved, or to remove and repair while naming exactly what changed. Both are worse experiences than the promise and both are better than silent breakage.

## Interfaces Affected

- Workspace creation, which gains a choice and therefore a step, in the flow least tolerant of extra steps
- Export and print, where the visual distinction has to survive rather than being a treatment that exists only in the app
- Reporting, which needs to exclude or label sample rows without asking each report to opt in
- The template gallery, whose use-case list becomes the contract for which sample sets exist

## Open Questions

Whether a collaborator invited into a workspace that still has sample data sees the same marking, or whether the marking is only legible to the person who chose it. Also unsettled: whether the removal offer fires on the first piece of real content, which is eager and will annoy people mid-evaluation, or on a threshold nobody has proposed a number for yet.
