---
Name: Signup Form Field Reduction
Owner: Clara Benton
Status: Draft
Last Updated: 2025-10-05
---

## Background

The signup form asks for seven things. Two are required by the product, two are used by marketing for segmentation, and three are used by nobody we can identify. Form abandonment is nineteen percent, concentrated on the second screen where the unused fields live.

## Proposal

Remove what is unused, defer what is not needed immediately, and keep the form to one screen.

- Three fields at signup: address, password or passkey, and workspace name
- Role and company size moved to a progressive prompt after first value
- The three unused fields removed, with their owners notified rather than consulted, since none could be found
- Address verification kept, since downstream recovery depends on it

## Scope

Self-serve signup. Enterprise onboarding collects more and should.

## Risks

Deferred fields are frequently never collected, and the marketing segmentation that depends on them will degrade. That is an acceptable trade only if we are honest that the segmentation will be partial, rather than discovering it during a campaign.

## Measurement

Signup completion rate, time to complete, and the collection rate of deferred fields after one week, which tells us the real cost of deferring.

## Interfaces Affected

The signup write path is shared with invite acceptance, which populates the same record with fewer fields and already tolerates a missing role. Dropping three columns is therefore not a schema change for this release: the columns stay and stop being written, and they go a release later once the jobs reading them are retired.

- The signup endpoint rejects the three removed fields rather than ignoring them
- Two warehouse jobs read those columns and will produce nulls from the cutover
- The progressive prompt needs a dismissal record, which the onboarding checklist does not have today

## What Would Change Our Mind

If the three unidentified fields turn out to have a consumer outside the warehouse, removal stops and they move to the deferred set instead. We searched query logs and job definitions, and neither covers anything reading the production tables directly. One such reader would make this a deprecation with notice rather than a deletion.

## Review Notes

The nineteen percent figure is abandonment across the whole form, not the second screen alone. Eleven points of it belong to the second screen, which is the number this change aims at, and completion should be read against that rather than against nineteen. Address verification stays on the first screen deliberately, since moving it later breaks the recovery path that depends on a verified address at creation.
