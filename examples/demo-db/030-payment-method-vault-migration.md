---
Name: Payment Method Vault Migration
Owner: Clara Benton
Status: In Review
Last Updated: 2026-02-27
---

## Context

Stored payment methods live in a vault built before tokenization was available from our processor. It works, but it is ours to secure, ours to audit, and the only component in the billing path that still requires a hardware module in the review scope.

## Proposal

Migrate to processor-held network tokens and retire the vault.

- New payment methods tokenize at the processor from the day the flag flips
- Existing methods migrate through the processor's bulk import, in account batches
- The vault moves to read-only once a batch is confirmed, then is destroyed on a schedule
- A dual-read period covers the window where either store might hold the method

## Non-goals

No change to the checkout interface, no change to which methods we accept, and no attempt to consolidate the separate vault the marketplace team maintains.

## Risks

The dual-read window is the risk. If a method migrates while a charge is in flight, we could charge against a stale token or, worse, twice. Migration batches run outside renewal windows and the charge path takes an account-level lock during the swap.

## Success metrics

Methods migrated, charge success rate per batch compared against the pre-migration baseline, and the audit scope line count, which is the reason we are doing this.

## Rollback

Rollback is per batch and available only until that batch's vault entries are destroyed, which is the one irreversible step in the plan. Before destruction, reverting an account is a flag flip back to vault reads. After it there is no path back, because a network token cannot be turned into a stored card number by design. That argues for a long gap between read-only and destruction: at least a full billing cycle, so every account in the batch has been charged successfully against the processor token before its old record disappears.

## Dependencies

- The processor's bulk import, which is rate limited and will set the batch size more than our own scheduling does
- Account-level locking in the charge path, which does not exist today and is the only new code going into the critical path
- Renewal calendars per account, since batches have to avoid renewal windows and renewals are not evenly spread across the month
- The audit scope document, updated as batches complete, or the benefit stays invisible to the people who asked for this

## Timeline

Tokenizing new methods ships first and stops the problem growing, which is worth having even if the rest slips. Existing methods migrate across roughly a quarter, smallest and least active accounts first, so the account-level lock is exercised before it meets a high-volume account. Destruction starts only after the final batch has survived a full billing cycle, which puts actual vault retirement, and therefore the audit scope reduction, two quarters out rather than one.
