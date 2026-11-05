---
Name: Synthetic Monitoring Coverage
Owner: Jonas Keller
Status: Draft
Last Updated: 2025-12-23
---

## Background

We monitor from inside: error rates and latency as measured by our own services. Three of our last six customer-reported outages were invisible in those metrics because the failure was in the path before our services, at the edge or in resolution.

## Proposal

Synthetic checks from outside, covering the journeys that matter.

- Six journeys, chosen by revenue impact: sign-in, search, create, checkout, export, and the public pages
- Run from four regions at a one-minute interval, from outside our network
- Alerting on the synthetic result independently of internal metrics
- Results published on the status page, so the external view is the one customers see

## Scope

The main product. Partner and embedded surfaces follow if this proves out.

## Risks

Synthetic checks produce false alarms from the vantage point's own network problems, and a noisy external check trains people to discount it, which defeats the purpose. Requiring agreement across two regions before alerting is the usual remedy and costs a little detection time.

## Measurement

Outages detected by synthetic check before customer report, false alarm rate, and the gap between synthetic and internal availability figures.

## Cost

Six journeys from four regions every minute is around thirty-five thousand runs a day, which is a pricing tier rather than a rounding error.

- Checkout and export need test accounts and test data that someone maintains, which is the hidden recurring cost
- A one-minute interval on all six is the expensive default; the public pages and sign-in earn it, create and export probably do not
- Publishing to the status page makes the vendor's own availability part of our customer-facing story

## Operational Impact

An external check that pages is a new alarm source with its own tuning and its own owner.

- Two-region agreement before alerting, which already costs the detection time the risks section describes
- Checkout test accounts must not generate real charges or appear in revenue reporting
- A synthetic failure with healthy internal metrics is the interesting case and needs a runbook, because the instinct is to disbelieve it

## Open Questions

Whether the status page shows the synthetic result directly or a derived state, since the raw result will sometimes show a regional failure that belongs to the vantage point and customers will read it as ours. The other is what the export journey actually checks, given that a real export runs longer than the interval and checking only that it starts tests less than it appears to.
