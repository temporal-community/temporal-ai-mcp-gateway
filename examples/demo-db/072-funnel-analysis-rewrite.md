---
Name: Funnel Analysis Rewrite
Owner: Hana Kobayashi
Status: In Review
Last Updated: 2026-02-02
---

## Problem

The funnel view computes each step independently and presents the results as a sequence, which means it will happily show a step with more completions than the step before it. It also cannot express a step that is optional, which describes half of our onboarding.

## Proposal

Rebuild on a proper sequence model with per-user path resolution.

- Steps evaluated as an ordered sequence per user within a configurable window
- Optional and alternative steps expressible in the definition
- Drop-off attributed to the step where the sequence ended, not inferred from counts
- The underlying per-user paths available for export when a number needs explaining

## Scope

The funnel view in the analytics product. The growth team's bespoke funnel models are separate and would migrate later if this proves out.

## Risks

The new numbers will differ from the old ones, in most cases downward, and the old numbers have been quoted in plans. A migration note explaining the difference per funnel is not optional, and should go out before the change rather than with it.

## Measurement

Funnels where the sequence resolves cleanly, support questions about impossible step counts, which should disappear, and use of the per-user export during analysis.

## Cost

Per-user path resolution is a different shape of query than counting completions per step. Each funnel view becomes a scan over ordered user events within the window rather than four independent aggregates, which is more expensive per view and much more expensive for a long window.

- Precompute paths for saved funnel definitions, resolve ad-hoc ones on request
- Cap the configurable window, since a ninety-day sequence over all users is not a view anyone waits for
- Keep the per-user export bounded, because exporting every path on a large funnel is a different product

## Migration

Both engines run side by side for a quarter. Each funnel gets its old and new numbers computed over the same period, and the per-funnel migration note quotes both rather than describing the difference in general terms. Funnels where the two agree can switch immediately; the ones that disagree most are the ones whose owners most need the conversation, and those switch last and by hand.

## Interfaces Affected

The funnel definition format gains optional and alternative steps, so every existing definition has to be readable as a sequence without change. Drop-off attribution moves from a derived number to a stored one, which means anything reading step counts from the old tables breaks. The growth team's bespoke models read those tables today, and while their migration is out of scope, their breakage is not.
