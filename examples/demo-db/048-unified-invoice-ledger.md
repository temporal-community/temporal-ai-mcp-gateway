---
Name: Unified Invoice Ledger
Owner: Dana Whitfield
Status: In Review
Last Updated: 2026-02-11
---

## Context

Invoice state lives in three places today: the billing service, the finance export job, and a spreadsheet the revenue team maintains by hand. When the three disagree, nobody can say which one is authoritative, and month-end close slips by two to four days while someone reconciles them line by line.

## Proposal

Stand up a single append-only ledger that every invoice event writes to, and make the other two consumers of it rather than sources.

- One event type per state change, with the actor and reason recorded
- The finance export reads the ledger instead of the service database
- The revenue spreadsheet becomes a generated view, refreshed nightly
- Historical invoices backfill in batches, oldest first

## Non-goals

This does not change invoice numbering, the chart of accounts mapping, or anything a customer sees. Credit notes keep their current flow until the ledger has run clean for a full quarter.

## Risks

The backfill is the dangerous part. Older invoices have gaps that the current code papers over at read time, and writing those gaps into a ledger would make them permanent. We will run the backfill in shadow mode first and diff the generated totals against the closed books for the last eight quarters.

## Success metrics

Days to close, reconciliation hours logged by finance, and the count of invoices where the three systems disagree, which should reach zero and stay there.

## Sequencing

Writing to the ledger and reading from it happen in that order, with a gap between. Dual-write first, billing service still authoritative, so the ledger accumulates a month of live events before anything reads it. The finance export cuts over next, since it is a batch consumer and a bad day can be rerun. The spreadsheet view goes last: the revenue team will stop maintaining the manual copy the moment a generated one exists, and there is no undo for that.

## Operational Impact

Close stops being a reconciliation exercise and becomes a review of exceptions, which changes who is busy and when. Finance absorbs the two-to-four day slip today as a known cost. Once the close is predictable, the days after it get committed to other work, and a bad ledger day then lands on a schedule with no slack. The ledger needs a close-window freeze and a named on-call owner through the first three closes.

## Rollback

Dual-write keeps the billing service database complete and authoritative throughout, so pointing the finance export back at it is a configuration change rather than a migration. That holds until credit notes move, which is why they stay on the current flow for a quarter. After credit notes cut over there is no cheap way back.

## Open Questions

What the shadow diff has to show before the backfill is accepted is undecided. Exact agreement across eight quarters is unlikely given the read-time patching old invoices rely on, and the tolerance is finance's call rather than engineering's. There is also no answer for an invoice whose gap cannot be resolved: recorded with an explicit unknown, or left out and handled by hand.
