---
Name: Reactivation Campaign for Dormant Accounts
Owner: Victor Alves
Status: Draft
Last Updated: 2026-07-19
---

## Background

About nine thousand accounts have been inactive for more than six months while remaining on a paid plan or a free tier. We contact none of them. Some have churned in all but name; some are seasonal; we cannot currently distinguish the two.

## Proposal

Segment the dormant population, contact deliberately, and accept that some outcomes are cancellations.

- Segmentation by prior usage pattern, plan, and whether the workspace has multiple members
- A short sequence for each segment with a genuine reason to return, tied to what they used before
- An explicit easy cancellation path in the message for those who have moved on
- A holdout to measure whether contact helps or accelerates departure

## Scope

Self-serve accounts. Dormant enterprise accounts are an account team conversation and should not receive automated contact.

## Risks

Reminding a dormant payer that they are paying may produce cancellations that silence would have deferred. That revenue is not real in any useful sense, but it is on the books, and the holdout is what will tell us the size of the effect rather than leaving it as a matter of opinion.

## Measurement

Return to activity against holdout, cancellations against holdout, and net revenue effect over two quarters.

## Data We Have

The nine thousand split roughly two to one between free tier and paid, and the paid portion carries both the upside and the risk. Usage history reaches far enough back to see what most of these accounts last did, with the exception of about eight hundred dormant since before the event schema change, which can only be segmented on plan and workspace size. Deliverability is the quieter problem: on a list untouched for a year, a meaningful share of the addresses will bounce, and bouncing at volume against a cold list is how a sending domain loses its reputation.

## Sequencing

Free tier goes first. There is nothing to cancel, so the downside is bounded, and it exercises segmentation, the sequence, and the holdout mechanics before any of that touches revenue. It also produces a current bounce rate, which is the number that decides whether the paid sends need a warm-up schedule. Paid segments follow one at a time, highest plan value last.

## Review Notes

- The holdout has to be sized to detect a difference in cancellations, not just in returns; cancellations are the rarer event and therefore set the size
- Multi-member workspaces need a rule for who is contacted, because mailing every member of a dormant team reads as pressure rather than an invitation
- The easy cancellation path should be as prominent in the copy that goes out as it is in this proposal, or the holdout is measuring a different message than the one described here
