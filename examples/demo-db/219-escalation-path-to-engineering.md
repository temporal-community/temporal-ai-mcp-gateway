---
Name: Escalation Path to Engineering
Owner: Hana Kobayashi
Status: In Review
Last Updated: 2026-07-05
---

## Context

Escalating a ticket to engineering means finding the right team and asking in their channel. Whether it gets picked up depends on who is reading. About a fifth of escalations receive no response within three days, and those tickets sit with the customer waiting.

## Proposal

A defined escalation path with acceptance criteria and a response commitment.

- A single intake per engineering team, routed from the service ownership directory
- Required information defined up front, so escalations arrive complete
- A response commitment of one business day to acknowledge, not to resolve
- Escalations visible in the engineering team's own planning queue rather than in chat

## Scope

Customer-affecting issues requiring engineering investigation. Feature requests follow the product intake, which already works.

## Risks

A commitment to acknowledge within a day is a commitment engineering teams have not agreed to, and imposing it without their involvement will produce compliance rather than help. The intake definition should be written with each team rather than handed to them.

## Measurement

Escalations acknowledged within a day, escalations with complete information at submission, and time from escalation to customer update.

## Dependencies

The service ownership directory is what routes an escalation, and it is accurate for services with an on-call rotation and stale for the rest. An escalation about the stale half routes to a team that no longer owns the code, which is today's failure with an extra step in front of it. The planning queue integration assumes every team works in the same tracker, which two do not, so for those the intake has to write where they actually work rather than where we would prefer.

## Rollout

Two teams first, chosen because they already read a queue rather than a channel, with their intake definitions written alongside them. Routing stays manual for the first month: support picks the team and the intake enforces completeness, which separates whether the form helps from whether the directory is right. The acknowledgement commitment is published only after a month of measured response times, so the number is one those teams have already been meeting.

## What Would Change Our Mind

If completeness at submission rises and acknowledgement does not, the quality of escalations was never the problem, and the fifth that go unanswered are a capacity question no form can reach. That moves the conversation to how escalation time is budgeted rather than how it is routed. The opposite result, acknowledgement improving while completeness stays flat, would say the planning queue visibility is doing the work and the required fields can be trimmed.
