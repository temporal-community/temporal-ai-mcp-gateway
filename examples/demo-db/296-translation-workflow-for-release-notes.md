---
Name: Translation Workflow for Release Notes
Owner: Grace Lindqvist
Status: Draft
Last Updated: 2026-03-01
---

## Problem

Release notes publish in English and are translated when someone remembers, typically weeks later. Customers in other languages read announcements about features after their colleagues have already used them, or not at all.

## Proposal

Translation in the publishing path rather than after it.

- Notes sent for translation at draft rather than at publish, so translation is not the long pole
- Machine translation with human review for the supported languages, rather than either alone
- Publication held until the supported languages are ready, within a defined window
- Terminology list shared with the translation vendor and maintained by the documentation team

## Scope

Release notes. Full product documentation translation is a much larger commitment and is out of scope.

## Risks

Holding publication for translation delays English readers, who are the majority. A defined window with publication proceeding regardless is the compromise, and it means some releases will publish without full coverage, which is better than the current state of coverage arriving randomly.

## Measurement

Languages published at release, delay to English publication, review corrections per thousand words, and readership per language.

## Dependencies

Sending at draft only helps if the draft holds still, and release notes are routinely rewritten in the last two days. The publishing pipeline needs a frozen state that triggers translation, and anything edited after that has to re-enter the queue rather than publish untranslated under the same heading. The vendor arrangement is the other dependency, since review inside the window needs a turnaround commitment the current contract does not contain.

## Cost

Per release the cost is small, and the volume is what adds up, since notes publish weekly through most quarters.

- Machine translation is negligible; review hours are the cost and they scale with the number of supported languages
- The terminology list costs maintenance rather than money, and it is what drives corrections per thousand words down
- A reviewer per language has to be reachable weekly, which is a scheduling commitment rather than a headcount one

## What Would Change Our Mind

If readership per language stays flat once translation is reliable, timing was never the problem and these notes are not what those customers read, which would argue for putting the effort into in-product announcements. The second signal is the correction rate: if review keeps finding substantive errors rather than style, machine translation is not carrying enough of the work at this cadence, and either the window widens or the language set shrinks.
