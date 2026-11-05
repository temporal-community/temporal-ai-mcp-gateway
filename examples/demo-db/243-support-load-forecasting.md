---
Name: Support Load Forecasting
Owner: Nikhil Shah
Status: Draft
Last Updated: 2026-04-13
---

## Context

Staffing is planned from last month's volume. This misses the predictable spikes entirely: the renewal wave at the start of each quarter, the day after a major release, and the annual tax documentation period, all of which we know about in advance and are reliably understaffed for.

## Proposal

Forecast from known drivers rather than from trailing volume.

- Drivers identified and quantified: renewals, releases, campaigns, and seasonal events
- A forecast per week by channel, published far enough ahead to act on
- Release calendar and campaign calendar as inputs, which requires those teams to share dates reliably
- Forecast error reviewed monthly, with the drivers adjusted rather than the forecast fudged

## Non-goals

No change to the staffing model itself. This gives the existing model better inputs.

## Risks

The forecast depends on other teams sharing plans that frequently change, and a forecast built on a release date that slips is worse than useless because it moves people to the wrong week. The model should express date uncertainty rather than assuming a single date.

## Measurement

Forecast error by week, response time attainment during known spikes, and overtime hours, which is the current absorption mechanism.

## Data We Have

Three years of volume by day and channel is enough to fit the seasonal drivers directly. The quarter-start renewal wave shows up in all twelve quarters and runs about thirty percent above baseline for four working days. Release-driven volume is harder, since release dates sit in a calendar nobody has joined to ticket history, and doing that join once is what turns the day after a release into a number.

- Campaign send dates, held by marketing in their own tool and exported nowhere
- Tax documentation volume, clean and strongly seasonal, the easiest driver to quantify first
- Overtime hours by week, which marks where the current model already failed

## Prior Art

The capacity model for the payments rota was built this way two years ago and still runs. Its lesson was that the forecast was ignored until it appeared in the same place as the roster, and that a weekly number was actionable where a monthly one was not. It also degraded quietly when an input stopped being maintained, which is why error review needs an owner rather than a dashboard.

## Failure Modes

A slipped release date is the obvious one. The quieter failure is a forecast that is right and ignored, because moving people between channels takes a conversation and the spike lands on Monday. Publishing three weeks out rather than one is what makes it actionable. The third is drift: drivers that explained volume last year explain less this year, and an error review that only adjusts coefficients will miss a driver that has stopped existing.
