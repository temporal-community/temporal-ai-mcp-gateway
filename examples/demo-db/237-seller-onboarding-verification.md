---
Name: Seller Onboarding Verification
Owner: Jonas Keller
Status: In Review
Last Updated: 2026-05-01
---

## Context

Seller verification takes between one and nine days depending on which documents arrive and who reviews them. Sellers abandon during the wait at a rate of about eighteen percent, and the abandonment is concentrated in the window between submission and first response.

## Proposal

Automate the checks that can be automated and communicate the rest honestly.

- Identity and bank verification through the provider path, which returns in minutes for most cases
- Manual review reserved for the cases the provider cannot clear
- A clear status with an expected timeframe, updated when the state changes
- Partial onboarding allowed: listing creation before verification, selling after

## Scope

New seller onboarding in our existing markets. New markets have different documentation requirements.

## Risks

Allowing listing creation before verification lets a bad actor build a storefront that never sells, which is mostly harmless, and lets them harvest buyer interest that they can redirect elsewhere, which is not. Listings should not be publicly visible until verification completes.

## Measurement

Time to verified by path, abandonment during verification, and fraudulent sellers reaching an active state, which must not rise.

## Dependencies

The provider path is the whole proposal, and its coverage differs by market. Identity clears in minutes where a national registry is reachable and drops to manual review where it is not, so the one-to-nine-day spread does not disappear, it narrows onto a smaller group. Bank verification runs through a second provider with a different country list, so a seller can clear identity in minutes and still wait three days on the account check.

- Provider coverage confirmed per market before any timeframe is published
- Manual review queue sized for the residual, not for current volume
- Listing visibility gated on verification state, which the catalog service does not read today

## Support Impact

An honest status with a timeframe moves contacts earlier and reduces them overall, as long as the timeframe holds. A published estimate that slips becomes the reason for the contact it was meant to prevent, so the number shown should be the ninetieth percentile for that path rather than the median. Sellers held in manual review also need to see what is missing, or support is the only way to find out.

## Timeline

Provider verification ships first, because it moves most of the eighteen percent without any policy change. Status and timeframes follow once the path distribution is measured rather than assumed. Partial onboarding goes last: it carries the fraud exposure and it depends on listing visibility being gated correctly, which is a catalog change rather than an onboarding one.
