---
Name: Developer Onboarding Time
Owner: Hugo Takahashi
Status: In Review
Last Updated: 2026-04-29
---

## Context

Time from start date to first merged change averages nine days. Exit interviews and the new-joiner survey both point at the same three obstacles: environment setup, access requests, and finding out who owns what.

## Proposal

Attack the three obstacles directly and measure the result.

- Environment setup covered by the one-command work, which is a dependency of this
- Access provisioned from the role at start date rather than requested individually
- An ownership directory that answers who owns this, generated from the service manifests
- A first-week task list of genuinely useful small changes, maintained by each team

## Non-goals

No change to the broader onboarding programme, which covers things outside engineering and is working well.

## Risks

The first-week task list decays quickly: good starter tasks get done, and nobody replenishes them. Making replenishment part of the team's own planning rather than a central request is the only version of this that survives, and even that needs checking.

## Measurement

Time to first merged change, access requests raised in week one, and new joiner survey responses on the three obstacles specifically.

## Dependencies

The one-command setup work is a hard dependency owned by another team with its own schedule, and the nine-day average will not move far without it. Role-based access needs role definitions that exist: the directory records eleven engineering roles where four are genuinely distinct in what access they imply. The ownership directory depends on complete service manifests, which hold for services deployed through the standard pipeline and not for the six that predate it.

## Staffing

- Each team names whoever keeps its first-week task list stocked, through its own planning rather than a central request
- The role-to-access mapping needs one person from security for roughly two weeks to agree what each role may touch
- The ownership directory is generated and needs no owner, which is the argument for generating it rather than writing it

## What Would Change Our Mind

If time to first merged change does not move once setup and access are fixed, the remaining delay is review latency or a shortage of ready work rather than onboarding friction, and the task list becomes the main lever instead of a supporting one. Counting access requests raised in week one separately is what lets those two explanations be told apart.
