---
Name: Churn Signals in Cancellation Reasons
Owner: Caleb Mortensen
Status: Draft
Last Updated: 2025-10-22
---

## Background

Cancellation asks for a reason from a list of six, with an optional comment. The list was written at launch, the most selected option is other, and the comments are read by nobody in particular.

## Proposal

Rewrite the list from the comments, and route what we learn to someone who can act.

- A new list derived from a classification of the last year of free-text comments
- Other retained but placed last, with a required comment when selected
- Reasons reported monthly to the product teams whose area they implicate
- A follow-up offer only where it is genuinely relevant, not as a retention reflex

## Non-goals

No retention offers in the cancellation flow beyond what exists. Making cancellation harder is not on the table.

## Risks

Stated reasons are not real reasons. People choose the least confrontational option, and price is selected when the real answer is that the product did not work for them. Treating the list as evidence rather than as a weak signal would send product teams after the wrong problems.

## Measurement

Share selecting other, comment rate, and whether reasons correlate with anything observable in usage before cancellation, which is the only way to know if they mean anything.

## Data We Have

A year of free-text comments is the input to the new list, and it is thinner than the cancellation volume suggests.

- Roughly four in ten cancellations leave a comment, and comments skew to the angry and the loyal
- Usage history exists for every cancelled account, which is what lets a stated reason be checked against behavior
- Account age and plan are attached, so the list can differ by segment if the comments say it should

The accounts that leave silently are the gap, and they are the majority. Nothing here learns anything about them, which is worth saying before a monthly report starts being read as the reasons people leave.

## Sequencing

The classification pass over last year's comments comes first and produces the list. Writing the list from what we expect to find would repeat the launch-day mistake. The monthly report to product teams waits for three months of data under the new list, since a report built on one month of a new question gets argued with rather than acted on.

## Open Questions

Whether a required comment on other produces a comment or just a different selection. Making it required moves people off other, and that movement is not information. We have also not settled who owns the list afterwards: a list never revised is the problem being fixed, and a list revised often cannot be compared month to month.
