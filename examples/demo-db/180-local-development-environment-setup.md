---
Name: Local Development Environment Setup
Owner: Priya Raman
Status: In Review
Last Updated: 2026-03-18
---

## Context

Setting up a working local environment takes a new engineer between two and five days, depending on who helps them. The documented steps are incomplete, several steps require credentials obtained by asking a specific person, and three services do not run locally at all.

## Proposal

One command to a working environment, with the gaps closed rather than documented.

- A single setup command producing a running stack, with dependencies containerized
- Credentials issued automatically to the developer's own identity, not shared
- The three unrunnable services given either a local mode or a documented shared instance
- Setup exercised weekly in a clean environment, so breakage is found before a new joiner finds it

## Scope

The main product stack. Infrastructure tooling has its own setup and is out of scope.

## Risks

Containerizing everything makes the environment reproducible and slower, and on the machines we issue, a full stack may not comfortably fit. A shared-instance mode for the heavier dependencies is the likely compromise and should be designed in rather than discovered.

## Measurement

Time from laptop to running stack, setup failures per week in the clean environment check, and new engineer time to first merged change.

## Sequencing

Credentials first. That is the step which blocks on another person being available, and it can be fixed without changing how anything runs. The single command comes next, covering the services that already run locally, which is most of the stack, so the two-to-five days falls before the hard part is solved. The three unrunnable services are last and are three decisions rather than one: a local mode is worth building where the service is small, and a documented shared instance is the honest answer where it is not.

## Operational Impact

The weekly clean-environment run is what keeps this from decaying, and it needs an owner and a failure path.

- A scheduled run from a clean image, with failures routed to the team whose change broke setup
- Setup treated as part of a change, so a dependency added without a setup path fails that week's check
- Shared instances sized for the whole engineering team, not for the three people who try them first

## Open Questions

Whether the machines we issue can run the containerized stack at a speed people will accept, which nobody has measured on the current specification with everything up at once. If they cannot, the shared instance stops being a compromise for heavy dependencies and becomes the normal case, which changes what a local environment means and what an engineer does when that shared instance is down.
