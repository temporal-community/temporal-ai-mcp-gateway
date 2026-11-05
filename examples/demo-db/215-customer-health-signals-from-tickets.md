---
Name: Customer Health Signals from Tickets
Owner: Sofia Marchetti
Status: Draft
Last Updated: 2026-02-23
---

## Context

Account teams learn that a customer is unhappy when the customer tells them, usually at renewal. The support history frequently shows it months earlier: rising volume, repeated issues, escalating tone. Nobody looks across tickets at the account level.

## Proposal

Aggregate ticket signals per account and surface them where the account team works.

- Volume, reopen rate, escalation count, and satisfaction trend per account
- A trend indicator rather than a score, since a score invites false precision
- Surfaced in the account view the team already uses, not in a new dashboard
- Notification only on significant change, not as a recurring report

## Non-goals

No prediction of churn. We do not have the evidence to support a prediction, and presenting one would be dressing up a correlation.

## Risks

Support data used for commercial purposes changes the relationship customers think they have with support, particularly if it starts influencing pricing conversations. The internal policy on what the signals may be used for should be written before the data is exposed, not after someone uses it unexpectedly.

## Measurement

Accounts where the trend indicator moved before the account team was aware, and whether renewal conversations begin earlier for flagged accounts.

## Data We Have

Ticket history runs back four years but is keyed on the contact's address rather than the account, so attribution has to be derived and will be wrong for customers whose staff write in from personal addresses or whose domain changed after an acquisition. Satisfaction responses cover about a third of closed tickets and skew to the extremes, which makes any trend on them noisy for all but the busiest accounts. Volume and reopen rate are complete and dependable, and they are also the two that confound most obviously with account size and product usage. The indicator has to normalize against both or every large customer reads as unhappy by default.

## Review Notes

- A trend indicator still needs a definition of significant change, and that threshold is exactly where false precision comes back if it is set by feel
- Tone is deliberately absent from the signal list, since reading it means classifying ticket text, which is a separate decision carrying its own policy question
- A notification should name the tickets behind the movement, because the first thing an account manager does is go and read them

## Timeline

The usage policy comes first and is not engineering work, which makes it the item most likely to slip while the pipeline looks finished. Aggregation and the account-level keying are a few weeks. Exposure in the account view waits on the policy whether or not the data is ready, and that ordering should be stated to the account teams up front rather than explained later as a delay.
