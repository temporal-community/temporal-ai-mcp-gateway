---
Name: Seller Payout Schedule Options
Owner: Clara Benton
Status: In Review
Last Updated: 2026-05-24
---

## Problem

Payouts run weekly on a fixed day. Small sellers want money sooner to fund restocking; large sellers want a predictable monthly cycle for their accounting. The single schedule suits neither well, and we receive the request from both directions.

## Proposal

Seller-chosen payout schedules within risk-defined bounds.

- Three options: daily, weekly, and monthly, selectable by the seller
- Daily restricted by account history and dispute rate, since it shortens our recourse window
- Schedule changes taking effect after the current cycle, to keep reconciliation clean
- A clear statement of when funds for a given order become eligible

## Scope

Payout timing. The holding period before funds become eligible is a risk decision and unchanged here.

## Risks

Daily payouts reduce the window in which a dispute can be settled from held funds, moving loss onto us. Restricting by history manages this but creates a tier that new sellers will experience as arbitrary unless the criteria are published.

## Measurement

Uptake per option, loss from disputes against sellers on daily schedules, seller satisfaction with payout timing, and support contacts about payouts.

## Data We Have

Dispute rate by seller tenure is already computed for risk scoring, and its shape is what the daily criteria should rest on: disputes concentrate in a seller's first ninety days and then fall by roughly an order of magnitude, which argues for a tenure threshold rather than a volume one.

- Payout support contacts, about four hundred a month, split evenly between where the money is and when it arrives
- Reconciliation effort per cycle, which is the number that multiplies when three schedules run at once

## Operational Impact

Finance reconciles one run a week today and would reconcile nightly runs, four weekly cohorts, and a monthly run. Effort is per run rather than per seller, so cost rises with the number of runs and not with uptake. Staggering the weekly cohorts across the week is what stops the load landing entirely on Monday.

- Payout file generation moves from weekly to nightly
- Per-payout transfer fees rise on a daily schedule, which belongs in the option description rather than being discovered

## Alternatives Considered

Letting sellers request an early payout on demand is what the support contacts actually ask for. It was rejected because an on-demand payout has no cycle to reconcile against and puts the cost on finance per request rather than per run. A published schedule chosen once is cheaper to operate and easier to explain than a request path with an approval behind it.
