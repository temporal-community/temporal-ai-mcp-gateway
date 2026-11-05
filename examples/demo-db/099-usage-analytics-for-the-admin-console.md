---
Name: Usage Analytics for the Admin Console
Owner: Ben Tsai
Status: Draft
Last Updated: 2026-04-21
---

## Context

The admin console has eighty-six screens. We do not know which are used. Every proposal to remove something stalls because nobody can say whether anyone would notice, so the console only ever grows.

## Proposal

Instrument the console and publish a usage view the whole team can read.

- Screen views and primary actions instrumented, with no capture of the data displayed
- Usage reported per screen per week, segmented by customer size
- A deprecation candidate list generated from the bottom of the distribution
- Customer-identifiable usage restricted to the support and account teams

## Non-goals

No behavioral tracking of individual administrators, which would be both intrusive and unnecessary for this purpose.

## Risks

Low usage is not the same as low value, and the console contains screens used once a year by one customer for something critical. The candidate list is an input to a conversation with the account team, not a removal queue, and should be labeled that way to prevent it being treated as one.

## Measurement

Screens with usage data, screens removed following review, and complaints after removal, which is the number that tells us whether the review worked.

## Prior Art

The marketing site was instrumented the same way three years ago. The deprecation list it produced was used twice and then ignored, because nobody owned the conversation that turns a low number into a decision. The account team review is exactly the part that failed then, which is why this proposal names it. Instrumentation was never what stalled.

## Failure Modes

- A screen reached only through a deep link in an email shows near-zero views while in daily use, because view counting misses entry paths that skip navigation
- Screens behind a feature flag look unused because most customers cannot see them, which reads as low value rather than low exposure
- Weekly buckets hide seasonal screens: a year-end reconciliation screen is unused for fifty weeks by design

Segmenting by customer size catches the second of these and neither of the others, so entry paths belong on the candidate list before anyone reads it as evidence.

## Review Notes

Restricting customer-identifiable usage to the support and account teams needs a stated retention period, which this draft does not give. Two reviewers asked whether primary actions include destructive ones. They do, and the action name is recorded without its parameters, so a deleted role is counted and which role was deleted is not.
