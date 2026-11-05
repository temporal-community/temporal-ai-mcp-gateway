---
Name: Partner Revenue Share Payouts
Owner: Jonas Keller
Status: In Review
Last Updated: 2026-04-24
---

## Background

Partner revenue share is calculated quarterly in a spreadsheet, reviewed by two people, and paid by bank transfer initiated by hand. Partners cannot see what they are owed until the statement arrives, and disputes are resolved by re-running the spreadsheet with the partner on a call.

## Proposal

Calculate share continuously and expose a running statement in the partner portal.

- Attribution recorded on the transaction, not reconstructed at quarter end
- A running balance visible to the partner, updated daily
- Payouts initiated from the same calculation, with a review step above a threshold
- A downloadable detail file so partners can check our arithmetic against theirs

## Scope

Referral and reseller agreements on standard terms. The six partners on bespoke terms stay manual until their contracts renew.

## Risks

Showing a running balance means showing it moving, including downward when a refund claws back a share already counted. The statement has to make clawbacks legible or the first refund-heavy month will generate more calls than the quarterly statement ever did.

## Measurement

Days from quarter end to payout, disputes raised per quarter, and the share of partner revenue calculated without manual intervention.

## Interfaces Affected

- The partner portal, which carries contract documents today and nothing financial, so it needs a view of who at the partner may see balances at all
- Checkout and subscription change, both of which gain an attribution field written at the time of the transaction
- Payment operations, moving from initiating every transfer to approving the ones above the threshold
- The quarterly statement, which should keep going out as a closing document even once the running balance exists

## Failure Modes

A transaction that arrives without attribution is silent: nothing is wrong on the invoice, the partner simply never sees it, and the error surfaces only if the partner's own records are better than ours. That argues for a daily count of unattributed transactions in the same report as the balances. The second failure is a payout initiated twice when the review step is retried after a timeout, which the spreadsheet process prevented by being slow and human. Payouts need an identity of their own, checked before the transfer, not after.

## Timeline

Attribution on the transaction comes first and ships alone, because it is the only part that cannot be backfilled; every quarter it is not in place is another quarter reconstructed by hand at close. The running balance follows once a quarter of attributed data exists to display. Payout initiation goes last and should not start until finance has watched a full quarter of calculated balances agree with the spreadsheet they would have produced.
