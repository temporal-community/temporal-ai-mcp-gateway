---
Name: Warehouse Access Tiering
Owner: Lena Fischer
Status: In Review
Last Updated: 2026-06-16
---

## Problem

Warehouse access is binary. Anyone who needs to run a query gets the same role, which can read raw tables containing personal data, including the customer support exports and the identity event tables. That is roughly two hundred people with access to data that perhaps twenty need.

## Proposal

Three tiers with clear boundaries, defaulting to the lowest.

- Modeled tier: curated, masked, covers what most analysis needs
- Raw tier: unmasked operational tables, requested with a reason and reviewed quarterly
- Restricted tier: identity and support data, named individuals only, access logged per query
- Requests routed to the dataset owner rather than to the platform team

## Non-goals

No change to the data itself and no new masking work beyond what the modeled tier already applies.

## Risks

If the modeled tier does not actually cover common needs, people will request raw access as a matter of routine and the tiers become a formality. We should measure which raw-tier queries could have been served by modeled tables and treat a high number as a signal to improve the models rather than to tighten the gate.

## Measurement

People per tier, raw-tier queries that modeled tables could have served, and time from request to granted access, which must stay under a day.

## Data We Have

Query logs run back two years and record which tables each query touched, which is enough to place most of the two hundred people into a tier without asking any of them. A first pass suggests the large majority have never read an unmasked personal-data table at all, so assignment should be computed and people should only have to ask when their own history says they need more. The logs are weak on intent: a query against the identity event tables looks identical whether it was an investigation or the accidental reach of a select-everything, and that is exactly the distinction the restricted tier cares about.

## Migration

Assign from history, tell everyone which tier they landed in, and leave two weeks before enforcement during which anyone can say the assignment is wrong. The alternative, dropping everyone to the modeled tier and letting them request their way back, produces two hundred requests in a week aimed at dataset owners who have never handled one. The time-to-grant target would be missed in the first days and nobody would learn anything from the miss.

## Operational Impact

Routing requests to dataset owners puts access decisions on people who have not made them before, and several of these datasets have an owner in name only. Every dataset needs a named owner who has agreed to the role before tiering goes live, or requests will queue behind someone who does not know they are the gate. Per-query logging on the restricted tier also implies a reader: a log nobody opens is a cost without a control.
