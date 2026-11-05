---
Name: Code Review Turnaround
Owner: Clara Benton
Status: Approved
Last Updated: 2026-04-23
---

## Problem

The median time from ready-for-review to first comment is nineteen hours, and the distribution has a long tail: about a tenth of changes wait more than three days. The delay is not reviewer workload so much as reviewer selection, since changes frequently sit unassigned.

## Proposal

Assign reviewers deliberately and surface what is waiting.

- Reviewer assignment from ownership and recent familiarity with the touched code, not round robin
- An AI summary attached to each change describing what it does and flagging the parts that warrant attention, so a reviewer can decide quickly whether they are the right person
- A team view of changes waiting, ordered by wait time rather than by creation
- A nudge at twenty-four hours to the assigned reviewer, and at forty-eight to the team

## Non-goals

No required review count change, and no automated approval of any kind.

## Risks

A generated summary of a change is a description of the diff, not an understanding of it, and a reviewer who reads the summary instead of the code is worse than no reviewer. The summary should describe and point, never assess, and we should watch review depth rather than assuming it holds.

## Measurement

Time to first comment at median and ninetieth percentile, changes waiting over forty-eight hours, and review depth measured by comments per changed line, watched for decline.

## Sequencing

Assignment and the waiting view ship first and are independent of everything else. If unassigned changes are the real cause, the nineteen-hour median should move on those two alone, and that result is worth having before the generated summary is built.

The nudges wait a month after that. A nudge on top of an assignment that is still frequently wrong trains people to ignore the notification, and a notification people ignore is hard to make matter again.

The summary ships last and ships off by default, enabled per team. Teams that opt in give us the review-depth comparison against teams that have not, which is the only honest read on whether the summary is being read instead of the code.

## Alternatives Considered

A review rotation with a daily duty reviewer was the obvious alternative and was rejected because it discards familiarity with the touched code, which is what makes a review fast as well as good. A service-level target on time to first comment was rejected for the opposite reason: it would move the median by producing shallow first comments, and the ninetieth percentile would not move at all.

## Data We Have

The nineteen-hour median and the three-day tail come from the last two quarters of review history, which also records who was assigned and when. Comments per changed line is available over the same window, so the review-depth baseline exists before any change ships. What we do not have is why a given reviewer was chosen, since round-robin assignments and deliberate ones are not distinguishable in the history.
