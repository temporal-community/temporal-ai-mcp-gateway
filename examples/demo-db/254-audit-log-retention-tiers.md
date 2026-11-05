---
Name: Audit Log Retention Tiers
Owner: Hugo Takahashi
Status: Draft
Last Updated: 2025-11-04
---

## Problem

Audit logs are retained for ninety days for everyone. Enterprise customers need a year or more for their own compliance, and our smallest customers do not need ninety days and are paying for the storage indirectly.

## Proposal

Retention tiers by plan, with export for anyone who needs longer.

- Thirty, ninety, and three hundred and sixty-five day tiers aligned to plans
- Export to customer-controlled storage available on every tier, so nobody is trapped
- Retention stated in the product and in the contract, matching each other
- Storage tiering so older logs cost less to keep, which makes the long tier affordable

## Scope

Customer-facing audit logs. Our own operational logs have separate retention driven by different needs.

## Risks

Reducing retention for existing customers on lower plans removes something they have today, which is a change that needs announcement and a grandfathering decision. The honest framing is that we are matching retention to plans rather than taking something away, and that framing is only honest if existing customers keep what they have.

## Measurement

Storage cost per tier, customers using export, enterprise deals where retention was raised, and complaints from existing customers about any change.

## Migration

Existing customers keep their ninety days regardless of plan, recorded as a per-workspace override rather than a tier, so the override stays visible and can be retired deliberately rather than by accident.

- New workspaces take the tier for their plan from the first day
- Existing workspaces that would drop below ninety days keep ninety until they change plan
- A downgrade applies the shorter tier going forward and does not delete what is already retained
- Contract language changes at renewal, not at launch

## Cost

Storage tiering is what makes the long retention affordable, and the saving is uneven. The three-hundred-and-sixty-five-day tier is mostly cold storage at a fraction of the hot path, while the thirty-day tier barely moves the bill because it was never the expensive part. The honest expectation is a revenue and compliance change with a modest cost effect, not a storage savings program.

## Support Impact

Two questions will arrive: where the older entries went, and how to export. The first is answered by stating retention in the product beside the log view rather than only in the contract. The second is answered by export being available on every tier, including the thirty-day one, which only holds if the destination setup is documented. An export path that exists and is undocumented generates more contacts than one that is absent.
