---
Name: Payout Hold Review Queue
Owner: Amara Osei
Status: In Review
Last Updated: 2026-06-11
---

## Problem

Payouts held by risk rules land in an undifferentiated queue. A first-time seller with an unusual order sits behind a sophisticated fraud case, and both wait the same two to five days. Sellers experience the hold as silence, because we do not tell them it happened until they ask.

## Proposal

Segment the queue by the reason for the hold and give each segment its own handling path.

- Rule-level routing, so velocity holds and identity holds go to different reviewers
- A triage pass where an AI summary of the account history is attached to each case before a reviewer opens it
- Clear seller-facing messaging at the moment of hold, including what we need and when we will respond
- Automatic release for holds that age past the rule's useful window without escalation

## Scope

Payout holds only. Order-level risk decisions are owned by the trust team and keep their current flow.

## Risks

The summaries attached during triage are an aid, not a decision, and the review interface should make that distinction visible rather than presenting a conclusion. Reviewers under queue pressure will trust whatever is at the top of the case, so the summary belongs beside the evidence and not in front of it.

## Measurement

Median hold duration by reason, seller contacts about holds, and reviewer decisions reversed on appeal.

## Staffing

Routing by rule only helps if the segments have reviewers who stay in them. Identity holds need someone who reads documents all day and gets fast at it; velocity holds need someone who reads account history. The rota rotates everyone through everything, which is why the median is flat across reasons that should differ by a day.

- Two named reviewers per segment, with cross-training rather than rotation
- A written standard per segment for what evidence is sufficient, which is what makes reversals reviewable
- Weekend coverage on velocity holds, since those age fastest and release automatically

## Rollout

Seller messaging ships first and alone. It fixes the silence, needs no queue changes, and holding it back until routing is ready would leave the worst part of the experience in place for a quarter.

- Week one: the hold notification, with a reason category and a response-time commitment per category
- Week four: rule-level routing, with reviewers assigned to segments
- Week eight: triage summaries, placed beside the evidence and visibly marked as summaries
- Week twelve: automatic release, per rule, only where the useful window is understood

## Open Questions

- Whether a seller sees the rule category or a plainer description, since the categories were named for reviewers
- What automatic release does to a case a reviewer has opened but not decided
- Whether reversals are attributed to the reviewer, which makes them traceable and also makes reviewers cautious in the direction that costs sellers days
