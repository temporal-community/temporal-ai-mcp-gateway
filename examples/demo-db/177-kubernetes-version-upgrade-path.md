---
Name: Kubernetes Version Upgrade Path
Owner: Marcus Reyes
Status: Approved
Last Updated: 2026-04-06
---

## Context

Our clusters run a version that leaves standard support in four months. The last upgrade took six weeks, involved two incidents, and was performed by one engineer who has since moved teams. The runbook is their chat history.

## Proposal

A repeatable upgrade procedure, exercised on non-production clusters first, with the next three upgrades scheduled in advance.

- Upgrade order fixed: development, staging, then production regions one at a time
- Deprecated interface usage detected and remediated before any upgrade begins
- A written procedure produced during the development cluster upgrade, then followed
- The next three upgrades scheduled now, so they are routine rather than events

## Scope

Cluster version upgrades. Node image updates are separate and already automated.

## Risks

Deprecated interface usage is the known hazard and is detectable in advance; the unknown hazard is the behavioral changes that are documented but easy to miss. Reading the full change notes for each intermediate version is tedious, skippable, and the thing most likely to cause the incident.

## Measurement

Time per cluster upgrade, incidents during upgrade, and the gap between our version and current support, which should stay within one release.

## Timeline

Four months of standard support left and one upgrade to perform, so the development cluster upgrade starts within three weeks or the production window lands against the deadline with no slack. Deprecated interface detection runs before that, because the remediation it produces is owned by service teams and moves at their lead time rather than ours. Production regions go a week apart; any closer and a problem that takes days to surface reaches the second region before it is seen in the first.

## Staffing

Two engineers across the whole sequence, not one.

- A second pair of eyes on every production region, which is also how the written procedure gets reviewed
- Change notes for each intermediate version split between them and read before the development upgrade, since that is the step that gets skipped
- A named contact per service for deprecated interface remediation

The last upgrade had one engineer and their chat history, and the cost of that is the position we are in now.

## Rollback

A cluster version upgrade does not roll back, and that fact shapes the rest of the procedure. What exists is a forward path: the written procedure records a recovery step for each stage, and the development and staging runs are where those steps are proved rather than imagined. For production the real control is region isolation, since one region at a time means a bad upgrade touches a fraction of traffic and the rest absorb it.
