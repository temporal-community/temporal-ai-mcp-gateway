---
Name: Mobile Form Autofill Compatibility
Owner: Nora Sellers
Status: Draft
Last Updated: 2025-09-02
---

## Background

Password managers and platform autofill work inconsistently with our forms. Some fields are not recognized at all, and the sign-in form in particular requires manual entry for several popular managers, which is a meaningful friction on a phone keyboard.

## Proposal

Annotate every field correctly and test against the managers people actually use.

- Content type and autofill hints set on every input, audited rather than assumed
- Associated domains configured correctly for both platforms, which they currently are not on one
- A test matrix across the four most used managers, run before each release
- One-time code fields marked so platform autofill offers the code from messages

## Scope

Sign-in, signup, and payment forms. Other forms benefit but are not worth the test matrix cost.

## Risks

The associated domain configuration is a deployment artifact that has broken silently before. It needs a monitored check rather than a line in a checklist, because the failure is invisible until someone tries to sign in.

## Measurement

Sign-in completion time on mobile, manual entry rate where autofill is available, and support contacts about password managers not working.

## Sequencing

The field annotations are cheap and independent, so they land first and on their own release. The associated domain fix on the platform where it is currently wrong lands second, because verifying it needs a real build on a real device rather than a simulator. The test matrix comes last: it is only worth building once the forms it tests are correct, otherwise every run reports the same four known failures.

## Interfaces Affected

- Sign-in, signup, and payment form markup, where the hints are set
- The associated domain files served from the site, and the build step that publishes them
- The one-time code field, which currently clears itself on paste from some managers
- Release checks, which gain the matrix run and the domain file check

The payment form is the sensitive one. Changing its field annotations changes which values a manager offers to fill, and an annotation that is wrong in a new way is worse than one that is missing.

## Rollback

Annotations revert with the release. The associated domain configuration does not: platforms cache it, so a bad file can keep failing for a day after the fix ships. That caching is the reason the monitored check matters more than the fix itself.
