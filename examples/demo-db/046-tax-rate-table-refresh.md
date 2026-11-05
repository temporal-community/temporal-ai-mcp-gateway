---
Name: Tax Rate Table Refresh
Owner: Lena Fischer
Status: Draft
Last Updated: 2025-09-18
---

## Background

Our tax rates are updated by hand from a quarterly bulletin. The process takes a day, happens late, and has produced four rate errors in two years, each of which required a correcting filing.

## Proposal

Move to the provider feed we already pay for and keep the manual table only as an override layer.

- Nightly ingest of the provider feed into a versioned rate table
- Rates resolve by jurisdiction and effective date, never by latest write
- A thin override table for the handful of cases the feed gets wrong for our product category
- A diff report mailed to finance whenever an effective rate changes

## Scope

Sales tax and value added tax on digital goods, in the jurisdictions where we currently collect. Physical goods are out of scope because the marketplace team owns that path and their category mapping is different.

## Risks

The override layer is where this goes wrong over time. Overrides that outlive their reason are invisible, so each one carries an expiry date and a named owner, and the diff report lists expired overrides at the top until someone removes them.

## Measurement

Rate errors per quarter, hours spent on the quarterly update, and the number of live overrides, which should trend down rather than accumulate.

## Migration

Backfill the versioned table from the provider's historical rates before any order resolves against it. A credit or a reissued invoice for an order placed in March has to resolve the March rate, not tonight's, and the provider publishes history far enough back to cover every order we can still amend. The hand-maintained table then seeds the override layer: each row that disagrees with the feed on the cutover date is imported as an override with a thirty-day expiry. That forces someone to justify it or let it lapse, at the cost of a noisy first diff report.

## Failure Modes

- The nightly ingest fails quietly and the table goes stale; a feed older than forty-eight hours should fail the job loudly rather than serve yesterday's rates
- The provider publishes a rate with an effective date in the past, changing the answer for orders already invoiced
- A jurisdiction splits or is renamed and its old identifier simply stops appearing in the feed rather than erroring
- An override is created by direct write, skipping the expiry and owner the form requires

## Staffing

One engineer for about six weeks covers ingest, resolution by effective date, and the diff report. The override form and the expiry sweep are another two weeks and are the part most likely to be cut, which would be the wrong cut. Finance needs a named reviewer for the diff report from the first week it runs, because a report nobody reads reproduces the problem this replaces.
