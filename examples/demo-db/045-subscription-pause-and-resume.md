---
Name: Subscription Pause and Resume
Owner: Sofia Marchetti
Status: Draft
Last Updated: 2025-12-12
---

## Problem

Customers who want to stop paying for three months have one option: cancel. About a fifth of them come back, and when they do they rebuild their configuration from scratch because we delete workspace data ninety days after cancellation.

## Proposal

A pause state that suspends billing without suspending existence.

- Up to three months, self-serve, once per twelve-month period
- Data retained in full, access restricted to export and settings
- Renewal resumes automatically with a reminder a week before
- A paused subscription counts separately in reporting, not as churn and not as active

## Non-goals

No pausing for annual plans in this phase, and no partial pause of individual seats.

## Risks

The reporting change is the one that will cause arguments. Pause sits between two numbers that leadership watches closely, and whichever bucket it lands in, somebody's dashboard moves for reasons unrelated to their work. Agreeing the definition before launch is more important than the feature.

The second risk is cannibalization: customers who would have kept paying choosing to pause instead. We propose measuring this honestly with a holdout rather than assuming the effect is small.

## Metrics

Pause uptake, resume rate at the end of the pause window, and net revenue against the holdout.

## Interfaces Affected

Billing, access control, and the deletion job each need a state they do not have. Billing gains a suspended state that neither cancels the subscription nor raises an invoice, and the renewal job has to skip a paused subscription without recording the skip as a failure. Access control needs a restricted mode where export and settings work and everything else returns a reason rather than a generic permission error. The ninety-day deletion job has to learn that paused is not cancelled, which is the one change where being wrong destroys customer data.

## Support Impact

Pause absorbs contacts that arrive today as cancellations, and creates a smaller set of its own.

- Cancellation requests become pause offers, which needs a script rather than discretion
- Resume reminders raise questions about the charge date in the week before each one
- Customers asking for a second pause inside twelve months, where the rule is firm and the answer has to be the same every time

## Review Notes

Finance accepted the separate reporting bucket on the condition that it is defined and published before the first pause rather than reconciled afterwards, which is the point the risks section makes. The holdout was questioned on size: customers who would have kept paying and choose to pause instead are a smaller effect than uptake, so the holdout needs a longer window than the three-month pause itself.
