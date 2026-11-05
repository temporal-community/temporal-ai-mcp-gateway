---
Name: Onboarding Help Chat Coverage
Owner: Maya Brennan
Status: Approved
Last Updated: 2026-03-25
---

## Problem

Help chat is available during business hours in one time zone. More than half of new workspaces are created outside those hours, and those workspaces activate at a measurably lower rate. The questions asked during onboarding are also highly repetitive: six questions account for most of the volume.

## Proposal

Cover the gap with an assistant for the repetitive questions and a clear path to a person for everything else.

- An AI assistant answering from the documentation, scoped to onboarding topics only
- Explicit handoff to human agents during covered hours, with the conversation history carried over
- Outside covered hours, a promise of a reply with a stated time rather than an open-ended wait
- Every assistant conversation reviewed weekly for answers that were wrong rather than merely unhelpful

## Scope

New workspaces in their first fourteen days. Established accounts keep the current support routing.

## Risks

An assistant that answers confidently about a product it has partial documentation for will mislead people during the exact window where their impression of us is forming. Scoping it to onboarding topics and reviewing transcripts weekly are both load-bearing, and the handoff to human agents must be one action rather than a negotiation.

## Measurement

Activation rate for workspaces created outside covered hours, questions resolved without handoff, handoff rate, and the weekly count of answers found to be wrong.

## Rollout

Start with the six questions and nothing beyond them. Something that answers six things well and plainly declines the seventh is more useful during onboarding than something that attempts everything, and it keeps the weekly review small enough to actually happen. Run it first during covered hours, where a person is one action away and a wrong answer is corrected within minutes, before it runs in the window when nobody is watching. The out-of-hours reply promise should be live from the same day, since it changes the experience most and depends on nothing being built.

## Staffing

The weekly review is the recurring commitment and it is not free. Reading transcripts for answers that were wrong rather than merely unhelpful takes someone who knows the product, which is the same group already covering chat. Budget a few hours a week, assign it to a named person, and expect the first weeks to run heavier while the scope boundary is still being found. The reply promise also needs a morning queue owner in the time zone where the team is thinnest, which is new work rather than absorbed work.

## Open Questions

What the stated reply time should be. A four-hour promise that is missed does more damage than a next-business-day promise that is kept, and nobody has checked what the current out-of-hours backlog would support. Also unresolved: what happens to a workspace that crosses day fourteen in the middle of a conversation, where the choice is finishing the thread or moving it to standard routing mid-sentence.
