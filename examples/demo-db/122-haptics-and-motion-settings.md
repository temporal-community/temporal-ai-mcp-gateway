---
Name: Haptics and Motion Settings
Owner: Grace Lindqvist
Status: Shipped
Last Updated: 2025-06-18
---

## Background

The application used haptic feedback and transition animation with no way to turn either off beyond the platform-wide setting, which many people do not want to change globally. For users with vestibular sensitivity, our list transitions were reported as genuinely unpleasant.

## Approach

Respect the platform preference and add in-application controls.

- The platform reduced-motion preference honored everywhere, which it previously was not
- An in-application setting for motion and one for haptics, independent of each other
- Reduced motion meaning cross-fade rather than no transition, so spatial relationships remain legible
- The settings surfaced during onboarding rather than buried

## Non-goals

No redesign of the transitions themselves, which were fine for most people.

## Risks

The main risk was partial implementation: honoring the preference on some screens and not others produces an inconsistency that is more disorienting than ignoring it everywhere. We audited every transition rather than the ones we remembered.

## Outcome

Shipped in May. About four percent of users have reduced motion enabled through the platform preference, which is a larger share than anyone on the team expected, and it has been raised twice in accessibility conversations with enterprise customers since.

## Interfaces Affected

The audit reached further than the list screens. Every transition now reads one motion token instead of each screen deciding for itself, which is what made a complete audit possible and what stops a new screen from reintroducing the inconsistency. Haptics went the same way: one call site, one setting. Two places resisted and were handled separately.

- The onboarding flow, which runs before the in-application setting exists and now follows the platform preference
- The embedded web views, which cannot read the in-application setting and receive the preference as a parameter

## Support Impact

Contacts describing the application as broken fell slightly after the release. Several of those had been people with reduced motion enabled at the platform level who were seeing transitions anyway, and who reported it as a defect rather than as a preference being ignored. Support now has one question to ask first, and the answer is visible in the settings screen rather than buried in a log.

## Open Questions

Whether the two settings should have stayed independent is still argued. Most people who turn one off turn both off, which suggests a single comfort setting would have been simpler, and the four percent figure says nothing about whether those who changed only one meant to. Nothing is planned here, but it is the first thing to revisit if the settings screen is reorganized.
