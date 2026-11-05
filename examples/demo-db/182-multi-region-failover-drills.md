---
Name: Multi-Region Failover Drills
Owner: Priya Raman
Status: Approved
Last Updated: 2026-03-04
---

## Context

We have a secondary region and a documented failover procedure. The procedure has never been executed outside a tabletop exercise, and the last three times we considered using it during an incident, we decided the risk of the untested path exceeded the risk of waiting.

## Proposal

Quarterly drills that actually move traffic, scheduled and announced.

- A scheduled window each quarter with the whole path exercised, not simulated
- Traffic moved for a defined period and moved back deliberately
- Every manual step encountered recorded as a defect against the procedure
- Success defined as completing within the recovery objective, not as avoiding incident

## Scope

The customer-facing request path and its data dependencies. Internal tooling follows later, once the main path is exercised.

## Risks

The first drill will cause a customer-visible event. This is the cost of discovering, on a Tuesday afternoon with everyone available, what we would otherwise discover during a genuine outage. The communication plan matters as much as the technical plan, and the decision to accept this cost should be made by leadership explicitly rather than assumed by the team running it.

## Measurement

Time to complete failover against the recovery objective, defects found per drill, and the number of manual steps remaining in the procedure, which should fall toward zero over four drills.

## Prior Art

The tabletop exercises produced a procedure that reads well and has never been contradicted by reality, which is the problem. Two neighboring teams already run something closer to this. The storage team fails a replica over monthly in a maintenance window, and the payments team rehearses its degraded mode quarterly without moving traffic. The storage drills are the useful precedent: their defect count fell for three cycles and then flattened, which is the shape to expect here and the reason the fourth drill tells us more than the first.

## Support Impact

A scheduled customer-visible event is still a customer-visible event, and the support queue absorbs it.

- The window is published to support a week ahead, with the expected symptom and duration
- A canned response and a status page entry are ready before traffic moves, not written during
- Contacts during the window are tagged so the cost of a drill can be counted separately

## Timeline

The first drill runs in the quarter after leadership accepts the customer-visible cost, with two weeks between that decision and the window so support, the status page, and the named owner of the move-back decision are all in place. Drills two through four follow the quarterly cadence. Internal tooling enters scope only after a drill completes inside the recovery objective with no new manual steps recorded, which on the current defect estimate is not before the third one.
