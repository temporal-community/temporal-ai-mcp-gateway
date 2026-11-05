---
Name: Welcome Email Sequence
Owner: Lena Fischer
Status: Shipped
Last Updated: 2025-07-11
---

## Context

New accounts received one welcome message and nothing else. The message was written four years ago, describes two features that no longer exist in that form, and had an open rate of about twenty-two percent with negligible click-through.

## Approach

A short behavioral sequence replacing the single message.

- Four messages over two weeks, each triggered by what the account has or has not done
- Content tied to the three actions that correlate with retention, one per message
- Suppression as soon as the relevant action is taken, so nobody is told to do what they did
- A hard stop at two weeks regardless of state

## Non-goals

No promotional content in the sequence, which would have changed its character and its deliverability.

## Risks

Behavioral triggers depend on event accuracy, and sending someone instructions for something they completed yesterday is worse than sending nothing. We required the suppression check at send time rather than at schedule time.

## Outcome

Shipped in June. Open rate across the sequence averages forty-one percent, the three target actions are up between six and fourteen percent in the first week, and unsubscribes are slightly below the previous single message.

## Operational Impact

What used to be one static message is now four templates carrying trigger conditions, so changing the copy is a release rather than an edit. The suppression check also reads the product event stream at send time, which makes a product event rename able to break a trigger quietly. That happened once in August and cost two days of sends to accounts that had already done the thing. The dependency belongs somewhere the event owner will see it, not only in this document.

## Review Notes

- Checking suppression at send time means a slow event pipeline delays a message rather than sending the wrong one, which is the right way round to fail
- The two-week stop is enforced on the schedule rather than on message count, so an account that triggers nothing simply receives nothing after day fourteen
- The forty-one percent open rate is not directly comparable to the old twenty-two percent, since the denominators are different populations

## Open Questions

Whether the lift in the three target actions holds into the second month or is pulling forward actions that would have happened anyway. The measurement as built cannot separate those, and no holdout was run. Also unresolved: what the fourth message should say to an account that completed all three actions in the first two days, which today gets the hard stop and silence.
