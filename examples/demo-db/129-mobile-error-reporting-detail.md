---
Name: Mobile Error Reporting Detail
Owner: Caleb Mortensen
Status: Draft
Last Updated: 2026-06-14
---

## Problem

When something fails on mobile, the person sees a generic message and we receive a stack trace with no context about what they were doing. Support cannot connect the two, so a reproducible bug frequently takes three exchanges just to establish what screen it happened on.

## Proposal

Attach bounded context to error reports and give the person a reference they can quote.

- A short reference code displayed with every error message, matching the report
- The last ten navigation events and the active screen attached, with no user content
- Network state and application version included, which currently are not
- A one-tap report action that attaches the above and nothing more

## Scope

Error reporting in the mobile applications. Crash reporting already carries adequate context.

## Risks

Attaching context is where accidental data collection happens. Navigation events can contain identifiers in route parameters, and those need stripping rather than hashing, since a hashed identifier is still an identifier for our purposes.

## Measurement

Support exchanges to establish reproduction steps, errors reported with a reference code, and the share of reports that reach a resolved state.

## Interfaces Affected

Route parameter stripping belongs in the navigation layer, where the route pattern is still known, rather than in the reporting layer where only the resolved path survives. That makes it a change to a component every screen depends on, and a mistake there leaks identifiers into every report rather than into some.

- Route definitions gain an explicit parameter classification; anything undeclared is dropped
- The reporting layer receives patterns, never resolved paths
- Reference codes are generated on the device, so the person sees one even when the report fails to send

## Support Impact

The reference code is what changes a support conversation, and it only works if staff can look one up directly. A code the customer reads out that returns nothing is worse than no code. The lookup has to cover reports that arrived without a matching session and reports that never arrived at all, which on-device generation makes it possible to tell apart.

## Timeline

Classifying parameters across existing routes is the long pole, not the reporting work. There are around ninety routes and each needs a decision, most obvious and a few genuinely unclear. That review should start before the reporting changes, since it is the only part that cannot be hurried safely.
