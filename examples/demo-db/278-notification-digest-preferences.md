---
Name: Notification Digest Preferences
Owner: Nora Sellers
Status: Approved
Last Updated: 2026-10-25
---

## Context

Notification settings offer immediate or off. For anyone in more than a few shared spaces, immediate is overwhelming and off means missing things that mattered, so people choose off and then complain about missing things.

## Proposal

A digest option with a real choice of cadence, and smarter defaults.

- Three cadences: immediate, hourly digest, daily digest, set per category
- Mentions and direct messages always immediate, not subject to the digest
- Defaults derived from how many spaces a person belongs to, since that is what predicts overload
- A preview of what a digest would have contained, so the choice is informed
- A short AI summary at the top of each digest, so a longer cadence does not trade away awareness

## Non-goals

No change to in-product notification, which has a different attention model.

## Risks

Digests delay things that were occasionally urgent, and the category boundaries will be wrong for somebody. Keeping mentions outside the digest covers most of the genuinely urgent cases; the rest is a preference people can adjust once they see the effect.

## Measurement

Share of people on each cadence, notification disable rate, which should fall, open rate per digest, and reports of missed information.

## Migration

Everyone sits at immediate or off today, and both are poor answers to a question we are about to ask better.

- People on immediate stay on immediate; nothing changes under someone who chose it
- People on off move to a daily digest, announced beforehand, with one click back to off
- The space-count default applies to new accounts only, since inferring a preference for someone who already stated one is backwards

Moving the off population carries the real risk. They turned notification off deliberately, and a digest arriving unannounced reads as us overriding that choice.

## Cost

Digests are cheaper in volume and more expensive per message. An hourly digest for someone in thirty spaces replaces perhaps forty sends with one, which is the saving. The summary at the top is computed once per digest per person, so the new recurring cost scales with how many people choose a digest cadence rather than with message volume. The preview is computed on request and is negligible.

## Open Questions

What a digest does when it would be empty. One that arrives to say nothing happened trains people to stop opening it, and one that silently does not arrive is indistinguishable from a delivery failure. We have also not decided whether the categories are ours alone or configurable per space, where configurable means a space owner can make their own notifications immediate for everybody in it.
