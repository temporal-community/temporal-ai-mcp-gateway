---
Name: Device Trust Signals at Login
Owner: Lena Fischer
Status: In Review
Last Updated: 2026-04-02
---

## Problem

Every sign-in is treated the same. A known device on a known network from a known location goes through the same challenge as a first-time sign-in from an unfamiliar country, which means the challenge is either too weak for the second case or too annoying for the first.

## Proposal

Score the sign-in context and vary the challenge accordingly.

- Signals limited to device identity, network reputation, and coarse location, with no behavioral profiling
- A score computed at sign-in and recorded with the decision for later review
- Low-risk sign-ins skip the second factor for a bounded period on that device
- High-risk sign-ins require a second factor and notify the account by a separate channel

## Scope

Sign-in only. Step-up verification for sensitive actions is a separate proposal and should stay separate.

## Risks

Any scoring system makes mistakes with a confidence it has not earned, and the people most affected by false positives are travelers and people on shared or mobile networks, who are not an edge case. The policy should fail toward challenge rather than toward denial, and the score must never be the sole reason for a block.

## Measurement

Second-factor prompts per successful sign-in, account takeover rate, and sign-in abandonment by region, watched for the regions where network reputation data is weakest.

## Data We Have

Two of the three signals already exist and are used for nothing.

- Device identity is recorded for the session list, with a stable identifier on mobile and a cookie on web
- Coarse location is derived at sign-in and is right about the country far more often than about the city
- Network reputation comes from a vendor feed we do not buy today, and its coverage is thinnest in the regions where abandonment is hardest to read

Recording the score with every decision from the first day is what makes the first threshold change defensible, so that lands before any challenge varies.

## Rollout

Score and record for a month with no change in behavior, which produces a distribution instead of an assumption. The high-risk path goes next, since requiring a second factor where we currently require none improves security and cannot lock anyone out. Skipping the second factor on low-risk sign-ins comes last, with a short bounded period on that device, because it is the only step that removes a control rather than adding one.

## Open Questions

Whether the separate-channel notification reaches an address the attacker already controls, which is what happened in the takeover sequence we have on record. We have also not settled what a traveler meets on the second and third day of a trip, where the device is familiar and the other two signals are both wrong, or whether a recent successful challenge should age the score rather than reset it.
