---
Name: Language Coverage for Support
Owner: Omar Haddad
Status: In Review
Last Updated: 2026-05-15
---

## Problem

We support three languages. About a fifth of tickets arrive in another, and those customers receive a response in English after a longer wait, which is a measurably worse experience in satisfaction and in resolution time.

## Proposal

Extend coverage pragmatically: machine translation for the long tail, people for the volume languages.

- Translation in the agent interface for inbound and outbound, with the original always visible
- Two additional staffed languages chosen by volume, which covers most of the gap
- A clear statement to the customer when a response has been machine translated
- Terminology list maintained for product terms, which translation systems consistently get wrong

## Scope

Email and tickets. Chat requires real-time translation quality we have not evaluated.

## Risks

Machine translation of a support response can invert meaning in ways neither party detects, particularly around negation and conditional commitments. Disclosure is the minimum; the more important control is keeping responses short and simple when translation is involved, which needs to be trained rather than assumed.

## Measurement

Resolution time and satisfaction by language against the English baseline, translation corrections requested, and the share of tickets handled in the customer's own language.

## Staffing

The two additional staffed languages are a hiring decision with a long lead, and the translated path has to carry those queues until the hires are productive.

- Two people per language, so a working week is covered without a single point of absence
- A reviewer in each new language for the first quarter, sampling outbound responses
- The terminology list owned by the localization lead, not by whoever last complained about a bad term

Hiring one person per language would be cheaper and would turn every absence into a coverage gap, which is the state the long-tail languages are in today.

## Dependencies

The translation vendor decision sits upstream of everything here, since quality varies by language pair and the two staffed languages we pick change which pairs the long tail still needs. The console work depends on the ticket system holding the original text alongside the translated text, which it does for email and does not for chat, the same gap that keeps chat out of scope. The terminology list needs a format the vendor can actually consume, or it is a document nobody applies.

## What Would Change Our Mind

If sampled review finds inverted meaning in more than roughly one response in fifty, disclosure stops being an adequate control and outbound translation should wait for someone who reads the language. The second signal is volume: if the two chosen languages do not move the share of tickets handled in the customer's own language by the expected amount, the volume ranking is wrong and the next hire goes elsewhere.
