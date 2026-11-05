---
Name: Ticket Routing Rules Rewrite
Owner: Amara Osei
Status: In Review
Last Updated: 2026-06-11
---

## Problem

Tickets route by the category the customer selects, which is wrong about forty percent of the time because the categories reflect our internal structure rather than how people describe problems. Misrouted tickets are reassigned by hand, adding a median of four hours before anyone qualified reads them.

## Proposal

Route on content rather than on the customer's category selection.

- Classification from the ticket text, with the customer's selection as one input among several
- Routing to a queue rather than to an individual, with skills recorded per queue
- Misroutes recorded with their correct destination, feeding classifier improvement
- Support agents able to reroute in one action, with the reason captured

## Scope

Inbound tickets through the help center and email. Chat has its own routing with a different latency requirement.

## Risks

Content-based routing fails most visibly on the tickets that matter: angry, ambiguous, or multi-issue messages, which are exactly the ones a human would route carefully. A confidence threshold below which the ticket goes to a general queue with an experienced reader is necessary, and the threshold should start conservative.

## Measurement

Misroute rate, time to first qualified response, reroutes per hundred tickets, and resolution time for the tickets that fall below the confidence threshold.

## Rollout

Shadow routing for six weeks: the classifier picks a queue, the pick is recorded, and the ticket still routes on the customer's category. That gives a labeled comparison against the forty percent baseline without anyone waiting four extra hours on an experiment. Live routing then starts on the three highest-volume queues with the cleanest boundaries, where a win is both likely and measurable, and widens only once the misroute rate on those three has stayed below the current one for two consecutive weeks.

## Data We Have

Eighteen months of tickets carry their final assigned queue, which is a better label than the original category because it reflects where the work actually happened. It is not a clean label. A ticket that passed through three queues is credited to the last, and the last is sometimes where it was dumped rather than where it belonged. Reroute reasons do not exist at all today, which is why capturing them sits in the proposal rather than arriving later: without them the classifier learns from exactly the end state that hides the problem.

## Operational Impact

Routing to a queue instead of a person changes who feels responsible for an unclaimed ticket, and unowned queues move slower than named assignments unless each queue carries its own response expectation. The general queue created by the confidence threshold needs staffing from the first day, and by definition it needs the most experienced readers, who are the scarcest. Starting the threshold conservative means that queue is largest when the team is least practiced at working it.
