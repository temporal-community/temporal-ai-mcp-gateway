---
Name: Quality Review Sampling
Owner: Nora Sellers
Status: In Review
Last Updated: 2026-07-22
---

## Context

Quality review covers about one percent of tickets, sampled by team leads when they have time. The sample is not random, skews toward tickets that were already flagged, and produces a quality picture that nobody believes.

## Proposal

Sample properly, score consistently, and use the result for coaching rather than ranking.

- A stratified random sample across queues, channels, and people, at a defined rate
- An AI pre-scoring pass against the rubric that flags candidate issues for the reviewer, with the human making every actual judgment
- A written rubric with worked examples, calibrated across reviewers quarterly
- Results used in coaching conversations, explicitly not in performance ranking

## Scope

Tickets and chat. Voice is excluded pending the pilot outcome.

## Risks

Pre-scoring will anchor reviewers toward the issues it flags and away from the ones it cannot see, such as tone that is technically correct and unkind. Reviewers should read the ticket before the flags, and we should measure whether reviewer findings outside the flagged set decline over time, which would tell us the anchoring is real.

The other risk is the stated separation from performance ranking eroding, which it will unless the data is structurally unavailable for that purpose.

## Measurement

Sample coverage and representativeness, inter-reviewer agreement at calibration, findings outside the pre-scored flags, and coaching actions following review.

## Staffing

A defined sample rate turns review from spare-time work into scheduled work, and the rate is a staffing decision before it is a statistical one.

- Reviewers drawn from senior staff on rotation, never the lead of the team being sampled
- A calibration session each quarter with every reviewer present, which is four hours nobody currently budgets
- The rubric owned by one person, since a rubric maintained by committee drifts between its own examples

Reviewing another team's tickets costs the reviewer context and removes the incentive to protect a number. The second matters more.

## Sequencing

The rubric and the first calibration come before the sample rate is raised, because a larger sample scored inconsistently is more confident and no more true. The pre-scoring pass goes on last, with its flags hidden until the reviewer has recorded a first read. That control is the one the risks section asks for, and it is only enforceable if the tool is built that way from the start. Voice stays out until the pilot reports.

## What Would Change Our Mind

If findings outside the flagged set fall quarter on quarter, the anchoring is real, and pre-scoring moves to after the human read rather than before it. If inter-reviewer agreement stays low after two calibrations, the rubric is the problem rather than the sample, and more coverage will not fix it. And if a review result turns up in a performance conversation, the separation was never structural, which ends the program rather than adjusts it.
