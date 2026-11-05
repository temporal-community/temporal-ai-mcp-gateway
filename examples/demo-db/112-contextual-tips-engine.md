---
Name: Contextual Tips Engine
Owner: Caleb Mortensen
Status: In Review
Last Updated: 2026-05-16
---

## Problem

Feature discovery after onboarding is accidental. People use the five things they learned in week one and never find the rest, which shows up as low adoption of features that interviewees say they wanted when we describe them.

## Proposal

Surface short, dismissible tips at the moment a feature would have helped.

- Triggered by observed behavior, such as repeating a manual action a feature automates
- An AI relevance pass that scores candidate tips against the person's recent activity, so the tip shown is the most useful one rather than the first eligible one
- A hard frequency cap of one tip per person per week, shared with the announcement surface
- Permanent dismissal per tip, and a global off switch in settings

## Non-goals

No tour, no multi-step walkthrough, and no tips for features the person's plan does not include.

## Risks

Behavioral triggers mean watching what people do in order to help them, and the line between helpful and uncomfortable is drawn differently by different people. The global off switch is not a nicety. The relevance scoring also risks over-fitting to short-term activity and repeatedly suggesting variations of the same thing, which is why dismissal must suppress a tip family rather than a single message.

## Measurement

Tip engagement rate, adoption of the featured capability against a holdout, dismissal and opt-out rates, and support contacts describing the product as intrusive.

## Sequencing

Hand-written triggers first, with no scoring at all: a small set of conditions, one tip each, and the frequency cap enforced. That is enough to learn whether tips move adoption, and it answers the helpful-versus-uncomfortable question with real people before any model is in the path. The relevance pass goes in only once there are regularly more eligible tips than the cap allows, which is the problem it exists to solve. If six triggers never collide with the cap, the scoring layer has nothing to do and should not ship.

## Dependencies

- A behavior event stream detailed enough to see a manual action repeated, which exists on some surfaces and not on others
- The announcement surface's own frequency budget, since the cap is shared and no one currently owns the shared total
- Plan entitlement evaluated at display rather than at trigger, because a trial ending between the two shows someone a tip for a feature they have just lost
- A tip family taxonomy, which has to exist before dismissal can suppress a family rather than a message

## Open Questions

Where the line falls between a trigger that reads as attentive and one that reads as surveillance. The only honest way to find it is to ask people who have seen a tip, not people who have had the idea described to them. Also unresolved: whether the global off switch stops the observation or only the display. Stopping only the display is much cheaper to build and is almost certainly not what someone switching it off means by it.
