---
Name: Data Residency Options
Owner: Felix Braun
Status: Draft
Last Updated: 2026-01-06
---

## Problem

All customer data is stored in one region. An increasing share of enterprise deals require storage within a specified jurisdiction, and we currently answer with a commitment to consider it, which is not an answer.

## Proposal

Regional data storage with a clear statement of what stays in region and what does not.

- Workspace data pinned to a chosen region at creation, immutable afterwards
- A published list of what remains global: account identity, billing, and operational telemetry
- Regional processing for the main request path, with cross-region calls enumerated and justified
- Residency stated in the product, not only in a contract

## Scope

Two additional regions initially, chosen by demand.

## Risks

Partial residency is worse than none if it is described imprecisely, because a customer who believes everything stays in region will eventually discover a counterexample. The published list has to be exhaustive and maintained as the architecture changes, which is a standing obligation rather than a launch task.

## Measurement

Workspaces per region, deals where residency was a stated requirement, cross-region data flows against the published list, and audit findings on residency claims.

## Cost

Two additional regions roughly triples the fixed infrastructure cost, because most of the per-region footprint is minimums rather than capacity. The database cluster, the cache tier, and the queue infrastructure each have a floor a small region hits immediately. Variable cost tracks workspaces and is a rounding error against that floor for the first year, so the sales case has to carry three regions of fixed cost rather than a proportional share of one.

- Each region runs the full stack, including components a small region barely uses
- The enumerated cross-region calls add latency to the paths they sit on, a product cost rather than an infrastructure one
- Retiring a region later costs more than standing one up, so the choice is close to irreversible

## Operational Impact

Every incident becomes a question of which regions are affected and every deployment becomes three. On-call needs regional dashboards rather than one, and a release that is correct in the home region can fail in a smaller one where the data shape differs.

## Timeline

The published list comes before the first region rather than with it. It is the artifact the sales conversation actually needs, it can be written against today's single-region architecture, and writing it will surface the cross-region assumptions the region work then has to resolve.
