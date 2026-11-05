---
Name: Seat Expansion Prompts
Owner: Grace Lindqvist
Status: In Review
Last Updated: 2026-02-22
---

## Context

Workspaces that hit their seat limit encounter it as a failure: an invitation that cannot be sent, with an error explaining the limit. Roughly a third of workspaces that hit the limit do not add seats within a month, and interviews suggest they simply share a login instead.

## Proposal

Surface the limit before it is hit and make adding seats a two-click action.

- A visible seat count once usage exceeds eighty percent, in the member list rather than in billing
- Adding seats from the invitation flow itself, with the prorated cost shown before confirmation
- A clear statement of what happens at the limit, before it is reached
- No restriction on inviting; the limit applies to activation, so an invitation is never silently blocked

## Non-goals

No change to pricing or to the seat model.

## Risks

Prompting for expansion is a sales motion inside the product, and getting the tone wrong turns a useful warning into something people resent and dismiss on sight. It should read as information about their own state rather than as an offer.

## Measurement

Workspaces adding seats before hitting the limit, time from limit to resolution, shared-credential patterns detected, and dismissal rate on the prompt.

## Prior Art

A billing-page banner at ninety percent usage ran two years ago and was retired after a quarter. Nearly everyone who saw it dismissed it, and the review concluded the placement was wrong rather than the idea: the person who notices a seat shortage is the one inviting people, and they are not in billing. Eighty percent is deliberately lower, since ninety left too little room to act before the next invitation.

## Interfaces Affected

Adding seats from the invitation flow means that path writes to billing, which it has never done. Ordering matters: seats are added first and the invitation goes out only once the seat change is confirmed, so a failure leaves a paid-for seat rather than an invitation with nothing behind it.

- The invitation endpoint gains a prorated-quote call, fast enough to sit inside a modal
- Seat changes from this path appear in the billing audit log with their origin recorded
- Admins without billing permission see the count but not the add-seats action

## Review Notes

Shared-credential detection is listed as a measure and has no agreed definition. The nearest thing available is concurrent sessions from distant addresses on one account, which also describes someone with a laptop and a phone on a train. Read that number as directional, and do not report it as a count of policy violations.
