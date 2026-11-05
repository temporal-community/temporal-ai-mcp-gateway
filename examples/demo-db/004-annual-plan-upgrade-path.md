---
Name: Annual Plan Upgrade Path
Owner: Maya Brennan
Status: Draft
Last Updated: 2025-07-21
---

## Context

Moving from monthly to annual requires contacting sales, even on the smallest plans. Roughly sixty accounts a month ask for it; about half complete, and the median time to complete is eleven days.

## Proposal

Self-serve annual conversion from the billing settings page.

- Credit the unused portion of the current month against the annual charge
- Show the twelve-month total and the saving before commitment, not after
- Immediate conversion, with the annual term starting on the day of payment
- A clearly stated and genuinely honored refund window of fourteen days

## Non-goals

No change to annual pricing, no multi-year terms, and no seat count changes bundled into the same transaction.

## Risks

Self-serve annual conversion moves revenue forward and makes a month look better than the run rate justifies, which is fine as long as reporting separates the two. It also increases refund exposure, since a fourteen-day window on an annual charge is a larger number than on a monthly one.

## Metrics

Conversions completed without human involvement, median time from intent to completion, refund rate within the window, and annual mix as a share of self-serve revenue.

## Interfaces Affected

Proration against an annual charge is new in billing. Credits today are applied within a period of the same length, and crediting a partial month into a twelve-month charge puts two line types on one invoice that have never appeared together. Finance reporting reads invoices by type, so that combination has to be classified before the first one is issued rather than reconciled afterwards. The sales path stays open and must not double-handle an account that already converted itself.

## Support Impact

Sixty requests a month reach sales today and most of them stop. What arrives instead is a smaller number of harder questions: why the credit is the amount it is, and what happens to the annual term when seats change mid-year. The second has no answer here, since seat changes are out of scope, which makes support the first place that gap gets noticed.

## Failure Modes

- A conversion that charges successfully and fails to update the plan leaves an account paying annually on monthly terms, which nobody notices until renewal
- A refund inside the window has to restore the previous monthly subscription rather than cancel outright, and that price may no longer exist if the monthly plan has changed
- Converting on the day a monthly charge falls due computes a credit against a period that is about to be billed again
