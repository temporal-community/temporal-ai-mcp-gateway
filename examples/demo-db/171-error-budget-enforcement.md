---
Name: Error Budget Enforcement
Owner: Omar Haddad
Status: Draft
Last Updated: 2026-05-06
---

## Background

Once objectives exist, the question is what happens when a budget is exhausted. Without an agreed answer, the budget is a number on a dashboard and teams will continue to make the same tradeoffs they make now.

## Proposal

A graduated response agreed in advance, applied automatically rather than negotiated per incident.

- At fifty percent consumed, a review of what consumed it, in the team's own planning
- At eighty, reliability work prioritized above new feature work for that service
- At one hundred, a change freeze on that service except for reliability and security fixes
- Freeze lifted by budget recovery, not by request

## Scope

Services with a defined objective, which after the objectives work will be most of them.

## Risks

A freeze applied automatically will at some point collide with a commercially critical deadline, and the pressure to make an exception will be substantial. If exceptions are routine the policy is theatre. The proposal is that exceptions require a named executive decision recorded in writing, which makes them possible and uncomfortable.

## Measurement

Budget consumption by service, freezes triggered, exceptions granted, and whether reliability work actually gets prioritized at the eighty percent threshold.

## Dependencies

The objectives work lands first and has to produce objectives teams believe, because a freeze keyed to a number nobody agreed with gets argued about on the day it fires rather than before. Budget accounting has to attribute consumption to the service that caused it, which today's measurement does not do for failures inherited from a dependency. And the freeze has to be enforced in the deployment pipeline rather than by convention, or the eighty percent threshold is the only one with teeth.

## Rollout

Thresholds are observed and reported for a quarter before anything is enforced, so teams watch their own consumption against a line that does not yet stop them. The fifty and eighty percent responses go live first, since both are prioritization decisions a team makes for itself. The freeze comes last and starts with the three services whose objectives are best understood, rather than the ones consuming the most budget, which are also where the measurement is least trusted.

## What Would Change Our Mind

If exceptions are granted more than once a quarter, the policy produces paperwork and nothing else, and the honest response is to move the thresholds rather than keep a freeze that is always waived. The other case is the eighty percent step: if reliability work is not actually prioritized there, the freeze carries the whole policy and the graduated part is decoration.
