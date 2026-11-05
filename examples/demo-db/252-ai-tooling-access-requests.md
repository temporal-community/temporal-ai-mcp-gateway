---
Name: AI Tooling Access Requests
Owner: Omar Haddad
Status: In Review
Last Updated: 2026-07-24
---

## Problem

Requests to use third-party developer tools arrive through four channels: a form, a chat message to the platform team, a procurement ticket, and occasionally a credit card expense that finance discovers afterwards. There is no inventory of what is in use and no consistent review.

## Proposal

One intake for all third-party tooling requests, with a review proportional to what the tool touches.

- A single request form covering purpose, data touched, and expected users
- Routed automatically to security, legal, or finance depending on what the answers indicate
- A published list of already-approved tools, so repeat requests are answered immediately
- Expense policy updated so that unreviewed purchases are rejected rather than reimbursed

## Scope

Third-party developer and productivity tooling. Infrastructure vendors follow the procurement process.

## Risks

A single intake with a real review will be slower than a credit card, and people will keep using the credit card unless the expense policy change has teeth. The published approved list is what makes the common case fast, and it needs maintaining or the intake becomes the bottleneck everyone routes around.

## Measurement

Requests through the single intake, time to a decision by route, tools discovered through expenses rather than requests, and the size of the approved list.

## Staffing

The routing is automatic; the reviews are not. Security, legal, and finance each need a named reviewer with a stated response window, and that window decides whether the intake gets used at all. Two working days for the common case is reachable only if the published list absorbs the repeats. Keeping that list current is roughly a quarter-day a month and belongs to the platform team, not to whichever reviewer last touched the tool. A missed window with no reason given is what sends the next requester back to the credit card.

## Dependencies

- The expense policy change lands before the intake opens, or the fast path and the slow path stay available at the same time
- Finance needs merchant-level card reporting to find purchases that bypassed the intake; today it is monthly and by category
- The approved list needs a home that can be read without filing anything, which rules out the ticket system it would otherwise live in

## Operational Impact

An inventory exists for the first time, and it stays incomplete for about a year because it only captures what is requested after the intake opens. Backfilling from expense history is the only way to see what is already in use, and that history names the merchant rather than the tool, so a person has to read it line by line. Renewals also become visible, which forces a decision nobody has made yet: what happens when an approved tool's terms change and no one re-requests it.
