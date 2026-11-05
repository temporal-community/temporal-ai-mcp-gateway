---
Name: Postmortem Process Refresh
Owner: Nora Sellers
Status: In Review
Last Updated: 2026-07-03
---

## Context

Postmortems are written for significant incidents and are mostly good. The problem is what happens afterwards: actions are recorded, assigned, and then not done. About forty percent of actions from the last year are still open, and several recurring incidents have repeat actions that were never completed.

## Proposal

Reduce the cost of writing them and raise the cost of ignoring the actions.

- An AI pass that assembles the timeline from alerts, deploys, and chat, so the author edits a draft rather than reconstructing events by hand
- Actions created in the team's own planning system, not in the document, with an owner and a due date
- Overdue actions surfaced in the weekly engineering review, by team
- Repeat incidents linked to the prior postmortem automatically, which makes the pattern visible

## Non-goals

No change to the blameless principle or to who writes them. The analysis stays with the people involved.

## Risks

An assembled timeline is a convenience and could become the analysis, which would make postmortems worse rather than cheaper. The draft should contain events and not conclusions, and the author must remain the person who decides what mattered. Assembled timelines are also only as complete as our instrumentation, and the gaps are exactly where the interesting parts tend to be.

## Measurement

Time to publish a postmortem, action completion rate within thirty days, and repeat incidents of a previously analyzed class.

## Dependencies

Timeline assembly reads three systems, and each has a gap worth knowing before anyone leans on it.

- Alert history, retained ninety days, which is shorter than the interval between some repeat incidents
- Deploy records, complete for services on the standard pipeline and absent for the four that are not
- Incident chat, the richest source and the one carrying the conclusions the draft is meant to leave out

Action tracking also assumes every team uses the same planning system, and three do not. Either those teams move, or their actions stay in a document and stay invisible to the weekly review, which reproduces the problem for the teams that have it worst.

## Failure Modes

The quiet failure is a draft that is confidently incomplete. A missing deploy record leaves no hole, just a plausible sequence with the cause absent, and an author under time pressure will accept it. Naming each source and its coverage window inside the draft is the cheap guard: a timeline that says which minutes it cannot see is one the author will question. The loud failure is actions closed rather than done, which a thirty-day completion rate reports as success. The automatic link to the prior postmortem is what catches that, which is why it matters more than it looks.

## Timeline

Six weeks to action creation in the planning system and the overdue report, since that addresses the forty percent directly and needs no assembly. Draft assembly follows, piloted with one team for a quarter before it is offered more widely, because a draft nobody trusts is harder to withdraw than one never promised.
