---
Name: Cross-Org Profile Visibility
Owner: Nora Sellers
Status: Draft
Last Updated: 2026-02-24
---

## Context

A person who belongs to two organizations has one profile. Their display name, photo, and status are shared across both, which is usually fine and occasionally a problem: contractors, people with different names in different professional contexts, and anyone who would rather their employer not see their other client's workspace.

## Proposal

Per-organization profile overrides, with a clear default.

- Name and photo overridable per organization, with the global profile as the default
- Membership in other organizations never visible to anyone, in any view
- Presence and status scoped to the organization being viewed
- A settings view that shows exactly what each organization can see

## Non-goals

No separate accounts, no profile verification, and no change to how identity is proven at sign-in.

## Risks

The transparency view is the hard part and the important part. If people cannot easily see what each organization sees, the override feature is just a setting they will not trust. Getting this view right matters more than the override mechanism itself.

## Measurement

Overrides configured, visits to the transparency view, and support contacts about profile information appearing where it was not wanted, which currently arrive roughly monthly.

## Failure Modes

Leaks here are quiet and cannot be taken back. A display name escapes its organization through many more surfaces than the profile view: mention autocomplete, the audit log, notification mail rendered by a different service, exports, the title of a shared document, a calendar invitation. Any one of them rendering the global name defeats the feature, and nobody reports it until after it has been seen. The honest version of this proposal carries an inventory of every place a name or photo is rendered, and building that inventory is most of the work.

## Support Impact

Support handles about one of these a month today and has nothing to offer but an apology. Afterwards they will field a different contact, that a colleague is seeing the wrong name, which cannot be diagnosed without seeing what the other organization sees. That means a support-side version of the transparency view, scoped to the person who asked and logged when it is used, or the feature creates cases support cannot close.

## Open Questions

Whether an organization administrator may require the global profile. Regulated customers will ask for it, and granting it hands an employer precisely the visibility the contractor case exists to prevent. Also unresolved: what a person is shown on a surface where two organizations meet, such as a shared document or an external channel. The proposal scopes presence to the organization being viewed, and those surfaces are being viewed from two.
