---
Name: Multi-Currency Settlement Reports
Owner: Yusuf Demir
Status: Approved
Last Updated: 2026-04-09
---

## Problem

Settlement reports are generated in the currency of the charge, so a seller trading in four currencies gets four reports with no combined view and no explanation of the conversion they actually received. Finance teams at larger sellers rebuild this themselves, badly.

## Approach

Add a settlement currency to the report model and generate a combined statement alongside the per-currency ones.

- Conversion rate and timestamp shown per line, not just per report
- Fees broken out by type rather than netted into the payout figure
- A combined statement in the seller's chosen reporting currency
- Historical reports regenerate on demand rather than being rewritten in place

## Scope

Reporting only. Nothing about when or how funds move changes, and payout scheduling stays where it is.

## Risks

Showing conversion rates per line invites the question of why they differ across a single day, which is a reasonable question with an unsatisfying answer. The support team should have a written explanation before this ships, not after the first ticket.

## Timeline

Six weeks to the combined statement behind a flag, two weeks of parallel generation against the existing reports, then default on for new sellers and opt-in for the rest through the end of the quarter.

## Support Impact

The written explanation of intraday rate variation is a deliverable, not a nicety. It has to name the rate source, say at which moment in the charge lifecycle the rate is captured, and explain why a refund converts at a different rate than the original charge. Without it every per-line rate becomes a ticket, and the sellers most likely to ask are the four-currency sellers this is built for.

- Explanation written and reviewed by finance before the flag goes on for anyone
- A worked example in the help center built from a real two-currency statement
- Fee type names in the report matching the names the support console shows

## Failure Modes

On-demand regeneration is the exposure. A report regenerated months later has to reproduce the rate applied at the time, so rate and timestamp have to be stored per line rather than looked up at render. A line with a missing historical rate has to fail loudly instead of substituting a current one, because a statement that silently restates history is worse than no statement. The two weeks of parallel generation are where this surfaces: any disagreement with the existing per-currency report is a defect, not a rounding difference to wave through.

## Cost

Storing rate and timestamp per line roughly doubles the settlement line record, the largest table outside events. Combined statements are generated on request rather than stored, so the rest of the cost is query time, plus doubled report generation during the parallel window.
