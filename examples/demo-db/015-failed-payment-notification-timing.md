---
Name: Failed Payment Notification Timing
Owner: Ruth Adeyemi
Status: Approved
Last Updated: 2026-05-07
---

## Problem

When a renewal charge fails, we email immediately and then again at each retry. Customers who were going to be charged successfully on the second attempt receive an alarming email for a problem that resolves itself twenty minutes later, and support agents field the resulting calls before the retry has even run.

## Proposal

Hold the first notification until the retry schedule has had a reasonable chance to succeed.

- No customer email until the first soft-decline retry has failed
- Hard declines notify immediately, because those will not self-resolve
- A single consolidated reminder at day three rather than one per attempt
- Internal visibility unchanged, so support agents can still see the first failure the moment it happens

## Scope

Self-serve renewals. Enterprise invoicing has a separate dunning path with a named contact and should not inherit this behavior.

## Risks

Delaying notification delays the chance to fix a card before suspension, so the day-three reminder has to be unmissable and the suspension date has to be stated plainly in it. If retries get worse, this change quietly makes the customer experience worse too, which argues for alarming on the gap between first failure and first notification.

## Measurement

Calls to support within an hour of a first failure, cards updated before suspension, and involuntary churn, which should not move.

## Data We Have

The processor's decline codes separate soft from hard, and that mapping is the whole basis of this change. It is also their judgment, not ours. An insufficient-funds decline is soft by their classification and recovers on retry about sixty percent of the time; a do-not-honor decline is soft by the same code set and recovers under ten percent. Treating the whole soft class as retryable is a simplification we can afford at the first retry and not at the third.

- Roughly four in five first-attempt failures succeed on a retry within the hour
- Median time to a successful retry is twenty-two minutes
- Hard declines are about one in eight failures and rarely recover without a new card

## Sequencing

The alarm on the gap between first failure and first notification goes in before the notification change, not after. It is the only thing that tells us the retry schedule has degraded, and a change resting on retries behaving needs its detector live first. The consolidated day-three reminder follows, and the per-attempt emails switch off last.

## Support Impact

Internal visibility is unchanged, so staff will see a failure the customer has not been told about, for up to a day. The account view needs that state read plainly, as failed, retrying, customer not yet notified, or someone will tell a caller about a failure they did not know they had. Call volume should fall; the calls that remain will be harder, since the customer arrives at day three with the suspension date already close.
