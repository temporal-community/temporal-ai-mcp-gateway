---
Name: Product Image Guidelines
Owner: Nora Sellers
Status: Draft
Last Updated: 2025-11-10
---

## Problem

Listing images range from professional to unusable. The guidelines exist in a help article nobody reads, and enforcement is nonexistent, so the browse experience is visually incoherent and our conversion on image-led categories is below what the category warrants.

## Proposal

Enforce a small number of mechanical requirements and advise on the rest.

- Mechanical requirements checked at upload: minimum resolution, aspect ratio, and no added text overlays
- Guidance shown inline at upload rather than in an article
- A grace period for existing listings, with the requirements applying to edits and new listings first
- Automatic background handling offered rather than required, since it helps consistency

## Scope

Listing images. Seller profile and storefront images are separate.

## Risks

Text overlay detection has false positives on legitimate product packaging, which has text on it by nature. The check needs to distinguish added overlays from photographed text, and if it cannot do that reliably it should warn rather than block.

## Measurement

Listings meeting the mechanical requirements, conversion in image-led categories, upload failures and their causes, and appeals against overlay detection.

## Timeline

Resolution and aspect ratio ship as soon as the inline guidance exists, since both are unambiguous and a seller can see at once why an upload was refused. Overlay detection needs a measured false positive rate on packaged goods before it blocks anything, so it goes out as a warning and is promoted only if appeals stay rare. The grace period for existing listings runs a quarter, timed to end before the next peak season rather than during it.

## Support Impact

Upload failures turn into contacts in the first week, and the ones that matter are from sellers who cannot tell what is wrong.

- The refusal names the failing requirement and the actual value, not the general rule
- Appeals against overlay detection need a route and a stated response time, since a blocked listing is lost revenue
- Sellers photographing on a phone are the common case for low resolution, so the guidance has to say what to do rather than what is wrong

## Open Questions

Whether the overlay check should block at all, or whether a warning plus lower ranking is the honest version of what the detector can support. Ranking is the quieter penalty and it is also the one a seller cannot see or appeal. The second is whether background handling stays optional once we know how listings that use it convert, since optional and recommended are different things and the second is harder to withdraw.
