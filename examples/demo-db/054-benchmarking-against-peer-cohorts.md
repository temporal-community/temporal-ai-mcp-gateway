---
Name: Benchmarking Against Peer Cohorts
Owner: Sofia Marchetti
Status: Parked
Last Updated: 2025-12-09
---

## Problem

Customers ask whether their numbers are good. We have the data to answer that comparatively and no way to do it without exposing information about other customers, so today the answer is an anecdote from whoever is on the call.

## Proposal

Aggregate benchmarks by industry and size band, with aggregation rules strict enough to be safe.

- Minimum cohort size enforced before any statistic is shown
- Only distribution statistics, never anything attributable to a single account
- Opt-in contribution, with the benefit of participation clearly stated
- Benchmarks refreshed quarterly rather than continuously, to limit inference from changes

## Scope

Three metrics to start. More metrics multiply the inference risk in ways that are hard to reason about.

## Risks

Even with minimum cohort sizes, repeated queries over time can isolate a contributor, especially in small industries where our customer list is close to the market. Getting this wrong is a confidentiality breach rather than a bug. Parked pending an opinion from legal and a properly adversarial review of the inference risk.

## Measurement

If it proceeds: opt-in rate, benchmark views per account, and whether any adversarial review finds an attributable statistic.

## Alternatives Considered

A survey benchmark, where customers report their own numbers, removes the confidentiality problem entirely, since nobody contributes data they did not choose to publish. It also produces worse numbers: self-reported figures run optimistic, response rates are low, and the sample tilts toward customers who are doing well. It stays on the table as the fallback if the inference review goes badly. Publishing one industry-wide figure with no cohorts is the other option, and it is safe and nearly useless, because good for a twelve-person shop and good for a two-thousand-seat account are different numbers.

## Prior Art

Two of our data providers publish benchmarks under the same constraints, and both use suppression rules rather than cohort minimums alone: a statistic is withheld when one contributor accounts for more than a set share of its cohort, however many members it has. That catches the case a minimum misses, a cohort of twenty where one account is most of the volume. Both also refresh annually rather than quarterly.

## What Would Change Our Mind

The adversarial review decides this. If a reviewer can isolate a contributor from published statistics across two refreshes, the quarterly cadence is wrong and the choice is annual or nothing. If isolation needs knowledge of cohort membership, the opt-in list stays private and the work continues. If legal reads opt-in consent as not covering inference by third parties, it does not proceed in any form.
