---
Name: Activation Metric Definition
Owner: Tom Okafor
Status: Approved
Last Updated: 2026-03-07
---

## Problem

Three teams measure activation three ways: account created with a verified address, first meaningful action, and first weekly return. The numbers differ by a factor of two and each team's roadmap is justified against its own definition.

## Proposal

One definition, chosen on evidence, owned by the growth team and defined in the semantic layer.

- Candidate definitions evaluated by how well they predict ninety-day retention
- The winner defined centrally, with the others deprecated rather than left available
- A transition period where both the old and new numbers are reported
- The definition carrying a written rationale, so the next person can see why

## Non-goals

No change to what we instrument. The data exists; this is about which question we agree to ask of it.

## Risks

Picking the most predictive definition optimizes for a correlation that may not survive a product change, and a definition that is predictive today can become a target that teams game tomorrow. Reviewing the definition annually against fresh retention data is part of the proposal, not an afterthought.

## Measurement

Teams reporting against the shared definition, variance between surfaces, and whether the chosen definition retains its predictive power at the first annual review.

## Migration

Deprecating the two losing definitions is the work. Each is embedded in dashboards, a weekly deck, and at least one alert threshold, and pulling a field out of the semantic layer breaks all of them at once. The transition runs two full reporting cycles with both numbers side by side and the old field marked deprecated in place, after which it is deleted rather than left as a field nobody dares remove.

- Inventory every dashboard, deck, and alert reading one of the three definitions
- Report both numbers for two cycles with the old field labeled deprecated
- Delete the old fields on a date set now, not when the last consumer agrees

## Operational Impact

The board number moves on the cycle the switch happens, by as much as the factor of two that currently separates the definitions. That has to be explained before it appears rather than after, and it is far easier to explain while both numbers are still reported. Teams whose roadmap was justified against a losing definition need their targets restated in the new units, and a restated target is not a missed one.

## Open Questions

The ninety-day window is settled; the population is not. Whether self-serve and enterprise accounts are evaluated together, or the winner is allowed to differ by segment, is undecided. A per-segment definition would predict retention better and would also reintroduce the disagreement this proposal exists to end.
