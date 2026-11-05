---
Name: Ticket Deflection at the Help Center
Owner: Priya Raman
Status: Approved
Last Updated: 2026-05-27
---

## Context

The help center's search is keyword-based and poor, so most visitors fail to find an answer and open a ticket. About thirty percent of those tickets are answered by an existing article, which means we are paying a person to do what a working search would have done.

## Proposal

Answer directly in the help center before offering the ticket form.

- An AI answering layer over the help center corpus, returning a direct answer with its sources
- The ticket form still one click away, never hidden behind the answer
- Answers restricted to the published corpus, with an explicit refusal when the corpus does not cover the question
- Every answered session recorded with whether a ticket followed, which is the honest measure of deflection

## Non-goals

No deflection target. A target on deflection creates pressure to make the ticket form harder to reach, which is the failure mode of every system like this.

## Risks

An answer assembled from articles that are themselves stale will be wrong with more authority than the articles were. The freshness work is a hard dependency rather than a parallel effort. We should also expect confident answers to questions about billing and cancellation specifically, where being wrong has a financial consequence, and those topics should be excluded until accuracy is measured.

## Measurement

Tickets per help center session, answered sessions followed by a ticket within a day, and accuracy sampled weekly against the corpus.

## Dependencies

- Corpus freshness, which the risks section already names as hard: roughly a fifth of published articles have not been reviewed since the screens they describe changed, and each one is a confident wrong answer waiting to be assembled
- An owner per article, because freshness without ownership is a backlog rather than a process
- Topic labeling reliable enough to exclude billing and cancellation, which the corpus does not carry today
- Session instrumentation that can link an answered session to a ticket opened afterwards, including one opened from a different device

## Rollout

Shadow first: the answering layer runs on live questions, every answer is recorded, and no visitor sees one. A week of those answers read by support staff who already know the right answer is the cheapest accuracy measurement available and costs no customer anything. Visible answers then start on the topics with the freshest articles and the lowest cost of being wrong, which is feature questions rather than account ones, and widen topic by topic as sampled accuracy holds. Billing and cancellation stay out until accuracy on adjacent topics has been steady for a month.

## Support Impact

The thirty percent of tickets an article already answers are also the easiest thirty percent. Removing them raises the average difficulty of everything left, so handle time will rise even as the queue shrinks, and that should be said out loud before anyone reads the handle-time chart as a regression. Support also becomes the reviewer for sampled answers, which is a few hours of recurring work a week, and the people best placed to do it are the ones already holding the hardest tickets.
