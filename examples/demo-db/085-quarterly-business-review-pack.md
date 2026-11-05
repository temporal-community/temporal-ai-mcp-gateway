---
Name: Quarterly Business Review Pack
Owner: Ruth Adeyemi
Status: Shipped
Last Updated: 2025-06-24
---

## Background

Account teams built quarterly review decks by hand for each customer, pulling numbers from four places. It took about four hours per account and the numbers occasionally disagreed with what the customer saw in their own dashboard, which is the worst possible error in that meeting.

## Approach

Generate the data portion of the pack from the same source the customer's dashboard reads.

- A generated section covering usage, adoption, and support history
- Numbers resolved through the same definitions the customer sees, with the as-of date stated
- A blank commentary section the account team writes themselves
- Generation on demand rather than on a schedule, since review dates vary

## Non-goals

No generated commentary. The analysis is the part the account team adds, and the pack is better for being honest about that.

## Risks

The main risk was the generated section being treated as the whole pack, with teams skipping the commentary. We made the commentary section impossible to ignore by placing it first and leaving it visibly empty.

## Outcome

Shipped in May. Preparation time is down to about an hour, and there have been no reported discrepancies between the pack and the customer's own view since, against roughly one a quarter before.

## Operational Impact

Generation reads the dashboard's own definition layer, so a change to a metric definition now has two consumers instead of one. The analytics team owns those definitions and did not previously have account teams downstream of them. A definition change now has to be checked against the pack as well, which adds a step to that review but keeps the two numbers from drifting apart again.

- On-demand generation puts load in bursts around quarter end rather than across a nightly window
- A failed run blocks a meeting already on a customer's calendar, so failures page the owning team instead of queueing
- The as-of date renders in the pack itself, which makes a stale run visible to the account team before the customer sees it

## Prior Art

An earlier attempt generated the whole deck, commentary included, and was dropped after two quarters. Account teams rewrote the commentary heavily enough that the draft saved no time, and the rewrites were hard to review against the numbers above them. Leaving the commentary blank reverses that approach deliberately; it is not a gap we plan to close later.

## Open Questions

Whether the four-hour baseline holds for the largest accounts is still unclear. The measured hour is an average across all accounts, and the biggest ones carry more support history to read through. There is also no decision on what happens when a customer disputes a number in the pack. Today that becomes a support ticket on the same path as a dashboard dispute, and nobody has checked whether that path suits a number that arrived in a deck.
