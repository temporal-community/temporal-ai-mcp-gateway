---
Name: Guided Setup for Integrations
Owner: Erin Vasquez
Status: In Review
Last Updated: 2026-04-25
---

## Problem

Connecting an integration requires steps in two products and an administrator in each. Our documentation describes the happy path. Support data shows that about forty percent of attempts stall, most commonly at the permission grant, and most of those never resume.

## Proposal

A guided flow that holds state across the gap and recovers from the common failures.

- Setup state persisted, so an interrupted attempt resumes rather than restarts
- The permission step explained in the other product's own vocabulary, not ours
- Explicit detection of the four known failure modes with specific remedies, not a generic error
- A path to invite the administrator when the person setting up lacks the rights

## Scope

The five most used integrations. The long tail keeps documentation-driven setup.

## Risks

The other products change their permission flows without notice, and a guided flow that describes a screen that no longer exists is worse than a generic instruction. Each guide needs an owner and a check that runs against the live flow, or this decays within two quarters.

## Measurement

Setup completion rate per integration, stalls resumed within a week, and support contacts per completed setup.

## Alternatives Considered

Rewriting the documentation was the cheap option and we have done it twice. Completion did not move, because the failure is losing the thread between two products rather than not knowing the steps. Asking partners to host setup inside their own products puts the flow where the permission actually lives, but it needs partner engineering time we cannot schedule and would cover one of the five. A pure support path, where every stall opens a ticket, costs more contacts than the current forty percent already produce.

## Operational Impact

Each of the five guides acquires an owner and a scheduled check against the live flow.

- The check runs weekly and fails loudly when a referenced screen or label disappears
- A failed check reverts that integration to the generic instruction until the guide is fixed
- Stall reasons are recorded by failure mode, so the list of four can be corrected

## Rollout

Ship first with the integration that has the worst stall rate and the most stable permission screen, so the first measurement is clean. Persisted setup state goes in for all five at once, since resuming an interrupted attempt helps even where no guided text exists yet. The administrator invite path ships last because it crosses into account permissions and carries its own review.
